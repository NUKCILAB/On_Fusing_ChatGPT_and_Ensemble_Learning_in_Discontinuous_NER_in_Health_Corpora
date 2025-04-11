import json
from collections import defaultdict, Counter

def extract_entities(ner_set):
    """將每個模型的實體標註從集合中提取出來"""
    entities = set()
    for entity in ner_set:
        entities.add(tuple(sorted(entity)))  # 將實體範圍轉換為排序的元組以便比較
    return entities

def hard_voting(entities_lists):
    """對所有模型的實體標註進行硬投票"""
    all_entities = defaultdict(int)
    
    for entities in entities_lists:
        for entity in entities:
            all_entities[entity] += 1
    
    # 選擇投票最多的實體，要求投票數量至少過半數
    threshold = len(entities_lists) // 2 + 1  # 大於等於一半的模型數量
    final_entities = [list(entity) for entity, count in all_entities.items() if count >= threshold]
    
    return final_entities

def process_data(input_file, output_file):
    """讀取 JSON 檔案，進行硬投票，並儲存結果"""
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    results = []
    
    for entry in data:
        text = entry['text']
        ner_sets = [entry[f'ner{i+1}'] for i in range(5)]
        
        # 提取每個模型的實體
        entities_lists = [extract_entities(ner_set) for ner_set in ner_sets]
        
        # 進行硬投票
        final_entities = hard_voting(entities_lists)
        
        results.append({
            'text': text,
            'ner': final_entities
        })
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    print(f'Results saved to {output_file}')

if __name__ == '__main__':
    input_file_path = 'input.json'
    output_file_path = 'output.json'
    process_data(input_file_path, output_file_path)
