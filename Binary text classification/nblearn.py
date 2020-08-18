from sys import argv
from math import log10
from pathlib import Path


class NaiveBayesModelTrain:

    # Data Structures
    training_set_location = ""
    save_data_location = "nbmodel.txt"
    vocabulary = set()
    spam_dict = dict()
    ham_dict = dict()

    # Constants
    SPAM = "spam"
    HAM ="ham"
    TOTAL_WORDS = 0         # Total number of words in the corpus
    TOTAL_SPAM_WORDS = 0    # Total number of spam words in the corpus
    TOTAL_HAM_WORDS = 0     # Total number of ham words in the corpus
    SMOOTHING_CONSTANT = 1  # For Laplace Smoothing

    # Probabilities
    # Prior probability of spam and ham
    probability = {
        "spam": 0.0,
        "ham": 0.0,
    }
    # Conditional probability for every token
    probability_of_being_spam = dict()
    probability_of_being_ham = dict()

    def __init__(self, input_file_path):
        self.training_set_location = Path(input_file_path)
        self.save_data = open(self.save_data_location, "w")

    # Utility to train Naive Bayes Classifier
    def train_naive_bayes_classifier(self):
        self.data_acquisition()
        self.compute_probabilities()
        self.save_model_parameters()

    # Utility to read data and their appropriate class labels to train the Naive Bayes Classifier
    def data_acquisition(self):
        # Recursively look for .txt files in training set location
        for each_email in self.training_set_location.rglob('*.txt'):
            # Determine actual label of data
            actual_label = Path(each_email).parent.name.lower().rstrip()
            # Read email contents one by one
            email_contents = open(each_email, "r", encoding="latin1")
            # Process each line of email
            for each_line in email_contents.readlines():
                # Remove newline characters and transform each line to lowercase
                each_line = each_line.rstrip().lower()
                word_list = each_line.split()
                # Add lines in email to appropriate category
                if self.SPAM in actual_label.lower():
                    for word in word_list:
                        self.spam_dict[word] = self.spam_dict.get(word, 0) + 1
                        self.vocabulary.add(word)
                    self.TOTAL_SPAM_WORDS += len(word_list)
                elif self.HAM in actual_label.lower():
                    for word in word_list:
                        self.ham_dict[word] = self.ham_dict.get(word, 0) + 1
                        self.vocabulary.add(word)
                    self.TOTAL_HAM_WORDS += len(word_list)
        # Total number of words in the entire corpus
        self.TOTAL_WORDS = self.TOTAL_SPAM_WORDS + self.TOTAL_HAM_WORDS

    # Utility to compute all the required probabilities
    def compute_probabilities(self):
        VOCABULARY_SIZE = len(self.vocabulary)
        # Compute prior probability of spam/ham messages
        self.probability[self.SPAM] = log10(self.TOTAL_SPAM_WORDS / self.TOTAL_WORDS)
        self.probability[self.HAM] = log10(self.TOTAL_HAM_WORDS / self.TOTAL_WORDS)
        # Compute conditional probability for every unique token in the vocabulary
        for token in self.vocabulary:
            spam_val = self.modified_division(self.spam_dict.get(token, 0) + self.SMOOTHING_CONSTANT,
                                              self.TOTAL_SPAM_WORDS + (self.SMOOTHING_CONSTANT * VOCABULARY_SIZE))
            self.probability_of_being_spam[token] = log10(spam_val)
            ham_val = self.modified_division(self.ham_dict.get(token, 0) + self.SMOOTHING_CONSTANT,
                                             self.TOTAL_HAM_WORDS + (self.SMOOTHING_CONSTANT * VOCABULARY_SIZE))
            self.probability_of_being_ham[token] = log10(ham_val)

    # Utility to save model parameters
    def save_model_parameters(self):
        line_format1 = lambda token, value1, value2: "{} {} {}\n".format(token, value1, value2)
        line_format2 = lambda tag, value: "{} {}\n".format(tag, value)
        # Save prior probability of spam and ham
        self.save_data.write(line_format2(self.SPAM, self.probability[self.SPAM]))
        self.save_data.write(line_format2(self.HAM, self.probability[self.HAM]))
        # Save conditional probability of every token
        self.save_data.write(line_format1("token", "spam", "ham"))
        for token in self.vocabulary:
            line = line_format1(token, self.probability_of_being_spam[token], self.probability_of_being_ham[token])
            self.save_data.write(line)
        self.save_data.close()

    # Utility to tackle division by 0
    # Returns zero instead of throwing an exception if denominator is zero
    def modified_division(self, numerator, denominator):
        if denominator == 0:
            return 0
        else:
            return numerator / denominator


if __name__ == '__main__':
    # Acquire location of corpus from command line
    file_path = " ".join(argv[1:])
    NB_model = NaiveBayesModelTrain(file_path)
    # Train Naive Bayes Classifier
    NB_model.train_naive_bayes_classifier()

