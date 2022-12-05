from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import numpy as np
import os
from parseLogs import *
from Dto.graphdatatype import *
from tqdm import tqdm


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
    for cases in tqdm(TestCases, ncols=80):
        testnode = TestNodes.build(cases)
        operaNode = matcher.match('Operation', operation=testnode.operation).first()
        if testnode.response_code >= 200 and testnode.response_code < 400:
            node = Node('SuccessTestCase', operation=testnode.operation, url=testnode.url, status_code=testnode.response_code,
                    responsebody=testnode.response_body, judge=testnode.judge, tags=testnode.tags)
        else:
            node = Node('FailTestCase', operation=testnode.operation, url=testnode.url, status_code=testnode.response_code,
                    responsebody=testnode.response_body, judge=testnode.judge, tags=testnode.tags)
        graph.create(node)


        if testnode.response_code >= 200 and testnode.response_code < 400 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal success case', operaNode)
            graph.create(relation)


        if testnode.response_code >= 400 and testnode.response_code < 500 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal bad request', operaNode)
            graph.create(relation)


        if testnode.response_code == 500 and 'mutated' not in testnode.tags:
            relation = Relationship(node, 'nominal server error case', operaNode)
            graph.create(relation)

        if testnode.response_code >= 200 and testnode.response_code < 400 and 'mutated' in testnode.tags:
            relation = Relationship(node, 'error fail case', operaNode)
            graph.create(relation)

        if testnode.response_code >= 400 and testnode.response_code < 500 and 'mutated' in testnode.tags:
            relation = Relationship(node, 'error pass case', operaNode)
            graph.create(relation)

        if testnode.response_code == 500 and 'mutated' in testnode.tags:
            relation = Relationship(node, 'error server error case', operaNode)
            graph.create(relation)




if __name__ == '__main__':
    testcases = parseTestCases()
    createOpera(testcases)
    createTestcase(testcases)