import math


class HMM:

    def __init__(self):
        self.trans_prob = dict()
        self.observe_prob = dict()
        self.word_count = dict()
        self.pos_count = dict()
        self.total_word_cnt = 0
        # min probabilities for smoothing
        self.min_observe_prob = 0
        self.min_trans_prob = 0

    def update_total_word_count(self):
        self.total_word_cnt += 1

    def update_word_count(self, cur, nxt):
        cur_tokens = [x.strip() for x in cur.split("/")]
        nxt_tokens = [y.strip() for y in nxt.split("/")]
        if len(cur_tokens) != 2 or len(nxt_tokens) != 2:
            return
        cur_word, cur_pos = cur_tokens
        nxt_word, nxt_pos = nxt_tokens
        self.put_dict(self.pos_count, cur_pos)
        self.put_dict(self.pos_count, (cur_pos, nxt_pos))
        self.put_dict(self.word_count, (cur_pos, cur_word))

    def build_model(self):
        self.build_observe_prob()
        self.build_trans_prob()
        self.observe_prob["MIN_PROB"] = self.min_observe_prob
        self.trans_prob["MIN_PROB"] = self.min_trans_prob

    def build_observe_prob(self):
        word_list = self.word_count.keys()
        for word in word_list:
            pos = word[0]
            self.observe_prob[(pos, word)] = math.log(self.word_count[word] / self.pos_count[pos])
            if self.observe_prob[(pos, word)] < self.min_observe_prob:
                self.min_observe_prob = self.observe_prob[(pos, word)]

    def build_trans_prob(self):
        pos_list = self.pos_count.keys()
        for pos in pos_list:
            if len(pos) == 2 and type(pos) == tuple:
                prev = pos[0]
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.pos_count[prev])
                if self.trans_prob[pos] < self.min_trans_prob:
                    self.min_trans_prob = self.trans_prob[pos]
            elif len(pos) == 1:
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.total_word_cnt)
                if self.trans_prob[pos] < self.min_trans_prob:
                    self.min_trans_prob = self.trans_prob[pos]

    def tagging(self, sentence):
        chain = self.init_chain(sentence)
        max_path = list()
        for t in range(len(chain)):
            max_value = -10000
            max_level = 0
            for level in range(len(chain[t])):
                if t == 0:
                    chain[t][level].state_prob = 0
                else:
                    prob = 0
                    for i in range(len(chain[t-1])):
                        key = (chain[t-1][i].last_pos, chain[t][level].first_pos)
                        trans_prob = self.smoothing_prob(self.trans_prob, key)
                        prob += (chain[t-1][i].state_prob + trans_prob)
                    chain[t][level].state_prob = prob
                if chain[t][level].state_prob > max_value:
                    max_value = chain[t][level].state_prob
                    max_level = level
            max_path.append(max_level)

        #print(self.min_observe_prob, self.min_trans_prob)
        result = ""
        for t in range(1, len(chain)):
            result += "{}({}) ".format(chain[t][max_path[t]].pos_string, chain[t][max_path[t]].state_prob)
        return result

    def init_chain(self, sentence):
        chain = list()
        temp = list()
        temp.append(Node(0, 0, "<s>/START_TAG"))
        chain.append(temp)
        for t in range(len(sentence)):
            chain.append([])
            temp = list()
            for level in range(len(sentence[t])):
                node = Node(t+1, level, sentence[t][level])
                node.observe_prob = self.calc_observe_prob(sentence[t][level])
                temp.append(node)
            chain[t+1] = temp
        return chain

    def calc_observe_prob(self, sentence):
        prob = 0
        tokens = sentence.split("+")
        for i in range(len(tokens)):
            morph = tokens[i].split("/")[0]
            pos = tokens[i].split("/")[1]
            prob += self.smoothing_prob(self.observe_prob, (pos, morph))
            if i < len(tokens)-1:
                next_pos = tokens[i+1].split("/")[1]
                prob += self.smoothing_prob(self.trans_prob, (pos, next_pos))
        return prob

    @staticmethod
    def put_dict(dictionary, word):
        if word not in dictionary:
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    @staticmethod
    def smoothing_prob(dictionary, key):
        if key not in dictionary:
            return dictionary["MIN_PROB"]-1
        else:
            return dictionary[key]


class Node:

    def __init__(self, t, level, pos_string):
        self.t = t
        self.level = level
        self.pos_string = pos_string
        self.first_pos, self.last_pos = self.get_first_last_pos(pos_string)
        self.observe_prob = 0
        self.state_prob = 0

    @staticmethod
    def get_first_last_pos(pos_string):
        tokens = pos_string.split("+")
        first = tokens[0].split("/")[1]
        last = tokens[-1].split("/")[1]
        return first, last
