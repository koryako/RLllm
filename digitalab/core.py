import requests
import json
import os
import queue

current_dir = os.path.dirname(os.path.abspath(__file__))    
URL_API="http://127.0.0.1:7001"
class digitalab():
    def __init__(self,client):
        self.client=client
        self.task_queue = queue.Queue()

    def open_api(self,messages,tools=""):
        model_name = self.client.models.list().data[0].id
        if tools:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto",  # auto is default, but we'll be explicit
            )
            response_message = response.choices[0].message
            
            return response_message
        else:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            response_message = response.choices[0].message
            return response_message

    def call_function(self,content):
        #第一步，调用tool 模式
        messages = [{"role": "user", "content": content}]
        response_message= self.open_api(messages,tools)
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        print(tool_calls)
        if tool_calls:
        # if  isinstance(res['response'], dict):
            return self.run_task(response_message, messages)
        return response_message , ""


    def run_task(self,response_message, messages):
        messages.append(response_message)  # extend conversation with assistant's reply
        import tool_fun as fm
        tool_calls = response_message.tool_calls
    
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            func = getattr(fm, function_name.lower())
            print("--得到调用工具名称---")
            print(function_name)
            #function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            # Step 3: call the function
            print("---工具回调参数结果---")
            print(function_args)
            function_response=func(**function_args)
            print("---执行工具后返回的数据----")
            print(function_response)
            # function_response = function_to_call(
            #     location=function_args.get("location"),
            #     unit=function_args.get("unit"),
            # )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        # Step 4: send the info for each function call and function response to the model
        response_message= open_api(messages)
        second_message=response_message.content
        print("---调用工具返回结果----")
        print(second_message)
        return second_message,tool_calls


    def action_api(self,payload=[]):
        
        headers = {"Content-Type": "application/json"}
        url=URL_API+"/rpa/action?codeType=js"
        res = requests.post(url, data=json.dumps(payload),headers=headers)
        return res.json()

    def read_prompt(self,filename):
        text=""
        with open(filename,'r',encoding='UTF-8') as f:
            text=f.read()
        return text
    
    #html 提炼出json
    def htmltojson(self,html,action):
        prompt=self.read_prompt(current_dir+'/prompt_json.txt').format(html,action)
        messages = [{"role": "user", "content": prompt}]
        output = self.open_api(messages)
        return output.content

    def act(self,state):
         #大模型根据全量步骤和历史步骤输出当前任务
        current_task=self.plan(state['alltasks'],[""] if len(state['historys'])<1 else [state['historys'][-1]])
        print(current_task)
        if "任务已经完成" in current_task:
            return {"type":"finish"},current_task
        elif "tool" in current_task:
            
            return {"type":"tool"},cuttent_task
        #获取格式化后的html 
        html=state['html']
        print("----html----")
        print(html)
        #大模型根据html和当前任务生成动作json
        jsonstring=self.htmltojson(html,current_task)
        print(jsonstring)
        #json转action
        current_action=self.json2Action(jsonstring)
        return current_action,current_task

    def plan(self,alltasks,historys=[]):
        # 计划生成，返回当前要执行的任务
        prompt=self.read_prompt(current_dir+'/prompt_action.txt').format(alltasks,"\n".join(historys))
        messages = [{"role": "user", "content": prompt}]
        output = self.open_api(messages)
        return output.content


        #格式化html
    def parserhtml(self):
        headers = {"Content-Type": "application/json"}
        url=URL_API+"/rpa/action?codeType=js"
        payload=[{"type":"fn","params":{"code":"""
                                const elements = document.querySelectorAll('select, input, button');
                            // 初始化一个空字符串用于存储HTML
                            let html = '';
                            // 遍历元素并拼接它们的outerHTML到html字符串
                            elements.forEach((element) => {
                            console.log(element.type)
                            if (element.type!="hidden"){
                            html += element.outerHTML;
                            }
                            });
                            // 输出拼接好的HTML字符串
                            console.log(html);
                    return html
                    """}}]
        res = requests.post(url, data=json.dumps(payload),headers=headers)
        return res.json()['msg']['data']

    def get_tasks(self):
        return self.read_prompt(current_dir+'/tasks.txt')


        # return {"msg":"ok","code":200}

    def json2Action(self,jsonstring):
        action_json=json.loads(jsonstring)
        payload={}
        if action_json['type']=="click":
            payload={"type":action_json['type'],"params":{"className":action_json['css_Selector']}}
        elif action_json['type']=="input":
            payload={"type":action_json['type'],"params":{"className":action_json['css_Selector'],"value":action_json['value']}}
        elif action_json['type']=="wait":
            payload={"type":"wait","params":{"time":action_json['value']}}
        elif action_json['type']=="jumper":
            payload={"type":"goto","params":{"url":action_json['url']}}
        #出参  json {type:click,id:id,value}
        return payload

if __name__ == '__main__':
    res2=parserhtml()
    print(res2)
   













  


