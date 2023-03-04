# From https://github.com/ertis-research/kafka-ml/blob/4542ab5dab6e3d03706ac020aedf2bd9ee4bbec0/README.md?plain=1#L279

cloud_input = keras.Input(shape=64, name='cloud_input')
x = tf.keras.layers.Dense(64, activation=tf.nn.relu, name='relu1')(cloud_input)
x = tf.keras.layers.Dense(128, activation=tf.nn.relu, name='relu2')(x)
x = tf.keras.layers.Dropout(0.2)(x)
cloud_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='cloud_output')(x)
cloud_model = keras.Model(inputs=cloud_input, outputs=[cloud_output], name='cloud_model')