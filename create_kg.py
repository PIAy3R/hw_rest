from py2neo import Graph, Node
from py2neo.matching import *
import os
from testoracle_kg.Dto import restct
from utils import *

graph = Graph('bolt://localhost:7687/neo4j', auth=("pzy", "pzy123456"))
nodemacher = NodeMatcher(graph)
relationmacher = RelationshipMatcher(graph)

def getNodes():
    name = []
    nodes_in_graph = list(nodemacher.match('API'))
    for nodes in nodes_in_graph:
        namedict = dict(nodes)
        name.append(namedict.get('name'))
    return name

def createAPI():
    getFileLoc()
    for location in file_path:
        with open(location, encoding='utf-8') as a:
            spec = yaml.safe_load(location)
        apiname = getApiName(spec)
        if apiname not in apilist:
            graph.create(Node('API',name = apiname))

def createOperation():
    pass


createAPI()
createOperation()
