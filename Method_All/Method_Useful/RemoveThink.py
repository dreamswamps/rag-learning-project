import re

def RemoveThink(model,text_remove:str):
    # 寻找到最后一次出现的</think>\n\n并截取后才停止
    # 事实上，本地deepseek是没法办法输入</think>的，因为会强制停止思考。
    # 只有部署在本地的deepseek才需要删除思考过程
    # 官方deepseek输入</think>貌似会有有意思的事情发生？
    if (model == "local_deepseek"):
        text_remove = text_remove.rsplit("</think>\n\n",1)[-1]
        # text_remove = re.sub(r'<think\b[^>]*>.*?</think>', '', text_remove, flags=re.IGNORECASE)
    return text_remove

def InputRemoveThink(model,processed:str):
    if(model=="local_deepseek"):
        processed = processed.replace("<think>", "").replace("</think>", "")
    return processed
