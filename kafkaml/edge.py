# From https://github.com/ertis-research/kafka-ml/blob/4542ab5dab6e3d03706ac020aedf2bd9ee4bbec0/README.md?plain=1#L279

edge_input = keras.Input(shape=(28,28,1), name='input_img')
x = tf.keras.layers.Conv2D(28, kernel_size=(3,3), name='conv2d')(edge_input)
x = tf.keras.layers.MaxPooling2D(pool_size=(2,2), name='maxpooling')(x)
x = tf.keras.layers.Flatten(name='flatten')(x)
output_to_fog = tf.keras.layers.Dense(64, activation=tf.nn.relu, name='output_to_fog')(x)
edge_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='edge_output')(output_to_fog)
edge_model = keras.Model(inputs=[edge_input], outputs=[output_to_fog, edge_output], name='edge_model')
