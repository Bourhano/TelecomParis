import numpy as np
import pandas as pd
import decision_functions

def main():
    alpha=0.5; minNum = 5; dataPath = 'data.csv'; defaultClassifierValue=1;
    
    tree = BuildDecisionTree(dataPath, minNum, defaultClassifierValue)
    
    printDecisionTree(tree)
    
    error = generalizationError(tree, alpha)
    print("The generalization error is",error)
    
    prunedTree = pruneTree(mytree, classifier, alpha)
    errorPruned=generalizationError(prunedTree, alpha)
    print("The generalization error of the pruned tree is",errorPruned,end="\n\n")
    printDecisionTree(prunedTree)