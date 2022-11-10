from testoracle_kg.Dto.parameter import buildParam
from testoracle_kg.Dto.parameter import AbstractParam
from testoracle_kg.Dto.keywords import ParamKey, DocKey
from testoracle_kg.Exception.exceptions import UnsupportedError
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

class Relationship:
    def __init__(self,operation1,operation2,relation):
        self.parabedepended = operation1
        self.paradepend = operation2
        self.relationship = relation

    @classmethod
    def _build_relation(cls):
        pass




