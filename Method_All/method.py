from Method_Useful.SendtoAi import SendtoAi
# 这一块的本质就是提供输入内容的模板

'''
用于实现方法的部分
拥有两个版本
第一个版本对应的fastapi_back.py代码已经被删除
'''

'''
# 测试封装----------------------------------------------

# 选择python/c++/java语言，根据需求，生成代码。
# 按照一定格式修改messages
def GenerateCode(client,model,language,requirement,messages):
    generate_prompt = f"使用{language}语言完成以下需求：{requirement}"
    messages.append({"role":"user","content":generate_prompt})
    reply = SendtoAi(client,model,messages)
    return reply

# 根据提供的代码进行注释。
def ExplainCode(client,model,language,code,messages):
    explain_prompt = f"请阅读这段{language}代码，进行详细的逻辑注释并说明实现了什么功能，代码如下{code}"
    messages.append({"role":"user","content":explain_prompt})
    reply = SendtoAi(client,model,messages)
    return reply

# 根据代码的报错给出建议。
def ErrorCode(client,model,language,code,error,messages):
    error_prompt = f"请对这段出现问题的{language}代码进行修复，代码如下：{code}，报错如下:{error}"
    messages.append({"role":"user","content":error_prompt})
    reply = SendtoAi(client,model,messages)
    return reply

# 根据提供的文章内容进行润色。
def PolishArticle(client,model,requirement,messages):
    polish_prompt = f"请对这篇文章进行润色修改，在不改变原本语义的前提下，让文章文笔更加优美，文章内容如下：{requirement}"
    messages.append({"role":"user","content":polish_prompt})
    reply = SendtoAi(client,model,messages)
    return reply

# 根据提供的文章内容进行单词和语法的改正。
def CorrcetSpell(client,model,requirement,messages):
    spell_prompt = f"这篇英语文章可能存在语法或者单词拼写的错误，请寻找出可能出现的错误，指出出现错误的位置并对错误进行改正，文章内容如下：{requirement}"
    messages.append({"role":"user","content":spell_prompt})
    reply = SendtoAi(client,model,messages)
    return reply

# 根据用户的需求生成文章。
def WriteArticle(client,model,requirement,messages):
    polish_prompt = f"请根据需求写一篇文笔优美的文章，无字数要求时字数不超过1000字，需求如下：{requirement}"
    messages.append({"role":"user","content":polish_prompt})
    reply = SendtoAi(client,model,messages)
    return reply
    
'''

# -------------------------------------------------
# 封装

class BaseMethod:

    def __init__(self,client,model,messages):
        self.client = client
        self.model = model
        self.messages = messages

    def SendRequest(self,prompt):
        self.messages.append({"role":"user","content":prompt})
        return SendtoAi(self.client,self.model,self.messages)
    
    def ClearMessages(self):
        self.messages.clear()

class Assistant(BaseMethod):
    def NormalChat(self):
        return SendtoAi(self)

    def GenerateCode(self,language,requirement):
        prompt = f"使用{language}语言完成以下需求：{requirement}"
        return self.SendRequest(prompt)
    
    def ExplainCode(self,language,code):
        prompt = f"请阅读这段{language}代码，进行详细的逻辑注释并说明实现了什么功能，代码如下{code}"
        return self.SendRequest(prompt)
    
    def ErrorCode(self,language,code,error):
        prompt = f"请对这段出现问题的{language}代码进行修复，代码如下：{code}，报错如下:{error}"
        return self.SendRequest(prompt) 

    def PolishArticle(self,requirement):
        prompt = f"请对这篇文章进行润色修改，在不改变原本语义的前提下，让文章文笔更加优美，文章内容如下：{requirement}"
        return self.SendRequest(prompt)
    
    def CorrcetSpell(self,requirement):
        prompt = f"这篇文章可能存在语法或者单词拼写的错误，请寻找出可能出现的错误，指出出现错误的位置并对错误进行改正，文章内容如下：{requirement}"
        return self.SendRequest(prompt)
    
    def WriteArticle(self,requirement):
        prompt = f"请根据需求写一篇文笔优美的文章，无字数要求时字数不超过1000字，需求如下：{requirement}"
        return self.SendRequest(prompt)
    