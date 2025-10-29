import streamlit as st
import json
import requests
from ..Method_Useful.RemoveThink import InputRemoveThink

def FreeDialogue_Load():
    # session_state 会话状态
    # 初始化会话状态    将会保存初始的提示词
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 输入框    (占位符)
    prompt = st.chat_input("输入内容")
    if prompt:
        prompt = InputRemoveThink(st.session_state["openai_model"],prompt)
        # 在临时会话中加入新的消息
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        '''
        这两段代码其实毫无差别
        只是早期代码留下的格式，后面经过优化后同样的localopenai接口已经可以同时实现两个功能了
        可以直接删除if判断使用相同的部分。
        '''

        # 链接本地deepseek
        if st.session_state["openai_model"] in ["local_deepseek"]:
            # 临时显示
            with st.spinner("正在思考……"):
                request_inputs = {
                    "model": st.session_state["openai_model"],
                    "messages": st.session_state.messages
                }
                response = requests.post("http://127.0.0.1:8000/localopenai",
                                        data= json.dumps(request_inputs))
            st.session_state.messages.append({"role":"assistant","content":response.json()})
            with st.chat_message("assistant"):
                st.markdown(response.json())

        # 链接deepseek官网
        if st.session_state["openai_model"] in ["deepseek-chat"]:
            # 临时显示
            with st.spinner("正在思考……"):
                request_inputs = {
                    "model": st.session_state["openai_model"],
                    "messages": st.session_state.messages
                }
                response = requests.post("http://127.0.0.1:8000/localopenai",
                                        data= json.dumps(request_inputs))
            st.session_state.messages.append({"role":"assistant","content":response.json()})
            with st.chat_message("assistant"):
                st.markdown(response.json())