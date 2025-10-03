# from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, set_tracing_disabled
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled= True)

# gemini_api_key= os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set in environment variables. ")


# external_client= AsyncOpenAI(
#     api_key= gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model= OpenAIChatCompletionsModel(
#     model= "gemini-2.5-flash",
#     openai_client= external_client
# )

# weather_agent= Agent(
#     name= "Weather Agent",
#     instructions= "You are a weather agent. your task is to to respond that the weather is sunny. ",
#     model= model
# )

# weather_agent_as_tool= weather_agent.as_tool(
#     tool_name= "weather_tool",
#     tool_description= "A tool to get the weather information. ",
# )

# mahar_agent= Agent(
#     name= "Mahar Agent",
#     instructions= "You are a mahar agent. your task is to to respond that mahar is great person and he is a AI Developer. ",
#     model= model
# )

# mahar_agent_as_tool= mahar_agent.as_tool(
#     tool_name= "mahar_tool",
#     tool_description= "A tool to get the information about mahar. ",
# )

# main_agent= Agent(
#     name= "Assistant",
#     instructions= "You are a helpful assistant. ",
#     model= model,
#     # handoffs= [weather_agent, mahar_agent]   # Handoffs allow the main agent to delegate tasks to these agents based on the conversation context.
#     tools=[weather_agent_as_tool, mahar_agent_as_tool]   # Tools allow the main agent to use these agents as tools when needed and that tool will be mentioned in this tools list if we want to use all the tools then mention all the tools r a specific.
# )

# result= Runner.run_sync(
#     starting_agent= main_agent,
#     input= "What is the weather today in Karachi? Also, tell me about mahar. ",
# )

# print(result.final_output)


# Handoffs r agent as tool mn differacne yh kh kh jb hm multiple agents ko main agent ko handoff krtay hn to wo instructions
# k mutabiq khud decide krta hn k konsa agent use krna hn agr hm agent ko tool k tor pr use krty hn to hm khud decide 
# krty hn k konsa agent use krna hn 




from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelSettings ,set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled= True)

gemini_api_key= os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables. ")

external_client= AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model= OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client= external_client
)


math_agent= Agent(
    name= "Math Agent",
    instructions= "You are a math agent. and your task is to solve the math problems. ",
    model= model
)

math_agent_as_tool= math_agent.as_tool(
    tool_name= "math_tool",
    tool_description= "A tool to solve math problems. ",
)

english_agent= Agent(
    name= "English Agent",
    instructions= "You are an english agent. and your task is to correct the english sentences. ",
    model= model
)

english_agent_as_tool= english_agent.as_tool(
    tool_name= "english_tool",
    tool_description= "A tool to correct english sentences. ",
)

main_agent= Agent(
    name= "Orchestrator Agent",
    instructions= "You are a helpful orchestrator agent. your task is to use the tools to solve the problems. ",
    model= model,
    tools= [math_agent_as_tool, english_agent_as_tool],
    model_settings= ModelSettings(tool_choice= "none" )  # tool_choice= "none" means that the agent will not use any tool by default and we have to specify the tool in the input prompt.
)

result= Runner.run_sync(
    starting_agent= main_agent,
    input= "Solve this math problem: 5 + 3 * 2. Also, correct this sentence: he go to school every day. ",
)

print(result.final_output)

