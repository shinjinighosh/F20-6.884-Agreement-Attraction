"""Script to create the training data
Given a csv file, and a translation json, mix and match to create training data
"""

import argparse
import csv
import os
import json

parser = argparse.ArgumentParser(description='Create training data')
parser.add_argument('--path', type=str, default=".", required=False)
parser.add_argument('--input', '-i', type=str, default=os.path.join('data', 'items_ParkerAn18.csv'), nargs='?',
                    help='name of input file')
parser.add_argument('--output', '-o', type=str, default='training_data.csv', nargs='?',
                    help='name of output file')
parser.add_argument('--translated', '-t', type=str, default=os.path.join('data', 'items_ParkerAn18_trans.json'), nargs='?',
                    help='name of translations file')

args = parser.parse_args()
input_filename = args.input
output_filename = input_filename[:-4] + "_training_data.csv"
translation_filename = args.translated


# utils
def mix_and_match(NP_src, CP_src, NP_dest, CP_dest):
    """Given an NP and a TP in a source and destination language each
    Returns a list of all possible mix and match combinations"""
    return [NP_src + CP_src, NP_src + CP_dest, NP_dest + CP_src, NP_dest + CP_dest]


# MAIN
print("Reading from", input_filename, "and writing to", output_filename, "translations at", translation_filename)

translations = {}
with open(translation_filename) as json_file:
    translations = json.load(json_file)
    json_file.close()

with open(input_filename) as csvfile:
    reader = csv.reader(csvfile)
    field_names = next(reader)
    csvfile.close()

with open(input_filename) as csvfile, open(output_filename, 'w') as output_file:
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(output_file, fieldnames=field_names)
    writer.writeheader()
    for row in reader:
        full_sentence = row["sentence"]
        if "who" in full_sentence:
            NP, TP = full_sentence.split("who")
            complementizer = "who"
        elif "that" in full_sentence:
            NP, TP = full_sentence.split("that")
            complementizer = "that"
        CP = complementizer + " " + TP
        V = row["target"]
        V_alt = row["alternative"]
        item = row["item"]
        condition = row["condition"]
        print(NP, CP)
        NP_translated = translations[NP]
        CP_translated = translations[CP]
        V_translated = translations[V]
        V_alt_translated = translations[V_alt]
        sentences = mix_and_match(NP, TP, NP_translated, CP_translated)
        datapoint = {'item': item, 'condition': condition}
        for possibility in sentences:
            datapoint["sentence"] = possibility
            datapoint["target"] = V
            datapoint["alternative"] = V_alt
            writer.writerow(datapoint)
            datapoint["target"] = V_translated
            datapoint["alternative"] = V_alt_translated
            writer.writerow(datapoint)

    csvfile.close()
    output_file.close()

print("Finished creating dataset")