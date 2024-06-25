

import os
import gradio as gr
from threading import Thread
import random
import time
import queue
import os
import json
from digitalab.core import digitalab
import pandas as pd
import re
import numpy as np
import queue
import threading


from openai import OpenAI
client = OpenAI(
    api_key='YOUR_API_KEY',
    base_url="http://0.0.0.0:23333/v1"
)

response_queue = queue.Queue()
exit_event = threading.Event()
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
        self.agent =Agent(num_agents)
        self.num_agents = num_agents
        self.processes = []
        

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def step(self):
        done = False
        
        while not done:
            action ,task= choose_action_strategy(self.agent.agent_id, self.agent.state)
            print(action)
            response_queue.put(f"{action}")
            
            new_state, reward, done = self.agent.step(action,task)
            self.agent.state = new_state
        exit_event.set()
        return done,self.agent.state


def bot_thread_func():
    env = MultiAgentEnv(num_agents=1)
    done,state = env.step()

bot_thread = Thread(target=bot_thread_func)


def user_thread_func(message, history):
    bot_thread.start()
    done=False
    while not exit_event.is_set():
        
        response = response_queue.get()
        print("响应")
        print(response)
        yield "", response
            

def bot(history,max_length, top_p, temperature):
        user_message = history[-1][0]
        for i, response in enumerate(user_thread_func(user_message, history)):
            if i == 0:
                history[-1][1] = response[1]
            else:
                history.append([None, response[1]])
            yield history

with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Web Automation Demo</h1>""")
    chatbot = gr.Chatbot()

    with gr.Row():
        with gr.Column(scale=4):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10, container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("Clear History")
            max_length = gr.Slider(0, 32768, value=8192, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.8, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0.01, 1, value=0.6, step=0.01, label="Temperature", interactive=True)


    def user(query, history):
        return "", history + [[query, ""]]


    submitBtn.click(user, [user_input, chatbot], [user_input, chatbot], queue=False).then(
        bot, [chatbot, max_length, top_p, temperature], chatbot
    )
    emptyBtn.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=5001, inbrowser=True, share=False)