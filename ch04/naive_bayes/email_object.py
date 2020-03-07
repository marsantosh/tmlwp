"""
Chapter 4. Naive Bayesian Classification
EmailObject class
"""
import email
import sys
from bs4 import BeautifulSoup


class EmailObject:
    
    CLRF = "\n\r\n\r"
    def __init__(self, filepath, category = None):
        self.filepath = filepath
        self.category = category
        self.mail = email.message_from_binary_file(self.filepath)
    
    def subject(self):
        return self.mail.get('Subject')
    
    def body(self):
        payload = self.mail.get_payload()
        if self.mail.is_multipart():
            parts = [self._single_body(part) for part in list(payload)]
        else:
            parts = [self._single_body(self.mail)]
        decoded_parts = []
        for part in parts:
            if len(part) == 0:
                continue
            if isinstance(part, bytes):
                decoded_parts.append(part.decode("utf-8", errors="ignore"))
            else:
                decoded_parts.append(part)
        return self.CLRF.join(decoded_parts)

    @staticmethod
    def _single_body(part):
        """
    Get text from part.
    :param part: email.Message
    :return: str body or empty str if body cannot be decoded
    """
        content_type = part.get_content_type()
        try:
            body = part.get_payload(decode=True)
        except Exception:
            return ""

        if content_type == "text/html":
            return BeautifulSoup(body, "html.parser").text
        elif content_type == "text/plain":
            return body
        return ""