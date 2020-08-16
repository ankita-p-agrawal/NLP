from itertools import chain
from collections import namedtuple
import csv
import glob
import os
import pycrfsuite
import sys
import time

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


def word2features(sent, i):
    var1 = True
    var2 = False
    text2 = sent[i][2]
    features = []
    tokens = []
    var3 = False
    endopen = False
    opinion = False
    var4 = False
    var5 = False
    var9 = False
    var10 = False
    varor = False
    varaa = False
    varpositive = False
    varnegative = False
    tags = []
    prev_token = []
    prev_tag = []
    tokentag = []
    var7 = "TOKEN=."
    tokenlist = []
    tagginglist = []
    varthank = False
    varenopop = False
    text4 = sent[i][3]

    if text4[len(text4) - 1] == '-':
        features.extend(
            [
                'lastexp-=%s' % var1
            ]
        )
    else:
        features.extend(
            [
                'lastexp=%s' % var2
            ]
        )

    if text2 != None:
        for token, tag in text2:
            tokens.append('TOKEN=' + token)
            tags.append('TAG=' + tag)
            # tokentag.append('TOKEN=' + token +','+'TAG=' + tag +',')
            if token.lower() == 'or':
                varor = True
            if token.lower() in whwords:
                var3 = True
            if token.lower() in backchannelwords:
                var4 = True
            if token == '?':
                var5 = True
            if token == '!':
                var9 = True
            if token == ',':
                var10 = True
            if token.lower() in opinionwords:
                opinion = True
            if token.lower() in endingopeningwords:
                endopen = True
            if token.lower() in negativewords:
                varnegative = True

    else:
        tokens.append('TOKEN=' + 'NO_WORD')
        tags.append('TAG=' + 'NO_WORD')

    bigrams = []
    bigramtag=[]
    for j in range(len(tokens) - 1):
        bigrams.append(tokens[j] +","+ tokens[j + 1])
    for k in range(len(tags)-1):
        bigramtag.append(tags[k]+","+tags[k+1])
    #print(bigrams)
    #print(bigramtag)
    features.extend(bigrams)
    features.extend(bigramtag)

    #print(bigrams)
    '''if i == 0:
            features.extend(
                prev_token

            )
            features.extend(prev_tag)
    else:
            text5 = sent[i - 1][2]
            if text5 != None:
                for token, tag in text5:
                    prev_token.append('PREVTOKEN=' + token)
                    prev_tag.append('PREVTAG=' + tag)

            else:
                prev_token.append('PREVTOKEN=' + 'NO_WORD')
                prev_tag.append('PREVTAG=' + 'NO_WORD')
    features.extend(
                prev_token
            )
    features.extend(prev_tag)'''

    # tokentag.append('TOKEN=' + 'NO_WORD' +','+'TAG=' + 'NO_WORD' +',')
    len1 = len(tokens)
    '''if varnegative:
        features.extend(
            [
                'negative=%s' % var1
            ]
        )
    else:
        features.extend(
            [
                'negative=%s' % var2
            ]
        )

    if tokens[len(tokens) - 1] == 'TOKEN=--':
        features.extend([
            'lasttoken=%s' % var1
        ])
    else:
        features.extend([
            'lasttoken=%s' % var2
        ])
    if tokens[len(tokens) - 1] == 'TOKEN=.':
        features.extend([
            'lasttokenstop=%s' % var1
        ])
    else:
        features.extend([
            'lasttokenstop=%s' % var2
        ])
    if tokens[len(tokens) - 1] == 'TOKEN=?':
        features.extend([
            'lasttokenqm=%s' % var1
        ])
    else:
        features.extend([
            'lasttokenqm=%s' % var2
        ])
    if ("TOKEN=NO_WORD" in tags):
        features.extend([
            'nonverbalpresence=%s' % var1
        ])
    else:
        features.extend([
            'nonverbalpresence=%s' % var2
        ])
    if var3:
        features.extend([
            'whwords=%s' % var1,
        ])
    else:
        features.extend([
            'whwords=%s' % var2,
        ])
    if var4:
        features.extend([
            'backchannelwords=%s' % var1
        ])
    else:
        features.extend([
            'backchannelwords=%s' % var2
        ])'''

    features.extend([
        'length=%s' % len1,
        # 'length=%s' %len2
    ])

    features.extend(
        tokens
    )

    features.extend(tags)


    if i == 0:
        features.extend([
            'firstword=%s' %var1,
            'speakerchange=%s' % var2,
            #notfirstword=%s' % var2,
            'lastword=%s' % var2
            # 'nospeakerchange=%s' %var1
            # 'previoustag=%s'%var8

        ])
    else:
        #print(i)
        if ((sent[i][1] != sent[i - 1][1]) and i != (len(sent) - 1)):
            features.extend([
                'firstword=%s' %var2,
                'speakerchange=%s' % var1,
                #'notfirstword=%s' % var2,
                'lastword=%s' % var2
                # 'nospeakerchange=%s' % var2

                #  'previoustag=%s' %var8
            ])
        elif ((sent[i][1] == sent[i - 1][1]) and (i != (len(sent) - 1))):
            features.extend(
                [
                    'firstword=%s' %var2,
                    'speakerchange=%s' % var2,
                    #'notfirstword=%s' % var2,
                    'lastword=%s' % var2
                    # 'nospeakerchange=%s' % var2
                    # 'previoustag=%s' % var8
                ]
            )
        elif ((i == len(sent) - 1) and (sent[i][1] != sent[i - 1][1])):
            features.extend([
                'firstword=%s' %var2,
                'speakerchange=%s' % var1,
                #'notfirstword=%s' % var2,
                'lastword=%s' % var1
                # 'nospeakerchange=%s' % var2

                #  'previoustag=%s' %var8
            ])
        elif ((i == len(sent) - 1) and (sent[i][1] == sent[i - 1][1])):
            features.extend([
                'firstword=%s' %var2,
                'speakerchange=%s' % var1,
                #'notfirstword=%s' % var2,
                'lastword=%s' % var1
                # 'nospeakerchange=%s' % var2

                #  'previoustag=%s' %var8
            ])

    # print(set(backchannelwordlist))
    # print(features)
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [sent[i][0] for i in range(len(sent))]


whwords = ['what', 'when', 'where', 'who', 'whom', 'which', 'whose', 'why', 'how']
backchannelwords = ['uh-huh', 'yeah', 'right', 'oh', 'yes', 'okay', 'oh yeah', 'huh', 'sure', 'um', 'huh-uh', 'uh']
negativewords = ['no', "don't"]
endingopeningwords = ['bye', 'hi', 'hello', 'thank', 'sorry', 'apologize', 'excuse', 'pardon', 'bye-bye', 'well']
opinionwords = ['think', 'believe', 'seems', "opinion", 'mean', 'suppose', 'of course']
X_train = [sent2features(s) for s in alist]
Y_train = [sent2labels(s) for s in alist]

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
for item in data:
    testfilename.append(item)
# Accuracy code
correctlabels = []
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

f.close()
# Accuracy
accuracy = (count / count1)*100
print(accuracy)
print(time.time() - start_time)
