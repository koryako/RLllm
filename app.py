

import os
import gradio as gr

from threading import Thread
import random
import time
def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def predict(history, max_length, top_p, temperature):
    
    # streamer = TextIteratorStreamer(tokenizer, timeout=60, skip_prompt=True, skip_special_tokens=True)
    # generate_kwargs = {
    #     "input_ids": model_inputs,
    #     "streamer": streamer,
    #     "max_new_tokens": max_length,
    #     "do_sample": True,
    #     "top_p": top_p,
    #     "temperature": temperature,
    #     "stopping_criteria": StoppingCriteriaList([stop]),
    #     "repetition_penalty": 1.2,
    # }
    # t = Thread(target=model.generate, kwargs=generate_kwargs)
    # t.start()
    
    bot_message = random.choice(["你好吗？", "我爱你", "我很饿"])
    history[-1][1] = ""
    for character in bot_message:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

    # for new_token in streamer:
    #     if new_token != '':
    #         history[-1][1] += new_token
    #         yield history


def chat_response(message, history):
    # 这里可以添加你的聊天机器人逻辑
    responses = ["回复1", "回复2", "回复3"]  # 示例回复列表
    
    for response in responses:
        yield "", response

def bot(history,max_length, top_p, temperature):
        user_message = history[-1][0]
        for i, response in enumerate(chat_response(user_message, history)):
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
        return "", history + [[parse_text(query), ""]]


    submitBtn.click(user, [user_input, chatbot], [user_input, chatbot], queue=False).then(
        bot, [chatbot, max_length, top_p, temperature], chatbot
    )
    emptyBtn.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=5001, inbrowser=True, share=False)