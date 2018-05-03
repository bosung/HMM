import math

class HMM:

    def __init__(self):
        self.trans_prob = dict()
        self.observe_prob = dict()
        self.word_count = dict()
        self.pos_count = dict()
        self.total_word_cnt = 0

    def update_trans_prob(self, target, value):
        self.trans_prob[target] = value

    def update_output_prob(self, target, value):
        self.observe_prob[target] = value

    def update_total_word_count(self):
        self.total_word_cnt += 1

    def update_word_count(self, prev, curr):
        prev_tokens = [x.strip() for x in prev.split("/")]
        curr_tokens = [y.strip() for y in curr.split("/")]
        if len(prev_tokens) != 2 or len(curr_tokens) != 2:
            return
        prev_word, prev_pos = prev_tokens
        curr_word, curr_pos = curr_tokens
        self.put_dict(self.pos_count, prev_pos)
        self.put_dict(self.pos_count, curr_pos)
        self.put_dict(self.pos_count, (prev_pos, curr_pos))
        self.put_dict(self.word_count, (prev_pos, prev_word))
        self.put_dict(self.word_count, (curr_pos, curr_word))

    def build_model(self):
        self.build_output_prob()
        self.build_trans_prob()

    def build_output_prob(self):
        word_list = self.word_count.keys()
        for word in word_list:
            pos = word[0]
            self.observe_prob[word] = math.log(self.word_count[word] / self.pos_count[pos])

    def build_trans_prob(self):
        pos_list = self.pos_count.keys()
        for pos in pos_list:
            if len(pos) == 2 and type(pos) == tuple:
                prev = pos[0]
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.pos_count[prev])
            elif len(pos) == 1:
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.total_word_cnt)

    def put_dict(self, dictionary, word):
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    def tagging(self, sentence):
        print(1)
