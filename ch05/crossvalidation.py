from pprint import pprint
from classifier import MushroomTree
from classifier import MushroomForest
from classifier import MushroomRegression
data = './input/agaricus-lepiota.data'
folds = 5

pprint('Calculating score for decision tree...')
tree = MushroomTree(data)
pprint(tree.validate(folds))

pprint('Calculating score for random forest method')
forest = MushroomForest(data)
pprint(forest.validate(folds))

pprint('Calculating score for regression tree')
regression = MushroomRegression(data)
pprint(regression.validate(folds))

