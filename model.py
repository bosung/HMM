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
        # 각 단어와 pos의 등장 횟수를 dictionary에 저장
        self.put_dict(self.pos_count, cur_pos)
        self.put_dict(self.pos_count, (cur_pos, nxt_pos))
        self.put_dict(self.word_count, (cur_pos, cur_word))

    def build_model(self):
        # observation, transition 확률을 구한다.
        self.build_observe_prob()
        self.build_trans_prob()
        # smoothing을 위해 각 확률의 최소값을 구한다.
        self.observe_prob["MIN_PROB"] = self.min_observe_prob
        self.trans_prob["MIN_PROB"] = self.min_trans_prob

    def build_observe_prob(self):
        # word, pos 등장 횟수를 이용해 observation probability 를 구한다.
        word_list = self.word_count.keys()
        for word in word_list:
            pos = word[0]
            self.observe_prob[(pos, word)] = math.log(self.word_count[word] / self.pos_count[pos])
            if self.observe_prob[(pos, word)] < self.min_observe_prob:
                self.min_observe_prob = self.observe_prob[(pos, word)]

    def build_trans_prob(self):
        # pos 의 sequence 정보를 이용해 transition 확률을 구한다.
        pos_list = self.pos_count.keys()
        for pos in pos_list:
            # pos_list 에는 각 pos 의 unigram, bigram key를 포함한다.
            # pos가 (NNG, JKO) 인 경우, len(pos) == 2
            # P(NNG,JKO | NNG) 일 확률을 구함
            if len(pos) == 2 and type(pos) == tuple:
                prev = pos[0]
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.pos_count[prev])
                if self.trans_prob[pos] < self.min_trans_prob:
                    self.min_trans_prob = self.trans_prob[pos]
            # pos가 (NNG) 인 경우, len(pos) == 1
            #  P(NNG) 일 확률을 구한다. P(NNG) = count(NNG) / count(total)
            elif len(pos) == 1:
                self.trans_prob[pos] = math.log(self.pos_count[pos]/self.total_word_cnt)
                if self.trans_prob[pos] < self.min_trans_prob:
                    self.min_trans_prob = self.trans_prob[pos]

    def tagging(self, sentence):
        chain = self.init_chain(sentence)
        self.forward(chain)
        return self.backward(chain)

    def forward(self, chain):
        # forward algorithm
        # t 는 각 어절 step 의 index, 즉 observation sequence의 index
        for t in range(len(chain)):
            # level 은 각 state 에 대한 index, 이 과제에서는 형태소 분석 결과 목록의 index
            for level in range(len(chain[t])):
                # start tag 일 경우
                if t == 0:
                    chain[t][level].state_prob = 0
                else:
                    prob = 0
                    max_prob = 0
                    max_track = 0
                    # t step 에서의 state probability 를 구하기 위해
                    # t-1 step 의 state prob, transition prob 를 순회한다.
                    for i in range(len(chain[t-1])):
                        key = (chain[t-1][i].last_pos, chain[t][level].first_pos)
                        # t-1 step 에서 t step 의 state로 가는 transition probability
                        trans_prob = self.smoothing_prob(self.trans_prob, key)
                        # t-1 step 의 state probability * transition probability
                        prev_prob = chain[t-1][i].state_prob + trans_prob
                        # backtracking 을 위해 max 값을 저장해 놓는다.
                        if prev_prob > max_prob:
                            max_prob = prev_prob
                            max_track = i
                        prob += prev_prob
                    # t-1 step 의 state_prob 와 P(t-1|t) transition 확률을 곱한 후
                    # sum 한 값인 prob 를 t step 의 state probability 에 저장
                    chain[t][level].state_prob = prob
                    chain[t][level].max_track = max_track

    def backward(self, chain):
        # forward()에서 저장해놨던 max node 를 backtracking 한다
        max_path = list()
        max_value = 0
        max_node = chain[-1][0]
        for node in chain[-1]:
            if node.state_prob > max_value:
                max_value = node.state_prob
                max_node = node
        max_path.append(max_node)
        for i in range(len(chain)-2, 0, -1):
            level = max_node.max_track
            max_path.insert(0, chain[i][level])
            max_node = chain[i][level]
        return max_path

    def init_chain(self, sentence):
        # tagging 을 위한 markov chain 을 initialize 한다.
        chain = list()
        temp = list()
        # result.txt 파일에는 시작 태그가 없으므로 추가해준다.
        temp.append(Node(0, 0, "<s>/START_TAG"))
        chain.append(temp)
        for t in range(len(sentence)):
            chain.append([])
            temp = list()
            for level in range(len(sentence[t])):
                node = Node(t+1, level, sentence[t][level])
                # 어절의 observation probability 를 구한다
                node.observe_prob = self.calc_observe_prob(sentence[t][level])
                temp.append(node)
            chain[t+1] = temp
        return chain

    def calc_observe_prob(self, sentence):
        # 입력 문장의 형태소 분석 결과가 string 으로 들어왔을 때, 어절의 observation 확률을 구한다.
        prob = 0
        tokens = sentence.split("+")
        for i in range(len(tokens)):
            morph = tokens[i].split("/")[0]
            pos = tokens[i].split("/")[1]
            # P(morph|pos) 일 확률을 구한다. ex) P('너'|NP)
            # train 데이터에 없는 정보라면 smoothing 기법을 이용해 최소값의 -1(log scale) 을 해준다.
            prob += self.smoothing_prob(self.observe_prob, (pos, morph))
            # 문장의 마지막이 아니라면 P(pos1|pos2) transition 확률을 구한다. ex) P(JKO|NP)
            if i < len(tokens)-1:
                next_pos = tokens[i+1].split("/")[1]
                prob += self.smoothing_prob(self.trans_prob, (pos, next_pos))
        # 어절 내 형태소의 모든 확률을 곱한(log scale 이므로 더함) prob 값을 return
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
        self.max_track = 0

    @staticmethod
    def get_first_last_pos(pos_string):
        tokens = pos_string.split("+")
        first = tokens[0].split("/")[1]
        last = tokens[-1].split("/")[1]
        return first, last
