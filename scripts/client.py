from llama_index.llms.openai import OpenAI
import dotenv
from llama_index.tools.mcp import McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall
from llama_index.core.workflow import Context
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

dotenv.load_dotenv()

llm = OpenAI(model="gpt-4o")


SYSTEM_PROMPT = """\
You are an AI assistant.

Before you help a user, you need to fetch the ip info first, to help you follow the laws of the country.
"""


async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can fetch the ip info of the user.",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_content, ctx=agent_context)
    async for event in handler.stream_events():
        if verbose and type(event) == ToolCall:
            print(f"Calling tool {event.tool_name} with kwargs {event.tool_kwargs}")
        elif verbose and type(event) == ToolCallResult:
            print(f"Tool {event.tool_name} returned {event.tool_output}")

    response = await handler
    return str(response)


async def main():
    # We consider there is a mcp server running on 127.0.0.1:8000, or you can use the mcp client to connect to your own mcp server.
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tool = McpToolSpec(client=mcp_client)

    # get the agent
    agent = await get_agent(mcp_tool)

    # create the agent context
    agent_context = Context(agent)

    tools = await mcp_tool.to_tool_list_async()
    for tool in tools:
        print(tool.metadata.name, tool.metadata.description)

    while True:
        user_input = input("Enter your message: ")
        if user_input == "exit":
            break
        print("User: ", user_input)
        response = await handle_user_message(
            user_input, agent, agent_context, verbose=True
        )
        print("Agent: ", response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
