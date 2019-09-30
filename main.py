from ner_parser import NERParser
from viterbi import Viterbi

# Training.
entities = []
parser = NERParser()
tokens = []
training_data = open('data/data_train.txt').readlines()

for row in training_data:
    parser.feed(row)
    result = parser.get_result()
    entities.append(result[0])
    tokens.append(result[1])

viterbi = Viterbi(entities, tokens)

# Testing.
entities = []
tokens = []
testing_data = open('data/data_test.txt').readlines()

for row in testing_data:
    parser.feed(row)
    result = parser.get_result()
    entities.append(result[0])
    tokens.append(result[1])

tags = viterbi.tag(tokens)
print(tags)
