fog_input = keras.Input(shape=32, name='fog_input')
output_to_cloud = tf.keras.layers.Dense(16, activation=tf.nn.relu, name='output_to_cloud')(fog_input)
fog_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='fog_output')(output_to_cloud)
fog_model = keras.Model(inputs=[fog_input], outputs=[output_to_cloud, fog_output], name='fog_model')