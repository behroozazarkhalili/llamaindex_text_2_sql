"""Utilities for Spider module."""

import json
import os
from typing import Dict, Tuple

from sqlalchemy import create_engine, text

from llama_index import LLMPredictor, SQLDatabase
from llama_index.indices import SQLStructStoreIndex
from llama_index.llms.openai import OpenAI


def load_examples(spider_dir: str) -> Tuple[list, list]:
    """
    Load examples from the specified spider directory.
    
    Args:
        spider_dir (str): The path to the spider directory.
        
    Returns:
        Tuple[list, list]: A tuple containing two lists. The first list contains the loaded examples from the spider's training data (train_spider.json and train_others.json), and the second list contains the loaded examples from the dev.json file.
    """
    
    with open(os.path.join(spider_dir, "train_spider.json"), encoding="utf-8") as f:
        train_spider = json.load(f)

    with open(os.path.join(spider_dir, "train_others.json"), encoding="utf-8") as f:
        train_others = json.load(f)

    with open(os.path.join(spider_dir, "dev.json"), encoding="utf-8") as f:
        dev = json.load(f)
        
    return train_spider + train_others, dev


def create_indexes(spider_dir: str, llm: OpenAI) -> Dict[str, SQLStructStoreIndex]:
    """
    Generate the indexes for the given Spider directory and LLModel.

    Args:
        spider_dir (str): The path to the Spider directory.
        llm (OpenAI): The LLModel instance.

    Returns:
        Dict[str, SQLStructStoreIndex]: A dictionary mapping database names to SQLStructStoreIndex objects.
    """
    
    # Create all necessary SQL database objects.
    databases = {}

    for db_name in os.listdir(os.path.join(spider_dir, "database")):
        db_path = os.path.join(spider_dir, "database", db_name, db_name + ".sqlite")

        if not os.path.exists(db_path):
            continue

        engine = create_engine("sqlite:///" + db_path)
        databases[db_name] = SQLDatabase(engine=engine)

        # Test connection.
        with engine.connect() as connection:
            connection.execute(text("select name from sqlite_master where type = 'table'")).fetchone()

    llm_predictor = LLMPredictor(llm=llm)
    llm_indexes = {}

    for db_name, db in databases.items():
        llm_indexes[db_name] = SQLStructStoreIndex(llm_predictor=llm_predictor,sql_database=db,)
        
    return llm_indexes
