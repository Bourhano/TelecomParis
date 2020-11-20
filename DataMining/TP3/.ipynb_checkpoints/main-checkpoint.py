import decision_functions as d

def main():
    alpha=0.5; minNum = 5; dataPath = 'data.csv'; defaultClassifierValue=1;
    
    tree = d.BuildDecisionTree(dataPath, minNum, defaultClassifierValue)
    
    d.printDecisionTree(tree)
    
    error = d.generalizationError(tree, alpha)
    print("The generalization error is",error)
    
    prunedTree = d.pruneTree(tree, alpha)
    errorPruned = d.generalizationError(prunedTree, alpha)
    print("The generalization error of the pruned tree is",errorPruned,end="\n\n")
    d.printDecisionTree(prunedTree)