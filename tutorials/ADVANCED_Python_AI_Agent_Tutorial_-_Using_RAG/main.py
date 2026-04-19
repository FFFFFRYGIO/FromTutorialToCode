import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from prompts import instruction_str, new_prompt

env_path = Path(__file__).with_name("openai.env")
load_dotenv(dotenv_path=env_path)

population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})

population_query_engine.query("What is the population of Canada?")
