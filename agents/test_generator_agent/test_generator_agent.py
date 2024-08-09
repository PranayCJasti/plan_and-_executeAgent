from agents.agent import Agent
from prompts.prompts import agent_system_prompt_template
from states.state import AgentGraphState, get_agent_graph_state, state
from utils.helper_functions import extract_docker_error_steps
from typing import TypedDict, Annotated,Literal
import ast
from states.state import AgentGraphState



class TestGeneratorAgent():

    
    test_code_generation: str = "test_code_generation"
    state_update: str = "state_update"
    execute_tools: str = "execute_tools"

    def __init__(self, tools, server, model, stop):
        self.execute_agent= Agent(tools=tools,model_service=server, model_name=model, stop=stop)
    def should_continue(self, data:AgentGraphState) -> Literal["planner","action"]:
        if data['agent_outcome']['tool_choice']=='no_tool' or data['agent_outcome']['error_correction'] != 'none':
            return "planner"
        else:
            return "continue"

    def run_agent(self, data:AgentGraphState):
        execute_agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=self.execute_agent.tool_description,chat_history='$$ '.join(str(e) for e in data['chat_history'][-5:]))
        print("agent data",data)
        if data['latest_execution_result'] != '':
            prompt="Asigned task :"+data['current_task']+ 'This is the output from the tool execution '+data['latest_execution_result']+ " Now that you have details about the task and the execution output, check if you can complete the task  "
        else:
            prompt= data['current_task'] 
        agent_outcome=self.execute_agent.think(data,execute_agent_system_prompt,prompt)
        # chatHis=data['chat_history']
        # chatHis.append(data['input'])
        return {"agent_outcome": agent_outcome}
    #agent work after think think
    def execute_tools(self,data:AgentGraphState):
        agent_action=data['agent_outcome']
        output=self.execute_agent.work(agent_action)
        
        print(f"The agent action is {agent_action}")
        print(f"The tool result is: {output}")
        return {"intermediate_steps": [(agent_action, str(output))]}

    def parse_output(self,data:AgentGraphState):
        print("tool output",data["intermediate_steps"][-1][1])
        tool_output=ast.literal_eval(data['intermediate_steps'][-1][1])
        parsed_output=' '.join(str(e) for e in extract_docker_error_steps(tool_output))
        print(f"the parsed output {parsed_output}")
        return {"latest_execution_result":parsed_output}





