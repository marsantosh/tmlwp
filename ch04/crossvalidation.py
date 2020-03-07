import io
import re
from naive_bayes.spam_trainer import SpamTrainer
from naive_bayes.email_object import EmailObject

print('Cross Validation')

correct = 0
false_positives = 0.0
false_negatives = 0.0
confidence = 0.0

def label_to_training_data(fold_file):
    training_data = []

    for line in io.open(fold_file, 'rb'):
        label_file = line.rstrip().split(b' ')
        training_data.append(label_file)
    
    return SpamTrainer(training_data)


def parse_emails(keyfile):
    emails = []
    print('parsing emails for ' + keyfile)

    for line in io.open(keyfile, 'rb'):
        label, file = line.rstrip().split(b' ')
        with io.open(file, 'rb') as f:
            emails.append(EmailObject(f, category = label))
        
    
    print('Done parsing files for ' + keyfile)
    return emails

def validate(trainer, set_of_emails):
    correct = 0
    false_positives = 0.0
    false_negatives = 0.0
    confidence = 0.0

    for email in set_of_emails:
        classification = trainer.classify(email)
        confidence += classification.score

        if classification.guess == 'spam' and email.category == 'ham':
            false_positives += 1
        elif classification.guess == 'ham' and email.category == 'spam':
            false_negatives += 1
        else:
            correct += 1
        
    total = false_positives + false_negatives + correct

    false_positive_rate = false_positives / total
    false_negative_rate = false_negatives / total

    accuracy = (correct) / total

    message = f'''
    False Positives: {false_positive_rate}
    False Negatives: {false_negative_rate}
    Accuracy: {accuracy}
    '''

    print(message)


trainer = label_to_training_data('tests/fixtures/fold1.label')
emails = parse_emails('tests/fixtures/fold2.label')

validate(trainer, emails)
