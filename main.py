import itertools
from document_parser import DocumentParser
from IPython.core.debugger import set_trace

class SearchQueryGenerator:
    def __init__(self, type, document_path):
        self.type = type
        self.document_path = document_path

    def generate_search_query(self):
        most_repeated_keywords = self.__get_most_repeated_keywords()
        query_string = ""
        for word in most_repeated_keywords:
            if len(query_string) == 0:
                query_string = '"' + word + '"'
            else:
                query_string += ' AND ' + '"' + word + '"'
        return query_string

    # Private methods 

    def __get_most_repeated_keywords(self):
        tokens = DocumentParser.tokenize(self.document_path)
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

if __name__ == '__main__':
    app = SearchQueryGenerator("job", "data/backend.txt")
    print(app.generate_search_query())