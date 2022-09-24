import json
import os
import sys
from classifier import classify
from onto_helper import get_keywords
from scrappy import get_text_from_web
import logging

ontology_file_name = sys.argv[1]
text_file_name = sys.argv[2]
output_file_name = sys.argv[3]

texts = []

if text_file_name:
    logging.debug("Text file name" + text_file_name)
    with open(text_file_name, "r") as f:
        texts = f.readlines()

logging.debug("Ontology file name" + ontology_file_name)
keywords = get_keywords(ontology_file_path=ontology_file_name)

search_terms = keywords.get("search_terms", None)
other_labels = keywords.get("other_labels", None)


if not texts:
    if search_terms:
        for search_term in search_terms:
            logging.debug("Searching web with search term: " + search_term)
            texts += get_text_from_web(search_term)

    elif other_labels:
        for label in other_labels:
            logging.debug("Searching web with label: " + label)
            texts += get_text_from_web(label)
    else:
        raise Exception("Both search terms and labels cannot be empty.")

candidate_labels = other_labels if other_labels else search_terms

output_dict = {}
for key in candidate_labels:
    output_dict[key] = []

for text in texts:
    classifier_output = classify(text, candidate_labels)

    for key in classifier_output.keys():
        output_dict[key].append(classifier_output[key])

print(output_dict)
with open(output_file_name, "a") as f:
    json.dump(output_dict, f)
