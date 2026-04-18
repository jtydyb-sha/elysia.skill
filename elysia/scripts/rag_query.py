#!/usr/bin/env python3
"""
RAG 查询脚本
用法: python rag_query.py "你的问题"
"""

import sys
import json
from pathlib import Path
from typing import List, Optional

from llama_index.core import (
    StorageContext, 
    load_index_from_storage, 
    Settings,
    QueryBundle
)
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.deepseek import DeepSeek


class RAGQueryEngine:
    """RAG 查询引擎，封装索引加载和查询逻辑"""
    def __init__(
        self, 
        persist_dir: str = "index/vector_store",
        embed_model: str = "bge-m3:567m-fp16",
        llm_model: str = "deepseek-chat",
        api_key: Optional[str] = None,
        config_path: str = "scripts/config.json"  # 新增配置文件路径
    ):
        """
        初始化 RAG 查询引擎
        
        Args:
            persist_dir: 索引持久化目录
            embed_model: Ollama embedding 模型名称
            llm_model: DeepSeek 模型名称
            api_key: DeepSeek API Key（优先级最高）
            config_path: 配置文件路径（优先级次之）
        """
        self.persist_dir = persist_dir
        
        # 获取 API Key 的优先级：
        # 1. 直接传入的 api_key
        # 2. 配置文件中的 api_key
        # 3. 环境变量中的 DEEPSEEK_API_KEY
        if api_key is None:
            api_key = self._load_config(config_path).get("api_key")
        
        # 从配置文件读取其他参数（如果存在）
        config = self._load_config(config_path)
        embed_model = config.get("embed_model", embed_model)
        llm_model = config.get("llm_model", llm_model)
        persist_dir = config.get("persist_dir", persist_dir)
        
        # 配置全局设置
        Settings.embed_model = OllamaEmbedding(model_name=embed_model)
        Settings.llm = DeepSeek(
            model=llm_model,
            api_key=api_key
        )
        
        # 加载索引
        self.index = self._load_index()
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=3,  # 默认检索 3 个片段
            response_mode="compact"  # 紧凑模式，合并相关片段
        )

    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 读取配置文件失败 {config_path}: {e}")
        return {}
    
    
    def _load_index(self):
        """加载向量索引"""
        if not Path(self.persist_dir).exists():
            raise FileNotFoundError(
                f"索引目录不存在: {self.persist_dir}\n"
                "请先运行构建索引的脚本"
            )
        
        storage_context = StorageContext.from_defaults(
            persist_dir=self.persist_dir
        )
        return load_index_from_storage(storage_context)
    
    def query(self, question: str, top_k: int = 3) -> dict:
        """
        执行查询并返回结果
        
        Args:
            question: 用户问题
            top_k: 检索的文档片段数量
            
        Returns:
            包含回答和引用来源的字典
        """
        # 更新 top_k
        if top_k != 3:
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=top_k,
                response_mode="compact"
            )
        
        # 执行查询
        response = self.query_engine.query(question)
        
        # 获取引用来源
        source_nodes = response.source_nodes if hasattr(response, 'source_nodes') else []
        
        return {
            "question": question,
            "answer": str(response),
            "sources": [
                {
                    "content": node.node.text,
                    "score": round(node.score, 4) if node.score else None,
                    "metadata": {
                        "file": node.node.metadata.get('file', 'unknown'),
                        "title": node.node.metadata.get('title', '')
                    }
                }
                for node in source_nodes
            ]
        }
    
    def query_formatted(self, question: str, top_k: int = 3) -> str:
        """
        执行查询并返回格式化的回答
        
        Args:
            question: 用户问题
            top_k: 检索的文档片段数量
            
        Returns:
            格式化的字符串，包含回答和引用
        """
        result = self.query(question, top_k)
        
        output = [f"回答: {result['answer']}", ""]
        
        if result['sources']:
            output.append("引用来源:")
            for i, source in enumerate(result['sources'], 1):
                file_name = source['metadata'].get('file', 'unknown')
                title = source['metadata'].get('title', '')
                score = source['score'] if source['score'] else 'N/A'
                
                # 截取内容前150字符作为预览
                content_preview = source['content'][:150].replace('\n', ' ')
                if len(source['content']) > 150:
                    content_preview += "..."
                
                output.append(f"\n{i}. {file_name}")
                if title:
                    output.append(f"   标题: {title}")
                output.append(f"   内容: {content_preview}")
                output.append(f"   相似度: {score}")
        
        return "\n".join(output)


# 全局单例，避免重复加载索引
_rag_engine: Optional[RAGQueryEngine] = None


def get_rag_engine() -> RAGQueryEngine:
    """获取 RAG 引擎单例"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGQueryEngine()
    return _rag_engine


def query_rag(question: str, top_k: int = 3) -> str:
    """
    便捷的查询函数
    
    Args:
        question: 用户问题
        top_k: 检索片段数
        
    Returns:
        格式化的回答字符串
    """
    engine = get_rag_engine()
    return engine.query_formatted(question, top_k)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python scripts/rag_query.py '你的问题' [top_k]")
        sys.exit(1)
    
    question = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    try:
        result = query_rag(question, top_k)
        print(result)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
'''

def main():
    question = "和爱莉希雅打招呼她会说什么?"
    top_k = 3
    result = query_rag(question, top_k)
    print(result)
'''

if __name__ == "__main__":
    main()