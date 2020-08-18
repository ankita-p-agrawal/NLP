import time
import sys
from collections import namedtuple
import csv
import glob
import os
import pycrfsuite

start_time = time.time()


def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]


def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)


def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)


DialogUtterance = namedtuple(
    "DialogUtterance", ("act_tag", "speaker", "pos", "text"))

DialogUtterance.__doc__ = """\
An utterance in a dialog. Empty utterances are None.

act_tag - the dialog act associated with this utterance
speaker - which speaker made this utterance
pos - a list of PosTag objects (token and POS)
text - the text of the utterance with only a little bit of cleaning"""

PosTag = namedtuple("PosTag", ("token", "pos"))

PosTag.__doc__ = """\
A token and its part-of-speech tag.

token - the token
pos - the part-of-speech tag"""


def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)


# if os.path.exists(filePath):
#   print(os.path.basename(filePath))
filepath = sys.argv[1]
# print(filepath)
# data=get_data('/Users/ankitaagrawal/Downloads/train 2/train')
data = get_data(filepath)
'''for i in range(getsizeof(data)):
    print("*******************",next(data))'''
# print(next(data))
# print(data)
alist = []
for item in data:
    alist.append(item)


# print(len(alist))
def word2features(sent, i):
    var1 = True
    var2 = False
    text2 = sent[i][2]
    features = []
    tokens = []
    tags = []
    tokenlist = []
    tagginglist = []
    if text2 != None:
        for token, tag in text2:
            tokens.append('TOKEN=' + token.lower())
            tokens.append('TAG=' + tag)
    else:
        tokens.append('TOKEN=' + 'NO_WORD')
        #tags.append('TAG=' + 'NO_WORD')

    features.extend(
        tokens

        # 'tokens=' + stringtoken,
        # 'tags=' + stringtag,
    )
    #features.extend(tags)
    if i == 0:
        features.extend([
            'firstword=%s' % var1,
            'speakerchange=%s' % var2

        ])

    else:
        if sent[i][1] != sent[i - 1][1]:
            features.extend([
                'firstword=%s' % var2,
                'speakerchange=%s' % var1
            ])
        elif sent[i][1] == sent[i - 1][1]:
            features.extend(
                [
                    'firstword=%s' % var2,
                    'speakerchange=%s' % var2
                ]
            )

    # print(features)
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [sent[i][0] for i in range(len(sent))]


X_train = [sent2features(s) for s in alist]
# print(numpy.shape(X_train))
Y_train = [sent2labels(s) for s in alist]
# print(numpy.shape(Y_train))
trainer = pycrfsuite.Trainer(verbose=False)
for xseq, yseq in zip(X_train, Y_train):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,  # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 50,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})
trainer.train('baselinetagger.crfsuite')
tagger = pycrfsuite.Tagger()
tagger.open('baselinetagger.crfsuite')
testfilename = []
filepath = sys.argv[2]
data = get_data(filepath)
# data=get_data('/Users/ankitaagrawal/Downloads/nlp/test')
for item in data:
    testfilename.append(item)

correctlabels = []
predictedlabels = []
filepath = sys.argv[3]

f = open(filepath, "w")
count = 0
count1 = 0
for s in testfilename:
    predictedlabels = []
    correctlabels = []
    for i in sent2labels(s):
        correctlabels.append(i)
    for i in tagger.tag(sent2features(s)):
        f.write(i + "\n")
        predictedlabels.append(i)
        # count1 =count1+ len(predictedlabels)
    f.write("\n")
    for i in range(len(predictedlabels)):
        if correctlabels[i] == predictedlabels[i]:
            count += 1
    # print(count)
    count1 += len(predictedlabels)

'''for s in testfilename:
    for i in sent2labels(s):
        correctlabels.append(i)

for s in testfilename:
    for i in tagger.tag(sent2features(s)):
        f.write(i+"\n")
        predictedlabels.append(i)
    f.write("\n")'''

f.close()
# Accuracy
accuracy = (count / count1) * 100
print(accuracy)
print(time.time() - start_time)
