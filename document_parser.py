import nltk
from nltk.corpus import stopwords
from IPython.core.debugger import set_trace


class DocumentParser:
    def __init__(self, document_path):
        self.document_path = document_path

    @staticmethod
    def tokenize(document_path):
        tokens = []

        retries = 3
        for i in range(retries):
            try:
                stopwords_list = stopwords.words('english')
            except LookupError:
                retries -= 1
                print("Stopwords will be downloaded.")
                nltk.download('stopwords')
                continue
            break

        with open(document_path, "r") as document:
            lines = document.read().split(".")
            for line in lines:
                line = line.replace("\n", " ")
                words = line.split(" ")
                tokens.append(words)
        
        cleaned_tokens = [word for word in sum(tokens,[]) if word and (word.lower() not in stopwords_list)] # flatten the arrays and remove empty strings
        return cleaned_tokens
        