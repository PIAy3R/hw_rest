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


class caseLog:

    def __init__(self):
        pass

    @classmethod
    def buildLogCase(cls):
        pass