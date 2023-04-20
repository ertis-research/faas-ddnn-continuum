# {"data_type": "uint8", "label_type": "uint8", "data_reshape": "28 28", "label_reshape": "1"}
# kafka-0.kafka-headless.kafka.svc.cluster.local:9092,kafka-1.kafka-headless.kafka.svc.cluster.local:9092
# 192.168.48.206:32001

cloud_input = keras.Input(shape=16, name='cloud_input')
cloud_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='cloud_output')(cloud_input)
cloud_model = keras.Model(inputs=cloud_input, outputs=[cloud_output], name='cloud_model')


