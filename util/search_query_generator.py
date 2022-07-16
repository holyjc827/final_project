import itertools
from .document_parser import DocumentParser

class SearchQueryGenerator:
    def __init__(self, type, document_path, gender, location):
        self.type = type
        self.document_parser = DocumentParser(document_path)
        self.gender = gender,
        self.location = location

    def generate_search_query(self):
        if self.type is None:
            self.__classify()

        match self.type:
            case 'developer':
                return self.__generate_search_query()
            case _:
                return

    # Private methods 

    def __classify(self): # TODO: classify the document with machine learning algo
        self.type = "developer"
        print(f"The job type is classified as {self.type}")

    def __get_most_repeated_keywords(self):
        tokens = self.document_parser.tokenize()
        token_dict = {}
        repeated_keywords = []
        for token in tokens:
            if token_dict.get(token) != None:
                value = token_dict.get(token)
                token_dict.update({token: value+1})
            else:
                token_dict.setdefault(token, 1)
        
        token_dict = dict(sorted(token_dict.items(), key=lambda item: item[1], reverse=True))
        repeated_keywords = [k for k, v in dict(itertools.islice(token_dict.items(), 5)).items()]
        return repeated_keywords
    
    def __generate_search_query(self):
        most_repeated_keywords = self.__get_most_repeated_keywords()
        query_string = ""
        for word in most_repeated_keywords:
            if len(query_string) == 0:
                query_string = '"' + word + '"'
            else:
                query_string += ' AND ' + '"' + word + '"'
        return query_string