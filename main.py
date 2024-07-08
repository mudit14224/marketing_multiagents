# Imports
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]="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"
os.environ["LANGCHAIN_PROJECT"]="marketing-crew"
# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from pydantic import BaseModel, Field
from crewai_tools import tool
import json
from agents import MarketingAgents
from tasks import Tasks
from agents import create_researcher_agent

def run_crews(url, client, search_criteria):
    # Define the tools
    serper_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool(website_url=url)
    website_search_rag_tool = WebsiteSearchTool()

    # Get the query agents
    market_agents = MarketingAgents(serper_tool, scrape_tool, website_search_rag_tool)
    information_specialist, search_query_generator, consolidator = market_agents.create_query_agents()

    # Get the query tasks
    tasks = Tasks(information_specialist, search_query_generator)
    scrape_task, generate_search_query_task = tasks.create_query_tasks()

    # Define the crew with the query tasks
    initial_crew = Crew(
        agents=[information_specialist, search_query_generator],
        tasks=[scrape_task, generate_search_query_task],
        process=Process.sequential  # Ensure sequential execution for the initial tasks
    )

    # generating the queries till we get the correct format
    # setting max retries so that the system does not get stuck in an infinite loop
    max_retries = 3
    retry_count = 0
    search_queries = None

    while retry_count < max_retries:
        search_queries = initial_crew.kickoff(inputs={'client': client, 'search_criteria': search_criteria})
        json_queries = json.loads(search_queries)
        search_queries = json_queries['queries']
        # Break the while loop if the format is correct
        if isinstance(search_queries, list) and all(isinstance(query, str) for query in search_queries):
            break
        
        # Else we will loop back and run the crew again
        retry_count += 1

    if not search_queries:
        raise ValueError("Failed to generate search queries in the correct format after multiple retries.")
    
    # print("HERE ARE THE FINAL SEARCH QUERIES: \n")
    # print(search_queries)

    # Get the search tasks
    search_tasks, consolidate_results_task = tasks.create_search_tasks(create_researcher_agent, consolidator, search_queries)

    # Define the final crew with search tasks and consolidation task
    final_crew = Crew(
        agents=[consolidator] + [task.agent for task in search_tasks],
        tasks=search_tasks + [consolidate_results_task],
        # process=Process.sequential  # Parallel execution for search tasks
    )

    # Kickoff the final crew to execute the search and consolidation tasks
    final_result = final_crew.kickoff()

    # print("FINAL RESULT: \n")
    # print(final_result)

    return final_result


if __name__ == '__main__':
    # url for finding similar providers
    url = 'https://www.sutterhealth.org/'
    client = 'Sutter Health'
    search_criteria = 'provider speciality and location'
    run_crews(url, client, search_criteria)

