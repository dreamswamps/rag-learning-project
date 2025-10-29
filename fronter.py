import streamlit as st
from Method_All.Fronter_Pattern.FreeDialogue import FreeDialogue_Load
from Method_All.Fronter_Pattern.CodeHelper import CodeHelper_Load
from Method_All.Fronter_Pattern.WirteHelper import WirteHelper_Load
from Method_All.Rag.RagChat import RagChat_Load

import os
import torch

# 这句代码并非必须，但添加上可以让streamlit和torch之间起码不会出warming
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

# -------------------------
# 启动streamlit
# streamlit run fronter.py 
# -------------------------

# 侧边栏
with st.sidebar:
    pattern = st.selectbox(
        "模式Pattern",
        ("自由对话","代码助手","写作助手","私有知识库")
    )
    # 选择箱
    option = st.selectbox(
        "模型Model",
        ("本地DeepSeek","DeepSeek官方")
    )
# 确定使用的模型
if option == "DeepSeek官方":
    st.session_state["openai_model"] = "deepseek-chat"
elif option == "本地DeepSeek":
    st.session_state["openai_model"] = "local_deepseek"

if pattern == "自由对话":
    st.title('大语言模型应用')
    st.caption(option+'自由对话💬')
    FreeDialogue_Load()
elif pattern == "代码助手":
    st.title("代码模块应用")
    st.caption(option+'代码助手💻')
    CodeHelper_Load()
elif pattern == "写作助手":
    st.title("写作模块应用")
    st.caption(option+"写作助手✍")
    WirteHelper_Load()
elif pattern == "私有知识库":
    st.title("私有知识库聊天")
    st.caption(option+"我词穷了😡")
    RagChat_Load()