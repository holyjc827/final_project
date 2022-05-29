import itertools

class SearchQueryGenerator:
    def __init__(self, type, document):
        self.type = type
        self.document = document

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

    def __tokenize(self):
        sentences = self.document.split(".")
        tokens = []
        for sentence in sentences:
            words = sentence.split(" ")
            tokens.append(words)
        cleaned_tokens = [word for word in sum(tokens,[]) if word]
        return cleaned_tokens
    
    def __get_most_repeated_keywords(self):
        tokens = self.__tokenize()
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

app = SearchQueryGenerator("job", "to me you are beautiful. I hope you are doing well.")
print(app.generate_search_query())