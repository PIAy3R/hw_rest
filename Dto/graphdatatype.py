from hw_rest.Exception import exceptions
from hw_rest.parseLogs import *
from hw_rest.Dto.testcase import *



class Strategy:
    pass


class TestNodes:
    def __init__(self,operation, tags, url, response_code, response_body, judge):
        self.operation = operation
        self.tags = tags
        self.url = url
        self.response_code = response_code
        self.response_body = response_body
        self.judge = judge


    @classmethod
    def build(cls, testcase: Testcase):
        operation = testcase.operation
        tags = testcase.tags
        url = testcase.url
        response_code = testcase.response_code
        response_body = testcase.response_body
        judge = testcase.judge

        return cls(operation, tags, url, response_code, response_body, judge)