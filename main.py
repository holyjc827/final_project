import util
from IPython.core.debugger import set_trace

class App:
    def configure(self):
        document_path = input("Please provide the location of the job description. Only txt file will be accepted. ")
        preference = input("Do you want to configure some special parameters? (y/n) ")

        if preference == "y":
            job_type, gender, location = self.__check_preference()
            self.execute(document_path, job_type, gender, location)
        else:
            self.execute(document_path=document_path)

    def execute(self, document_path=None, type=None, gender=None, location=None):
        search_query_generator = util.SearchQueryGenerator(type, document_path, gender, location)
        search_query = search_query_generator.generate_search_query()
        print(search_query)

    # Private methods 
    
    def __check_preference(self):
        job_type = input("Please provide the job type (developer, sales, marketing, other) ")
        gender = input("Are you looking for a male or female candidate? (male, female, none) ")
        location = input("Do you need your candidate to be in a specific area? If yes, then please provide a city name. Otherwise, press enter. ")        
        return job_type, gender, location

if __name__ == '__main__':
    application = App()
    application.configure()