"""
Chapter 4. Naive Bayesian Classification
EmailObject class
"""
import email
import sys
from bs4 import BeautifulSoup


class EmailObject:
    def __init__(self, filepath, category = None):
        self.filepath = filepath
        self.category = category
        self.mail = email.message_from_file(self.filepath)
    
    def subject(self):
        return self.mail.get('Subject')
    
    def body(self):
        content_type = part.get_contenct_type()
        body = part.get_payload(decode = True)

        if content_type == 'text/html':
            return BeautifulSoup(body).text
        elif content_type == 'text/plain':
            return body
        else:
            return ''