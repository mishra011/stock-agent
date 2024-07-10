import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from crewai_tools import ScrapeWebsiteTool


from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = "NA"


llm_selected = "AzureOpenAI"
#llm_selected = "Ollama"

if llm_selected == "Ollama":
  from langchain.llms import Ollama
  llm = Ollama(model="llama3")
elif llm_selected == "AzureOpenAI":
  from langchain_openai import AzureChatOpenAI
  from langchain.llms import AzureOpenAI

  AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
  AZURE_KEY = os.getenv("AZURE_KEY")
  AZURE_VERSION = os.getenv("AZURE_VERSION")
  AZURE_DEP_NAME = os.getenv("AZURE_DEP_NAME")

  # llm = AzureOpenAI(deployment_name=AZURE_DEP_NAME,
  #                         openai_api_version=AZURE_VERSION,
  #                           openai_api_key=AZURE_KEY,
  #                           azure_endpoint=AZURE_ENDPOINT)

  llm = AzureChatOpenAI(deployment_name=AZURE_DEP_NAME,
                          openai_api_version=AZURE_VERSION,
                            openai_api_key=AZURE_KEY,
                            azure_endpoint=AZURE_ENDPOINT)


class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    #tool = ScrapeWebsiteTool()
    tool = ScrapeWebsiteTool(website_url=website)
    text = tool.run()
    #print(text)
    #elements = partition_html(text=response.text)
    elements = text.split()
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing research and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do research about a given topic.",
          allow_delegation=False,
          llm=llm
          )
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
