from sys import argv
from pathlib import Path


class NaiveBayesClassification:

    corpus_location = ""
    read_parameter_location = "nbmodel.txt"
    save_data_location = "nboutput.txt"
    vocab_dict = dict()

    SPAM = "spam"
    HAM ="ham"

    probability = {
        "spam": 0.0,
        "ham": 0.0,
    }
    # Conditional probability for every token
    probability_of_being_spam = dict()
    probability_of_being_ham = dict()

    def __init__(self, input_file_path):
        self.corpus_location = Path(input_file_path)
        self.parameter_reader = open(self.read_parameter_location, "r")
        self.labelled_output_writer = open(self.save_data_location, "w")

    # Perform prediction task using trained Naive Bayes Classifier
    def prediction(self):
        self.read_parameters()
        self.classification_engine()

    # Read learned parameters
    def read_parameters(self):
        spam_line = self.parameter_reader.readline().strip().split()
        ham_line = self.parameter_reader.readline().strip().split()
        header, label1, label2 = self.parameter_reader.readline().strip().split()

        self.probability[self.SPAM] = float(spam_line[1])
        self.probability[self.HAM] = float(ham_line[1])

        for each_line in self.parameter_reader.readlines():
            word, label1_val, label2_val = each_line.strip().split()
            self.vocab_dict[word] = {label1 : float(label1_val),
                                     label2 : float(label2_val)}

    # Utility that classifies email as either spam or ham using Naive Bayes Classifier
    def classification_engine(self):
        first_time = True
        # Recursively look for .txt files
        for each_email in self.corpus_location.rglob('*.txt'):
            # Read email contents one by one
            email_reader = open(each_email, "r", encoding="latin1")
            # Make prediction by adding logarithms of probabilities
            probability_of_being_spam = self.probability[self.SPAM]
            probability_of_being_ham = self.probability[self.HAM]
            # Process each line of email
            for each_line in email_reader.readlines():
                each_line = each_line.rstrip().lower()
                word_list = each_line.split()
                for word in word_list:
                    if word in self.vocab_dict:
                        probability_of_being_spam += self.vocab_dict[word][self.SPAM]
                        probability_of_being_ham += self.vocab_dict[word][self.HAM]
            if probability_of_being_ham >= probability_of_being_spam:
                if first_time:
                    first_time = False
                    self.labelled_output_writer.write(self.HAM + "\t" + str(each_email))
                else:
                    self.labelled_output_writer.write("\n" + self.HAM + "\t" + str(each_email))
            else:
                if first_time:
                    first_time = False
                    self.labelled_output_writer.write(self.SPAM + "\t" + str(each_email))
                else:
                    self.labelled_output_writer.write("\n" + self.SPAM + "\t" + str(each_email))


if __name__ == '__main__':
    file_path = " ".join(argv[1:])
    NB_model = NaiveBayesClassification(file_path)
    NB_model.prediction()