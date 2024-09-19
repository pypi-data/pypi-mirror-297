from contextvars import ContextVar
from functools import wraps
from typing import Callable, Generator, Optional, TypeVar

from flask import Flask, g
from werkzeug.local import LocalProxy

T = TypeVar("T")


def contextproxy(
    app: Flask,
) -> Callable[[Callable[[], Generator[T, None, None]]], LocalProxy]:
    """
    Factory function that returns a decorator for creating context-based lazy-loaded proxy objects.

    It lazily retrieves the object from the generator when accessed. The generator is executed
    only once per request, and the yielded object is stored in the Flask context (`g`).

    The code block prior to the `yield` statement is executed when the object is first accessed.
    The code block after the `yield` is executed during the teardown phase of the request,
    ensuring proper cleanup.

    Parameters
    ----------
    app : Flask
        The Flask application instance to which this context proxy is bound.

    Returns
    -------
    Callable
        A decorator that transforms a generator function into a context-based lazy-loaded proxy object.

    Decorator Parameters
    --------------------
    func : Callable[[], Generator]
        A generator function. The first `yield` provides the object to be accessed,
        and the remaining code is executed during teardown.

    Returns (Decorator)
    --------------------
    LocalProxy
        A proxy object that retrieves the object from the generator when accessed.

    Example
    -------
    ```python
    @contextproxy(app)
    def example_model():
        uuid = uuid4()
        yield f"example {uuid=}"
        print(f"Destroyed example model ({uuid})")

    @app.route("/hello", methods=["GET"])
    def hello():
        return f"hello world {example_model}"
    ```

    Notes
    -----
    This pattern follows the context manager pattern but is adapted to Flask's request lifecycle.
    The object is lazily initialized and tied to the request context, while teardown ensures
    the generator completes or handles any exceptions.
    """

    def decorator(func: Callable[[], Generator[T, None, None]]) -> LocalProxy:
        return _create_proxy(func, app)

    return decorator


def _create_proxy(
    func: Callable[[], Generator[T, None, None]], app: Flask
) -> LocalProxy:
    generator_started: ContextVar[bool] = ContextVar(
        f"{func.__name__}_started", default=False
    )
    generator_instance: ContextVar[Optional[Generator[T, None, None]]] = ContextVar(
        f"{func.__name__}_gen", default=None
    )

    @wraps(func)
    def _get() -> T:
        if func.__name__ not in g:
            gen = func()
            generator_instance.set(gen)
            generator_started.set(True)  # Mark the generator as started
            # Retrieve the object yielded by the generator
            value = next(gen)
            setattr(g, func.__name__, value)
        return getattr(g, func.__name__)

    def _teardown(exception: Optional[BaseException]) -> None:
        if not generator_started.get():
            # Generator was never started; no teardown needed
            return

        gen = generator_instance.get()
        if gen is None:
            # Should not happen, but guard anyway
            return

        # Remove the object from the context
        g.pop(func.__name__, None)

        try:
            if exception is None:
                # No exception occurred; proceed with normal teardown
                try:
                    next(gen)
                except StopIteration:
                    # Generator properly exhausted
                    pass
                else:
                    # Generator did not stop after cleanup
                    raise RuntimeError("Generator did not stop after cleanup")
            else:
                # An exception occurred; throw it into the generator
                try:
                    gen.throw(exception)
                except StopIteration:
                    # Generator properly exhausted after handling exception
                    pass
                except Exception as e:
                    if e is not exception:
                        # An unexpected exception occurred
                        raise
                    # Exception was handled inside the generator
                    pass
        finally:
            # Cleanup complete
            pass

    def _register_teardown(app: Flask) -> None:
        # Register the teardown function with the Flask app
        if hasattr(app, "teardown_appcontext"):
            # Flask >= 0.9
            # app.teardown_appcontext(_teardown)
            app.teardown_request(_teardown)
        elif hasattr(app, "teardown_request"):
            # Flask >= 0.7, < 0.9
            app.teardown_request(_teardown)
        else:
            # Flask < 0.7
            def after_request_teardown(response):
                _teardown(None)
                return response

            app.after_request(after_request_teardown)

    # Register the teardown function immediately
    _register_teardown(app)

    return LocalProxy(_get)
