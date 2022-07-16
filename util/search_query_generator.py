import itertools
import pickle
from .document_parser import DocumentParser
from model import jd_vectorizer
from IPython.core.debugger import set_trace

class SearchQueryGenerator:
    def __init__(self, type, document_path, gender, location):
        self.type = type
        self.document_path = document_path
        self.document_parser = DocumentParser(document_path)
        self.gender = gender,
        self.location = location
        self.job_type_mapping = {'Accounting/Auditing': 1, 
                                 'Administrative': 2, 
                                 'Advertising': 3, 
                                 'Art/Creative': 4, 
                                 'Business Analyst': 5, 
                                 'Business Development': 6, 
                                 'Consulting': 7, 
                                 'Customer Service': 8, 
                                 'Data Analyst': 9, 
                                 'Design': 10, 
                                 'Distribution': 11, 
                                 'Education': 12, 
                                 'Engineering': 13, 
                                 'Finance': 14, 
                                 'Financial Analyst': 15, 
                                 'General Business': 16, 
                                 'Health Care Provider': 17, 
                                 'Human Resources': 18, 
                                 'Information Technology': 19, 
                                 'Legal': 20, 
                                 'Management': 21, 
                                 'Manufacturing': 22, 
                                 'Marketing': 23, 
                                 'Other': 24, 
                                 'Product Management': 25, 
                                 'Production': 26, 
                                 'Project Management': 27, 
                                 'Public Relations': 28, 
                                 'Purchasing': 29, 
                                 'Quality Assurance': 30, 
                                 'Research': 31, 
                                 'Sales': 32, 
                                 'Science': 33, 
                                 'Strategy/Planning': 34, 
                                 'Supply Chain': 35, 
                                 'Training': 36, 
                                 'Writing/Editing': 37}

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
        pickled_model = pickle.load(open('rfc_final.pkl', 'rb'))
        vectorized_document = jd_vectorizer.JDVectorizer.vectorize(open(self.document_path, "r"))
        result = pickled_model.predict(vectorized_document)
        self.type = list(self.job_type_mapping.keys())[list(self.job_type_mapping.values()).index(result[0])]
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