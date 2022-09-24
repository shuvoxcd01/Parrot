from transformers import pipeline
import os

os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "120"

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli", multi_label=True)

CLASSIFICATION_THRESHOLD = 0.8


def classify(sequence_to_classify: str, candidate_lables: list):
    output = classifier(sequence_to_classify, candidate_lables)

    output_dict = {}
    for i in range(len(candidate_lables)):
        score = output["scores"][i]
        if score > CLASSIFICATION_THRESHOLD:
            output_dict[output["labels"][i]] = output["sequence"]

    return output_dict
