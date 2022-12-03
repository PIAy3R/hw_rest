# -*- coding: utf-8 -*-
# @Author  : Lixin
# @Time    : 2022/11/30 21:16
# @Function: transfer test case and test order to neo4j
from pathlib import Path
from py2neo import Graph
from tqdm import tqdm
import jsonlines
import json


class Transfer:
    def __init__(self, model: str, test_suite: str):
        """
        :param model: model.jsonl
        :param test_suite: 文件夹，读取其中的test_order文件和test_case文件
        """
        self._model_file = model
        self._test_suite = test_suite

        self._operations = list()
        self._test_seqs = list()
        self._test_requests = dict()
        self._read_model()

        self.graph = Graph('bolt://localhost:7687/neo4j', auth=("pzy", "pzy123456"))

        # 知识图谱实体
        # the list of attributes, e.g., {"id" = id, "name" = name}
        # the set of names, e.g., resource_name, its id is the same as name when create the node in the graph
        self.resources = list()
        self.manipulations = list()
        self.method_types = set()
        self.parameters = list()  # todo: 将不同参数类型的参数区分开
        self.response_template = list()
        self.locations = set()
        self.defaults = set()
        self.enums = set()
        self.param_type = set()
        # 测试用例相关实体
        self.test_cases = set()
        self.requests = list()
        self.assignments = list()
        self.values = list()
        self.response = list()

        # 知识图谱关系
        # the list of (head_id, tail_id)
        self.hasManipulation = list()  # 资源 -> 操作
        self.hasMethod = list()  # 操作 -> method
        self.hasParameter = list()  # 操作 -> 参数
        self.hasResponseTemplate = list()  # 操作 -> response 模板
        self.hasProperty = list()  # object参数 -> 属性参数
        self.hasItem = list()  # array参数 -> item参数
        self.hasEnum = list()  # 参数 -> Enum
        self.hasDefault = list()  # 参数 -> default
        self.isLocatedIn = list()  # 参数 -> location
        self.isTypeOf = list()  # 参数 -> param_type
        self.isFormatOf = list()  # 参数 -> param_format
        self.hasExpectedReturn = list()  # response_template -> template参数
        # 测试用例相关关系
        self.hasSuccessFollow = list()  # request -> request
        self.hasFailedFollow = list()  # request -> request
        self.hasBugFollow = list()  # request -> request
        self.isComposedOf = list()  # test_case -> request
        self.isImplementedOf = list()  # manipulation -> request
        self.hasAssignment = list()  # request -> assignment
        self.hasResponse = list()  # request -> response
        self.isAssignedTo = list()  # assignment -> parameters
        self.hasItemValue = list()  # array value -> item value
        self.hasPropertyValue = list()  # object value -> property value
        self.hasValue = list()  # -> basic type value: integer, string, etc.

    def _read_model(self):
        """
        read all data with respect to kg
        :return:
        """
        with jsonlines.open(self._model_file) as reader:
            for obj in reader:
                self._operations.append(obj)
        for file in Path(self._test_suite).iterdir():
            if file.is_file():
                if "_case" in file.with_suffix("").name:
                    with file.open("r") as fp:
                        self._test_requests.update(json.load(fp))
                elif "_order" in file.with_suffix("").name:
                    with file.open("r") as fp:
                        for line in fp.readlines():
                            elements = [e.strip("\n").strip() for e in line.split("***")]
                            seq = list()
                            req = list()
                            for index in range(len(elements)):
                                req.append(elements[index])
                                if index % 3 == 2:
                                    seq.append(req)
                                    req = list()
                            self._test_seqs.append(seq)

    def extract_test(self):
        """
        extract entities and relations from test suites
        :return: nothing
        """
        for seq in self._test_seqs:
            tc_id = self._get_id(["tc", seq[0][0], seq[0][1], seq[0][2]])
            self.test_cases.add(tc_id)
            pre_success_id = None
            for r_index, req in enumerate(seq):
                # entities
                req_id = self._get_id(req)
                op_id = self._get_id([req[0], req[1]])
                req_str = "***".join(req)
                req_json = self._test_requests[req_str]
                status_code = str(req_json.get("status_code"))

                attributes = dict()
                attributes["id"] = req_id
                attributes["statusCode"] = status_code
                if attributes not in self.requests:
                    self.requests.append(attributes)
                    self.isImplementedOf.append(tuple([op_id, req_id]))

                if r_index == 0 or pre_success_id is None:
                    self.isComposedOf.append(tuple([tc_id, req_id]))
                    if 200 <= int(status_code) < 300:
                        pre_success_id = req_id
                else:
                    if 200 <= int(status_code) < 300:
                        self.hasSuccessFollow.append(tuple([pre_success_id, req_id]))
                        pre_success_id = req_id
                    elif 500 <= int(status_code) < 600:
                        self.hasBugFollow.append(tuple([pre_success_id, req_id]))
                    else:
                        self.hasFailedFollow.append(tuple([pre_success_id, req_id]))

                a_ids = self._extract_test_assignment(op_id, req_id, req_json.get("assignment", {}))
                for a_id in a_ids:
                    self.hasAssignment.append(tuple([req_id, a_id]))
                r_id = self._extract_test_response(req_id, status_code, req_json.get("response", {}))
                self.hasResponse.append(tuple([req_id, r_id]))

    def _extract_test_assignment(self, op_id: str, req_id: str, assignment: dict):
        """
        :param op_id: the id of the manipulation
        :param req_id: the id of the test request
        :param assignment: the json data of the test request assignment
        :return:
        """
        a_ids = list()
        for loc, p_json in assignment.items():
            if loc == "url":
                continue
            for p_name, p_value in p_json.items():
                attributes = dict()
                a_id = self._get_id([req_id, p_name])
                p_id = self._get_id([op_id, p_name])
                # if p_id not in self.parameters:
                #     raise ValueError("Parameter Entity '{}' does not exist")
                self.isAssignedTo.append(tuple([a_id, p_id]))
                a_ids.append(a_id)
                attributes["id"] = a_id
                attributes["name"] = p_name
                attributes["loc"] = loc
                self.assignments.append(attributes)
                if isinstance(p_value, list):
                    for item_id in self._process_value(a_id, p_value):
                        self.hasItemValue.append(tuple([a_id, item_id]))
                elif isinstance(p_value, dict):
                    for prop_id in self._process_value(a_id, p_value):
                        self.hasPropertyValue.append(tuple([a_id, prop_id]))
                else:
                    self.hasValue.append(tuple([a_id, self._process_value(a_id, p_value)]))

        return a_ids

    def _process_value(self, prefix_id, value):
        if isinstance(value, list):
            v_id = self._get_id([prefix_id, "list"])
            self.values.append({"id": v_id})
            for index, item in enumerate(value):
                item_id = self._process_value(v_id, item)
                item_index_id = self._get_id([v_id, str(index)])
                self.values.append({"id": item_index_id, "serial_number": index, "type": "item"})
                self.hasItemValue.append(tuple([v_id, item_index_id]))
                if not isinstance(item_id, list):
                    self.hasValue.append(tuple([item_index_id, item_id]))
                else:
                    for id_ in item_id:
                        self.hasValue.append(tuple([item_index_id, id_]))
            return v_id
        elif isinstance(value, dict):
            v_id = self._get_id([prefix_id, "dict"])
            self.values.append({"id": v_id, "type": "dict"})
            p_ids = list()
            for d_k, d_v in value.items():
                d_id = self._get_id([v_id, d_k])
                p_ids.append(d_id)
                self.values.append({"id": d_id, "name": d_k, "type": "property"})
                self.hasPropertyValue.append(tuple([v_id, d_id]))
                self.hasValue.append(tuple([d_id, self._process_value(d_id, d_v)]))
            return v_id
        else:
            if value not in self.values:  # todo: 效率低，使用图查询
                self.values.append(value)
            return value

    def _extract_test_response(self, req_id, status_code, response):
        r_id = self._get_id([req_id, status_code])
        attributes = {"id": r_id, "statusCode": status_code}
        self.response.append(attributes)
        if isinstance(response, list) and len(response) > 0:
            for item_id in self._process_value(r_id, response):
                self.hasItemValue.append(tuple([r_id, item_id]))
        elif isinstance(response, dict):
            for prop_id in self._process_value(r_id, response):
                self.hasPropertyValue.append(tuple([r_id, prop_id]))
        else:
            self.hasValue.append(tuple([r_id, self._process_value(r_id, response)]))
        return r_id

    def extract_model(self):
        """
        extract entities and relations from the specification
        :return: nothing
        """
        for operation in self._operations:
            url = operation.get("url")
            method = operation.get("method")
            description = operation.get("description")
            description_id = self._get_id([url, method])
            self.resources.append({"id": url, "name": url})
            self.manipulations.append({"id": description_id, "description": description})
            self.method_types.add(method)
            self.hasManipulation.append(tuple([url, description_id]))
            self.hasMethod.append(tuple([description_id, method]))

            op_id = self._get_id([url, method])

            for parameter in operation.get("parameters"):
                p_id = self._extract_model_parameter(op_id, parameter)
                self.hasParameter.append(tuple([description_id, p_id]))

            for response in operation.get("responses"):
                r_id = self._extract_model_response(op_id, response)
                self.hasResponseTemplate.append(tuple([description_id, r_id]))

    def _extract_model_response(self, op_id, response: dict):
        """
        属性：statusCode
        实体：template
        """
        attributes = dict()
        status_code = response.pop("statusCode")
        attributes["statusCode"] = status_code
        r_id = self._get_id([op_id, status_code])
        attributes["id"] = r_id
        attributes["name"] = status_code
        self.response_template.append(attributes)
        # template 是 parameter 实体
        template = response.pop("template")
        if len(template.keys()) > 0:
            if template["name"] == "":
                template["name"] = "template"
            t_id = self._extract_model_parameter(r_id, template, False)
            self.hasExpectedReturn.append(tuple([r_id, t_id]))

        # check whether we ignored some properties
        assert len(response.keys()) == 0
        return r_id

    def _extract_model_parameter(self, op_id, parameter: dict, hasLoc: bool = True):
        """
        special情况：item, properties
        type实体：paramType, paramFormat
        location实体：loc
        value实体：enum, default
        属性：maxItems，name, description, isConstrained, exclusiveMaximum, minimum, required, minLength, maxLength, minItems, maximum, exclusiveMinimum, unique

        :param hasLoc: response的template也是参数，但是没有loc信息
        """
        attributes = dict()
        attributes["name"] = parameter.pop("name")
        attributes["description"] = parameter.pop("description")
        attributes["isConstrained"] = parameter.pop("isConstrained")
        attributes["required"] = parameter.pop("required")

        if "maxItems" in parameter.keys():
            attributes["maxItems"] = parameter.pop("maxItems")
        if "exclusiveMaximum" in parameter.keys():
            attributes["exclusiveMaximum"] = parameter.pop("exclusiveMaximum")
        if "exclusiveMinimum" in parameter.keys():
            attributes["exclusiveMinimum"] = parameter.pop("exclusiveMinimum")
        if "minimum" in parameter.keys():
            attributes["minimum"] = parameter.pop("minimum")
        if "maximum" in parameter.keys():
            attributes["maximum"] = parameter.pop("maximum")
        if "minLength" in parameter.keys():
            attributes["minLength"] = parameter.pop("minLength")
        if "maxLength" in parameter.keys():
            attributes["maxLength"] = parameter.pop("maxLength")
        if "minItems" in parameter.keys():
            attributes["minItems"] = parameter.pop("minItems")
        if "unique" in parameter.keys():
            attributes["unique"] = parameter.pop("unique")

        p_id = self._get_id([op_id, attributes["name"]])
        attributes["id"] = p_id
        self.parameters.append(attributes)

        # value实体处理
        if "enum" in parameter.keys():
            for value in parameter.pop("enum"):
                self.enums.add(value)
                self.hasEnum.append(tuple([p_id, value]))
        if "default" in parameter.keys():
            default = parameter.pop("default")
            if isinstance(default, list):
                for value in default:
                    self.defaults.add(value)
                    self.hasDefault.append(tuple([p_id, value]))
            else:
                self.defaults.add(default)
                self.hasDefault.append(tuple([p_id, default]))

        # loc实体处理
        location = parameter.pop("loc")
        if hasLoc and location != "NONE":
            self.locations.add(location)
            self.isLocatedIn.append(tuple([p_id, location]))

        # type实体处理
        p_type = parameter.pop("paramType")
        self.param_type.add(p_type)
        self.isTypeOf.append(tuple([p_id, p_type]))

        if "paramFormat" in parameter.keys():
            p_format = parameter.pop("paramFormat")
            if p_format != "NONE":
                self.param_type.add(p_format)
                self.isFormatOf.append(tuple([p_id, p_format]))

        # item实体处理
        if "item" in parameter.keys():
            item = parameter.pop("item")
            item_id = self._extract_model_parameter(self._get_id([op_id, p_id]), item)
            self.hasItem.append(tuple([p_id, item_id]))

        # properties实体处理
        if "properties" in parameter.keys():
            properties = parameter.pop("properties")
            for prop_p in properties.values():
                prop_p_id = self._extract_model_parameter(self._get_id([op_id, p_id]), prop_p)
                self.hasProperty.append(tuple([p_id, prop_p_id]))
        # check whether we ignored some keywords
        # assert len(parameter.keys()) == 0
        return p_id

    def _write_node(self, entities, entity_type):
        """
        create node in the graph
        :param entities: the list of entities, in the format of {"id": id, "name": name, ...}
        :param entity_type: the string representation of the entity type
        :return: nothing
        """
        if isinstance(entity_type, (tuple, list)):
            entity_type = ":".join(entity_type)
        print("写入 {0} 实体".format(entity_type))
        for node in tqdm(entities, ncols=80):
            if not isinstance(node, dict):
                node = {"id": str(node), "name": str(node)}
            cql = """MERGE(n:{label}{{{attributes}}})""".format(  # todo: bool 类型 v
                label=entity_type, attributes=", ".join([k.replace("'", "") + ":\'" + str(v).replace("'", "") + "\'" for k, v in node.items()]))

            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def _write_edge(self, tuples, head_type, tail_type, relation):
        """
        insert edge into the graph
        :param tuples: the tuples of [head_id, tail_id]
        :param head_type: corresponding to the entity container name, the type of the element of self.resource is "resource"
        :param tail_type: is set like head_type
        :param relation: corresponding to the relation container name, the type of the relation of self.hasParameter is "hasParameter"
        :return: nothing
        """
        print("写入 {0} 关系".format(relation))
        for head, tail in tqdm(tuples, ncols=80):
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                            WHERE p.id='{head}' AND q.id='{tail}'
                            MERGE (p)-[r:{relation}]->(q)""".format(
                head_type=head_type, tail_type=tail_type, head=head.replace("'", "") if isinstance(head, str) else head,
                tail=tail.replace("'", "") if isinstance(tail, str) else tail, relation=relation)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    @staticmethod
    def _get_id(info: list):
        """
        所有实体的id规则如下：
        url: url
        method: [method, method]
        description of method (manipulation): [url, method]
        parameter: [url, method, param_name]
        property of object parameter: [url, method, obj_name, prop_name]
        item of array parameter: [url, method, array_name, item_name]. item_name = "item" if item_name is None or item_name == ""
        response template: [url, method, status code]
        the template of response: [url, method, status code, template name]. template_name = "template" if template_name is None or template_name == ""
        test case: ["tc", url, method, num]
        request: [url, method, num]
        :param info:
        :return: id string
        """
        return "_".join(info)

    def create_nodes(self):
        """
        batch import entity nodes
        :return: nothing
        """
        self._write_node(self.resources, Entity.resource)
        self._write_node(self.manipulations, Entity.manipulation)
        self._write_node(self.method_types, Entity.method_type)
        self._write_node(self.parameters, Entity.parameter)
        self._write_node(self.response_template, Entity.response_template)
        self._write_node(self.locations, Entity.location)
        self._write_node(self.defaults, [Entity.value_template, Entity.default])
        self._write_node(self.enums, [Entity.value_template, Entity.enum])
        self._write_node(self.param_type, Entity.param_type)

        # 测试相关
        self._write_node(self.test_cases, Entity.test_case)
        self._write_node(self.requests, Entity.request)
        self._write_node(self.assignments, [Entity.assignment, Entity.value])
        self._write_node(self.values, Entity.value)
        self._write_node(self.response, Entity.response)

    def create_edges(self):
        """
        batch import the edge of relation
        :return: nothing
        """
        self._write_edge(self.hasManipulation, Entity.resource, Entity.manipulation, Relation.has_manipulation)
        self._write_edge(self.hasMethod, Entity.manipulation, Entity.method_type, Relation.has_method)
        self._write_edge(self.hasParameter, Entity.manipulation, Entity.parameter, Relation.has_parameter)
        self._write_edge(self.hasResponseTemplate, Entity.manipulation, Entity.response_template,
                         Relation.has_response_temp)
        self._write_edge(self.hasProperty, Entity.parameter, Entity.parameter, Relation.has_property)
        self._write_edge(self.hasItem, Entity.parameter, Entity.parameter, Relation.has_item)
        self._write_edge(self.hasEnum, Entity.parameter, Entity.enum, Relation.has_enum)
        self._write_edge(self.hasDefault, Entity.parameter, Entity.default, Relation.has_default)
        self._write_edge(self.isLocatedIn, Entity.parameter, Entity.location, Relation.is_located_in)
        self._write_edge(self.isTypeOf, Entity.parameter, Entity.param_type, Relation.is_type_of)
        self._write_edge(self.isFormatOf, Entity.parameter, Entity.param_type, Relation.is_format_of)
        self._write_edge(self.hasExpectedReturn, Entity.response_template, Entity.parameter,
                         Relation.has_expected_return)

        # 测试相关
        self._write_edge(self.hasSuccessFollow, Entity.request, Entity.request, Relation.has_success_follow)
        self._write_edge(self.hasFailedFollow, Entity.request, Entity.request, Relation.has_failed_follow)
        self._write_edge(self.hasBugFollow, Entity.request, Entity.request, Relation.has_bug_follow)
        self._write_edge(self.isComposedOf, Entity.test_case, Entity.request, Relation.is_composed_of)
        self._write_edge(self.isImplementedOf, Entity.manipulation, Entity.request, Relation.is_implemented_of)
        self._write_edge(self.hasAssignment, Entity.request, Entity.assignment, Relation.has_assignment)
        self._write_edge(self.hasResponse, Entity.request, Entity.response, Relation.has_response)
        self._write_edge(self.isAssignedTo, Entity.assignment, Entity.parameter, Relation.is_assigned_to)
        self._write_edge(self.hasItemValue, Entity.value, Entity.value, Relation.has_item_value)
        self._write_edge(self.hasPropertyValue, Entity.value, Entity.value, Relation.has_property_value)
        self._write_edge(self.hasValue, Entity.value, Entity.value, Relation.has_value)


class Entity:
    resource = "resource"
    manipulation = "manipulation"
    method_type = "method"
    parameter = "parameter"
    response_template = "responseTemplate"
    location = "location"
    value_template = "valueTemplate"
    default = "default"
    enum = "enum"
    param_type = "paramType"

    # 测试相关
    test_case = "testCase"
    request = "request"
    assignment = "assignment"
    value = "value"
    response = "response"


class Relation:
    has_manipulation = "hasManipulation"
    has_method = "hasMethod"
    has_parameter = "hasParameter"
    has_response_temp = "hasResponseTemplate"
    has_property = "hasProperty"
    has_item = "hasItem"
    has_enum = "hasEnum"
    has_default = "hasDefault"
    is_located_in = "isLocatedIn"
    is_type_of = "isTypeOf"
    is_format_of = "isFormatOf"
    has_expected_return = "hasExpectedReturn"

    # 测试相关
    has_success_follow = "hasSuccessFollow"
    has_failed_follow = "hasFailedFollow"
    has_bug_follow = "hasBugFollow"
    is_composed_of = "isComposedOf"
    is_implemented_of = "isImplementedOf"
    has_assignment = "hasAssignment"
    has_response = "hasResponse"
    is_assigned_to = "isAssignedTo"
    has_item_value = "hasItemValue"
    has_property_value = "hasPropertyValue"
    has_value = "hasValue"


if __name__ == "__main__":
    transfer = Transfer(model="D:/gitcode/sources/RestCTKG/model.jsonl",
                        test_suite="D:/gitcode/sources/RestCTKG/testSuites")
    transfer.extract_model()
    transfer.extract_test()
    transfer.create_nodes()
    transfer.create_edges()
