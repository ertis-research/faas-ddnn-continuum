edge_input = keras.Input(shape=(28,28,1), name='input_img')
x = tf.keras.layers.Flatten(name='flatten')(edge_input)
mid = tf.keras.layers.Dense(32, activation=tf.nn.relu, name='mid')(x)
output_to_cloud = tf.keras.layers.Dense(16, activation=tf.nn.relu, name='output_to_cloud')(mid)
edge_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='edge_output')(output_to_cloud)
edge_model = keras.Model(inputs=[edge_input], outputs=[output_to_cloud, edge_output], name='edge_model')
# {"data_type": "uint8", "label_type": "uint8", "data_reshape": "28 28", "label_reshape": "1"}
# kafka.kafka:9092
# kafkaml.inference.fog-input
# kafka.kafka:9092
# kafkaml.inference.fog-output
# 192.168.43.7:32001
# kafkaml.inference.input-cloud
# https://192.168.48.206:6443
# 0.5