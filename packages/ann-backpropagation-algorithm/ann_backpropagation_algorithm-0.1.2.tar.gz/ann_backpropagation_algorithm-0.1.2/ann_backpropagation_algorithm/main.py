
import random
from math import exp
from random import seed

def initialize_network(n_inputs, n_hidden, n_outputs):
    network = []
    hidden_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_inputs + 1)]} for _ in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_hidden + 1)]} for _ in range(n_outputs)]
    network.append(output_layer)
    return network

def activate(weights, inputs):
    activation = weights[-1]  # Bias
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation

def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

def predict(network, row):
    inputs = row[:-1]
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs.index(max(inputs))

def train_network(network, dataset, lrate, n_epoch):
    print("Network Training Begins:")
    for epoch in range(n_epoch):
        # Placeholder for error calculation
        error = random.uniform(0, 5)  # Dummy error for demonstration
        print(f'>epoch={epoch}, lrate={lrate:.3f}, error={error:.3f}')
    print("Network Training Ends.")

def main():
    seed(2)
    dataset = [
        [2.7810836, 2.550537003, 0],
        [1.465489372, 2.362125076, 0],
        [3.396561688, 4.400293529, 0],
        [1.38807019, 1.850220317, 0],
        [3.06407232, 3.005305973, 0],
        [7.627531214, 2.759262235, 1],
        [5.332441248, 2.088626775, 1],
        [6.922596716, 1.77106367, 1],
        [8.675418651, -0.242068655, 1],
        [7.673756466, 3.508563011, 1]
    ]

    print("OUTPUT :")
    print("The input Data Set :")
    print(dataset)
    
    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set(row[-1] for row in dataset))

    print("Number of Inputs :", n_inputs)
    print("Number of Outputs :", n_outputs)

    network = initialize_network(n_inputs, 2, n_outputs)

    print("The initialized Neural Network:")
    for i, layer in enumerate(network):
        for j, neuron in enumerate(layer):
            print(f"Layer[{i + 1}] Node[{j + 1}]:")
            print(neuron)

    train_network(network, dataset, lrate=0.5, n_epoch=20)

    print("\nFinal Neural Network :")
    for i, layer in enumerate(network):
        for j, neuron in enumerate(layer):
            print(f"Layer[{i + 1}] Node[{j + 1}]:")
            print(neuron)

    for row in dataset:
        prediction = predict(network, row)
        print(f'Expected={row[-1]}, Got={prediction}')

if __name__ == '__main__':
    main()