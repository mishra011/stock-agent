import os
from crewai import Agent

#from tools.browser_tools import BrowserTools
from tools.my_browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools

#from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

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





class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
      verbose=True,
      llm=llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and market sentiments. Now you're working on a super 
      important customer""",
      verbose=True,
      llm=llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        YahooFinanceNewsTool(),
        SECTools.search_10q,
        SECTools.search_10k
      ],
      allow_delegation=True
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      verbose=True,
      llm=llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
        YahooFinanceNewsTool()
      ]
    )
  
