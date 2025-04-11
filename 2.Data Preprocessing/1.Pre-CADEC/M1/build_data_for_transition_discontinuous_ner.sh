

#input cadec 
#"./data/Corpora/CADEC/cadec/original" 
#"./data/Corpora/CADEC/cadec/text" 

#mkdir ./data/Experiments/CADEC/all


echo "Extract annotations ..." >> build_data_for_transition_discontinous_ner.log
python extract_annotations.py --log_filepath build_data_for_transition_discontinous_ner.log

echo "Tokenization ..." >> build_data_for_transition_discontinous_ner.log
python tokenization.py --log_filepath build_data_for_transition_discontinous_ner.log

echo "Convert annotations from character level offsets to token level idx ..." >> build_data_for_transition_discontinous_ner.log
python convert_ann_using_token_idx.py --log_filepath build_data_for_transition_discontinous_ner.log

echo "Create text inline format ..." >> build_data_for_transition_discontinous_ner.log
python convert_text_inline.py --log_filepath build_data_for_transition_discontinous_ner.log

echo "Split the data set into train, dev, test splits ..." >> build_data_for_transition_discontinous_ner.log
python split_train_test.py 