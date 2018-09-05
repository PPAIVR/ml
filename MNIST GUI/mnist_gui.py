
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pylab as plt
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk


""" # Initialize weights

def init_weights(shape):
  init_random_dist = tf.truncated_normal(shape,stddev=0.1)
  return tf.Variable(init_random_dist)

# Initialize biases

def init_bias(shape):
  init_bias_vals = tf.constant(0.1, shape=shape)
  return tf.Variable(init_bias_vals)

# Convolutional 2D

def conv2d(x,W):
  # x = [batch, Height, Width,Color channels]
  # W = [filter height, filter width, color channels in, color channels out]
  
  return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

# Pooling layer

def max_pool_2by2(x):
  # x = [batch, Height, Width,Color channels]
  
  return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# Convolutional layer

def convolutional_layer(input_x,shape):
  W = init_weights(shape)
  b= init_bias([shape[3]])
  return tf.nn.relu(conv2d(input_x,W)+b)

# Normal layer

def normal_full_layer(input_layer,size):
  input_size = int(input_layer.get_shape()[1])
  W = init_weights([input_size,size])
  b = init_bias([size])
  return tf.matmul(input_layer,W) + b

init = tf.global_variables_initializer()
epochs = 5000


# Placeholders

x = tf.placeholder(tf.float32,shape=[None,784])
y_true = tf.placeholder(tf.float32,shape=[None,10])

# Layers
x_image = tf.reshape(x,[-1,28,28,1])

convo_1 = convolutional_layer(x_image,shape=[5,5,1,32])
convo_1_pooling = max_pool_2by2(convo_1)

convo_2 = convolutional_layer(convo_1_pooling,shape=[5,5,32,64])
convo_2_pooling = max_pool_2by2(convo_2)

convo_2_flat = tf.reshape(convo_2_pooling,[-1,7*7*64])
full_layer_one = tf.nn.relu(normal_full_layer(convo_2_flat,1024))

# Dropout
hold_probabilities = tf.placeholder(tf.float32)
full_one_dropout = tf.nn.dropout(full_layer_one,keep_prob=hold_probabilities)

y_pred = normal_full_layer(full_one_dropout,10)

# Loss function

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_true,logits=y_pred))

# Optimizer and trainer

optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
train = optimizer.minimize(cross_entropy)

init = tf.global_variables_initializer()

epochs = 300
accuracy_percent = 0 """

def trainGraph():
    """ with tf.Session() as sess:
        sess.run(init)

        for i in range(epochs):
            batch_x, batch_y = mnist.train.next_batch(50)
            
            sess.run(train, feed_dict={x: batch_x,y_true: batch_y, hold_probabilities: 0.5})

            if i % 100 == 0:
                print("On step: {}".format(i))

                matches = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_true, 1))
                accuracy = tf.reduce_mean(tf.cast(matches, tf.float32))

                accuracy_percent = sess.run(accuracy, feed_dict={x: mnist.test.images, y_true: mnist.test.labels, hold_probabilities: 1.0})
                accuracy_percent = accuracy_percent * 100
                accuracy_percent = math.floor(accuracy_percent)
                print(accuracy_percent)
            if i == epochs - 1:
                updateAcc(accuracy_percent) """

            

def runGraph():
 print("RUNNING GRAPH")
 i = np.random.randint(0, 5000)
 data = mnist.train.images[i].reshape(28, 28)
 showImage(data)


def hide_widget(e):
    e.widget.pack_forget()

def disable_widget(e):
    x.config(state="normal")


def showImage(image):
    fig = plt.figure(figsize=(5, 4))
    _ = plt.imshow(image, cmap='gray_r')
    plt.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=root)
    # Todo:
    canvas.get_tk_widget().delete('all')

    canvas.show()
    # Todo:
    canvas.get_tk_widget().place(anchor='ne')
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


def updateAcc(acc):
    text_label.set(str(acc)+"%")


root = tk.Tk()
root.wm_title("Train Ai")
frame = tk.Frame(root, width=420, height=200).pack()
text_label = tk.StringVar()
text_label.set("0%")
label = tk.Label(textvariable=text_label).pack()

btnTrain = tk.Button(text="Train AI", command=lambda: trainGraph()).pack()
btnRun = tk.Button(text="Run AI", command=lambda: runGraph()).pack()

root.mainloop()
