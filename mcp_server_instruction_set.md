# Instruction Set: Building MCP Servers (Python, Time Server Pattern)

## 1. **Project Structure**

Organize your MCP server as a Python package, with the following structure:

```
your_server/
  src/
    your_server_name/
      __init__.py
      server.py         # Main server logic (see below)
      __main__.py       # Entrypoint for CLI/module execution
  README.md
  pyproject.toml
  Dockerfile            # (optional, for containerization)
  test/
    test_server.py      # (unit/integration tests)
```

## 2. **Imports and Dependencies**

- Use standard libraries (`datetime`, `json`, etc.).
- Use [Pydantic](https://docs.pydantic.dev/) for input/output schemas.
- Use the MCP server framework (`mcp.server`, `mcp.types`, etc.).
- Use any domain-specific libraries as needed.

## 3. **Define Tool Names**

- Use an `Enum` or constants to define tool names, e.g.:

```python
from enum import Enum

class MyTools(str, Enum):
    TOOL_ONE = "tool_one"
    TOOL_TWO = "tool_two"
```

## 4. **Define Input and Output Schemas**

- Use Pydantic models for all tool inputs and outputs.

```python
from pydantic import BaseModel

class ToolOneInput(BaseModel):
    param1: str
    param2: int

class ToolOneResult(BaseModel):
    result: str
    details: dict
```

## 5. **Implement Business Logic**

- Encapsulate logic in a class (e.g., `MyServer`).
- Each tool should be a method with clear input/output types.

```python
class MyServer:
    def tool_one(self, param1: str, param2: int) -> ToolOneResult:
        # Implement logic
        return ToolOneResult(result="...", details={})
```

## 6. **Utility Functions**

- Abstract environment/system-specific logic into helpers.
- Validate and sanitize all external inputs early.

## 7. **MCP Server Setup**

- Use the MCP server framework to:
  - Instantiate the server with a unique name.
  - Register tool listing and tool call handlers using decorators.
  - Provide a JSON schema for each tool’s arguments.

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

async def serve():
    server = Server("mcp-your-server")
    my_server = MyServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=MyTools.TOOL_ONE.value,
                description="Describe tool one.",
                inputSchema=ToolOneInput.model_json_schema(),
            ),
            # Add more tools as needed
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == MyTools.TOOL_ONE.value:
            input_data = ToolOneInput(**arguments)
            result = my_server.tool_one(input_data.param1, input_data.param2)
            return [TextContent(type="text", text=result.model_dump_json(indent=2))]
        # Handle other tools
        else:
            raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
```

## 8. **Error Handling**

- Validate all arguments and provide clear, actionable error messages.
- Use custom exceptions for domain-specific errors.

## 9. **Entrypoint**

- In `__main__.py`, provide a CLI entrypoint to run the server:

```python
import asyncio
from .server import serve

if __name__ == "__main__":
    asyncio.run(serve())
```

## 10. **Documentation**

- Document each tool, its arguments, and response schema in your README.
- Provide example requests and responses.
- Include installation, configuration, and debugging instructions.

## 11. **Testing**

- Write unit tests for each tool’s business logic.
- Write integration tests for the server interface.

## 12. **Extensibility**

- To add a new tool:
  1. Add a new enum value.
  2. Define new input/output schemas.
  3. Implement the business logic method.
  4. Register the tool in `list_tools` and handle it in `call_tool`.

## 13. **Style and Best Practices**

- Follow PEP 8 and your organization’s code style.
- Use descriptive identifiers and docstrings.
- Keep functions/classes focused on a single responsibility.
- Prefer composition over inheritance.
- Ensure all code is testable in isolation.

## 14. **Security and Robustness**

- Validate all external input.
- Handle exceptions and edge cases explicitly.
- Log enough context for debugging, but avoid leaking sensitive data.

## 15. **Packaging and Distribution**

- Provide a `pyproject.toml` for packaging.
- Optionally, provide a `Dockerfile` for containerized deployment.

## 16. **Contribution and Licensing**

- Encourage contributions and clearly state your license (e.g., MIT).

---

**This instruction set can be adapted for any new MCP server. For other languages (e.g., TypeScript), follow analogous patterns: strong typing, schema-driven design, separation of business logic, and protocol handler registration.**
