from pathlib import Path
from sys import argv


class NaiveBayesPerformanceEvaluation:

    # Constants
    SPAM = "spam"
    HAM = "ham"

    def __init__(self, input_file_name):
        # Open file for reading
        input_reader = open(input_file_name, "r")

        # Actual number of spams/hams in data set
        actual_number_of_spam = 0
        actual_number_of_ham = 0

        # Total number of emails classified as spam/ham after prediction
        predicted_as_spam = 0
        predicted_as_ham = 0

        # Total number of correct classifications
        correctly_classified_as_spam = 0
        correctly_classified_as_ham = 0

        # Total number of incorrect classifications
        incorrectly_classified_as_spam = 0
        incorrectly_classified_as_ham = 0

        # Read input file containing results of classifications line by line
        for line in input_reader.readlines():
            # Till we reach EOF
            if line != "":
                # Split till we hit first space
                elements = line.rstrip().split("\t", 1)
                if len(elements) == 2:
                    predicted_label, email_file_path = elements
                else:
                    # To deal with incorrect entries
                    continue

                # Extract folder name
                proper_file_path = Path(email_file_path)
                actual_label = proper_file_path.parent.name.lower().rstrip()

                # Collect number of correct and incorrect classifications for spam/ham
                if self.SPAM in actual_label:
                    actual_number_of_spam += 1
                    # Verify true and predicted labels for spam
                    if predicted_label.lower() in actual_label:
                        predicted_as_spam += 1
                        correctly_classified_as_spam += 1
                    else:
                        predicted_as_ham += 1
                        incorrectly_classified_as_spam += 1
                elif self.HAM in actual_label:
                    actual_number_of_ham += 1
                    # Verify true and predicted labels for ham
                    if predicted_label.lower() in actual_label:
                        predicted_as_ham += 1
                        correctly_classified_as_ham += 1
                    else:
                        predicted_as_spam += 1
                        incorrectly_classified_as_ham += 1
                else:
                    # Invalid label in file path -> cannot verify
                    print(" {} -> {} ".format(predicted_label, file_path))
                    continue
        # ----------------------------------- Compute Precision -----------------------------------
        spam_classification_precision = self.modified_division(correctly_classified_as_spam, predicted_as_spam)
        ham_classification_precision = self.modified_division(correctly_classified_as_ham, predicted_as_ham)

        # ----------------------------------- Compute Recall -----------------------------------
        spam_classification_recall = self.modified_division(correctly_classified_as_spam, actual_number_of_spam)
        ham_classification_recall = self.modified_division(correctly_classified_as_ham, actual_number_of_ham)

        # ----------------------------------- Compute F1 Score -----------------------------------
        spam_f1_num = 2 * spam_classification_precision * spam_classification_recall
        spam_f1_den = spam_classification_precision + spam_classification_recall
        spam_classification_f1_score = self.modified_division(spam_f1_num, spam_f1_den)
        ham_f1_num = 2 * ham_classification_precision * ham_classification_recall
        ham_f1_den = ham_classification_precision + ham_classification_recall
        ham_classification_f1_score = self.modified_division(ham_f1_num, ham_f1_den)

        # Print results
        print("spam precision: " + str(spam_classification_precision))
        print("spam recall: " + str(spam_classification_recall))
        print("spam F1 score: " + str(spam_classification_f1_score))
        print("ham precision: " + str(ham_classification_precision))
        print("ham recall: " + str(ham_classification_recall))
        print("ham F1 score: " + str(ham_classification_f1_score))


    # Utility to tackle division by 0
    # Returns zero instead of throwing an exception if denominator is zero
    def modified_division(self, numerator, denominator):
        if denominator == 0:
            return 0
        else:
            return numerator / denominator

    # Utility to print metrics
    def print_result(self, main_category, class1_name, class1_value, class2_name, class2_value, is_percent=False):
        if is_percent:
            print("{} {}: {} ({:.2f})%".format(class1_name.capitalize(), main_category,
                                               class1_value, class1_value * 100))
            print("{} {}: {} ({:.2f})%".format(class2_name.capitalize(), main_category,
                                               class2_value, class2_value * 100))
        else:
            print("{} {}: {}".format(main_category, class1_name, class1_value))
            print("{} {}: {}".format(main_category, class2_name, class2_value))


if __name__ == '__main__':
    # Obtain file path containing results of prediction task from command line
    file_path = " ".join(argv[1:])
    # Compute metrics
    performance_evaluation = NaiveBayesPerformanceEvaluation(file_path)

