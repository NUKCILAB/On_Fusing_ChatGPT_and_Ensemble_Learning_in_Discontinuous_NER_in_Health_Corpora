'''Update date: 2020-Jan-13'''
import argparse, os, sys, re
from typing import List

def extract_indices_from_brat_annotation(indices: str) -> List[int]:
    indices = re.findall(r"\d+", indices)
    indices = sorted([int(i) for i in indices])
    return indices


def parse_parameters(parser=None):
    if parser is None: parser = argparse.ArgumentParser()

    ## Required
    
    #輸入標註實體檔案
    parser.add_argument("--input_ann", default="./data/Corpora/CADEC/cadec/original", type=str)
    #輸入標註文字檔案
    parser.add_argument("--input_text", default="./data/Corpora/CADEC/cadec/text", type=str)
    #輸出全部檔案標註結果
    parser.add_argument("--output_filepath", default="./data/Experiments/CADEC/all/ann", type=str)
    #感興趣entity ("ADR","Drug","Disease","Symptom","") ""=All Entity
    parser.add_argument("--type_of_interest", default="ADR")

    args, _ = parser.parse_known_args()
    return args


def _get_mention_from_text(text, indices):
    tokens = []
    for i in range(0, len(indices), 2):
        start = int(indices[i])
        end = int(indices[i + 1])
        tokens.append(text[start:end])
    return " ".join(tokens)


if __name__ == "__main__":
    args = parse_parameters()
    num_annotations = 0
    with open(args.output_filepath, "w") as out_f:
        for document in os.listdir(args.input_ann):
            with open(os.path.join(args.input_ann, document), "r") as in_f:
                document = document.replace(".ann", "")
                text = open(os.path.join(args.input_text, "%s.txt" % document)).read()
                for line in in_f:
                    line = line.strip()
                    if line[0] != "T": continue
                    sp = line.strip().split("\t")
                    assert len(sp) == 3
                    mention = sp[2]
                    sp = sp[1].split(" ")
                    label = sp[0]
                    if args.type_of_interest != "" and args.type_of_interest != label: continue
                    indices = extract_indices_from_brat_annotation(" ".join(sp[1:]))
                    mention_from_text = _get_mention_from_text(text, indices)
                    if mention != mention_from_text:
                        print("Update the mention from (%s) to (%s)." % (mention, mention_from_text))
                        mention = mention_from_text
                    num_annotations += 1
                    out_f.write("%s\t%s\t%s\t%s\n" % (document, label, ",".join([str(i) for i in indices]), mention))

    print("Extract %d annotations." % num_annotations)
