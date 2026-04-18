import json
from pathlib import Path
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.deepseek import DeepSeek

# 1. 配置模型
Settings.embed_model = OllamaEmbedding(model_name="bge-m3:567m-fp16")
Settings.llm = DeepSeek(
    model="deepseek-chat",  # 或 deepseek-reasoner
    api_key="your_api_key",  # 替换为你的API Key
)

# 2. 加载文档（改进版）
def load_all_json_docs(folder_path):
    all_docs = []
    json_files = Path(folder_path).glob("*.json")
    
    for json_path in json_files:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        for sec in data:
            content = sec['content'].replace('\n', ' ')
            # 把标题放到内容最前面
            text = f"标题：{sec['title']}\n内容：{content}"
            text = f"文件：{json_path.name}\n{text}"
            
            doc = Document(
                text=text,
                metadata={"title": sec['title'], "file": json_path.name}
            )
            all_docs.append(doc)
    
    return all_docs

# 3. 分割文档
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
docs = load_all_json_docs("data_clean")
nodes = splitter.get_nodes_from_documents(docs)

# 4. 建立索引
index = VectorStoreIndex(nodes, embed_batch_size=1)
index.storage_context.persist(persist_dir="index/vector_store")


# 5. 查询测试
query_engine = index.as_query_engine()
response = query_engine.query("和爱莉希雅打招呼她会说什么?")
print(response)

# 1. 加载和切分文档
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
docs = load_all_json_docs("data_clean")
nodes = splitter.get_nodes_from_documents(docs)  # 用 nodes 而不是 docs
