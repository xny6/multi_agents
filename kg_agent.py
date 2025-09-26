from dataclasses import asdict
import json
import asyncio
import os
import shutil
import inspect
import logging
import logging.config
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc, logger, set_verbose_debug
from lightrag.kg.shared_storage import initialize_pipeline_status

from dotenv import load_dotenv
import re

load_dotenv(dotenv_path=".env", override=False)

WORKING_DIR = "/home/NingyuanXiao/LightRAG_test/working_dir_advanced_ollama"


def configure_logging():
    """Configure logging for the application"""

    # Reset any existing handlers to ensure clean configuration
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "lightrag"]:
        logger_instance = logging.getLogger(logger_name)
        logger_instance.handlers = []
        logger_instance.filters = []

    # Get log directory path from environment variable or use current directory
    log_dir = os.getenv("LOG_DIR", os.getcwd())
    log_file_path = os.path.abspath(os.path.join(log_dir, "/home/NingyuanXiao/LightRAG_test/working_dir_advanced_ollama.log"))

    print(f"\nLightRAG compatible demo log file: {log_file_path}\n")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Get log file max size and backup count from environment variables
    log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 10485760))  # Default 10MB
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))  # Default 5 backups

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(levelname)s: %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "file": {
                    "formatter": "detailed",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "lightrag": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    # Set the logger level to INFO
    logger.setLevel(logging.INFO)
    # Enable verbose debug if needed
    set_verbose_debug(os.getenv("VERBOSE_DEBUG", "false").lower() == "true")


async def initialize_rag(working_dir=WORKING_DIR):
    rag = LightRAG(
        working_dir=working_dir,
        llm_model_func=ollama_model_complete,
        llm_model_name=os.getenv("LLM_MODEL", "deepseek-r1:32b"),
        llm_model_max_token_size=8192,
        llm_model_max_async=12,
        max_parallel_insert=3,
        llm_model_kwargs={
            "host": os.getenv("LLM_BINDING_HOST", "http://localhost:11434"),
            "options": {"num_ctx": 32768},
            "timeout": int(os.getenv("TIMEOUT", "600")),
        },
        embedding_func=EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "768")),
            max_token_size=int(os.getenv("MAX_EMBED_TOKENS", "8192")),
            func=lambda texts: ollama_embed(
                texts,
                embed_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
                host=os.getenv("EMBEDDING_BINDING_HOST", "http://localhost:11434"),
            ),
        ),
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


async def query_kg(rag, question,param):
    response = await rag.aquery(
        question,
        param=param,
    )
    return response

from tqdm import tqdm
async def query_kg_write_to_json(file_path):
    try:

        # Initialize RAG instance
        rag = await initialize_rag()

        query_param = QueryParam(mode='global', stream=False, history_turns=0)

        with open (file_path, 'r') as f:
            data = json.load(f)

        for entry in tqdm(data, desc="Processing KG Queries"):
            question = entry.get("KG Query", "").strip()
            response = await query_kg(rag, question, query_param)
            response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
            entry["KG Result"] = response

        with open(file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

        # with open('/home/NingyuanXiao/Vanna_test/multi_round/enhanced_sql_kg_2_answer_50.json', 'r') as f:
        #     data2 = json.load(f)

        # for entry in data2:
        #     question = entry.get("KG Query", "").strip()
        #     response = await query_kg(rag, question, query_param)
        #     entry["KG Result"] = response

        # with open('/home/NingyuanXiao/Vanna_test/multi_round/enhanced_sql_kg_2_answer_50.json', 'w') as f:
        #     json.dump(data2, f, ensure_ascii=False, indent=4)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.llm_response_cache.index_done_callback()
            await rag.finalize_storages()

# if __name__ == "__main__":
#     # Configure logging before running the main function
#     configure_logging()
#     asyncio.run(main())
#     print("\nDone!")
