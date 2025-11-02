# 大语言模型交互网站

> 一个基于LangChain的大语言模型交互网站，提供了自由对话、代码助手、写作助手和私有知识库等功能。允许本地模型和API接口调用。

## 语言

- [英文](README.md)
- [中文](README-ZH.md)

## ✨ 功能描述

1. **自由对话：** 与大语言模型进行自然语言交互
2. **代码助手：**
    - 根据用户需求生成Python、Java和C++代码
    - 根据提供代码进行逻辑解释
    - 根据错误信息修复代码问题
3. **写作助手：**
    - 润色文章内容
    - 纠正英语文章中的拼写和语法错误
    - 根据用户需求生成文章
4. **私有知识库：** 用户上传PDF、DOCX、TXT等文件，根据文件内容提升问答质量

## ✅ 支持模型
- 本地部署的DeepSeek模型
- DeepSeek官方API

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 依赖库（详见requirements.txt）
- MySQL数据库

### 安装与运行

1. 克隆项目：
    ```bash
    git clone https://github.com/dreamswamps/rag-learning-project.git
    cd rag-learning-project
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置环境变量：<a id="env"></a>
    - 在项目根目录下创建名为`.env`的文件
    - 编辑`.env`文件，填入并修改以下内容：
    ```
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=your_database
    ```

4. 配置数据库：
    - 创建数据表：
    ```sql
    CREATE TABLE `apikey` (
        `APIKey_id` varchar(24) PRIMARY KEY,
        `APIKey_code` varchar(48) UNIQUE NOT NULL,
        `URL` varchar(48) NOT NULL,
        `Personal` tinyint DEFAULT 0
    );
    ```
    - 往数据库中插入包含密钥和地址的两条记录：
    ```sql
    INSERT INTO `apikey` VALUES 
    ('deepseek-chat', 'your-api-key-here', 'https://api.deepseek.com', 1),
    ('local_deepseek', 'local-key', 'your-local-LLM-URL', 0);
    ```

## 📖 使用说明 <a id="configuration"></a>

1. **开启终端**：请分别在根目录和Method_All两个文件夹下打开终端

2. **启动后端服务**：
    在Method_All目录下的终端输入以下内容
    ```bash
    uvicorn fastapi_back:app --reload
    ```

3. **启动前端界面**：
    在根目录下的终端输入以下内容
    ```bash
    streamlit run fronter.py
    ```

4. **访问页面**：
    查看终端显示的地址并访问

5. **功能切换**：
    在侧边栏选择模型和功能

## 📁 项目结构

```
rag-learning-project/
├── 📁 Method_All
|   ├── 📁 Fronter_Pattern
|   |   ├── CodeHelper.py       # 代码助手功能
|   |   ├── FreeDialogue.py     # 自由对话功能
|   |   └── WriteHelper.py      # 写作助手功能
|   ├── 📁 Method_Useful
|   |   ├── GetApikey.py        # 获取API密钥
|   |   ├── RemoveThink.py      # 移除思考结果
|   |   └── SendtoAi.py         # AI请求发送
|   ├── 📁 Rag
|   |   ├── RagChat.py          # Rag交互页面
|   |   └── RagMethod.py        # Rag核心算法
|   ├── fastapi_back.py    # FastAPI Web服务
|   └── method.py          # 封装业务请求
├── ⚙️ .env            # 环境配置（需手动创建）
├── .gitignore 
└── 🚀 fronter.py      # 应用主入口
```

## ⚠️ 注意事项

- 确保MySQL服务已启动
- 本地模型需要提前部署并保证数据表中的URL可访问
- 首次运行可能较慢

## 🔧 故障排除

**Q: 启动前后端服务时出现报错？**

**A:** 请按照以下步骤进行排查： 
1. 请查看[使用说明](#configuration)，确保你在两个不同的终端输入了正确的命令。
2. 请确保已安装所有依赖：`pip install -r requirements.txt`。

**Q: 数据库连接失败？**

**A:** 请按照以下步骤进行排查：
1. 请查看[环境配置](#env)，确保数据库配置正确。
2. 检查MySQL服务是否启动。
3. 确保数据表已经被创建。

## ❓ 常见问题

**Q: 为什么文件中会出现名为`__pycache__`的文件夹？**

**A:** 这是Python第一次对模块编译的字节码缓存，可以加快后续的启动速度。

**Q: 克隆项目并运行后，终端显示警告/报错，该如何解决？**

**A:** 这个问题可能是因为LangChain的版本更新导致的旧接口被弃用情况。LangChain的版本更新可能伴随着接口的弃用，在该情况下，请查看`requirements.txt`中的对应版本。或者查看警告信息，可能找到指示弃用接口被替换为哪个的信息。