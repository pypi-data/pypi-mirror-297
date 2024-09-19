import pytest
from flask import Flask, g
from contextproxy import contextproxy
import threading


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for each test."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def contextproxy_decorator(app):
    """Provide the contextproxy decorator bound to the app."""
    return contextproxy(app)


def test_basic_usage(app, contextproxy_decorator):
    teardown_called = False

    @contextproxy_decorator
    def resource():
        nonlocal teardown_called
        resource_value = "Resource Value"
        yield resource_value
        teardown_called = True

    @app.route("/test")
    def test_view():
        assert resource == "Resource Value"
        return "Success"

    # Use the test client as a context manager
    with app.app_context():
        response = app.test_client().get("/test")
        assert response.data.decode() == "Success"
        # At this point, the teardown has not occurred yet

    assert teardown_called


def test_lazy_initialization(app, contextproxy_decorator):
    init_called = False
    teardown_called = False

    @contextproxy_decorator
    def resource():
        nonlocal init_called, teardown_called
        init_called = True
        yield "Lazy Resource"
        teardown_called = True

    @app.route("/unused")
    def unused_view():
        return "Unused Resource"

    with app.app_context():
        response = app.test_client().get("/unused")
        assert response.data.decode() == "Unused Resource"

    assert not init_called
    assert not teardown_called


def test_exception_in_view(app, contextproxy_decorator):
    init_called = False
    teardown_called = False
    exception_handled = False

    @contextproxy_decorator
    def resource():
        nonlocal init_called, teardown_called, exception_handled
        init_called = True
        try:
            yield "Resource with Exception"
        except Exception:
            exception_handled = True
        finally:
            teardown_called = True

    @app.route("/error")
    def error_view():
        _ = str(resource)  # Force the proxy to evaluate
        raise ValueError("Intentional Error")

    with pytest.raises(ValueError, match="Intentional Error"):
        with app.app_context():
            response = app.test_client().get("/error")
            # Assert that an error occurred (status code 500)
            assert response.status_code == 500

    assert init_called
    assert exception_handled
    assert teardown_called


def test_exception_in_resource(app, client, contextproxy_decorator):
    @contextproxy_decorator
    def resource():
        raise RuntimeError("Initialization Error")
        yield "Unreachable"

    @app.route("/init-error")
    def init_error_view():
        _ = str(resource)  # Force the proxy to evaluate
        return "This should not be reached"

    with pytest.raises(RuntimeError, match="Initialization Error"):
        client.get("/init-error")


def test_multiple_resources(app, client, contextproxy_decorator):
    @contextproxy_decorator
    def resource_a():
        yield "Resource A"

    @contextproxy_decorator
    def resource_b():
        yield "Resource B"

    @app.route("/multi")
    def multi_view():
        return f"{resource_a} and {resource_b}"

    response = client.get("/multi")
    assert response.data.decode() == "Resource A and Resource B"


def test_thread_safety(app, contextproxy_decorator):
    @contextproxy_decorator
    def resource():
        # NB: threading.get_ident() might has the same value for different threads @see https://stackoverflow.com/a/72773655
        # threading.get_native_id() is subject to OS-specific limitations
        # Use generated thread name for uniqueness
        yield f"Resource in Thread {threading.current_thread().name}"

    results = []
    lock = threading.Lock()

    def access_resource():
        with app.test_request_context("/thread-test"):
            res = str(resource)
            with lock:
                results.append(res)

    threads = [threading.Thread(target=access_resource, name=f"Thread {i}") for i in range(5)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(results) == 5
    assert len(set(results)) == 5  # Ensure resources are unique per thread


def test_teardown_called_once(app, contextproxy_decorator):
    teardown_call_count = 0

    @contextproxy_decorator
    def resource():
        nonlocal teardown_call_count
        yield "Resource"
        teardown_call_count += 1

    @app.route("/multiple-access")
    def multiple_access_view():
        _ = str(resource)
        _ = str(resource)
        return "OK"

    with app.app_context():
        app.test_client().get("/multiple-access")

    assert teardown_call_count == 1


def test_resource_access_in_teardown(app, client, contextproxy_decorator):
    # NB: This must be defined before the resource, so it come after in the teardown
    @app.teardown_appcontext
    def custom_teardown(exception):
        assert getattr(g, "resource", None) is None

    @contextproxy_decorator
    def resource():
        yield "Resource Value"

    @app.route("/test-teardown")
    def test_teardown_view():
        _ = str(resource)
        return "OK"

    client.get("/test-teardown")


def test_error_handling_in_teardown(app, contextproxy_decorator):
    @contextproxy_decorator
    def resource():
        yield "Resource Value"
        raise RuntimeError("Error during teardown")

    @app.route("/error-in-teardown")
    def error_in_teardown_view():
        _ = str(resource)
        return "OK"

    with pytest.raises(RuntimeError, match="Error during teardown"):
        with app.app_context():
            app.test_client().get("/error-in-teardown")


if __name__ == "__main__":
    pytest.main()
