import tensorflow as tf
from numpy.random import RandomState


batch_size = 8

# 两个输入节点
x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
# 一个输出节点（回归问题一般只有一个输出节点）
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

# 定义一个单层神经网络前向传播的过程（这里就是简单的加权）
w1 = tf.Variable(tf.random_normal([2, 1], stddev=1, seed=1))
y = tf.matmul(x, w1)

# 定义预测多了和预测少了的成本(自定义损失函数)
loss_less = 10
loss_more = 1
loss = tf.reduce_sum(tf.where(tf.greater(y, y_), (y - y_) * loss_more, (y_ - y) * loss_less))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

# 通过随机数生成一个模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
Y = [[x1 + x2 + rdm.rand()/10.0 - 0.05] for (x1, x2) in X]

# 训练神经网络
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    STEPS = 5000
    for i in range(STEPS):
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size, dataset_size)
        sess.run(train_step, feed_dict={x: X[start: end], y_: Y[start: end]})
        print(sess.run(w1))

# batch_size = n
#
# # 每次读取一小部分数据作为当前的训练数据来执行反向传播
# x = tf.placeholder(tf.float32, shape=(batch_size, 2), name='x-input')
# y_ = tf.placeholder(tf.float32, shape=(batch_size, 1), name='y-input')
#
# # 定义神经网络结构和优化算法
# loss = …
# train_step = tf.train.AdamOptimizer(0.001).minimize(loss)
#
# # 训练神经网络
# with tf.Session() as sess:
#     # 参数初始化
#     …
#     # 迭代的更新参数
#     for i in range(STEPS):
#         # 准备batch_size个训练数据，一般将所有数据随机打乱后在选取可以得到更好的优化效果
#         current_X, current_Y = …
#         sess.run(train_step, feed_dict={x: current_X, y_: current_Y})