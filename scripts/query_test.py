from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.deepseek import DeepSeek

# ⚠️ 加载前也必须设置完全相同的配置
Settings.embed_model = OllamaEmbedding(model_name="bge-m3:567m-fp16")
Settings.llm = DeepSeek(
    model="deepseek-chat",
    api_key="your_api_key"
)

# 加载索引
storage_context = StorageContext.from_defaults(persist_dir="index/vector_store")
index = load_index_from_storage(storage_context)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("和爱莉希雅打招呼她会说什么?")
print(response)