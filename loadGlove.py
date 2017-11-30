import numpy as np
import pickle

def loadGloveModel(gloveFile):
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    pickle.dump(model, open( "word-to-vec.p", "wb" ))

path = "/glove.840B.300d.txt" # give path to the downloaded glove file
loadGloveModel(path)