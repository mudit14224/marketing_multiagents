# Imports
from crewai import Agent
from crewai_tools import SerperDevTool


class MarketingAgents: 
    def __init__(self, serper_tool, scrape_tool, website_search_rag_tool):
        self.serper_tool = serper_tool
        self.scrape_tool = scrape_tool
        self.website_search_rag_tool = website_search_rag_tool

    def create_query_agents(self):
        # Information Specialist
        information_specialist = Agent(
            role = 'Information Specialist',
            goal = 'Gather all information about a healthcare provider',
            backstory = 
                """You work for a digital healthcare company called as Healee.
                You are an expert in detailed research and data compilation.
                You have to find out all the important information possible about {client} healthcare provider.""",
            tools = [self.scrape_tool],
            verbose = True,
            allow_delegation=False
        )

        # Query Agent
        search_query_generator = Agent(
        role='Search Query Generator',
        goal='Generate search queries to find similar healthcare providers companies to {client} based on provided criteria and gathered information',
        backstory='Proficient in creating effective search queries from given data.',
        allow_delegation=False, 
        verbose = True
        )

        # Final Consolidator Agent
        consolidator = Agent(
            role='Result Consolidator',
            goal='Combine all the results from the researcher agents into a final list of healthcare companies.',
            backstory='You excel at synthesizing information from multiple sources into a clear, concise list which has the company name and also the website link.',
            verbose=True,
            allow_delegation=False
        )

        return information_specialist, search_query_generator, consolidator

# Researcher Agent function
def create_researcher_agent(query):
    serper_tool = SerperDevTool()
    return Agent(
        role='Internet Researcher',
        goal=f'Find similar healthcare provider companies using the query: {query}',
        backstory="""You work in the marketing team of a digital healthcare company.
                    You are adept at using online resources to find relevant information quickly.
                    You are looking for potential healthcare provider clients similar to {client}
                    that your company can pitch your platform to and sign them.""",
        tools=[serper_tool],
        allow_delegation=False
    )