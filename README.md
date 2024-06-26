# Criadex SDK

A Python library to interact with the [Criadex](https://github.com/CriaYU/Criadex) RESTful API.

## Getting Started

1. Install the package from locally cloned repository

```shell
$ pip install --upgrade git+file://c:/users/user/PycharmProjects/criadexsdk 
```

2. Make your first query

```python
import asyncio
from CriadexSDK import CriadexSDK
from CriadexSDK.routers.content import GroupContentSearchRoute

# Create client
criadex: CriadexSDK = CriadexSDK(api_base="https://api-base.com/")  # <-- Trailing slash doesn't matter


# Query criadex
async def execute_query():
    await criadex.authenticate(api_key="MASTER_API_KEY_HERE")

    response: GroupContentSearchRoute.Response = await criadex.content.search(
        group_name="group_name",
        prompt="What day is Assignment 3 due?",
        top_k=5
    )

    print("Retrieved Vectors: ", response)


# Run the async function
asyncio.get_event_loop().run_until_complete(execute_query())
```

## Available Configuration

- Set `CRIADEX_SDK_TIMEOUT` to a value like `30.0` to configure timeouts
- Set `error_stacktrace` to `True` or `False` to configure seeing Criadex stacktraces for errors 

## Available Methods

Every endpoint from the Criadex API is implemented.

### Authorization

- `client.auth.create`
- `client.auth.delete`
- `client.auth.check`

### Group Authorization

- `client.auth.create`
- `client.auth.delete`
- `client.auth.check`

### Model Management

- `client.models.create`
- `client.models.delete`
- `client.models.about`

### Model Agents

- `client.agents.chat`
- `client.agents.intents`
- `client.agents.language`

### Group Management

- `client.manage.create`
- `client.manage.delete`
- `client.manage.about`

### Content Management

- `client.content.upload`
- `client.content.update`
- `client.content.delete`
- `client.content.list`
- `client.content.search`