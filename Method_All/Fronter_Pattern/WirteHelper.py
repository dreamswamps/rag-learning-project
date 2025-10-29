import streamlit as st
import json
import requests

def WirteHelper_Load():

    # 提示词
    prompt_word = '''
    你是最好的写作助手，你需要帮助用户，根据文章的内容使用中文或者英文。
    根据具体需求帮助用户润色改进文章内容、
    找到并修改文章中的出现的单词拼写和语法使用的错误、
    或者写一篇满足需求的文章。
    '''

    keys_to_init = ["polish_article","correct_spell","write_article"]
    for key in keys_to_init:
        if key not in st.session_state:
            st.session_state[key] = ""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"system","content":prompt_word}]

    tab_polish,tab_spell,tab_write = st.tabs(["润色改进文章","拼写语法纠错","自动生成文章"])

    with tab_polish:
        with st.form("润色改进文章"):
            requirement = st.text_area("文章内容",placeholder="输入需要润色的文章……",height=400)
            submit = st.form_submit_button("提交")
            if submit:
                with st.spinner("正在润色文章……"):
                    request_inputs = {
                        "requirement":requirement,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/polish",
                                             data=json.dumps(request_inputs))
                    st.session_state["polish_article"] = response.json()
                    st.markdown(st.session_state["polish_article"])

    with tab_spell:
        with st.form("拼写语法修正"):
            requirement = st.text_area("英语文章",placeholder="输入需要修正的英语文章……",height=400)
            submit = st.form_submit_button("提交")
            if submit:
                with st.spinner("正在尝试寻找错误……"):
                    request_inputs = {
                        "requirement":requirement,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/spell",
                                             data=json.dumps(request_inputs))
                    st.session_state["correct_spell"] = response.json()
                    st.markdown(st.session_state["correct_spell"])

    with tab_write:
        with st.form("自动生成文章"):
            requirement = st.text_area("想法",placeholder="想要写一篇什么样的文章？",height=400)
            submit = st.form_submit_button("提交")
            if submit:
                with st.spinner("正在绞尽脑汁……"):
                    request_inputs = {
                        "requirement":requirement,
                        "model":st.session_state["openai_model"],
                        "messages":st.session_state.messages
                    }
                    response = requests.post("http://127.0.0.1:8000/write",
                                             data=json.dumps(request_inputs))
                    st.session_state["generate_article"] = response.json()
                    st.markdown(st.session_state["generate_article"])