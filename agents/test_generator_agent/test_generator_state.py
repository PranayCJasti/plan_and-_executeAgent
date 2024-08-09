
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
import operator
from pydantic_class.py_models  import Task

from typing import TypedDict, Annotated, List, Union,Literal,Dict


# Define the state object for the agent graph
class TestGeneratorAgentState(TypedDict):
    project_name: Annotated[
        str, 
        "The name of the project."
    ]

     
    project_folder_strucutre: Annotated[
        str,
        "The organized layout of directories and subdirectories that form the project's "
        "file system, adhering to best practices for project structure."
    ]

    # @in 
    requirements_overview: Annotated[
        str, 
        "A comprehensive, well-structured document in markdown format that outlines "
        "the project's requirements derived from the user's request. This serves as a "
        "guide for the development process."
    ]

    # @in
    generated_project_path: Annotated[
        str,
        "The absolute path in the file system where the project is being generated. "
        "This path is used to store all the project-related files and directories."
    ]

    # @inout
    current_task: Annotated[
        Task,
        "The Task object currently in focus, representing the active task that team "
        "members are working on."
    ]
    
    # @inout
    messages: Annotated[
        list[tuple[str, str]], 
        "A chronological list of tuples representing the conversation history between the "
        "system, user, and AI. Each tuple contains a role identifier (e.g., 'AI', 'tool', "
        "'user', 'system') and the corresponding message."
    ]

    # @out
    code: Annotated[
        str, 
        "The complete, well-documented working code that adheres to all standards "
        "requested with the programming language, framework user requested ",
    ]

    # @out
    files_created: Annotated[
        list[str], 
        "The absolute paths of file that were created for this project "
        "so far."
    ]

    # @out
    infile_license_comments: Annotated[
        dict[str, str],
        "A list of multiline license comments for each type of file."
    ]
     


# Define the nodes in the agent graph
def get_agent_graph_state(state:TestGeneratorAgentState, state_key:str):
    if state_key == "docker_agent_all":
        return state["docker_agent_response"]
    elif state_key == "docker_agent_latest":
        if state["docker_agent_response"]:
            return state["docker_agent_response"][-1]
        else:
            return state["docker_agent_response"]
    # elif state_key=="main_agent_all":
    #     return state["main_agent_response"]
    # elif state_key=="main_agent_latest":
    #     if state["main_agent_response"]:
    #         return state["main_agent_response"][-1]
    #     else:
    #         return state["main_agent_response"]        
    else:
        return None
    
state = {
    "input":"",
    "chat_history": [],
    "agent_outcome": None,
    "intermediate_steps":[],
    "latest_execution_result":""
    # "docker_agent_response":[],
    # "main_agent_response":[]
}