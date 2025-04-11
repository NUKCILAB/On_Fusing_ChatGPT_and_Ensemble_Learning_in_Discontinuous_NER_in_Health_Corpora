import json
from collections import defaultdict, Counter

def extract_entities(ner_set):
    """�N�C�Ӽҫ�������е��q���X�������X��"""
    entities = set()
    for entity in ner_set:
        entities.add(tuple(sorted(entity)))  # �N����d���ഫ���ƧǪ����եH�K���
    return entities

def hard_voting(entities_lists):
    """��Ҧ��ҫ�������е��i��w�벼"""
    all_entities = defaultdict(int)
    
    for entities in entities_lists:
        for entity in entities:
            all_entities[entity] += 1
    
    # ��ܧ벼�̦h������A�n�D�벼�ƶq�ܤֹL�b��
    threshold = len(entities_lists) // 2 + 1  # �j�󵥩�@�b���ҫ��ƶq
    final_entities = [list(entity) for entity, count in all_entities.items() if count >= threshold]
    
    return final_entities

def process_data(input_file, output_file):
    """Ū�� JSON �ɮסA�i��w�벼�A���x�s���G"""
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    results = []
    
    for entry in data:
        text = entry['text']
        ner_sets = [entry[f'ner{i+1}'] for i in range(5)]
        
        # �����C�Ӽҫ�������
        entities_lists = [extract_entities(ner_set) for ner_set in ner_sets]
        
        # �i��w�벼
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
