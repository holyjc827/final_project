import util
from IPython.core.debugger import set_trace

class App:
    def __init__(self, type, document_path):
        self.type = type
        self.document_path = document_path

    def execute(self):
        c = util.SearchQueryGenerator(self.type, self.document_path).classify()
        print(c)


if __name__ == '__main__':
    application = App("developer","data/backend.txt")
    application.execute()