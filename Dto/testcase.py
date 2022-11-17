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

class Testcase:
    def __init__(self):
        pass