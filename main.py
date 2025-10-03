# Note: In the project we are orchestrating multiple agents via LLM.

from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
enable_verbose_stdout_logging()
# set_tracing_disabled(disabled= True)


gemini_api_key= os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables. ")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model= OpenAIChatCompletionsModel(
    openai_client= external_client,
    model= "gemini-2.5-flash"
)

web_search_agent= Agent(
    name= "Web Search Agent",
    instructions= "You are a web search agent that can search the web for information.",
    model= model
)

#1.  Now we are making agent as tool.
web_search_agent_as_tool= web_search_agent.as_tool(
    tool_name="web_search_tool",
    tool_description= "Useful for searching the web for information about a topic."
)


data_analysis_agent= Agent(
    name= "Data Analysis Agent",
    instructions= "You are a data analysis agent that can analyze data about topic-related task and provide insights.",
    model= model
)

# 2. Now we are making agent as tool.
data_analysis_agent_as_tool= data_analysis_agent.as_tool(
    tool_name="data_analysis_tool",
    tool_description= "Useful for analyzing data and providing insights."
)


writer_agent= Agent(
    name= "Writer Agent",
    instructions= "Your task is to write a formal, structured report on the basis of provided analysis of user's topic. ",
    model= model
)

# 3. Now we are making agent as tool.
writer_agent_as_tool= writer_agent.as_tool(
    tool_name="writer_tool",
    tool_description= "Useful for writing formal, structured reports based on analysis."
)


main_agent= Agent(
    name= "Orchestrator Agent",
    instructions= """
You are an intelligent orchestrator agent.
1. Use web search tool to gather information about user's topic.
2. Use data analysis tool to analyze the gathered information and provide insights.
3. Use writer tool to write a formal, structured report based on the analysis.""",
model= model,
tools= [web_search_agent_as_tool, data_analysis_agent_as_tool, writer_agent_as_tool],
)

result= Runner.run_sync(
    starting_agent= main_agent,
    input= "Tell me about OpenAI agents SDK."
)

print(result.final_output)
