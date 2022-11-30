from hw_rest.Dto.parameter import buildParam
from hw_rest.Dto.parameter import AbstractParam
from hw_rest.Dto.keywords import ParamKey, DocKey, Logs
from hw_rest.Exception.exceptions import UnsupportedError
from hw_rest.utils import *
import json
import re
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Set
from hw_rest.Dto.parameter import AbstractParam, EnumParam
from enum import Enum

class Testcase:
    def __init__(self, Operation, Tags, Url, Response_code, Response_body, Judge, Message):
        self.operation = Operation
        self.tags = Tags
        self.url = Url
        self.response_code = Response_code
        self.response_body = Response_body
        self.judge = Judge
        self.message = Message

    @classmethod
    def buildCase(cls, Operation, testInteractions, testResults):

        operation = CutOperation(Operation)
        tags = testInteractions.get(Logs.TAGS)
        Url = testInteractions.get(Logs.REQUESTURL)
        Response_code = testInteractions.get(Logs.RESPONSESTATUSCODE).get(Logs.CODE)
        Response_body = testInteractions.get(Logs.RESPONSEBODY)

        if ParamKey.STRATEGY in tags:
            Judge = testResults.get(Logs.ERRORSTATUSCO).get(Logs.RESULT)
            Message = testResults.get(Logs.ERRORSTATUSCO).get(Logs.MESSAGES)
        else:
            Judge = testResults.get(Logs.STATUSCO).get(Logs.RESULT)
            Message = testResults.get(Logs.STATUSCO).get(Logs.MESSAGES)



        return cls(operation, tags, Url, Response_code, Response_body, Judge, Message)

    def showSelf(self):
        print(self.operation)
        print(self.url)
        print(self.response_code)
        print(self.judge)
        print(self.tags)
        print(self.message)


