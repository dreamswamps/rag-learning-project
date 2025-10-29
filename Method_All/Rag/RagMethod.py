# 功能：实现与私有知识库的交互
# 关键词：为了方便理解和记忆，将词中关键的部分提取出来，下一次看到这一部分能有大致的印象

# 允许和openai模型对话
# 关键词openai,chat
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
# 用于读取文档/获取私有知识库   import部分,分别是处理PDF和处理text文本
# 关键词document(文档),PDF,Text
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
# 实现文本分割  对文本的分析，本质上是把文本按照一定的大小，分割成多个段落
# 后续的文本查找，查找的对象是分割后的段落  段落也是为了方便向量化
# 关键词split(分割),character(段落)
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 文本过滤工具  通过简化文本的复杂数据，只保留关键信息，目的是方便向量化和训练
# 关键词vector(向量),complex(复杂)
from langchain_community.vectorstores.utils import filter_complex_metadata
# Chroma向量存储库  将文本数据向量化并存储  
# Chroma可以完成embedding生成的任务
# 关键词Chroma
from langchain_community.vectorstores import Chroma
# 提示模板库    目的是生成适合特定任务的提示词
# 关键词prompt(提示)
from langchain_core.prompts import ChatPromptTemplate
# 可以运行的逻辑组件，将模型和其他流程集成在一起。实现1+1
# 关键词runnable(可运行)
from langchain.schema.runnable import RunnablePassthrough
# 处理解析器，把返回的结果变成字符串
# 关键词output(输出),parser(解析器),Str
from langchain.schema.output_parser import StrOutputParser
# Lambda表达式  一次性函数(不用想名字的函数)
from langchain.schema.runnable import RunnableLambda

# embedding支持的一种默认的免费的embedding模型，在这段代码里其功能已经被huggingface所选用的模型代替
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()
import requests
import json
import os

# 设置国内镜像网站  不用魔法也可以下载模型
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from langchain_huggingface import HuggingFaceEmbeddings

# 复用且固定的提示词模板
SYSTEM_PROMPT = '''你是协助用户完成问答工作的助手。\n使用以下检索到的上下文来回答问题。\n检索内容不一定完全正确。\n如果你不知道答案，那就回答你不知道。\n内容如下:\n'''

'''
与RagChat.py配套的后端代码
原版为不适用处理链仅实现函数一步步调用完成
前端代码关于原版的配套代码已经被删除

Ragchat类方法包括：
1.初始化
2.填充提示词
3.文章片段整合
4.获取文件并切割(由前端调用,因为后端不保留文件地址)
5.MMR最大边界相关算法
6.fastapi接口访问
7.处理链
'''


'''
# 原版----------------------------------------------------------------------
class Ragchat:
    # 初始化需要使用的方法及参数
    def __init__(self,embedding_fn = default_ef):
        self.model = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key = "sk-11",
            openai_api_base= "http://127.0.0.1:1234/v1"
        )
        # 文本分割块的参数初始化
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 256,
            chunk_overlap = 64
        )
        # 创建Embedding事件
        self.embedding_fn = embedding_fn
        
        self.embedding_hf = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
            model_kwargs = {"device":"cuda"},
            encode_kwargs = {
                "normalize_embeddings":True
            })

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",SYSTEM_PROMPT),
                ("user","{question}"),
            ]
        )

    # 拼接出提示词和用户问题
    def PromptJoin(self,text,question):
        return [
                {"role":"system","content":f"{SYSTEM_PROMPT}{text}"},
                {"role":"user","content":f"{question}"},
                ]

    # 这是一个用于拼接块/段落的函数
    # 作用是在每个块之间加上"\n\n"并把块拼接在一起最后返回一个LiteralString文本字符串
    # 格式化
    def FormatDocs(self,docs):
        reply = ""
        for i in range(0,len(docs)):
            reply += "\n\n".join(doc.page_content for doc in docs[i])
        return reply
 
    def GetAndSplitPDF(self,file_path:str):
        docs = PyPDFLoader(file_path=file_path).load()
        # 根据参数，分割文档docs，分割后的结果保存在chunks（块）中
        chunks = self.text_splitter.split_documents(docs)
        # 将chunks中无用的信息过滤，结果更新chunks
        chunks = filter_complex_metadata(chunks)
        docs.clear()
        return chunks

    def MMRSearch(self,chunks,query):
        answer = list()
        for i in range(0,len(chunks)):
            db = Chroma.from_documents(documents=chunks[i],embedding=self.embedding_hf)
            buffer = db.max_marginal_relevance_search(query,
                                                    k=3,
                                                    fetch_k=9)
            answer.append(buffer)
            db.delete_collection
        chunks.clear()
        # print("-------------------",answer)
        return answer

    def IngestPDFToAI(self,chunks,question):
        # chunks = self.GetAndSplitPDF(file_path)
        search_answer = self.MMRSearch(chunks,question)
        prompt_messages = self.PromptJoin(self.FormatDocs(search_answer),question)
        client = OpenAI(
        api_key="sk-1",
        base_url="http://127.0.0.1:1234/v1"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=prompt_messages,
        )
        chunks = None
        search_answer.clear()
        prompt_messages.clear()
        reply = response.choices[0].message.content
        return reply

#   ------------------------------------------------------------------------------ 
'''

#   处理链+lambda表达式

