import json

file1='/home/NingyuanXiao/multi-agents/attack/eva_qwen2_final_50.json'
file2="/home/NingyuanXiao/multi-agents/attack/new_eva_qwen_final.json"

final_output_file='/home/NingyuanXiao/multi-agents/attack/filter_new_eva_qwen2_final_50.json'

def choose_same_user_query(file1,file2,final_output_file):
    # 读取第一个 JSON 文件
    with open(file1, "r", encoding="utf-8") as f:
        data1 = json.load(f)

    # 读取第二个 JSON 文件
    with open(file2, "r", encoding="utf-8") as f:
        data2 = json.load(f)

    # 创建一个集合来存储第一个文件中的 User Query
    user_queries_set = {item["User Query"] for item in data1}

    # 过滤第二个文件中的数据，只保留 User Query 在第一个文件中的项
    filtered_data = [item for item in data2 if item.get("User Query") in user_queries_set]

    # 将结果保存到新的 JSON 文件
    with open(final_output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"筛选完成，结果共 {len(filtered_data)} 条，已保存到 {final_output_file}")

    # 检查 file1 中的重复项
    user_queries_file1 = [item["User Query"] for item in data1]
    duplicates_file1 = {query for query in user_queries_file1 if user_queries_file1.count(query) > 1}
    print(f"file1 中的重复 User Query: {duplicates_file1}")

    # 检查 file2 中的重复项
    user_queries_file2 = [item["User Query"] for item in data2]
    duplicates_file2 = {query for query in user_queries_file2 if user_queries_file2.count(query) > 1}
    print(f"file2 中的重复 User Query: {duplicates_file2}")

if __name__ == "__main__":
    choose_same_user_query(file1,file2,final_output_file)

    # 检查 file1 中的重复项
