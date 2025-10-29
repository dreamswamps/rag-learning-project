import streamlit as st
import json
import requests

def CodeHelper_Load():

    # 提示词
    prompt_word = '''
    你是最好的代码助手，你需要帮助用户，使用用户指定的语言类型。
    根据需求生成代码、解释代码的功能和逻辑，或是根据软件报错内容进行代码的修正。
    '''

    with st.sidebar:
        language = st.selectbox(
            "代码语言",
            ("python","java","c++")
        )

    # 三种方法存储变量初始化
    keys_to_init = ["generate_code","explain_code","error_code"]
    for key in keys_to_init:
        if key not in st.session_state:
            st.session_state[key] = ""

    # 初始化提示词
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"system","content":prompt_word}]
    
    # tab   主界面的选项，思路和侧边栏相似
    tab_generate,tab_explain,tab_error = st.tabs(["代码生成","代码解释","代码纠错"])

    with tab_generate:
        with st.form("代码生成"):
            # text_area 和 输入框类似但是从一行变成多行
            requirement = st.text_area("代码需求",placeholder="想要实现……",height=200)
            submit = st.form_submit_button("提交")
            # 点击生效
            if submit:
                # 临时会话
                with st.spinner("正在生成代码……"):
                    request_inputs = {
                        "language":language,
                        "requirement":requirement,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/generate",
                                             data=json.dumps(request_inputs))
                    st.session_state["generate_code"] = response.json()
                    st.markdown(st.session_state["generate_code"])

    with tab_explain:
        with st.form("代码解释"):
            code = st.text_area("代码内容",placeholder="输入需要解释的代码……",height=400)
            submit = st.form_submit_button("提交")
            if submit:
                with st.spinner("正在进行解释……"):
                    request_inputs = {
                        "language":language,
                        "code":code,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/explain",
                                             data=json.dumps(request_inputs))
                    st.session_state["explain_code"] = response.json()
                    st.markdown(st.session_state["explain_code"])

    with tab_error:
        with st.form("代码纠错"):
            code = st.text_area("代码内容",placeholder="输入需要解释的代码……",height=400)
            error = st.text_area("报错内容",placeholder="输入软件报错内容")
            submit = st.form_submit_button("提交")
            if submit:
                with st.spinner("正在尝试改正……"):
                    request_inputs = {
                        "language":language,
                        "code":code,
                        "error":error,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/error",
                                             data=json.dumps(request_inputs))
                    st.session_state["error_code"] = response.json()
                    st.markdown(st.session_state["error_code"])            