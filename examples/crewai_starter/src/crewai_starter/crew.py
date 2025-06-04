from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import FileWriterTool
from .utils.file_name_generator import generate_filename


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_writer_tool = FileWriterTool()


@CrewBase
class CrewaiStarter():
    """CrewaiStarter crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    # TODO: Figure out how to make it use tools and write to disk   
    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'], # type: ignore[index]
    #         output_file='report.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiStarter crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    # tools
    @tool("DuckDuckGoSearch")
    def search(search_query: str):
        """Search the web for information on a given topic."""
        print("USING DUCK DUCK GO SEARCH")
        return DuckDuckGoSearchRun().run(search_query)
    
    # tools
    @tool("SaveOutputMarkdown")
    def save_markdown_report(markdown_content: str):
        """Write generated makrdown report to file"""
        print("WRITING OUTPUT TO FILE   ")
        file_name = generate_filename()
        result = file_writer_tool._run(file_name, markdown_content, '.')
        return f"Wrote contents to {file_name}"