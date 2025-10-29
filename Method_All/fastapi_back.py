from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from method import Assistant
from Method_Useful.RemoveThink import RemoveThink,InputRemoveThink
from Method_Useful.GetApikey import GetApikey
from Method_Useful.SendtoAi import SendtoAi

'''
fastapi接口段
接口暴露
不同的页面会通过POST不同的地址访问来自后端的不同种类的代码
'''

# -----------------------------------------------
# uvicorn fastapi_back:app --reload     启动服务器
# -----------------------------------------------

app = FastAPI()

# 这段代码的格式 Item包括了发送给ai的messages中的角色role和对话内容content
# RequestInput包括了大语言模型名称和messages包含了Item里的内容
class Item(BaseModel):
    role: str
    content: str

# None表示非必需   
class RequestInput(BaseModel):
    language: str = None
    requirement: str = None
    code: str = None
    error: str = None
    model: str
    messages: list[Item]

# ----------------------------
#  样例输入:  {
#     "model":"deepseek",
#     "messages":[{
#         "role":"user",
#         "content":"hello"
#     }]
# }         -->(RequestInput)
# ----------------------------

# localopenai早期实现fastapi接口的代码，将被保留下来

# 定义post接口   调用SendtoAi
@app.post("/localopenai")
async def OpenAi(request_inputs:RequestInput):
    client = GetApikey(request_inputs.model)
    reply = await SendtoAi(client,request_inputs.model,request_inputs.messages)
    # 样例输入 reply = await SendtoAi("ds",[{"role": "user", "content": "Hello."}])
    reply = RemoveThink(request_inputs.model,reply)
    return reply

'''
# ------这块已经被弃用-------
# 已经可以依靠Get_Apikey返回不同的client内容不需要自行设定
# !调用ds官网要保证model正确.
# @app.post("/openai")
# async def OpenAi(request_inputs:RequestInput):
#     client = Get_Apikey(request_inputs.model)
#     reply = await SendtoAi(client,request_inputs.model,request_inputs.messages)
#     return reply
# --------------------------
'''

# 代码优化后的结果，并不一定要如此
# 这段代码创建了来自method.py中的Assistand类
# Assistand类包含了多种实现方法。
# 由于目前Assistand中仅仅包含六种方法，两种实现方法之间的差距并不大。

def CreateAssistant(request_inputs:RequestInput):
    # 通过model获取匹配的client
    client = GetApikey(request_inputs.model)
    # 完成初始化__init__，创建Assistant类
    return Assistant(client,request_inputs.model,request_inputs.messages)

async def RequestAssistant(request_inputs:RequestInput,Action):
    # 调用↑函数
    assistant = CreateAssistant(request_inputs)
    # Action来自每个api接口定义的一个Action配方，在创建Assistant类后
    # 根据Action配方中的内容，从request_inputs中拿去对应的值实现函数方法
    # 作用是在写api接口时的配方只需要关心需要使用的方法和参数
    reply = await Action(assistant)
    # 加工输出结果
    return RemoveThink(request_inputs.model,reply)

# -------
# api接口
# -------

# 代码助手部分
@app.post("/generate")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.GenerateCode(
            request_inputs.language,
            request_inputs.requirement
        )
    return await RequestAssistant(request_inputs,Action)

@app.post("/explain")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.ExplainCode(
            request_inputs.language,
            request_inputs.code
        )
    return await RequestAssistant(request_inputs,Action)

@app.post("/error")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.ErrorCode(
            request_inputs.language,
            request_inputs.code,
            request_inputs.error
        )
    return await RequestAssistant(request_inputs,Action)

@app.post("/polish")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.PolishArticle(
            request_inputs.requirement
        )
    return await RequestAssistant(request_inputs,Action)

@app.post("/spell")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.CorrcetSpell(
            request_inputs.requirement
        )
    return await RequestAssistant(request_inputs,Action)

@app.post("/write")
async def OpenAi(request_inputs:RequestInput):
    async def Action(assistant:Assistant):
        return await assistant.WriteArticle(
            request_inputs.requirement
        )
    return await RequestAssistant(request_inputs,Action)


# tips:实际上   /ragchat实现的功能和/localopenai完全没有任何区别，我就是想单独开一个玩
@app.post("/ragchat")
async def OpenAi(request_inputs:RequestInput):
    if (request_inputs.model=="deepseek-chat"):
        return "呵呵,私有知识库不支持deepseek官网,因为测试费钱"
    client = GetApikey(request_inputs.model)
    reply = await SendtoAi(client,request_inputs.model,request_inputs.messages)
    reply = RemoveThink(request_inputs.model,reply)
    return reply