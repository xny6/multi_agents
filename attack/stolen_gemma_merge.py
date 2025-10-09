import json
import glob

def merge_results(output_file='stolen_data_gemma.json'):
    all_results = []
    for file in glob.glob('stolen_data_gemma_*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            all_results.append(json.load(f))
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(all_results, out_f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    merge_results()
    print("All results have been merged into 'stolen_data_gemma.json'.")