class HMM():

    def __init__(self):
        self.trans_prob = dict()
        self.output_prob = dict()


    def update(self, target, value):
        self.trans_prob[target] = value

