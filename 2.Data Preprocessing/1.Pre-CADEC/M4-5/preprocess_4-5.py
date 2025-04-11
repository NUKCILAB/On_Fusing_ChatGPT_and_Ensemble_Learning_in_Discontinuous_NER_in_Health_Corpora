import os
import json

def convert_format(data):
    # 將Input格式轉換為Output格式
    converted_data = []
    
    for item in data:
        sentence = item['word_list']
        ner_annotations = []
        
        for entity in item.get('entity_list', []):
            # 轉換 tok_span 範圍為索引列表
            tok_start, tok_end = entity['tok_span']
            ner_annotations.append({
                'index': list(range(tok_start, tok_end + 1)),
                'type': entity['type']
            })
        
        converted_data.append({
            'sentence': sentence,
            'ner': ner_annotations
        })
    
    return converted_data

def main():
    # 設定 input 和 output 資料夾的路徑 (Input檔案為M3的Output)
    input_folder = 'Input'
    output_folder = 'Output'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 處理每個檔案
    for filename in ['train_data.json', 'valid_data.json', 'test_data.json']:
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)
        
        # 讀取Input的 JSON 檔案
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        # 轉換格式
        converted_data = convert_format(data)
        
        # 儲存Output的 JSON 檔案
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(converted_data, outfile, ensure_ascii=False, indent=4)
        
        print(f'Converted {filename} and saved to {output_file_path}')

if __name__ == '__main__':
    main()
