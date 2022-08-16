import util
from IPython.core.debugger import set_trace

class App:
    def configure(self):
        document_path = input("Please provide the location of the job description. Only txt file will be accepted. ")
        preference = input("Do you want to configure some special parameters? (y/n) ")

        if preference == "y":
            job_type, job, gender, location, degree, seniority = self.__check_preference()
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
        job_type = self.__validate_job_type(input("Please provide the job type [Business, Creative, Finance, Science/Engineering, Service, Other] "))
        gender = self.__validate_gender(input("Are you looking for a male or female candidate? [male, female, both, none] "))
        location = input("Do you need your candidate to be in a specific area? If yes, then please provide a city name. Otherwise, press enter. ")
        seniority = self.__validate_seniority(input("Define the skill level of the candidate [junior, medior, intermediate, senior, internship, experienced] "))
        job = self.__validate_job(input("Is it a full time job or part time? [full time, part time] "))
        degree = input("Please define the required education level, such as bachelor or masters ")

        return job_type, job, gender, location, seniority, degree

    def __validate_gender(self, gender):
        if gender not in util.constant.GENDER:
            print("Wrong gender is given. Please provide one in male, female, both, none")
            raise
        else:
            return gender.lower()

    def __validate_job_type(self, job_type):
        if job_type not in util.constant.JOB_TYPE:
            print("Wrong job type is given. Please provide one in Business, Creative, Finance, Science/Engineering, Service, Other. It is case-sensitive")
            raise
        else:
            return job_type

    def __validate_job(self, job):
        if job not in util.constant.JOB:
            print("Wrong job level is given. Please provide one in full time, part time")
            raise
        else:
            return job.lower()

    def __validate_seniority(self, seniority):
        if seniority not in util.constant.SENIORITY:
            print("Wrong seniority is given. Please provide one in junior, medior, intermediate, senior, internship, experienced")
            raise
        else:
            return seniority.lower()

if __name__ == '__main__':
    application = App()
    application.configure()