from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import numpy as np
import os
from parseLogs import *
from Dto.graphdatatype import *


graph = Graph('bolt://localhost:7687/neo4j', auth=("pzy", "pzy123456"))
matcher = NodeMatcher(graph) #创建关系需要用到

#create operation
def createOpera():
    operationList = []
    for cases in TestCases:
        if cases.operation not in operationList:
            operationList.append(cases.operation)
    for operations in operationList:
        graph.create(Node('Operation', operation = operations))



def createTestcase():
    for cases in TestCases:
        testnode = TestNodes.build(cases)
        if testnode.response_code >= 200 and testnode.response_code < 400 and 'mutated' not in testnode.tags:
            operaNode = matcher.match('Operation', operation = testnode.operation).first()
            node = Node('TestCase', operation=testnode.operation, url=testnode.url, status_code=testnode.response_code, responsebody=testnode.response_body,judge=testnode.judge)
            graph.create(node)
            relation = Relationship(node, 'success case', operaNode)
            graph.create(relation)

def test():
    pass


if __name__ == '__main__':
    parseTestCases()
    createOpera()
    createTestcase()