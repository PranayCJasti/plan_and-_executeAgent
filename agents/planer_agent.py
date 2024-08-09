from agents.agent import Agent

from prompts.planner_prompt import planner_agent_system_prompt_template
from states.state import AgentGraphState, get_agent_graph_state, state
from utils.helper_functions import extract_docker_error_steps
from typing import TypedDict, Annotated,Literal
import ast
from states.state import AgentGraphState



class PlannerAgent():
    def __init__(self, tools, server, model, stop):
        self.planner_agent= Agent(tools=tools,model_service=server, model_name=model, stop=stop)

    def should_continue(self, data:AgentGraphState) -> Literal["__end__","agent"]:
        if (data['current_task']=='none' or (data['agent_outcome']['error_correction'] != 'none' if data['agent_outcome'] != {} else False) ):
            return "end"
        else:
            return "continue"
    def run_planner_agent(self, data:AgentGraphState):
        planner_agent_system_prompt = planner_agent_system_prompt_template.format(tool_descriptions=self.planner_agent.tool_description,chat_history='$$ '.join(str(e) for e in data['chat_history'][-5:]) if data['chat_history'] is not None else "",task_steps=data['task_steps'],task_status=data['steps_status'],task_execution=data['current_task'],task_result=data['latest_execution_result'])
        print("planner_agent data",data)
        if data['latest_execution_result'] != '':
            prompt="The executor performed the task " +data['current_task'] + ". The output of the task performed by the executor "+ data['latest_execution_result'] + " Now looking at the output of the task, assign the executor new task after updating the executed tasak status in the task_status dictionary or request for more information from the user or End the execution if all tasks are completed by making the task_execution as none"
        else:
            prompt= data['input'] 
        planner_agent_outcome=self.planner_agent.think(data,planner_agent_system_prompt,prompt)
        print("planner agent", planner_agent_outcome)
        return {"task_steps": planner_agent_outcome['tasks_created'],"chat_history":data['input'],"steps_status":planner_agent_outcome['task_status'],"current_task":planner_agent_outcome['task_execution']}





