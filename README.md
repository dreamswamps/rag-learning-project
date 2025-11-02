# Large Language Model Interactive Website

> A large language model interactive website based on LangChain, providing features such as free dialogue, code assistant, writing assistant, and private knowledge base. Supports locally deployed model and API interface calls.

## Language

- [English](README.md)
- [Chinese](README-ZH.md)

## ✨ Feature Description

1. **Free Dialogue:** Having natural language interaction with large language model
2. **Code Assistant:**
    - Generate the Python, Java, and C++ code based on user requirements 
    - Explain the logic based on provided code
    - Fix the code issues based on error messages
3. **Writing Assistant:**
    - Polish article content
    - Correct spelling and grammar errors in English articles
    - Generate articles based on user requirements
4. **Private Knowledge Base:** Users can upload PDF, DOCX, TXT and other files to improve the Q&A quality based on file content

## ✅ Supported Models
- Locally deployed DeepSeek model
- DeepSeek official API

## 🚀 Quick Start

### Environment Requirements

- Python 3.8+
- Dependent libraries (see details in requirements.txt)
- MySQL database

### Installation and Running

1. Clone the project:
    ```bash
    git clone https://github.com/dreamswamps/rag-learning-project.git
    cd rag-learning-project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure environment variables:<a id="env"></a>
    - Create a file named `.env` in the project root directory
    - Edit the `.env` file, fill in and modify the following content:
    ```
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=your_database
    ```

4. Configure database:
    - Create data table:
    ```sql
    CREATE TABLE `apikey` (
        `APIKey_id` varchar(24) PRIMARY KEY,
        `APIKey_code` varchar(48) UNIQUE NOT NULL,
        `URL` varchar(48) NOT NULL,
        `Personal` tinyint DEFAULT 0
    );
    ```
    - Insert two records containing keys and addresses into the database:
    ```sql
    INSERT INTO `apikey` VALUES 
    ('deepseek-chat', 'your-api-key-here', 'https://api.deepseek.com', 1),
    ('local_deepseek', 'local-key', 'your-local-LLM-URL', 0);
    ```

## 📖 Usage Instructions <a id="configuration"></a>

1. **Open Terminals**: Please open terminals in both the root directory and the Method_All folder respectively

2. **Start backend service**:
    In the terminal under the Method_All directory, enter the following command
    ```bash
    uvicorn fastapi_back:app --reload
    ```

3. **Start frontend interface**:
    In the terminal under the root directory, enter the following command
    ```bash
    streamlit run fronter.py
    ```

4. **Access the page**:
    Check the address displayed in the terminal and access it

5. **Feature Switching**:
    Select the model and feature in the sidebar

## 📁 Project Structure

```
rag-learning-project/
├── 📁 Method_All
|   ├── 📁 Fronter_Pattern
|   |   ├── CodeHelper.py       # Code assistant feature
|   |   ├── FreeDialogue.py     # Free dialogue feature
|   |   └── WriteHelper.py      # Writing assistant feature
|   ├── 📁 Method_Useful
|   |   ├── GetApikey.py        # Get API key
|   |   ├── RemoveThink.py      # Remove thinking results
|   |   └── SendtoAi.py         # Send AI requests
|   ├── 📁 Rag
|   |   ├── RagChat.py          # Rag interaction page
|   |   └── RagMethod.py        # Rag core algorithm
|   ├── fastapi_back.py    # FastAPI Web service
|   └── method.py          # Encapsulate business requests
├── ⚙️ .env            # Environment configuration (needs to be create manually)
├── .gitignore 
└── 🚀 fronter.py      # Application main entry
```

## ⚠️ Notes

- Ensure the MySQL service is running
- The local model needs to be deployed in advance and ensure the URL in the database table is accessible
- The first run may be slower

## 🔧 Troubleshooting

**Q: Errors occur when starting the frontend and backend services?**

**A:** Please troubleshoot according to the following steps:
1. Please check the [Usage Instructions](#configuration) to ensure you entered the correct commands in the different terminals.
2. Please ensure all dependencies are installed:`pip install -r requirements.txt`.

**Q: Database connection failed?**

**A:** Please troubleshoot according to the following steps:
1. Please check the [Environment Configuration](#env) to ensure the database configuration is correct.
2. Check if the MySQL service is running.
3. Ensure the database table has been created.

## ❓ Frequently Asked Questions

**Q: Why does a folder named `__pycache__` appear in the files?**

**A:** This is the bytecode cache generated the first time Python compiles the modules,which can increase speed for subsequent startups.

**Q: After cloning the project and running, the terminal displays warnings/errors. How to solve this?**

**A:** This issue may be caused by the deprecation of old interfaces due to the version update of LangChain. The version update of LangChain may be accompanied by deprecating interfaces. In such situations, please check the corresponding version in `requirements.txt`. Or check the warning information, which may indicate information about which deprecated interface should be replaced by what.