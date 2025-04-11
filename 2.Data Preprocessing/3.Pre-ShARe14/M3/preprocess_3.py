# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:08:08 2023

@author: nick8
"""
import re
import json

def extract_ent_fr_txt_by_char_sp(char_span, text, language=None):
    sep = " " if language == "en" else ""
    segs = []
    for idx in range(0, len(char_span), 2):
        ch_sp = [char_span[idx], char_span[idx + 1]]
        segs.append(text[ch_sp[0]:ch_sp[1]])
    return sep.join(segs)
    

def merge_spans(spans, text=None):
    '''
    merge continuous spans
    :param spans: [1, 2, 2, 3]
    :return: [1, 3]
    '''
    new_spans = []
    for pid, pos in enumerate(spans):
        p = pos
        if pid == 0 or pid % 2 != 0 or pid % 2 == 0 and p != new_spans[-1]:
            new_spans.append(pos)
        elif pid % 2 == 0 and p == new_spans[-1]:
            new_spans.pop()

    new_spans_ = []
    if text is not None:  # merge spans if only blanks between them
        for pid, pos in enumerate(new_spans):
            if pid != 0 and pid % 2 == 0 and re.match("^\s+$", text[new_spans[pid - 1]:pos]) is not None:
                new_spans_.pop()
            else:
                new_spans_.append(pos)
        new_spans = new_spans_

    return new_spans


def get_tok2char_span_map(tokens):
    tok2char_span = []
    char_num = 0
    for tok in tokens:
        tok2char_span.append([char_num, char_num + len(tok)])
        char_num += len(tok) + 1  # +1: whitespace
    return tok2char_span
    




def convert_daixiang_data(path, data_type=None):
    with open(path, "r", encoding="utf-8") as file_in:
        lines = [line.strip("\n") for line in file_in]
        data = []
        for i in range(0, len(lines), 3):
            sample = lines[i: i + 3]
            text = sample[0]
            word_list = text.split(" ")
            annstr = sample[1]
            ent_list = []
            word2char_span = get_tok2char_span_map(word_list)

            # entities
            for ann in annstr.split("|"):
                if ann == "":
                    continue
                offsets, ent_type = ann.split(" ")
                offsets = [int(idx) for idx in offsets.split(",")]
                assert len(offsets) % 2 == 0
                for idx, pos in enumerate(offsets):
                    if idx % 2 != 0:
                        offsets[idx] += 1

                extr_segs = []
                char_span = []
                tok_span = []
                for idx in range(0, len(offsets), 2):
                    wd_sp = [offsets[idx], offsets[idx + 1]]
                    ch_sp_list = word2char_span[wd_sp[0]:wd_sp[1]]
                    ch_sp = [ch_sp_list[0][0], ch_sp_list[-1][1]]

                    seg_wd = " ".join(word_list[wd_sp[0]: wd_sp[1]])
                    seg_ch = text[ch_sp[0]:ch_sp[1]]
                    assert seg_ch == seg_wd

                    char_span.extend(ch_sp)
                    tok_span.extend(wd_sp)
                    extr_segs.append(seg_ch)
                ent_txt_extr = extract_ent_fr_txt_by_char_sp(char_span, text, "en")
                ent_txt = " ".join(extr_segs)

                assert ent_txt == ent_txt_extr
                ent = {
                    "text": ent_txt,
                    "type": ent_type,
                    "char_span": char_span,
                    "tok_span": tok_span,
                }
                ent_list.append(ent)

            # merge continuous spans
            for ent in ent_list:
                ori_char_span = ent["char_span"]
                merged_span = merge_spans(ori_char_span)
                ent_ori_extr = extract_ent_fr_txt_by_char_sp(ori_char_span, text, "en")
                ent_extr = extract_ent_fr_txt_by_char_sp(merged_span, text, "en")
                ent["char_span"] = merged_span
                assert ent_ori_extr == ent_extr == ent["text"]

            new_sample = {
                "text": sample[0],
                "word_list": word_list,
                "word2char_span": word2char_span,
                "entity_list": ent_list,
            }
            if data_type is not None:
                new_sample["id"] = "{}_{}".format(data_type, len(data))

            data.append(new_sample)

    return data

        
train_data = convert_daixiang_data("./Input/train.txt")
valid_data = convert_daixiang_data("./Input/dev.txt")
test_data = convert_daixiang_data("./Input/test.txt")

with open("./Output/train_data.json", "w") as f:
    json.dump(train_data, f)

with open("./Output/valid_data.json", "w") as f:
    json.dump(valid_data, f)

with open("./Output/test_data.json", "w") as f:
    json.dump(test_data, f)       

                

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

