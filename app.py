import asyncio
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient
import os

async def run_memory_chat():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"
    print("Initializing chat...")

    client = MCPClient.from_config_file(config_file)

    

    llm = ChatGroq(
        model="qwen-qwq-32b",  
        groq_api_key=api_key
    )

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )



    print("\n==========Chat with LLM using MCP==========\n")

    try:
        while True:
            user_input = input("\n\nYou: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Exiting...")
                break

            if user_input.lower() in ["clear", "cls"]:
                agent.clear_conversation_history()

            print("\nAssistant: ", end="", flush=True)
            response = await agent.run(user_input)
            print(f"Agent: {response}")
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())


