# Flask Context Proxy

`contextproxy` is a `@contextmanager` style `LocalProxy`, managed by `flask.g`, designed to simplify the management of lazily loaded, context-based resources in `Flask` applications. It allows resources to be easily accessed, automatically initialized and cleaned up based on `Flask`'s request and application lifecycle, and can be used to share resources across multiple requests or manage them on a per-request basis.

## Features

- **Easy Access**: Resources can be accessed using decorated names, making them easy to use in your application.
- **Lazy Initialization**: Resources are only initialized when accessed, saving computation and memory for unused resources.
- **Automatic Teardown**: Resources are cleaned up automatically after the application context is torn down.
- **Supports `Flask` Contexts**: The decorator works seamlessly with `Flask`'s request and application contexts, ensuring context isolation and cleanup.
- **Thread Safety**: Ensures that resources are unique per thread in multi-threaded environments.

## Installation

You can install `contextproxy` by including the file in your project directory or packaging it as a Python module.

```bash
pip install .
```

## Usage

To use `contextproxy`, simply apply it as a decorator to a generator function that yields the resource you want to manage. The resource will be lazily initialized and binded to `flask.g` for the duration of the application context.

It should be noted that the resource is finalized only after the application context ends (for `Flask>=0.9`). That means the resource will be shared across multiple requests within the same application context.

### Basic Example

```python
from flask import Flask
from contextproxy import contextproxy

app = Flask(__name__)

@contextproxy(app)
def resource():
    # Initialize the resource
    resource_value = "This is a shared resource"
    yield resource_value
    # Teardown logic (e.g., closing connections) goes here
    print("Resource has been cleaned up")

@app.route('/')
def index():
    return f"Resource: {resource}"

if __name__ == "__main__":
    app.run(debug=True)
```

In the example above, the `resource` is lazily initialized the first time it's accessed and will be automatically cleaned up after the application context ends.

## Advanced Usage

### Handling Exceptions in Resource Initialization

If your resource initialization involves risky operations (like database connections), you can handle exceptions cleanly within the resource function.

```python
@contextproxy(app)
def risky_resource():
    uuid = uuid4()
    print(f"before: Preparing to create resource ({uuid})")
    try:
        print(f"yielding: Creating resource ({uuid})")
        yield f"resource {uuid=}"
        print(f"yielded: where is this? ({uuid})")
    except Exception as e:
        print(f"except: error processing resource ({uuid}): {type(e)}: {e}")
    else:
        print(f"else: okey processing resource ({uuid})")
    finally:
        print(f"finally: Destroying resource ({uuid})")
    print(f"after: Destroyed resource ({uuid})")
```

## **Contributing**

If you’d like to contribute to `contextproxy`, feel free to fork the repository, submit issues, or open a pull request!

## **License**

This project is licensed under the MIT License.
