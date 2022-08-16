import util
from IPython.core.debugger import set_trace

class App:
    def configure(self):
        document_path = input("Please provide the location of the job description. Only txt file will be accepted. ")
        preference = input("Do you want to configure some special parameters? (y/n) ")

        if preference == "y":
            job_type, job, gender, location, seniority = self.__check_preference()
            params = self.__build_params_dict(job_type, job, gender, location, degree, seniority)            
            self.execute(document_path, params)
        elif preference == "n":
            params = self.__build_params_dict()
            self.execute(document_path, params)
        else:
            print("Wrong input was given. Terminating the application.")

    def execute(self, params, document_path=None):        
        search_query_generator = util.SearchQueryGenerator(document_path, params)
        search_query = search_query_generator.generate_search_query()
        print(search_query)

    # Private methods 
    
    def __build_params_dict(self, type=None, job=None, gender=None, location=None, degree=None, seniority=None):
        return {
            "gender": gender,
            "location": location,
            "job_type": type,
            "job" : job,
            "seniority": seniority,
            "degree": degree
        }

    def __check_preference(self):
        job_type = input("Please provide the job type (developer, sales, marketing, other) ")
        gender = input("Are you looking for a male or female candidate? (male, female, none) ")
        location = input("Do you need your candidate to be in a specific area? If yes, then please provide a city name. Otherwise, press enter. ")
        seniority = input("Define the skill level of the candidate, such as junior or senior ")
        job = input("Is it a full time job or part time or internship?")
        degree = input("Please define the required education level, such as bachelor or masters")

        return job_type, job, gender, location, seniority, degree

if __name__ == '__main__':
    application = App()
    application.configure()