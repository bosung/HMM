class HMM:

    def __init__(self):
        self.trans_prob = dict()
        self.output_prob = dict()
        self.word_count = dict()
        self.pos_count = dict()

    def update_trans_prob(self, target, value):
        self.trans_prob[target] = value

    def update_output_prob(self, target, value):
        self.output_prob[target] = value

    def update_word_count(self, prev, curr):
        prev_tokens = [x.strip() for x in prev.split("/")]
        curr_tokens = [y.strip() for y in curr.split("/")]
        if len(prev_tokens) != 2 or len(curr_tokens) != 2:
            return
        prev_word, prev_pos = prev_tokens
        curr_word, curr_pos = curr_tokens
        self.put_dict(self.word_count, prev)
        self.put_dict(self.word_count, curr)
        self.put_dict(self.word_count, (prev, curr))

    def build_model(self):
        word_list = self.word_count.keys()
        for word in word_list:
            if len(word) == 1:


    def build_trans_prob(self):
        pos_list = self.pos_count.keys()
        for i in range(0, len(pos_list)):



    def put_dict(self, dict, word):
        if word not in self.dict:
            self.dict[word] = 1
        else:
            self.dict[word] += 1
