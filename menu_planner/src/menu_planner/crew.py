from menu_planner.tools.custom_tool import foodDatabase
from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq
from agentops.agent import track_agent
import agentops
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


agentops.init()

# Uncomment the following line to use an example of a custom tool
# from menu_planner.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class MenuPlannerCrew():
	"""MenuPlanner crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self) -> None:
		#Groq
		self.groq_llm = ChatGroq(
			temperature=0,
			groq_api_key=os.environ.get("GROQ_API_KEY"),
			model_name="llama3-70b-8192",
		)

		#Ollama
		self.ollama_llm = ChatOpenAI(
			model="mistral",
			base_url="http://localhost:11434/v1",
			api_key = "ollama",
			temperature = 0,

		)

    #@track_agent(name="userInteractionAgent")
	@agent
	def userInteractionAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['userInteractionAgent'],
			#tools=[foodDatabase()], # Example of custom tool, loaded on the beginning of file
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)
    
	#@track_agent(name="dietaryAnalysisAgent")
	@agent
	def dietaryAnalysisAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['dietaryAnalysisAgent'],
			#tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)
    
	#@track_agent(name="recipeRecommendationAgent");
	@agent
	def recipeRecommendationAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['recipeRecommendationAgent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)
    
	#@track_agent(name="calorieTrackingAgent");
	@agent
	def calorieTrackingAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['calorieTrackingAgent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)
    
	#@track_agent(name="menuCreationAgent");
	@agent
	def menuCreationAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['menuCreationAgent'],
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)

	@task
	def userInteraction(self) -> Task:
		return Task(
			config=self.tasks_config['userInteraction'],
			agent=self.userInteractionAgent(),
			output_file = "userInteraction.md"
		)

	@task
	def dietaryAnalysis(self) -> Task:
		return Task(
			config=self.tasks_config['dietaryAnalysis'],
			agent=self.dietaryAnalysisAgent(),
			output_file = "dietaryAnalysis.md"
		)

	@task
	def recipeRecommendation(self) -> Task:
		return Task(
			config=self.tasks_config['recipeRecommendation'],
			agent=self.recipeRecommendationAgent(),
			output_file = "recipeRecommendation.md"
		)

	@task
	def calorieTracking(self) -> Task:
		return Task(
			config=self.tasks_config['calorieTracking'],
			agent=self.calorieTrackingAgent(),
			output_file = "calorieTracking.md"
		)
	
	@task
	def menuCreation(self) -> Task:
		return Task(
			config=self.tasks_config['menuCreation'],
			agent=self.menuCreationAgent(),
			output_file = "Menu.md"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MenuPlanner crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			 process=Process.sequential,
			 memory=False,
			 #max_rpm=2,
			 verbose=2 ,# In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)