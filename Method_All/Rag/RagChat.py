import streamlit as st
import tempfile
import os
import json
from .RagMethod import *
import chromadb

'''
功能：
私有知识库的前端代码
由于实现的功能较多，代码量较大，所以单开一块
未来可能优化合并到Fronter_Pattern中
'''

'''
# 原版------------------------------------------------------------------------------
# Warming   该段代码仍然可能存在问题    使用时请花费时间测试修改
chunks_global = []

def ReadyToGetFile():
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name
        with st.session_state["ingestion_spinner"],st.spinner(f"Ingesting{file.name}"):
            global chunks_global 
            chunks_global.append(st.session_state["assistant"].GetAndSplitPDF(file_path))
        os.remove(file_path)
        # print(chunks_global[0])

def RagChat_Load():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state["ingestion_spinner"] = st.empty()

    files = st.file_uploader(
            "上传PDF文件",
            type=["pdf"],
            key="file_uploader",
            on_change=ReadyToGetFile,
            label_visibility="collapsed",
            accept_multiple_files=True
            )
    st.session_state["assistant"] = Ragchat()

    if files:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("输入内容")
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("思考中"):
                    reply = st.session_state["assistant"].IngestPDFToAI(chunks_global,prompt)
                    st.markdown(reply)
                    
#   ----------------------------------------------------------------------------------
'''

#   处理链+lambda表达式
#   ↑优化版本
#   现在已支持三种文件的读取
#   doc出现的问题较多，且由于是老板word文件，所以就直接删掉这个功能。

def ReadyToGetFile():
    st.session_state["assistant"] = Ragchat()
    # 每次对一个文件进行split(即使是已经被split过的也会被重新执行split)
    # 未来可能加入新的标识符用来判断一个文件是否被split过(与之配套还需要记录是否被删除，删除则需要在数组中删除该文件内容)
    for file in st.session_state["file_uploader"]:
        # 保存文件后缀的file_ext
        # os.path.splitext作用：获取文件路径最后一个点到末尾的内容，并且进行分割。
        # 假设文件为Test.txt。那么[1]值为txt，[0]值为Test。忽略"."
        file_ext = os.path.splitext(file.name)[1]   
        # 创建临时文件  delete表示是否自动删除  设为flase后需要手动释放资源
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            # 一次性写入二进制数据
            tf.write(file.getbuffer())
            # 这里的flie_path是一个临时路径，不包含任何文件名称有关信息！所以不要想着靠对file_path进行加工获得有用的信息
            file_path = tf.name
        # 临时会话
        with st.session_state["ingestion_spinner"],st.spinner(f"Ingesting{file.name}"):
            st.session_state["chunks"] = st.session_state["assistant"].GetAndSplitPDF(file_path,file_ext.lower())
            # 清楚缓存  可以规避部分报错
            chromadb.api.client.SharedSystemClient.clear_system_cache()

        # 释放临时文件  因为临时文件tf的内容已经写入file_path中，所以只需要释放file_path就可以了
        os.remove(file_path)

def RagChat_Load():
    if "messages" not in st.session_state:
        st.session_state.messages = [] 

    if "chunks" not in st.session_state:
      st.session_state["chunks"] = [] 

    files = st.file_uploader(
            "请上传文件",
            type=["pdf","docx","txt"],
            key="file_uploader",
            on_change=ReadyToGetFile,
            label_visibility="collapsed",
            accept_multiple_files=True
            )
    st.session_state["ingestion_spinner"] = st.empty()
    
    if files:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                

        prompt = st.chat_input("输入内容")
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("思考中"):
                    reply = st.session_state["assistant"].IngestQuery(st.session_state["chunks"],prompt,st.session_state["openai_model"])
                    st.markdown(reply)
