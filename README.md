# Web+AI策略自动化

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/2.png)

## 📝目录

- [Web+AI策略自动化](#webai策略自动化)
  - [📝目录](#目录)
  - [📖 简介](#-简介)
  - [🚀 News](#-news)
  - [🛠️ 使用方法](#️-使用方法)
    - [快速开始](#快速开始)
      - [LMDeploy启动模型](#lmdeploy启动模型)
  - [🖊️ Citation](#️-citation)

## 📖 简介

使用大语言模型通过AI agent 执行web自动化任务，比如测试用例自动化测试帮助减轻测试人员的工作。往往缺乏的先验知识，导致语言模型生成任务轨迹不稳定，且无法评价生成轨迹的有效性。我们用加入轨迹知识库，稳定模型的输出。另外未来还将通过RL模型学习专家模型在不同任务执行后发生的状态改变,不断优化策略轨迹。

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/5.png)

如果你觉得这个项目对你有帮助，欢迎 ⭐ Star，让更多的人发现它！






## 🚀 News

\[2024.06.26] 完善了README，技术路线。

\[2024.06.24] 上传代码仓库，优化代码依赖结构。

\[2024.06.20] 项目框架搭建完成

## 🛠️ 使用方法

### 快速开始


1.  本地部署

```bash
git clone https://github.com/koryako/RLllm.git
python main.py
```


2. UI Demo

```bash
python app.py
```

[观看Demo视频](https://www.bilibili.com/video/BV1Tt3qezEdh/?spm_id_from=333.999.0.0)


#### LMDeploy启动模型

*   首先安装LMDeploy

```shell
pip install -U lmdeploy
```
*   LMDeploy 启动模型

```shell
lmdeploy serve api_server 你的模型目录地址/internlm2-chat-7b --server-port 23333
```
*   openAI 函数请求接口
```shell
 from openai import OpenAI
 client = OpenAI(
     api_key='YOUR_API_KEY',#这里可以空置
     base_url="http://0.0.0.0:23333/v1"
 )
```
<details>
<summary> 应用场景 </summary>

数据采集与分析

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/1.jpg)

测试用例

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/3.png)

AI客服

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/4.png)

</details>
## 🖊️ Citation

```bibtex
@misc{2024,
    title={An LLM Model Utilizing a Reinforcement Learning Framework},
    author={Jay},
    howpublished = {\url{https://github.com/koryako/RLllm}},
    year={2024}
}
```


