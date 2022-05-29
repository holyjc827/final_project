from nltk.corpus import stopwords

class DocumentParser:
    def __init__(self, document_path):
        self.document_path = document_path

    def tokenize(self):
        tokens = []

        with open(self.document_path, "r") as document:
            lines = document.read().split(".")
            for line in lines:
                line = line.replace("\n", " ")
                words = line.split(" ")
                tokens.append(words)
        
        return self.__remove_empty_and_stopwords(tokens)

    # private methods
    def __remove_empty_and_stopwords(self, tokens):
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

        return [word for word in sum(tokens,[]) if word and (word.lower() not in stopwords_list)] # flatten the arrays and remove empty strings