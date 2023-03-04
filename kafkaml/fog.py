# From https://github.com/ertis-research/kafka-ml/blob/4542ab5dab6e3d03706ac020aedf2bd9ee4bbec0/README.md?plain=1#L279

fog_input = keras.Input(shape=64, name='fog_input')
output_to_cloud = tf.keras.layers.Dense(64, activation=tf.nn.relu, name='output_to_cloud')(fog_input)
fog_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='fog_output')(output_to_cloud)
fog_model = keras.Model(inputs=[fog_input], outputs=[output_to_cloud, fog_output], name='fog_model')
