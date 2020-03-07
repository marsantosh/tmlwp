import io
import re
import email
import unittest
from bs4 import BeautifulSoup
from naive_bayes.email_object import EmailObject
'''
- Any method that is prefixed with test_ will be treated as a test to be run.
- setUp(self) is a special method that gets run before any test gets run. Think of
this like a block of code that gets run before all tests
'''
class TestPlaintextEmailObject(unittest.TestCase):
    CLRF = b'\\ n'
    def setUp(self):
        self.plain_file = './tests/fixtures/plain.eml'
        self.plaintext = io.open(self.plain_file, 'rb')
        self.text = self.plaintext.read()
        self.plaintext.seek(0)
        self.plain_email = EmailObject(self.plaintext)
        self.maxDiff = None
    
    def test_parse_plain_body(self):
        body = self.CLRF.join(self.text.split(self.CLRF)[:1])
        self.assertEqual(self.plain_email.body(), body)
    
    def test_parses_the_subject(self):
        subject = re.search('Subject: (.*)', str(self.text)).group(1)
        self.assertEqual(str(self.plain_email.subject()), subject)



class TestHTMLEmail(unittest.TestCase):
    def setUp(self):
        self.html_file = io.open('./tests/fixtures/html.eml', 'rb')
        self.html = self.html_file.read()
        self.html_file.seek(0)
        self.html_email = EmailObject(self.html_file)
        self.maxDiff = None
    
    def test_parses_stores_inner_text_html(self):
        body = b'\n\n'.join(self.html.split(b'\n\n')[1:])
        expected = BeautifulSoup(body, features = 'html.parser').text
        self.assertEqual(self.html_email.body(), expected)
    
    def test_stores_subject(self):
        subject = re.search('Subject: (.*)', str(self.html)).group(1)
        self.assertEqual(str(self.html_email.subject()), subject)


if __name__ == '__main__':
    unittest.main()