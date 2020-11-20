def BuildDecisionTree(path, minNum, default):
    import numpy as np
    import pandas as pd
    df=pd.read_csv(path)
    df=df[:20]
    A=list(df.columns[:-1])
    classifier=df.columns[-1]
    D = df
    default = 0
    tree= createNode(D, A, "Root", 0, classifier, minNum, default)
    continueTree(tree)
    return tree

def printDecisionTree(tree):
    printNode(tree)
    print()
    nodesByLevel= getTreeOrdered(tree)
    for level in nodesByLevel[1:]:
        if level == []:
            continue
        i=0
        for node in level:
            i+=1
            printNode(node)
            if (i != len(level)):
                print('*********')
        print()

def generalizationError(tree, alpha):
    nodesByLevel= getTreeOrdered(tree)
    complexity=0
    mistakes=0
    for level in nodesByLevel[1:]:
        for node in level:
            if(node["type"]=="Leaf"):
                complexity+=1
                vals=node["tree"].T
                for row in node["tree"].T:
                    test = sum(node["tree"][node["classifier"]])/len(node["tree"]) > 0.5
                    cl = 1 if test else 0
                    if (len(node["tree"])<node["min"]): cl = node["default"]
                    if(vals[row][node["classifier"]]!=cl):
                        mistakes+=1
    error = mistakes + alpha * complexity
    return error/len(tree["tree"])
    #return error, mistakes, complexity

def pruneTree(root, classifier, alpha):
    import copy
    root = copy.deepcopy(root)
    nodesByLevel=getTreeOrdered(root)
    levels= getLevels(root)[-1]
    for level in range(levels,0,-1):
        nodesByLevel[level].reverse()
        nodes = nodesByLevel[level]
        for node in nodes:
            if node["type"] != "Leaf":
                ierror=generalizationError(root,alpha)
                left, right = pruneNode(node)
                error=generalizationError(root,alpha)
                if(error > ierror):
                    restoreNode(node, left, right)
    return root

def GINI(data, classifier):
    """returns the Gini of the given node, based on the Class"""
    classVals=getVals(data,classifier)
    cl=data[classifier]
    sqSum = 0
    for val in classVals:
        prob= len(cl[cl==val])/len(data)
        sqSum += prob**2
    GINI= 1-sqSum
    return GINI

def getVals(df, attribute):
    """returns the DISTINCT values of a specified attribute from a dataset"""
    vals = []
    for val in list(df[attribute]):
        if val not in vals:
            vals += [val]
    vals.sort()
    return vals

def split(data, attribute, value):
    """returns two nodes based on a given split (attribute < value), input is a dataframe"""
    yes = data[data[attribute] < value]
    no = data[data[attribute] >= value]
    return yes,no

def GINIsplit(data, attribute, value, classifier):
    """returns the Gini of the split if applied on the given attribute with the specified classifier, input is a dataframe"""
    [yes,no]=split(data, attribute, value)
    gini = (GINI(yes,classifier)*len(yes)+GINI(no, classifier)*len(no))/len(data)
    return gini

def bestCandidate(data, attributes, classifier):
    ginis={}
    for att in attributes:
        vals = getVals(data, att)
        for val in vals[1:]:
            ginis[(att ,val)]=GINIsplit(data, att, val, classifier)
    best = min(ginis, key=ginis.get)
    return best

def allEqual(D, A):
    for att in A:
        iterator = D[att]
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        answer = all(first == rest for rest in iterator)
        if answer == False:
            return answer
    return True

def printNode(node):
    nType = node["type"]
    nLevel= node["level"]
    nGini =node["gini"]
    print(nType)
    print("Level",nLevel)
    if nType in ("Root","Intermediate"):
        feature = node["feature"]
        print("Feature",feature[0],end=" ")
        for i in range(min(getVals(node["tree"],feature[0])),feature[1]):
            if (i != feature[1] - 1):
                print(i, end = " ")
            else:
                print(i, end = "")
        print()
    else:
        test = sum(node["tree"][node["classifier"]])/len(node["tree"]) > 0.5
        cl = 1 if test else 0
        if (len(node["tree"])<node["min"]): cl = node["default"]
        print("Class",cl)
    if(nGini!=0):
        print("Gini","{:.4}".format(nGini))
    else:
        print("Gini",0)

def getNextLevel(tree, result):
    if 'left' in tree.keys():
        result[tree['level']+1]= result[tree['level']+1] + [tree['left']]
        result[tree['level']+1]= result[tree['level']+1] + [tree['right']]
        getNextLevel(tree['left'],result)
        getNextLevel(tree['right'],result)
        
def getTreeOrdered(tree):
    nodesByLevel=[[]]*len(tree["tree"].columns)*4 #recently edited!!!
    nodesByLevel[0] = [tree]
    getNextLevel(tree, nodesByLevel)
    nodesByLevel = list(filter(None, nodesByLevel))
    return nodesByLevel

def getLevels(tree):
    nodesByLevel= getTreeOrdered(tree)
    levels =[0]
    for a in nodesByLevel:
        for val in a:
            level= val["level"]
            if level not in levels:
                levels += [level]
    return levels

def pruneNode(node):
    left=node.pop("left")
    right=node.pop("right")
    node["type"]="Leaf"
    return left,right

def restoreNode(node, left,right):
    node["left"]=left
    node["right"]=right
    node["type"]="Intermediate"
    
def createNode(D, A, nodeType, level, classifier, minNum=5, default = 1):
    node = {}
    node["tree"] = D
    node["attributes"] = A
    node["type"] = nodeType
    node["level"] = level
    node["classifier"] = classifier
    node["min"]=minNum
    node["default"]=default
    node["gini"]=float(GINI(D,classifier))
    return node

def continueTree(root):
    A = list(root["attributes"])
    D = root["tree"]
    classifier = root["classifier"]
    sameAttributes = allEqual(D, A)
    if len(D)<=root["min"] or root["gini"]==0 or sameAttributes:
        root["type"]= "Leaf"
    elif root["type"] != "Leaf":
        root["feature"]= [attribute, value] = bestCandidate(D, A, classifier)
        left,right = split(D, attribute, value)
        root["left"]  = createNode(left , A, "Intermediate", root["level"]+1, classifier, minNum, default)
        root["right"] = createNode(right, A, "Intermediate", root["level"]+1, classifier, minNum, default)
        continueTree(root["left"])
        continueTree(root["right"])
