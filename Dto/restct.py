import argparse
import json
from argparse import Namespace
from pathlib import Path


class Config:
    # swagger file path
    swagger = "C:/Users/NaaRiAh/Desktop/specifications/GitLab_APIs"

    # operation sequence covering strength
    s_strength = 0

    # all parameter covering strength
    a_strength = 0

    # essential parameter covering strength
    e_strength = 0

    # maximum of op_cover_strength
    MAX_OP_COVER_STRENGTH = 5

    # minimum of op_cover_strength
    MIN_OP_COVER_STRENGTH = 1

    # maximum of param_cover_strength
    MAX_PARAM_COVER_STRENGTH = 5

    # minimum of param_cover_strength
    MIN_PARAM_COVER_STRENGTH = 1

    # output folder
    output_folder = ""

    # test budget (secs)
    budget = 0

    # constraint patterns for nlp recognition
    patterns = ""

    # acts jar file
    jar = ""

    # auth token
    header = dict()

    # auth token
    query = dict()

    # experiment unique name
    columnId = ""

    # data and log path
    dataPath = "D:/gitcode/sources/logs/Project-20221117143524777/Report/ErrorFuzzer"
