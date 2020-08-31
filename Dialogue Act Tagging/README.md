This project is to get some experience with sequence labeling. Specifically, you
will be assigning dialogue acts to sequences of utterances in conversations from a corpus. In
sequence labeling it is often beneficial to optimize the tags assigned to the sequence as a whole
rather than treating each tag decision separately. With this in mind, you will be using a machine
learning technique, conditional random fields, which is designed for sequence labeling. You will
be using the toolkit, CRFsuite.

1. Python program (baseline_tagger.py) that reads in a directory of CSV
files, trains a CRFsuite model, tags the CSV files, and prints the
output labels .
In the baseline feature set, for each utterance you include:
• a feature for whether or not the speaker has changed in comparison with the previous utterance.
• a feature marking the first utterance of the dialogue.
• a feature for every token in the utterance (see the description of CRFsuite for an example).
• a feature for every part of speech tag in the utterance (e.g., POS_PRP POS_RB POS_VBP POS_.).

2. Python program (advanced_tagger.py) has been written to improve the accuracy. The feature used to increase the accuracy is the Bi-gram model.
