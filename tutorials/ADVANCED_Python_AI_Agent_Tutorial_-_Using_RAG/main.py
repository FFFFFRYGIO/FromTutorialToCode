import asyncio
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from llama_index.llms.openai import OpenAI
from note_engine import note_engine
from prompts import context, instruction_str, new_prompt

env_path = Path(__file__).with_name("openai.env")
load_dotenv(dotenv_path=env_path)

TEST_QUERY_ENGINE = False

population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})

if TEST_QUERY_ENGINE:
    result = population_query_engine.query("What is the population of Canada?")
    print("Answer:", result)
    print("Raw:", getattr(result, "response", None))
    print("Metadata:", getattr(result, "metadata", None))

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="this gives information at the world population and demographics",
        ),
    ),
]

llm = OpenAI(model="gpt-3.5-turbo")
agent = ReActAgent(llm=llm, tools=tools, verbose=True, system_prompt=context)


async def main_loop():
    while (prompt := input("Enter a prompt (q to quit): ")) != "q":
        handler = agent.run(prompt)   # or agent.run(user_msg=prompt)
        result = await handler
        print(result)

asyncio.run(main_loop())
