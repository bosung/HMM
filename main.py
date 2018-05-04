from model import HMM
import preprocess


def train():
    # train.txt 에서 'morph/pos' 의 모든 list를 가져온다.
    data = preprocess.read_train_data("train.txt")
    hmm = HMM()
    for i in range(0, len(data)-1):
        cur = data[i]
        nxt = data[i+1]
        # 문장의 끝과 처음일 경우 skip
        if cur == "</s>/END_TAG" and nxt == "<s>/START_TAG":
            continue
        hmm.update_word_count(cur, nxt)
        hmm.update_total_word_count()
    hmm.update_total_word_count()
    # count를 이용하여 observation, transition 확률을 계산한다.
    hmm.build_model()
    return hmm


def tag(model):
    data = preprocess.read_result_data("result.txt")
    f = open("output.txt", "w", encoding='utf-8')
    for sentence in data:
        # tagging
        result = model.tagging(sentence)
        output = ""
        for e in result:
            output += e.pos_string + " "
        f.write(output+"\n")
    f.close()


hmm = train()
tag(hmm)

