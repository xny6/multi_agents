from eva_functtions import reduce_payload_in_queries, compose_json_for_evaluation, evaluate_results,handel_json_wrong,merge_json_files

files_to_merge_attack = [
    '/home/NingyuanXiao/multi-agents/attack/attack_kg_sql_qwen2_final.json',
    '/home/NingyuanXiao/multi-agents/attack_sql_kg_qwen2_date_summary.json',
    '/home/NingyuanXiao/multi-agents/attack_sql_kg_qwen2_name_summary.json'
]

output_merged_file_attack = '/home/NingyuanXiao/multi-agents/attack/attack_qwen2_all.json'

merge_json_files(files_to_merge_attack, output_merged_file_attack)

files_to_merge_correct = [
    '/home/NingyuanXiao/multi-agents/kg_sql_qwen2_final.json',
    '/home/NingyuanXiao/multi-agents/sql_kg_qwen2_date_summary.json',
    '/home/NingyuanXiao/multi-agents/sql_kg_qwen2_name_summary.json'
]
output_merged_file_correct = '/home/NingyuanXiao/multi-agents/attack/origin_data_qwen2_all.json'
merge_json_files(files_to_merge_correct, output_merged_file_correct)

reduce_payload_in_queries(
    json_file_B_path="/home/NingyuanXiao/multi-agents/attack/attack_qwen2_all.json",
    output_file_path="/home/NingyuanXiao/multi-agents/attack/attack_qwen2_all_no_payload.json"
)

compose_json_for_evaluation(
    file_a_stolen_with_wrong_answer="/home/NingyuanXiao/multi-agents/attack/wrong_answer_qwen2.json",
    file_b_filter_result_without_payload="/home/NingyuanXiao/multi-agents/attack/attack_qwen2_all_no_payload.json",
    file_c_origin_result="/home/NingyuanXiao/multi-agents/attack/origin_data_qwen2_all.json",
    output_file_for_eva="/home/NingyuanXiao/multi-agents/attack/results_for_evaluation_qwen2_all.json"
)

evaluate_results(
    input_file="/home/NingyuanXiao/multi-agents/attack/results_for_evaluation_qwen2_all.json",
    output_file="/home/NingyuanXiao/multi-agents/attack/eva_qwen2.json",
    model_name="gemma3:27b"
)


handel_json_wrong(
    input_file="/home/NingyuanXiao/multi-agents/attack/eva_qwen2.json",
    output_file="/home/NingyuanXiao/multi-agents/attack/eva_qwen2_final.json"
)