import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    'Evidence' will be structured as a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    'Labels' is the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

    with open(filename, newline='') as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        for row in data:
            line = []

            line.append(int(row['Administrative']))
            line.append(float(row['Administrative_Duration']))
            line.append(int(row['Informational']))
            line.append(float(row['Informational_Duration']))
            line.append(int(row['ProductRelated']))
            line.append(float(row['ProductRelated_Duration']))
            line.append(float(row['BounceRates']))
            line.append(float(row['ExitRates']))
            line.append(float(row['PageValues']))
            line.append(float(row['SpecialDay']))
            line.append(months[row['Month']])
            line.append(int(row['OperatingSystems']))
            line.append(int(row['Browser']))
            line.append(int(row['Region']))
            line.append(int(row['TrafficType']))
            line.append(1 if row['VisitorType'] == 'Returning_Visitor' else 0)
            line.append(1 if row['Weekend'] == 'TRUE' else 0)

            evidence.append(line)

            labels.append(1 if row['Revenue'] == 'TRUE' else 0)

        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, this function creates and returns a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    `sensitivity` is a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` is a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives = 0
    negatives = 0
    for label in labels:
        if label == 1:
            positives += 1
        elif label == 0:
            negatives += 1
    
    true_positive = 0
    true_negative = 0
    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                true_positive += 1
            elif predictions[i] == 0:
                true_negative += 1

    sensitivity = true_positive / positives
    specificity = true_negative / negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
