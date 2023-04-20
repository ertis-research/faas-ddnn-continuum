cloud_input = keras.Input(shape=16, name='cloud_input')
cloud_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='cloud_output')(cloud_input)
cloud_model = keras.Model(inputs=cloud_input, outputs=[cloud_output], name='cloud_model')
