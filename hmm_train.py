from model import HMM


def read_train_data(data_path):
    data = list()
    f = open(data_path, "r", encoding='utf-8')
    start_sentence = True
    for line in f.readlines():
        tokens = [x.strip() for x in line.split("\t")]
        if len(tokens) == 2:
            if start_sentence is True:
                data += ["<s>/START_TAG"]
                start_sentence = False
            data += tokens[1].split("+")
            if tokens[1][-4:] == './SF':
                data += ["</s>/END_TAG"]
                start_sentence = True

    return data


def read_result_data(data_path):
    f = open(data_path, "r", encoding='utf-8')
    for sentence in f.readlines():
        tokens = [x.strip() for x in sentence.split(" ")]
        print(tokens)


def train():
    data = read_train_data("train.txt")
    hmm = HMM()
    for i in range(0, len(data)-1):
        prev = data[i]
        curr = data[i+1]
        if prev == "</s>/END_TAG" and curr == "<s>/START_TAG":
            continue
        hmm.update_word_count(prev, curr)
        hmm.update_total_word_count()
    hmm.update_total_word_count()
    hmm.build_model()
    print('end')
    return hmm


def tag(model):
    read_result_data("result.txt")


#hmm = train()
#tag(hmm)
read_result_data("result.txt")

