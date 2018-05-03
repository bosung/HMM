from model import HMM
import preprocess


def train():
    data = preprocess.read_train_data("train.txt")
    hmm = HMM()
    for i in range(0, len(data)-1):
        cur = data[i]
        nxt = data[i+1]
        if cur == "</s>/END_TAG" and nxt == "<s>/START_TAG":
            continue
        hmm.update_word_count(cur, nxt)
        hmm.update_total_word_count()
    hmm.update_total_word_count()
    hmm.build_model()
    return hmm


def tag(model):
    data = preprocess.read_result_data("result.txt")
    for sentence in data:
        result = model.tagging(sentence)
        print(result)


hmm = train()
tag(hmm)

