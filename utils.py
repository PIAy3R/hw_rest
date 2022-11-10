import json
import yaml
from pathlib import Path
from testoracle_kg.Dto.keywords import DocKey, ParamKey, DataType, Method
from testoracle_kg.Dto.operation import Operation
from testoracle_kg.Dto.parameter import buildParam, Example
from testoracle_kg.Dto.operation import Response
from testoracle_kg.Exception.exceptions import UnsupportedError
from testoracle_kg.Dto import restct
from testoracle_kg.Dto.restct import Config
import os

URL_PREFIX = ""
DEFINITIONS = dict()
file_path = []





def parse(location:str):
    with open(location, encoding='utf-8') as a:
        spec = yaml.safe_load(a)

    # get url prefix for all resources' url in paths
    global URL_PREFIX
    URL_PREFIX = _compile_url(spec)

    # get definitions
    global DEFINITIONS
    DEFINITIONS = spec.get(DocKey.DEFINITIONS, {})

    #get the API the yaml file belongs to
    apiName = getApiName(spec)

    #parse paths
    paths = spec.get(DocKey.PATHS, {})
    # if len(paths) > 0:
    #     parse_paths(paths)

    # parse dependency
    _show_dependency(DEFINITIONS)





def getFileLoc():
    swagger = Config.swagger
    for file_name in os.listdir(swagger):
        fileLocation = swagger + '/' + file_name
        file_path.append(fileLocation)



def getApiName(swagger:dict):
    info = swagger.get('info')
    Apiname = info.get('title')
    return Apiname


def _compile_url(spec: dict):
    """
    get url prefix, e.g. http://localhost:30000/v4/api
    :param spec: swagger dict
    :return: url prefix
    """
    protocol = spec.get(DocKey.SCHEMES, ["http"])[0]
    baseurl = spec.get(DocKey.BASEPATH, "")
    host = spec.get(DocKey.HOST, "")

    return "{}://{}/{}".format(protocol, host.strip("/"), baseurl.strip("/"))



def parse_paths(paths:dict):
    for url_str, url_info in paths.items():
        extraParamList = url_info.get(DocKey.PARAMS, list())
        for method_name, method_info in url_info.items():
            if method_name not in [m.value for m in Method]:
                continue
            operation = Operation(URL_PREFIX.rstrip("/") + "/" + url_str.lstrip("/"), method_name)
            # process parameters
            paramList = method_info.get(DocKey.PARAMS, [])
            paramList.extend(extraParamList)
            for param_info in paramList:
                operation.addParam(buildParam(param_info, DEFINITIONS))
                if DocKey.EXAMPLE in param_info.keys():
                    example = Example(param_info.get(ParamKey.NAME), param_info.get(DocKey.EXAMPLE))
                    example.operation = operation
                    Example.members.add(example)

            # process responses
            for status_code, response_info in method_info.get(DocKey.RESPONSES, {}).items():
                operation.addResponse(Response.buildResponse(status_code, response_info, DEFINITIONS, operation))
            print(operation)
            for i in operation.responseList:
                print(i.expected_status_code)



def _show_dependency(definetion:dict):
    print(definetion)

