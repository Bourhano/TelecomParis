def BuildDecisionTree(path, minNum, default):
    df=pd.read_csv(path)
    df=df[:20]
    A=list(df.columns[:-1])
    classifier=df.columns[-1]
    D = df
    default = 0
    tree= createNode(D, A, "Root", 0, classifier, minNum, default)
    continueTree(tree)
    return tree

def printDecisionTree():
	pass

def generalizationError():
	pass

def pruneTree():
	pass