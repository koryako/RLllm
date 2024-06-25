import os
import json
from digitalab.core import digitalab
import pandas as pd
import re
import numpy as np
from openai import OpenAI
client = OpenAI(
    api_key='YOUR_API_KEY',
    base_url="http://0.0.0.0:23333/v1"
)


webrobot=digitalab(client)

def choose_action_strategy(agentid,state):
    #print(agentid)
    current_action,current_task=webrobot.act(state)
    return current_action,current_task

class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        # 初始化环境状态
        self.state = self.reset()

    def reset(self):
        # 重置环境状态
        #读取知识库任务步骤,返回环境的初始状态
        state={"historys":["开始"],"html":"","alltasks":webrobot.get_tasks()}
        return state

    def step(self, action,task):
        # 执行动作，改变环境状态
        # 这应该返回新的状态、奖励和是否完成的标志
        # 例如：return new_state, reward, done
        done = False
        if action["type"]=="finish":
            done=True
            return self.state, "", done
            #调用工具
        elif  action['type']=="tool":
            call_response,_=webrobot.call_function(task)
            self.state['historys'].append(task)
            return self.state, "", done
        #动作响应
        response=webrobot.action_api(action)
        print(response)
        #更新html
        self.state["html"]=webrobot.parserhtml()
        self.state['historys'].append(task)
        return self.state, "", done

class MultiAgentEnv:
    def __init__(self, num_agents):
        self.agents = [Agent(agent_id) for agent_id in range(num_agents)]
        self.num_agents = num_agents
        self.processes = []

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def step(self):
        done = False
        for agent in self.agents:
            action ,task= choose_action_strategy(agent.agent_id, agent.state)
            print(action)
            new_state, reward, done = agent.step(action,task)
           
            agent.state = new_state
        return done

  
if __name__ == '__main__':
    
   
    env = MultiAgentEnv(num_agents=1)
    done = False
    while not done:
        done = env.step()

 
   
 