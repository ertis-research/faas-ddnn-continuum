import tensorflow as tf
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt

tf.keras.backend.clear_session()

# (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0

# input_shape = x_train[0].shape

image_index = 6995

def edge():
    edge_input = keras.Input(shape=10, name='input_img')

    x = tf.keras.layers.Dense(10, name='conv2d')(edge_input)
    x = tf.keras.layers.Dense(10, name='maxpooling')(x)
    x = tf.keras.layers.Dense(10,name='flatten')(x)

    output_to_fog = tf.keras.layers.Dense(10, activation=tf.nn.relu, name='output_to_fog')(x)
    edge_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='edge_output')(output_to_fog)

    edge_model = keras.Model(inputs=[edge_input], outputs=[output_to_fog, edge_output], name='edge_model')
    edge_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    edge_model.save("tensorflow/out/edge.h5")
    # edge_prediction = edge_model.predict(x_test[image_index].reshape(1, 28, 28, 1))
    # print("\nDISTRIBUTED PREDICTIONS BEFORE TRAINING")
    # print("Edge Output to Fog: ", edge_prediction[0].shape)
    # print("Edge prediction: ", edge_prediction[1].argmax())

def fog():
    fog_input = keras.Input(shape=10, name='fog_input')
    
    output_to_cloud = tf.keras.layers.Dense(10, activation=tf.nn.relu, name='output_to_cloud')(fog_input)
    fog_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='fog_output')(output_to_cloud)
    
    fog_model = keras.Model(inputs=[fog_input], outputs=[output_to_cloud, fog_output], name='fog_model')

    fog_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    fog_model.save("tensorflow/out/fog.h5")
    
    # fog_prediction = fog_model.predict(edge_prediction[0])
    # print("Fog Output to Cloud: ", fog_prediction[0].shape)
    # print("Fog prediction: ", fog_prediction[1].argmax())
    # 

def cloud():
    cloud_input = keras.Input(shape=10, name='cloud_input')
    
    x = tf.keras.layers.Dense(10, activation=tf.nn.relu, name='relu1')(cloud_input)
    x = tf.keras.layers.Dense(10, activation=tf.nn.relu, name='relu2')(x)
    x = tf.keras.layers.Dense(10, activation=tf.nn.relu, name='relu2')(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    cloud_output = tf.keras.layers.Dense(10, activation=tf.nn.softmax, name='cloud_output')(x)
    
    cloud_model = keras.Model(inputs=cloud_input, outputs=[cloud_output], name='cloud_model')

    cloud_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    cloud_model.save("tensorflow/out/cloud.h5")

    # cloud_prediction = cloud_model.predict(fog_prediction[0])
    # print("Cloud prediction: ", cloud_prediction.argmax())

edge()
fog()
cloud()


# plt.imshow(x_test[image_index].reshape(28,28))
# plt.show()
# 
# # Complete network
# img_input = keras.Input(shape=input_shape, name='image')
# edge = edge_model(img_input)
# fog = fog_model(edge[0])
# cloud = cloud_model(fog[0])
# model = keras.Model(inputs=[img_input], outputs=[edge[1], fog[1], cloud], name='model')
# 
# model.compile(optimizer='adam', loss={'edge_model':'sparse_categorical_crossentropy', 'fog_model':'sparse_categorical_crossentropy', 'cloud_model':'sparse_categorical_crossentropy'}, metrics=['accuracy'], loss_weights=[0.001, 0.001, 0.001])
# 
# model.fit(x=x_train, y=[y_train, y_train, y_train], epochs=5)
# 

# model.evaluate(x_test, [y_test, y_test, y_test])
# 
# pred = model.predict(x_test[image_index].reshape(1, 28, 28, 1))
# print("\nFULL NETWORK PREDICTIONS")
# print("Edge prediction: ", pred[0].argmax())
# print("Fog prediction: ", pred[1].argmax())
# print("Cloud prediction: ", pred[2].argmax())
# 
# # Distributed predictions again
# edge_prediction = edge_model.predict(x_test[image_index].reshape(1, 28, 28, 1))
# print("\nDISTRIBUTED PREDICTIONS AFTER TRAINING")
# print("Edge prediction: ", edge_prediction[1].argmax())
# 
# fog_prediction = fog_model.predict(edge_prediction[0])
# print("Fog prediction: ", fog_prediction[1].argmax())
# 
# cloud_prediction = cloud_model.predict(fog_prediction[0])
# print("Cloud prediction: ", cloud_prediction.argmax())