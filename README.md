# Criadex SDK

A Python library to interact with the [Criadex](https://github.com/CriaYU/Criadex) RESTful API, now powered by Ragflow.

## Getting Started

1.  **Install the package from your locally cloned repository:**

    ```shell
    pip install .
    ```
    For development and testing, you may want to install it in editable mode:
    ```shell
    pip install -e '.[tests]'
    ```

2.  **Make your first query:**

    The SDK class name remains `CriadexSDK` for compatibility, but it now interacts with the new Ragflow-based backend.

    ```python
    import asyncio
    from CriadexSDK import CriadexSDK
    from CriadexSDK.ragflow_schemas import GroupSearchResponse, SearchGroupConfig

    # Create client targeting the Criadex service
    criadex: CriadexSDK = CriadexSDK(api_base="http://127.0.0.1:25574/")


    # Query criadex
    async def execute_query():
        # Authenticate with the Criadex API key
        await criadex.authenticate(api_key="YOUR_API_KEY_HERE")

        # Define the search configuration
        search_config = SearchGroupConfig(
            prompt="What day is Assignment 3 due?",
            top_k=5
        )

        # Execute the search
        response: GroupSearchResponse = await criadex.content.search(
            group_name="your_group_name",
            search_config=search_config.model_dump()
        )

        print("Retrieved Nodes: ", response.nodes)


    # Run the async function
    asyncio.run(execute_query())
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
- `client.auth.reset`

### Group Authorization

- `client.group_auth.create`
- `client.group_auth.delete`
- `client.group_auth.check`
- `client.group_auth.list`

### Model Management

- `client.models.create`
- `client.models.delete`
- `client.models.about`
- `client.models.update`

### Model Agents

The SDK provides access to different agent functionalities, which are categorized by the underlying model provider.

#### Ragflow Agents (`client.agents.azure`)

**Note:** These agents are currently accessed via the `client.agents.azure` attribute for backward compatibility.

- `client.agents.azure.chat`
- `client.agents.azure.intents`
- `client.agents.azure.language`
- `client.agents.azure.related_prompts`
- `client.agents.azure.transform`

#### Cohere Agents (`client.agents.cohere`)

- `client.agents.cohere.rerank`

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

## 📜 Licensing

This project is licensed under the GNU v3.0 License — See the [LICENSE](LICENSE) project file for details.