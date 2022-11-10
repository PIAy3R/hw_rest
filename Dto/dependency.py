from testoracle_kg.Dto.parameter import buildParam
from testoracle_kg.Dto.parameter import AbstractParam
from testoracle_kg.Dto.keywords import ParamKey, DocKey
from testoracle_kg.Exception.exceptions import UnsupportedError
from testoracle_kg.Dto.operation import *
import json
import re
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Set
from testoracle_kg.Dto.parameter import AbstractParam, EnumParam
from enum import Enum

class Dependency:
    def __init__(self):
        self.operationList: List[Operation] = list()
        self.dependency = ''

    def addOperation(self,opera1: Operation):
        self.operationList.append(opera1)

    def defDependency(self,dependency:str):
        self.dependency = dependency


    def test(self):
        pass


