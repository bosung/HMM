from model import HMM


def read_data(data_path):
    data = list()
    f = open(data_path, "r")
    for line in f.readlines():
        tokens = [x.strip() for x in line.split("\t")]
        if len(tokens) == 2:
            data.append(tokens[1])
    return data


def train():
    data = read_data("train.txt")
    hmm = HMM()
    for token in data:
        tokens = [x.strip() for x in token.split("+")]
        if len(tokens) > 1:
            for i in range(0, len(tokens)-1):
                print(tokens[0], tokens[1])
                prev = tokens[0]
                curr = tokens[1]
                hmm.update_word_count(prev, curr)
        break

train()
