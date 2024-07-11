# Web+AI策略自动化

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/2.png)

## 📝目录

- [Web+AI策略自动化](#webai策略自动化)
  - [📝目录](#目录)
  - [📖 简介](#-简介)
        - [使用大语言模型的优点](#使用大语言模型的优点)
        - [使用大语言模型的缺点](#使用大语言模型的缺点)
        - [使用大语言模型通过AI agent](#使用大语言模型通过ai-agent)
        - [动作策略改进：](#动作策略改进)
        - [模型训练和更新：](#模型训练和更新)
        - [总结](#总结)
  - [🚀 News](#-news)
  - [🛠️ 使用方法](#️-使用方法)
    - [快速开始](#快速开始)
      - [LMDeploy启动模型](#lmdeploy启动模型)
  - [🖊️ Citation](#️-citation)

## 📖 简介


本项目展示了一种使用强化学习 (RL) 进行任务自动化的设计，其中包括利用大语言模型 (LLM) 来生成任务和动作。这是一个非常有前途的尝试，尤其是结合了 LLM 的自然语言处理能力和 RL 的序列决策优化。

##### 使用大语言模型的优点
1. 任务序列生成：
使用 LLM 来生成当前任务，这种方法可以灵活应对多种复杂任务，尤其是那些涉及自然语言处理的任务。
通过历史步骤来调整当前任务，可以使任务序列更加动态和智能化。
2. 动作生成：
基于 HTML 和当前任务生成 JSON 动作，这种方法能够应对网页自动化和其他基于 HTML 界面的任务。

3. 多智能体框架的使用：
支持多智能体并行执行任务，这对于需要分工协作的复杂任务非常有用。

#####  使用大语言模型的缺点
1. 环境感知不足：
当前框架中智能体的动作生成主要依赖预定义的任务序列和 HTML 解析结果，对环境变化的感知能力较弱。可以考虑增加环境状态的实时监控和感知机制。



##### 使用大语言模型通过AI agent
执行web自动化任务，比如测试用例自动化测试帮助减轻测试人员的工作。往往缺乏的先验知识，导致语言模型生成任务轨迹不稳定，且无法评价生成轨迹的有效性。我们用加入轨迹知识库，稳定模型的输出。另外未来还将通过RL模型学习专家模型在不同任务执行后发生的状态改变,不断优化策略轨迹。

提升环境感知能力的一种方法是引入更多的环境特征和状态信息，通过这些信息来动态调整任务和动作。例如，可以通过网页上的动态元素变化来调整任务执行策略。

##### 动作策略改进：

当前的动作生成策略比较静态，主要依赖预定义的任务和 HTML 解析结果。可以考虑引入强化学习中的策略网络（Policy Network）或者价值网络（Value Network），通过训练来优化动作选择。
采用深度 Q 网络（DQN）或者策略梯度方法，可以使智能体在不同环境状态下学会更优的动作选择策略。
奖励机制设计：

目前的框架中，奖励机制未详细设计。奖励机制在强化学习中至关重要，合理的奖励设计能够大大提升学习效果。可以根据任务完成情况、动作执行效果等多维度设计奖励函数。
探索与利用平衡：

在任务执行过程中，智能体需要在探索新策略和利用已知最佳策略之间取得平衡。可以采用 ε-贪心策略或者其他探索策略来改进智能体的任务执行效果。



##### 模型训练和更新：

未来考虑引入离线训练和在线更新相结合的策略，通过离线数据训练初始模型，然后在实际任务执行过程中逐步更新和优化模型参数。

##### 总结
利用 LLM 和 RL 进行任务自动化在未来有一定的潜力。通过引入更加动态的环境感知机制、优化动作策略和设计合理的奖励机制，可以进一步提升智能体的执行效果和适应能力。这将有助于在更加复杂和动态的任务环境中实现智能化任务自动化。

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/5.png)

如果你觉得这个项目对你有帮助，欢迎 ⭐ Star，让更多的人发现它！






## 🚀 News

\[2024.07.08] 该项目进入2024 世界人工智能大会(WAIC2024)-智浦大模型挑战赛50强。[媒体报道](https://mp.weixin.qq.com/s/hUcOwavLyzMThLgf4z1Y1g)

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

<details>
<summary> 智浦大模型挑战赛（夏季）50强 </summary>

![image](https://raw.githubusercontent.com/koryako/RLllm/main/image/10.png)

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


