from hw_rest.Exception import exceptions
from hw_rest.parseLogs import *
from hw_rest.Dto.testcase import *

class TestNodes:
    def __init__(self,testcase:Testcase):
        self.operation = testcase.operation
        self.tags = testcase.tags
        self.url = testcase.url
        self.response_code = testcase.response_code
        self.response_body = testcase.response_body
        self.judge = testcase.judge

    #
    # @classmethod
    # def build(cls, Operation, testInteractions, testResults):
    #     testcase = Testcase.buildCase(Operation, testInteractions, testResults)
    #     return cls(testcase)