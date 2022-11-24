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


class TestLog:

    def __init__(self, method, path, statuscode, paramslist):
        self.method = method
        self.path = path
        self.statuscode = statuscode
        self.paramslist = paramslist

    @classmethod
    def buildtestlog(cls, responseJson):
        method = responseJson.get('method')
        path = responseJson.get('path')
        statuscode = responseJson.get('status')
        paramslist = responseJson.get('params')
        return cls(method, path, statuscode, paramslist)

    def __repr__(self):
        return self.method + ' http://localhost:3000' + self.path

class ErrorLog:
    def __init__(self, exceptionmessage,exceptionbacktrace):
        self.exceptionmessage = exceptionmessage
        self.exceptionbacktrace = exceptionbacktrace

    @classmethod
    def builderrorlog(cls, log):
        exceptionmessage = log.get('exception.message')
        exceptionbacktrace = log.get('exception.backtrace')
        return cls(exceptionmessage,exceptionbacktrace)