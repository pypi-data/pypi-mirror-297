import random
from math import exp
from random import seed

# Initialize the network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = []
    hidden_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_inputs + 1)]} for _ in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_hidden + 1)]} for _ in range(n_outputs)]
    network.append(output_layer)
    return network

# Activate neuron using weights and inputs
def activate(weights, inputs):
    activation = weights[-1]  # Bias
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation

# Sigmoid activation function
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

# Derivative of the transfer function (used in backpropagation)
def transfer_derivative(output):
    return output * (1.0 - output)

# Forward propagate input through the network
def forward_propagate(network, row):
    inputs = row[:-1]
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = []
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = sum([neuron['weights'][j] * neuron['delta'] for neuron in network[i + 1]])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update weights for the network
def update_weights(network, row, lrate):
    for i in range(len(network)):
        inputs = row[:-1] if i == 0 else [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += lrate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] += lrate * neuron['delta']

# Train the neural network
def train_network(network, dataset, lrate, n_epoch, n_outputs):
    print("\n The Network Training Begins...\n")
    for epoch in range(n_epoch):
        sum_error = 0
        for row in dataset:
            outputs = forward_propagate(network, row)
            expected = [0 for _ in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, lrate)
        print(f'>epoch={epoch}, lrate={lrate:.3f}, error={sum_error:.3f}')
    print("\n The Network Training Ends...\n")
    print("-----------------------------------------------------")

# Predict output for a given row
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

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
    print("\n The input Data Set :\n")
    print(dataset)

    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set(row[-1] for row in dataset))

    print("\n Number of Inputs :\n", n_inputs)
    print("\n Number of Outputs :\n", n_outputs)

    network = initialize_network(n_inputs, 2, n_outputs)

    print("\n The initialized Neural Network:\n")
    for i, layer in enumerate(network):
        for j, neuron in enumerate(layer):
            print(f"Layer[{i + 1}] Node[{j + 1}]:")
            print(neuron)

    train_network(network, dataset, lrate=0.5, n_epoch=20, n_outputs=n_outputs)

    print("\nFinal Neural Network:\n")
    for i, layer in enumerate(network):
        for j, neuron in enumerate(layer):
            print(f"Layer[{i + 1}] Node[{j + 1}]:")
            print(neuron)

    print("\nPredictions:\n")
    correct_predictions = 0
    for i, row in enumerate(dataset):
        prediction = predict(network, row)
        expected = row[-1]
        print(f' Expected={expected}, Got={prediction}')
        

if __name__ == '__main__':
    main()