class Ragchat:
    def __init__(self,embedding_fn = default_ef):
        # 本地模型client  该属性已废弃
        self.model = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key = "sk-11",
            openai_api_base= "http://127.0.0.1:1234/v1"
        )
        
        # 文件裁剪格式
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 256,
            chunk_overlap = 64
        )

        # 自带默认embedding 该属性已废弃
        self.embedding_fn = embedding_fn

        # huggingface模型下载并调用(下载至缓存  未来可能会进行优化  当前准确率仅50%+)
        self.embedding_hf = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            # 允许GPU
            model_kwargs = {"device":"cuda"},
            encode_kwargs = {
                # 规范化嵌入    功能存疑    用于同意向量长度/模    在进行向量相似度比较时有优势
                "normalize_embeddings":True
            })
        
        # 创建处理链
        self.chain = self.CreateChain()

    def PromptJoin(self,text,question):
        return [
                {"role":"system","content":f"{SYSTEM_PROMPT}{text}"},
                {"role":"user","content":f"{question}"},
                ]

    def FormatDocs(self,docs,question):
        reply = ""
        for i in range(0,len(docs)):
            reply += "\n\n".join(doc.page_content for doc in docs[i])
        return {
            "formatted_docs":reply,
            "question":question
        }

    def GetAndSplitPDF(self,file_path:str,file_type:str):
        # print(file_type)
        # docs = PyPDFLoader(file_path=file_path).load()
        if file_type == ".pdf":
            loader = PyPDFLoader(file_path).load()          
        elif file_type == ".docx":
            loader = Docx2txtLoader(file_path).load()
        elif file_type == ".txt":
            loader = TextLoader(file_path=file_path,encoding="utf-8").load()
        else:
            return "\n不支持该文件类型\n"
        chunks = self.text_splitter.split_documents(loader)
        chunks = filter_complex_metadata(chunks)
        chunks_global = []
        chunks_global.append(chunks)
        # print("\n\n\n\n------------------------------\n",chunks_global)
        return chunks_global

    def MMRSearch(self,chunks,query):
        # print(chunks)
        answer = list()
        for i in range(0,len(chunks)):
            db = Chroma.from_documents(documents=chunks[i],embedding=self.embedding_hf)
            buffer = db.max_marginal_relevance_search(query,
                                                    k=3,
                                                    fetch_k=9)
            answer.append(buffer)
            db.delete_collection
        return {
            "docs":answer,
            "question":query
        }
    
    def CallOpenAI(self,prompt_messages,model):
        # 为了让model能被正确的传递到这里，大面积修改之前的逻辑，可能有更好的优化方向
        request_inputs = {
            "model": model["model"],
            "messages": prompt_messages
        }
        response = requests.post("http://127.0.0.1:8000/ragchat",
                                 data=json.dumps(request_inputs))
        return response.json()

    # 处理链生成方法
    def CreateChain(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # 非常非常非常非常重要重要重要重要
        # 这个参数传进来的，就是原始的值，传进的参数保存在哪，使用的参数就在哪
        # 直白点    在函数里把传参改了，那就是真的改了😡有病吧连吃带拿
        chain_input = {
            "chunks":RunnablePassthrough(),
            "question":RunnablePassthrough(),
            "model":RunnablePassthrough()
        }
        
        # lambda表达式 :前的x表示参数   :后的语句表示return内容

        # mmr算法获得最相近的内容
        mmr_search = RunnableLambda(lambda x:self.MMRSearch(x["chunks"],x["question"]))

        # 将相近内容组合在一起方便提供给模型
        format_docs = RunnableLambda(lambda x:self.FormatDocs(x["docs"],x["question"]))

        # 将组合好的话和最开始传入的question拼接为提示词
        # 链式处理流程会保存传入的参数，因此在这里虽然上一个流程结束后没有传出question
        # 仍然可以通过RunnablePassthrough()获得一开始传入的问题
        join_prompt = RunnableLambda(lambda x:self.PromptJoin(x["formatted_docs"],x["question"]))

        # 将提示词发送给AI等待回复
        call_openai = RunnableLambda(lambda x:self.CallOpenAI(x["joined_docs"],x["model"]))

        # 链式处理流程  流程获得的参数为上一个流程传出的参数

        return (
            chain_input
            | {
                "joined_docs": mmr_search | format_docs | join_prompt,
                "model":RunnablePassthrough()
            }
            | call_openai
        ) 
    
    # 启动方式  IngestQuery翻译：采样查询
    def IngestQuery(self,chunks,question,model):
        # print("=============================",chunks)
        # 这段代码大概率是不会触发的
        if not chunks:
            return "请上传至少一个文件或等待文件读取完毕！"
        elif not question:
            return "请输入有效内容！"
        # 处理链的生成和运行是分离开来的，即使生成好了处理链没有使用invoke()进行传参
        # 那么处理链也不会启动，代码也不会生效
        return self.chain.invoke({
            "chunks":chunks,
            "question":question,
            "model":model,
        })
    

# file_path = "C:/Users/17937/Desktop/第十六届服创大赛《参赛手册》、《赛题手册》等系列材料/03-第十六届中国大学生服务外包创新创业大赛参赛承诺书.pdf"
# Test = Ragchat()
# chunks = []
# chunks.append(Test.GetAndSplitPDF(file_path))
# question = "文章的作者是谁？"
# print(Test.IngestQuery(chunks,question,"local_deepseek"))