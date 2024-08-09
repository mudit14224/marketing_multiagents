# Imports
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

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
    
class ContactSearchAgents:
    def __init__(self) -> None:
        pass

    def create_contact_search_agents(self): 
        search_agent = Agent(
            role = 'Contact Searcher', 
            goal = 'Find the contact details of the marketing team or relevant people from a specified client.',
            backstory = 
            """
            You are a dedicated member of the marketing team at Healee, a digital healthcare company. 
            Your expertise lies in leveraging online resources to quickly gather essential information. 
            You have identified {client} as a potential client for the Healee platform. 
            Your task is to find contact information such as email addresses, LinkedIn profiles, Phone no. 
            of key individuals within {client}'s organization who can be approached to set up a meeting. 
            This includes members of their marketing team or other relevant stakeholders. 
            """, 
            tools = [SerperDevTool()], 
            allow_delegation = False
        )

        scraper_agent = Agent(
            role='Web Scraper',
            goal='Scrape relevant information from specified websites',
            backstory="""
            You are a skilled web scraper working for the marketing team at Healee, a digital healthcare company. 
            Your task is to extract crucial information from websites to support various marketing and research activities. 
            This includes gathering contact details, company profiles, and other relevant data from the given URLs.
            """,
            tools=[ScrapeWebsiteTool()],
            allow_delegation=False
        )

        # Final Consolidator Agent
        contact_consolidator = Agent(
            role='Result Consolidator',
            goal='Combine all the contact information gathered by the scraper agents into a final, organized list of relevant contacts.',
            backstory=(
                "You are a highly skilled data synthesizer, adept at merging information from multiple sources. "
                "Your expertise lies in compiling comprehensive, clear, and concise lists of relevant contact information. "
                "Your meticulous approach ensures no detail is overlooked, providing a valuable resource for your team."
            ),
            verbose=True,
            allow_delegation=False
        )

        return search_agent, scraper_agent, contact_consolidator