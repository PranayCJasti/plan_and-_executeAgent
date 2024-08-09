from typing import TypedDict, Annotated,Literal

from agents.agent import (
   Agent
)
from prompts.prompts import (
    agent_system_prompt_template

)
from langgraph.graph import StateGraph, END
from utils.helper_functions import extract_docker_error_steps
import json
import ast
from tools.docker_builder import execute_docker_cmds
# from tools.google_serper import get_google_serper
# from tools.basic_scraper import scrape_website
from states.state import AgentGraphState, get_agent_graph_state, state

from langgraph.checkpoint.sqlite import SqliteSaver
from agents.docker_agent import DockerAgent
from agents.planer_agent  import PlannerAgent



class DockerGraph():
    def __init__(self,server,model,stop,tools):
        self.execute_agent = DockerAgent(tools=tools,server=server, model=model, stop=stop)
        self.planner_agent= PlannerAgent(tools=tools,server=server, model=model, stop=stop)
        graph=StateGraph(AgentGraphState)
        graph.add_node("agent",self.execute_agent.run_agent)
        graph.add_node("action",self.execute_agent.execute_tools)
        graph.add_node("parser",self.execute_agent.parse_output)
        graph.add_node("planner",self.planner_agent.run_planner_agent)

        graph.set_entry_point("planner")
        graph.add_conditional_edges("agent",self.execute_agent.should_continue, {"continue":"action","planner":"planner"})
        graph.add_edge('action','parser')
        graph.add_edge('parser','agent')
        graph.add_edge('planner','agent')
        graph.add_conditional_edges("planner",self.planner_agent.should_continue, {"continue":"agent","end":END})

        self.dockergraph= graph

def compile_workflow(graph):
    db_location="/home/pranay/persistance.db"
    memory =SqliteSaver.from_conn_string(db_location)
    workflow = graph.compile(checkpointer=memory)
    return workflow
