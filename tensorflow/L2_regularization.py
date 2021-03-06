"""
This is an example of L2 regularization. It prints out the final cost of 
100 different regularization rates evenly spaced between 0 and 1.  
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import math

result = []

learning_rate = 0.001
training_epochs = 1000
reg_lambda = 0.  # Regularization rate
x_dataset = np.linspace(-1, 1, 100)
num_coeffs = 9
y_dataset_params = [0.] * num_coeffs
y_dataset_params[2] = 1
y_dataset = 0
for i in range(num_coeffs):
    y_dataset += y_dataset_params[i] * np.power(x_dataset, i)
y_dataset += np.random.randn(*x_dataset.shape) * 0.3


def split_dataset(x_dataset, y_dataset, ratio):
    arr = np.arange(x_dataset.size)
    np.random.shuffle(arr)
    num_train = int(ratio * x_dataset.size)
    x_train = x_dataset[arr[0:num_train]]
    x_test = x_dataset[arr[num_train:x_dataset.size]]
    y_train = y_dataset[arr[0:num_train]]
    y_test = y_dataset[arr[num_train:x_dataset.size]]
    return x_train, x_test, y_train, y_test


(x_train, x_test, y_train, y_test) = split_dataset(x_dataset, y_dataset, 0.7)
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)


def model(X, w):
    terms = []
    for i in range(num_coeffs):
        term = tf.multiply(w[i], tf.pow(X, i))
        terms.append(term)
    return tf.add_n(terms)


w = tf.Variable([0.] * num_coeffs, name="parameters")
y_model = model(X, w)
# Regularlized cost function:
# cost = (|(predicted - correct)^2| + reg_lambda * |w^2|) / 2 * x_train.size
cost = tf.div(tf.add(tf.reduce_sum(tf.square(Y-y_model)),
                     tf.multiply(reg_lambda, tf.reduce_sum(tf.square(w)))),
              2*x_train.size)
train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
for reg_lambda in np.linspace(0, 1, 100):
    for epoch in range(training_epochs):
        sess.run(train_op, feed_dict={X: x_train, Y: y_train})

    final_cost = sess.run(cost, feed_dict={X: x_test, Y: y_test})
    print('reg lambda', reg_lambda)
    print('final cost', final_cost)
    w_val = sess.run(w)
    result.append({
        'cost': final_cost,
        'w': w_val
    })

sess.close()

lowest_cost = {'cost': math.inf}
for x in result:
    if x['cost'] < lowest_cost['cost']:
        lowest_cost = x

print('Training is finished, lowest cost =', lowest_cost['cost'])
print(lowest_cost)
print(lowest_cost['w'][0])
print(type(lowest_cost['w']))

predY = 0
for i in range(num_coeffs):
    predY += lowest_cost['w'][i] * np.power(x_dataset, i)

plt.scatter(x_test, y_test)
plt.plot(x_dataset, predY)
plt.show()
