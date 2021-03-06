import tensorflow as tf
import numpy as np
#tf.set_random_seed(777)

sample = "Why are you act like this"
idx2char = list(set(sample))
char2idx = {c : i  for i, c in enumerate(idx2char)}
#print(char2idx)
#print(idx2char)


################## Hyper parameters ################
dim_size = len(char2idx)        #input_size
hidden_size = len(char2idx)     #output_size
num_classes = len(char2idx)     #final output_size after RNN or softmax
batch_size = 1                 #one sample data, one batch
sequence_length = len(sample) - 1
learning_rate = 0.1

sample_idx = [char2idx[i] for i in sample]
print(sample_idx)
x_data = [sample_idx[:-1]]
y_data = [sample_idx[1:]]

x = tf.placeholder(tf.int32, [None, sequence_length])
y = tf.placeholder(tf.int32, [None, sequence_length])

x_one_hot = tf.one_hot(x, num_classes)
cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_size, state_is_tuple=True)
initial_state = cell.zero_state(batch_size, tf.float32)
outputs, _states = tf.nn.dynamic_rnn(
    cell, x_one_hot, initial_state = initial_state, dtype=tf.float32)

############# Fully connected Layer ####################

x_for_fc = tf.reshape(outputs, [-1, hidden_size])
outputs = tf.contrib.layers.fully_connected(x_for_fc, num_classes, activation_fn=None)

outputs = tf.reshape(outputs, [batch_size, sequence_length, num_classes])

weights = tf.ones([batch_size, sequence_length])
sequence_loss = tf.contrib.seq2seq.sequence_loss(
    logits=outputs, targets=y, weights=weights)
loss =tf.reduce_mean(sequence_loss)
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

prediction = tf.argmax(outputs, axis=2)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(30):
        l, _ = sess.run([loss, train], feed_dict={x:x_data, y:y_data})
        result = sess.run(prediction, feed_dict={x:x_data})

        result_str = [idx2char[i] for i in np.squeeze(result)]
        print(i, "loss:", l, "Prediction:", ''.join(result_str))
