from openai import OpenAI
import mysql.connector
from mysql.connector import Error
import os

'''
功能：
通过接收到的模型，从数据库调用匹配该模型的数据给client赋值
client用于传递给SendtoAi用于访问大语言模型
'''


# 读取环境文件  不加读不到.env文件
from dotenv import load_dotenv
load_dotenv()

def GetApikey(model):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        # if connection.is_connected():
        #     print("成功连接到MySQL数据库")

        # 之前会根据输入model的不同执行不同的代码，目前已经将其删除
        # 输入的model将直接作为SQL查询语句的条件
        # 省去if语句
        # 要求这里使用的model和mysql中的属性值一样，并且该值是能够被例如deepseek官方api接受的

        cursor = connection.cursor()
        query_1 = "SELECT APIKey_code FROM testssm.apikey WHERE APIKey_id = %s"
        query_2 = "SELECT URL FROM testssm.apikey WHERE APIKey_id = %s"
        cursor.execute(query_1, (model,))
        api_key=cursor.fetchone()[0]
        cursor.execute(query_2,(model,))
        base_url=cursor.fetchone()[0]
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
    except Error as e:
        print(f"连接错误: {e}")
    finally:
        # 确保连接被关闭
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            # print("MySQL连接已关闭")

    return client

# ----测试语句----
# print(GetApikey("deepseek-chat").api_key)
# print(GetApikey("local_deepseek").api_key)
# ---------------