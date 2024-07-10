from crewai import Agent

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import AzureChatOpenAI

from crewai_tools.tools import WebsiteSearchTool, FileReadTool
from crewai_tools import SerperDevTool
from crewai import Task
from crewai import Crew,Process


## TOOL 
web_search_tool = WebsiteSearchTool()
#seper_dev_tool = SerperDevTool()

## AGENT

from langchain_community.llms import Ollama

llm = Ollama(model="llama3")


# AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
# AZURE_KEY = os.getenv("AZURE_KEY")
# AZURE_VERSION = os.getenv("AZURE_VERSION")
# AZURE_DEP_NAME = os.getenv("AZURE_DEP_NAME")

# llm = AzureChatOpenAI(deployment_name=AZURE_DEP_NAME,
#                          openai_api_version=AZURE_VERSION,
#                           openai_api_key=AZURE_KEY,
#                            azure_endpoint=AZURE_ENDPOINT)

coder_agent = Agent(
    role="Senior Python Developer",
    goal='Generate python code for solving the {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of"
        "innovation, eager to explore and share knowledge that could change"
        "the world and python community"

    ),
    tools=[web_search_tool],
    llm=llm,
    allow_delegation=True
)

## TASK
# Writing task with language model configuration
coding_task = Task(
  description=(
    "Generate Python code on {topic}."
    "Explain the topic and the code to a python beginner."
    "Focus on details by Commenting at important steps in the code."
  ),
  expected_output='A article and the Python code on the {topic}, formatted as markdown.',
  tools=[web_search_tool],
  agent=coder_agent,
  async_execution=False,
  output_file='code.md'  # Example of output customization
)

# EXECUTE

crew=Crew(
    agents=[coder_agent],
    tasks=[coding_task],
    process=Process.sequential,
)


result=crew.kickoff(inputs={'topic':'Binary Search'})
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(result)