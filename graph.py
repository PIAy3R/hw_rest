from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import numpy as np
import os
from parseLogs import *
from Dto.graphdatatype import *

operationList = []

graph = Graph('bolt://localhost:7687/neo4j', auth=("pzy", "pzy123456"))
matcher = NodeMatcher(graph) #创建关系需要用到


parseTestCases()

#create operation
for cases in TestCases:
    if cases.operation not in operationList:
        operationList.append(cases.operation)
for operations in operationList:
    graph.create(Node('Operation', operation = operations))


for cases in TestCases:
    testnode = TestNodes(cases)
    if testnode.response_code != 404:
        operaNode = matcher.match('Operation', operation = testnode.operation).first()
        node = Node('TestCase', operation=testnode.operation, url=testnode.url, status_code=testnode.response_code, responsebody=testnode.response_body,judge=testnode.judge)
        graph.create(node)
        relation = Relationship(node, 'belongs to', operaNode)
        graph.create(relation)

def test():
    pass
