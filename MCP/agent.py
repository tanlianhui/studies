import asyncio
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,
)  # Optional
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseServerParams,
    StdioServerParameters,
)
import logging

logging.basicConfig(level=logging.WARNING)


# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv("../.env")


async def get_agent_async():
    """Gets tools from the File System MCP Server."""
    common_exit_stack = AsyncExitStack()

    # print("Attempting to connect to MCP Filesystem server...")
    math_tools, _ = await MCPToolset.from_server(
        # Use StdioServerParameters for local process communication
        connection_params=SseServerParams(
            command="npx",  # Command to run the server
            args=[
                "mcp-remote",
                "https://remote-mcp-server-authless.thomas-tan.workers.dev/sse",
            ],
        ),
        async_exit_stack=common_exit_stack
    )

    print(f"Fetched {len(math_tools)} tools from MCP server.")
    root_agent = LlmAgent(
        model="gemini-2.0-flash",  # Adjust model name if needed based on availability
        name="Agent",
        instruction="Help user interact with the MCP servers using available tools.",
        tools=math_tools,  # Provide the MCP tools to the ADK agent
    )
    return root_agent, common_exit_stack


async def async_main():
    session_service = InMemorySessionService()
    # Artifact service might not be needed for this example
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name="mcp_filesystem_app", user_id="user_fs"
    )

    # TODO: Change the query to be relevant to YOUR specified folder.
    # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"

    while True:
        query = input("Please ask - key in 'quit' to quit:\n")

        print(f"User Query: '{query}'")
        content = types.Content(role="user", parts=[types.Part(text=query)])

        root_agent, exit_stack = await get_agent_async()

        if query == "quit":
            # Crucial Cleanup: Ensure the MCP server process connection is closed.
            print("Closing MCP server connection...")
            await exit_stack.aclose()
            print("Cleanup complete.")

        runner = Runner(
            app_name="mcp_filesystem_app",
            agent=root_agent,
            artifact_service=artifacts_service,  # Optional
            session_service=session_service,
        )

        # print("Running agent...")
        events_async = runner.run_async(
            session_id=session.id, user_id=session.user_id, new_message=content
        )

        async for event in events_async:
            # print(f"Event received: {event}")
            if "text" in event.content.parts[0].__dict__:
                print(event.content.parts[0].text)


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")
