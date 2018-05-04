def read_train_data(data_path):
    """
    read and parse train data
    :param data_path:
    :return: list of tags
    """
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
    f.close()
    return data


def read_result_data(data_path):
    f = open(data_path, "r", encoding='utf-8')
    data = list()
    sentence_pos_result = list()
    pos_candis = list()
    for sentence in f.readlines():
        tokens = [x.strip() for x in sentence.split(" ")]
        if len(tokens) == 1 and tokens[0] == '':
            if len(pos_candis) > 0:
                sentence_pos_result.append(pos_candis)
                data.append(sentence_pos_result)
            sentence_pos_result = list()
            pos_candis = list()
        elif len(tokens) == 1:
            if len(pos_candis) > 0:
                sentence_pos_result.append(pos_candis)
            pos_candis = list()
        elif len(tokens) > 1:
            pos_candis.append(tokens[-1])

    if len(pos_candis) > 0:
        sentence_pos_result.append(pos_candis)
        data.append(sentence_pos_result)

    f.close()
    return data
