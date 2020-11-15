try:
	from decision_functions import BuildDecisionTree
	t=BuildDecisionTree('data.csv', 5, 1)
	print('BuildDeciosionTree loaded!')
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import printDecisionTree
	printDecisionTree(t)
	print('printDecisionTree loaded!')
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import generalizationError
	e=generalizationError(t)
	print('generalizationError loaded!', e)
	print('----')
except Exception as e:
	raise e

try:
	from decision_functions import pruneTree
	p=pruneTree(t)
	print('pruneTree loaded!')
	print('----')
except Exception as e:
	raise e