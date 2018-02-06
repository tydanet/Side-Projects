import numpy as np
import matplotlib.pyplot as plt

from pprint import pprint

class NeuralNet:
    def __init__(self, structure):
        ''' Creates NeuralNet object
            
            structure: Tuple containing integers denoting number of nodes in each layer
        '''

        self.structure = structure

        self.weights = [ np.random.uniform(size=(m, n)) for m, n in zip(structure[:-1], structure[1:]) ]
        self.biases = [ np.random.uniform(size=(n, 1)) for n in structure[1:] ]

    def sigmoid(self, t):
        return 1/(1+np.exp(-t))

    def sigPrime(self, t):
        return np.exp(-t)/(1+np.exp(-t))**2

    def feedForward(self, X):
        zs = []
        activations = [X]

        for i in range(len(self.weights)):
            z = np.dot(activations[-1], self.weights[i])# + self.biases[i]

            zs.append(z)
            activations.append(self.sigmoid(z))

        return zs, activations

    def predict(self, X):
        return self.feedForward(X)[1][-1][0]

    def backPropagate(self):
        pass


class NeuralNetTester:
    def __init__(self):
        np.random.seed(0)
        self.net = NeuralNet((1, 3, 1))

    def checkWeights(self):
        pprint(self.net.weights)

    def checkBiases(self):
        pprint(self.net.biases)

    def testSigmoid(self):
        xs = np.arange(-10, 10, 0.1)
        ys = self.net.sigmoid(xs)

        plt.plot(xs, ys)
        plt.show()

    def testSigPrime(self):
        xs = np.arange(-10, 10, 0.1)
        ys = self.net.sigPrime(xs)

        plt.plot(xs, ys)
        plt.show()

    def testFeedForward(self):
        zs, acts = self.net.feedForward([1])

        pprint(zs)
        pprint(acts)

    def testPredict(self):
        xs = np.arange(0, 2*np.pi, 0.1)
        ys = [ self.net.predict(x) for x in xs ]
        zs = np.sin(xs)
        
        plt.plot(xs, zs)
        plt.plot(xs, ys)
        plt.show()
    
nnt = NeuralNetTester()
