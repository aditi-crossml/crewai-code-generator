import subprocess
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
# tool for setting up the environment, e.g., installing dependencies
class SetupToolInput(BaseModel):
    argument: str = Field(..., description="Shell command to set up the environment.")

class SetupTool(BaseTool):
    name: str = "Setup Tool"
    description: str = "Runs a setup shell command like installing dependencies (e.g., pip install)."
    args_schema: Type[BaseModel] = SetupToolInput

    def _run(self, argument: str) -> str:
        try:
            output = subprocess.check_output(argument, shell=True, text=True)
            return f"Command executed:\n{output}"
        except subprocess.CalledProcessError as e:
            return f"Command failed:\n{e.output}"

# tool for generating file and its extension, e.g., generating a Python script
class FileGenerationToolInput(BaseModel):
    argument: str = Field(..., description="File name and extension to generate.")

class FileGenerationTool(BaseTool):
    name: str = "File Generation Tool"
    description: str = "Generates a file with the specified name and extension."
    args_schema: Type[BaseModel] = FileGenerationToolInput

    def _run(self, argument: str) -> str:
        # Placeholder for actual file generation logic
        return f"Generated file: {argument}"


# tool for code generation, e.g., generating a Python script

class CodeGenerationToolInput(BaseModel):
    argument: str = Field(..., description="Prompt for code generation.")

class CodeGenerationTool(BaseTool):
    name: str = "Code Generation Tool"
    description: str = "Generates code based on the provided prompt."
    args_schema: Type[BaseModel] = CodeGenerationToolInput

    def _run(self, argument: str) -> str:
        # Placeholder for actual code generation logic
        return f"Generated code based on prompt: {argument}"


#tool for saving code, e.g., saving a Python script to a file
class CodeSavingToolInput(BaseModel):
    filename: str = Field(..., description="Filename to save the code to.")
    code: str = Field(..., description="The code to write into the file.")

class CodeSavingTool(BaseTool):
    name: str = "Code Saving Tool"
    description: str = "Saves the provided code to the specified file."
    args_schema: Type[BaseModel] = CodeSavingToolInput
    
    def _run(self, filename: str, code: str) -> str:
        try:
            folder = "/home/adititiwari/Documents/saved-outputs"
            os.makedirs(folder, exist_ok=True)
            full_path = os.path.join(folder, filename)
            with open(full_path, "w") as file:
                file.write(code)
            return f"Code saved to '{filename}'"
        except Exception as e:
            return f"Failed to save code:\n{str(e)}"

        
# tool for running code, e.g., executing a Python script

class CodeExecutionToolInput(BaseModel):
    argument: str = Field(..., description="Code to execute.")

class CodeExecutionTool(BaseTool):
    name: str = "Code Execution Tool"
    description: str = "Executes the provided code."
    args_schema: Type[BaseModel] = CodeExecutionToolInput

    def _run(self, argument: str) -> str:
        try:
            output = subprocess.check_output(["python", "-c", argument], text=True)
            return f"Code executed successfully:\n{output}"
        except subprocess.CalledProcessError as e:
            return f" Code execution failed:\n{e.output}"

# tool for testing code, e.g., running unit tests
class CodeTestingToolInput(BaseModel):
    argument: str = Field(..., description="Code to test.")

class CodeTestingTool(BaseTool):
    name: str = "Code Testing Tool"
    description: str = "Runs tests on the provided code."
    args_schema: Type[BaseModel] = CodeTestingToolInput

    def _run(self, argument: str) -> str:
        # Placeholder for actual code testing logic
        return f"Running tests on the following code:\n{argument}"