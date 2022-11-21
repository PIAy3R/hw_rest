import json
import yaml
from pathlib import Path
from hw_rest.Dto.keywords import DocKey, ParamKey, DataType, Method
from hw_rest.Dto.operation import Operation
from hw_rest.Dto.parameter import buildParam, Example
from hw_rest.Dto.operation import Response
from hw_rest.Exception.exceptions import UnsupportedError
from hw_rest.Dto import restct
from hw_rest.Dto.restct import Config
import os


def CutOperation(Operation):
    loc = Operation.rindex('-')
    operation = Operation[:loc]
    return operation