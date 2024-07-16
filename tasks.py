# Imports
from crewai import Task
from pydantic import BaseModel, Field

# Using Pydantic for structured output
class Queries(BaseModel):
    queries: list[str] = Field(..., title="List of queries generated by the agent.")

class Tasks:
    def __init__(self, information_specialist, search_query_generator):
        self.information_specialist = information_specialist
        self.search_query_generator = search_query_generator

    def create_query_tasks(self):
        scrape_task = Task(
            description="""Scrape and extract all the relevant information about the company.""",
            agent=self.information_specialist,
            expected_output="""All the details about the {client} in a concise summary that can be used to build search queries based on the 
            search criteria of {search_criteria} to find similar companies.""")

        generate_search_query_task = Task(
        description="""Generate succinct search queries based on the provided criteria: {search_criteria} and 
        information gathered by the Information Specialist. The each query must include all of the search criteria. Generate at max 4 queries.""",
        expected_output='A Python list of strings, where each string is a search query.',
        agent=self.search_query_generator,
        output_json = Queries
        )

        return scrape_task, generate_search_query_task

    def create_search_tasks(self, create_researcher_agent, consolidator, search_queries):
        search_tasks = [
            Task(
                description=f"Search the internet using the query: '{query}' to find similar companies.",
                agent=create_researcher_agent(query),
                expected_output=f"A list of potential companies along with their website links found using the query: '{query}'"
            ) for query in search_queries
        ]

        # Define the consolidate results task
        consolidate_results_task = Task(
            description="Consolidate the list of potential companies from the researcher agents into a final list.",
            agent=consolidator,
            expected_output="A final list of potential companies including brief descriptions and website links"
        )

        return search_tasks, consolidate_results_task