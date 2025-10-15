from eva_functtions import reduce_payload_in_queries, compose_json_for_evaluation, evaluate_results,handel_json_wrong,merge_json_files

files_to_merge_attack = [
    '/home/NingyuanXiao/multi-agents/attack/new_attack_kg_sql_qwen2_final_final.json',
    '/home/NingyuanXiao/multi-agents/new_attack_sql_kg_qwen2_date_summary.json',
    '/home/NingyuanXiao/multi-agents/new_attack_sql_kg_qwen2_name_summary.json'
]

output_merged_file_attack = '/home/NingyuanXiao/multi-agents/attack/new_attack_qwen_all.json'

merge_json_files(files_to_merge_attack, output_merged_file_attack)

# files_to_merge_correct = [
#     '/home/NingyuanXiao/multi-agents/kg_sql_deepseek_final.json',
#     '/home/NingyuanXiao/multi-agents/sql_kg_deepseek_date_summary.json',
#     '/home/NingyuanXiao/multi-agents/sql_kg_deepseek_name_summary.json'
# ]
# output_merged_file_correct = '/home/NingyuanXiao/multi-agents/attack/origin_data_deepseek_all.json'
# merge_json_files(files_to_merge_correct, output_merged_file_correct)

reduce_payload_in_queries(
    json_file_B_path="/home/NingyuanXiao/multi-agents/attack/new_attack_qwen_all.json",
    output_file_path="/home/NingyuanXiao/multi-agents/attack/new_attack_qwen_all_no_payload.json"
)

compose_json_for_evaluation(
    file_a_stolen_with_wrong_answer="/home/NingyuanXiao/multi-agents/attack/new_wrong_answer_qwen2_wrong_rename.json",
    file_b_filter_result_without_payload="/home/NingyuanXiao/multi-agents/attack/new_attack_qwen_all_no_payload.json",
    file_c_origin_result="/home/NingyuanXiao/multi-agents/attack/origin_data_qwen2_all.json",
    output_file_for_eva="/home/NingyuanXiao/multi-agents/attack/new_results_for_evaluation_qwen_all.json"
)

evaluate_results(
    input_file="/home/NingyuanXiao/multi-agents/attack/new_results_for_evaluation_qwen_all.json",
    output_file="/home/NingyuanXiao/multi-agents/attack/new_eva_qwen.json",
    model_name="gemma3:27b"
)


handel_json_wrong(
    input_file="/home/NingyuanXiao/multi-agents/attack/new_eva_qwen.json",
    output_file="/home/NingyuanXiao/multi-agents/attack/new_eva_qwen_final.json"
)