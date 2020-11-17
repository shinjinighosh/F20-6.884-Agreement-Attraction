"""Script for translation.
Given a csv file, goes through sentences and split by relativizer.
Translates them to output language
Outputs a json file with the sentences"""

import argparse
import csv
from googletrans import Translator
import json

parser = argparse.ArgumentParser(description='Translate sentences')
parser.add_argument('--path', type=str, default=".", required=False)
parser.add_argument('--input', '-i', type=str, default='items_ParkerAn18.csv', nargs='?', help='name of input file')
parser.add_argument('--output', '-o', type=str, default='translated.json', nargs='?', help='name of output file')

args = parser.parse_args()
input_filename = args.input
output_filename = input_filename[:-4] + "_trans.json"

translator = Translator()
translated_dict = {}

with open(input_filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        full_sentence = row["sentence"]
        if "who" in full_sentence:
            NP, TP = full_sentence.split("who")
            complementizer = "who"
        elif "that" in full_sentence:
            NP, TP = full_sentence.split("that")
            complementizer = "that"
        CP = complementizer + " " + TP
        if NP not in translated_dict:
            NP_translated = translator.translate(NP, dest='fr', src='en').text
            translated_dict[NP] = NP_translated
        if CP not in translated_dict:
            CP_translated = translator.translate(CP, dest='fr', src='en').text
            translated_dict[CP] = CP_translated
    csvfile.close()

with open(output_filename, 'w') as output_file:
    json.dump(translated_dict, output_file)
    output_file.close()

