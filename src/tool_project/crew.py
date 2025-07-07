from json import tool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.custom_tool import (
    MyCustomTool,
    FileGenerationTool,
    CodeGenerationTool,
    CodeSavingTool,
    CodeExecutionTool,
    CodeTestingTool,
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ToolProject():
    """ToolProject crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    tools: List[str] = []  # Add any custom tools you want to use in your crew

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

   
    def tools(self):
        return [
        MyCustomTool(),
        FileGenerationTool(),
        CodeGenerationTool(),
        CodeSavingTool(),
        CodeExecutionTool(),
        CodeTestingTool(),
    ]

    # @agent
    # def setup_agent(self) -> Agent:
    #     return Agent(
    #     config=self.agents_config['setup_agent'],
    #     tools=[MyCustomTool(), FileGenerationTool()],
    #     verbose=True
    #     )   

    @agent
    def code_generation_agent(self) -> Agent:
        return Agent(
        config=self.agents_config['code_generation_agent'],
        tools=[CodeGenerationTool()],
        verbose=True
    )

    @agent
    def code_saving_agent(self) -> Agent:
        return Agent(
        config=self.agents_config['code_saving_agent'],
        tools=[CodeSavingTool(), FileGenerationTool()],
        verbose=True
    )

    @agent
    def code_execution_agent(self) -> Agent:
        return Agent(
        config=self.agents_config['code_execution_agent'],
        tools=[CodeExecutionTool()],
        verbose=True
    )

    @agent
    def code_testing_agent(self) -> Agent:
        return Agent(
        config=self.agents_config['code_testing_agent'],
        tools=[CodeTestingTool()],
        verbose=True
    )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    #@task
    # def setup_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['setup_task'], # type: ignore[index]
    #     )

    @task
    def code_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_generation_task'], # type: ignore[index]
            # output_file='.report.md'
        )
    @task
    def code_saving_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_saving_task'], # type: ignore[index]
        )

    @task
    def code_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_execution_task'], # type: ignore[index]
        )

    @task
    def code_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_testing_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ToolProject crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
