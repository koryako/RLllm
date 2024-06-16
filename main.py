import os
import json
from util import action_api,plan,parserhtml,htmltojson,get_tasks,json2Action
import pandas as pd
import re
import numpy as np

def choose_action_strategy(agentid,state):
    #print(agentid)
    #大模型根据全量步骤和历史步骤输出当前任务
    current_task=plan(state['alltasks'],[""] if len(state['historys'])<1 else [state['historys'][-1]])
    print(current_task)
    if "任务已经完成" in current_task:
        return {"type":"finish"},current_task
    #获取格式化后的html 
    html=parserhtml()
    print(html)
    #大模型根据html和当前任务生成动作json
    jsonstring=htmltojson(html,current_task)
    print(jsonstring)
    #json转action
    current_action=json2Action(jsonstring)
    return current_action,current_task

class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        # 初始化环境状态
        self.state = self.reset()

    def reset(self):
        # 重置环境状态
        #读取知识库任务步骤,返回环境的初始状态
        state={"historys":["开始"],"html":"","alltasks":get_tasks()}
        return state

    def step(self, action,task):
        # 执行动作，改变环境状态
        # 这应该返回新的状态、奖励和是否完成的标志
        # 例如：return new_state, reward, done
        done = False
        if action["type"]=="finish":
            done=True
            return self.state, "", done    
        #动作响应
        response=action_api(action)
        print(response)
        #更新html
        self.state["html"]=parserhtml()
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
   
 
