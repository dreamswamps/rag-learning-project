from openai import OpenAI
from langchain_openai import ChatOpenAI

# 发送给大模型并获得回复
async def SendtoAi(client,model,messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,  
    )
    reply = response.choices[0].message.content
    return reply
