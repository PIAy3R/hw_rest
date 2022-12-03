from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import numpy as np
import os
from parseLogs import *
from Dto.graphdatatype import *


graph = Graph('bolt://localhost:7687/neo4j', auth=("pzy", "pzy123456"))
matcher = NodeMatcher(graph)

#create operation
def createOpera(TestCases:list):
    operationList = []
    for cases in TestCases:
        if cases.operation not in operationList:
            operationList.append(cases.operation)
    for operations in operationList:
        graph.create(Node('Operation', operation=operations))



def createTestcase(TestCases:list):
    for cases in TestCases:
        testnode = TestNodes.build(cases)
        operaNode = matcher.match('Operation', operation=testnode.operation).first()
        node = Node('TestCase', operation=testnode.operation, url=testnode.url, status_code=testnode.response_code,
                    responsebody=testnode.response_body, judge=testnode.judge)
        graph.create(node)


        if testnode.response_code >= 200 and testnode.response_code < 400 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal success case', operaNode)
            graph.create(relation)


        if testnode.response_code >= 400 and testnode.response_code < 500 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal bad request', operaNode)
            graph.create(relation)


        if testnode.response_code == 500 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal bad request', operaNode)
            graph.create(relation)

        if testnode.response_code >= 200 and testnode.response_code < 400 and 'mutated' in testnode.tags:
            relation = Relationship(node, 'nominal success case', operaNode)
            graph.create(relation)





if __name__ == '__main__':
    testcases = parseTestCases()
    createOpera(testcases)
    createTestcase(testcases)