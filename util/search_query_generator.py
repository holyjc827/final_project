import itertools
import pickle
from .document_parser import DocumentParser
from util import jd_vectorizer, constant
from IPython.core.debugger import set_trace

class SearchQueryGenerator:
    def __init__(self, type, document_path, gender, location):
        self.type = type
        self.document_path = document_path
        self.document_parser = DocumentParser(document_path)
        self.gender = gender,
        self.location = location

    def generate_search_query(self):
        if self.type is None:
            self.__classify()

        for key, value in constant.JOB_MAPPING.items():
            if self.type in value:
                job_group = key
        print(f"The job group is classified as {job_group}")
        
        match job_group:
            case 'Science':
                return self.__generate_search_query_for_science(job_group)
            case 'Service':
                return self.__generate_search_query_for_service(job_group)
            case 'Creative':
                return self.__generate_search_query_for_creative(job_group)
            case 'Strategic':
                return self.__generate_search_query_for_strategic(job_group)
            case 'Legal':
                return self.__generate_search_query_for_legal(job_group)
            case 'Finance':
                return self.__generate_search_query_for_finance(job_group)
            case 'Manufacturing':
                return self.__generate_search_query_for_manufacturing(job_group)
            case 'Other':
                return self.__generate_search_query_for_other(job_group)
    # Private methods 

    def __classify(self):
        pickled_model = pickle.load(open('rfc_final.pkl', 'rb'))
        vectorized_document = jd_vectorizer.vectorize(open(self.document_path, "r"))
        result = pickled_model.predict(vectorized_document)
        
        self.type = list(constant.JOB_TYPE_MAPPING.keys())[list(constant.JOB_TYPE_MAPPING.values()).index(result[0])]

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
        repeated_keywords = [k for k, v in dict(itertools.islice(token_dict.items(), 20)).items()]
        return repeated_keywords
    
    def __generate_search_query_with_most_relevant_keywords(self, job_group):
        tokens = self.document_parser.tokenize()
        relevant_keywords = []
        seniority = []
        developer_classification = []
        for token in tokens:
            keyword = token.lower()
            if keyword in constant.SENIORITY:
                seniority.append(token)
            if job_group == "Science":
                if keyword in constant.SCIENCE_HARD_SKILL:
                    relevant_keywords.append(token)
                if keyword in constant.DEVELOPER_CLASSIFICATION:
                    developer_classification.append(token)
        seniority = " AND ".join(list(set(seniority))) if len(seniority) > 0 else "any experience level"
        query = " AND ".join(list(set(relevant_keywords)))
        developer_query = " OR ".join(list(set(developer_classification)))
        return f"(({query}) AND ({seniority}) AND ({developer_query}))"

    def __generate_search_query_with_most_repeated_keywords(self):
        most_repeated_keywords = self.__get_most_repeated_keywords()
        query_string = ""
        for word in most_repeated_keywords:
            if len(query_string) == 0:
                query_string += word
            else:
                query_string += ' AND ' + word
        return query_string

    def __get_basis_search_query_string(self):
        gender = "(male OR female)"
        location = "(Anywhere OR Remote)"
        job = "(job OR occupation OR internship)"
        degree = "(bachelor OR masters)"
        platform = "(Linkedin OR Glassdoor OR Indeed OR Monster OR Google)"
        query = " AND ".join([gender, location, job, degree, platform])
        return f"({query})"

    def __generate_search_query_for_science(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        science = "(science OR technology)"
        query = " AND ".join([basis, repeated, relevant, science])
        return query 
    
    def __generate_search_query_for_service(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        service = "(client OR customer OR service)"        
        query = " AND ".join([basis, repeated, relevant, service])
        return query

    def __generate_search_query_for_creative(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        creative = "(advertising OR creative OR design OR marketing OR ads)"        
        query = " AND ".join([basis, repeated, relevant, service])
        return query

    def __generate_search_query_for_strategic(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        strategic = "(business OR analysis OR analyst OR management OR manage OR strategic OR strategy OR supply)"        
        query = " AND ".join([basis, repeated, relevant, strategic])
        return query

    def __generate_search_query_for_legal(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        legal = "(legal OR law OR lawyer OR litigation OR regulation)"        
        query = " AND ".join([basis, repeated, relevant, legal])
        return query

    def __generate_search_query_for_finance(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        finance = "(capital OR finance OR money OR bank OR accounting)"        
        query = " AND ".join([basis, repeated, relevant, finance])
        return query

    def __generate_search_query_for_manufacture(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        manufacture = "(produce OR manufacture OR manufacturing OR quality)"        
        query = " AND ".join([basis, repeated, relevant, manufacture])
        return query

    def __generate_search_query_for_other(self, job_group):
        basis = self.__get_basis_search_query_string()
        repeated = self.__generate_search_query_with_most_repeated_keywords()
        relevant = self.__generate_search_query_with_most_relevant_keywords(job_group)
        query = " AND ".join([basis, repeated, relevant])
        return query