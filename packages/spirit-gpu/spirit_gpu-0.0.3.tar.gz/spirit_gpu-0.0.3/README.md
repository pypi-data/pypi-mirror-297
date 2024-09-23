# Spirit-GPU

- [Spirit-GPU](#spirit-gpu)
  - [Install](#install)
  - [Usage example](#usage-example)
  - [API](#api)

## Install
```
pip install spirit-gpu
```

## Usage example

```python
from spirit_gpu import start
from spirit_gpu.env import Env


def handler(request: Dict[str, Any], env: Env):
    """
    request: Dict[str, Any], from client http request body.
    request["input"]: Required.
    request["webhook"]: Optional string for asynchronous requests.

    returned object to be serialized into JSON and sent to the client.
    in this case: '{"output": "hello"}'
    """
    return {"output": "hello"}


def gen_handler(request: Dict[str, Any], env: Env):
    """
    append yield output to array, serialize into JSON and send to client.
    in this case: [0, 1, 2, 3, 4]
    """
    for i in range(5):
        yield i


async def async_handler(request: Dict[str, Any], env: Env):
    """
    returned object to be serialized into JSON and sent to the client.
    """
    return {"output": "hello"}


async def async_gen_handler(request: Dict[str, Any], env: Env):
    """
    append yield output to array, serialize into JSON and send to client.
    """
    for i in range(10):
        yield i


def concurrency_modifier(current_allowed_concurrency: int) -> int:
    """
    Adjusts the allowed concurrency level based on the current state.
    For example, if the current allowed concurrency is 3 and resources are sufficient,
    it can be increased to 5, allowing 5 tasks to run concurrently.
    """
    allowed_concurrency = ...
    return allowed_concurrency


"""
Register the handler with serverless.start().
Handlers can be synchronous, asynchronous, generators, or asynchronous generators.
"""
start({
    "handler": async_handler, "concurrency_modifier": concurrency_modifier
})
```

## API
See [API](https://github.com/datastone-spirit/spirit-gpu/blob/main/API.md) or [中文 API](https://github.com/datastone-spirit/spirit-gpu/blob/main/API.zh.md) for more details.