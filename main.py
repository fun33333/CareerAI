import chainlit as cl
import os
from dotenv import load_dotenv
from typing import cast
from agent_files.main_agent import main_agent
from agents import Runner 
# from agents.run import RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
    # #Reference: https://ai.google.dev/gemini-api/docs/openai
    # external_client = AsyncOpenAI(
    # api_key=gemini_api_key,
    # base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    # )

    # model = OpenAIChatCompletionsModel(
    # model="gemini-2.0-flash",
    # openai_client=external_client
    # )

    # config = RunConfig(
    # model=model,
    # model_provider=external_client,
    # tracing_disabled=True
    # )

    cl.user_session.set("history", [])
    # cl.user_session.set("config", config)

    

    # agent: Agent = Agent(
    #     name="Assistant",
    #     instructions="""You are a career couselling model that can help users with their career choices and decisions.Do not give any information about the user's personal information. ANd only help with career related questions or information. you only can answer in urdu roman but smartly use english words to make it more natural and human like. """,
    #     model=model
    # )
    # cl.user_session.set("history",[])

    # # await cl.Message(content="Hello, Welcome to the Career Counselling Model! let's discuss your career goals and aspirations.").send()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Simple Calculation",
            message="What is 25 + 17?",
            icon="/public/calculator_icon.svg",
        ),
        cl.Starter(
            label="Complex Math",
            message="Solve for x: 2x + 5 = 15",
            icon="/public/calculator_icon.svg",
        ),
        cl.Starter(
            label="Web Search",
            message="Who is the current president of Pakistan?",
            icon="/public/web_search_icon.svg",
        ),
        cl.Starter(
            label="Current Events",
            message="What are the latest developments in AI?",
            icon="/public/web_search_icon.svg",
        ),
        cl.Starter(
            label="Math Help",
            message="Can you help me understand how to calculate percentages?",
            icon="/public/calculator_icon.svg",
        )
    ]


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})
    msg = cl.Message(content="thinking...")
    await msg.send()

    # agent: Agent = cast(Agent, cl.user_session.get("agent"))
    # config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
   
    try:
        # print("\n[CALLING_AGENT_WITH_HISTORY]\n", history,"\n")

        result =Runner.run_sync(
            starting_agent=main_agent,
            input=history,
            # run_config=config
        )

        # print("\n[AGENT_RESPONSE]\n", result.final_output,"\n")

        response = result.final_output
        msg.content = response
        await msg.update()

        cl.user_session.set("history", result.to_input_list())

        print(f"User: {message.content}\nAssistant: {response}")

    except Exception as e:
        msg.content = f"Sorry, I encountered an error while processing your request. Please try again later. Error: {e}"
        await msg.update()

        print(f"Error: {e}")

if __name__ == "__main__":
    cl.run()