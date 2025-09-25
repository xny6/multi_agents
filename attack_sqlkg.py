import json
from functions import sql_kg_process_date_attack,sql_kg_process_name_attack,add_summary_to_json
import re
from kg_agent import query_kg_write_to_json
import asyncio

input_file_date='/home/NingyuanXiao/multi-agents/attack/wrong_answer_qwen2.json'
output_file_date='sql_kg_deepseek_date.json'
output_file_date_summary= 'sql_kg_deepseek_date_summary.json'

input_file_name='/home/NingyuanXiao/multi-agents/attack/wrong_answer_qwen2.json'
output_file_name='sql_kg_deepseek_name.json'
output_file_name_summary='sql_kg_deepseek_name_summary.json'

model_name='qwen2'

sql_kg_process_date_attack(input_file_date, output_file_date,model_name)
sql_kg_process_name_attack(input_file_name, output_file_name,model_name)

asyncio.run(query_kg_write_to_json(output_file_date))
asyncio.run(query_kg_write_to_json(output_file_name))

add_summary_to_json(output_file_name,output_file_name_summary,model_name)
add_summary_to_json(output_file_date,output_file_date_summary,model_name)

