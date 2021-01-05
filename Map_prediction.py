import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Autoencoder Parameters
latent_dim_encoder = 100

# LSTM Parameters
max_len_sequence=20
num_lstm_cell=50

# Constant
max_map_dimension = 128
latent_dim_decoder = max_map_dimension*max_map_dimension



# Post processing
dict_values_processing={
    "0.000":".",
    "0.150":"nan",
    "0.300":"nan",
    "0.450":"#"
}


class Autoencoder(Model):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = tf.keras.Sequential([
            layers.Flatten(),
            layers.Dense(latent_dim_encoder, activation='relu'),
        ])
        self.decoder = tf.keras.Sequential([
            layers.Dense(latent_dim_decoder, activation='sigmoid'),
            layers.Reshape((max_map_dimension, max_map_dimension))
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


class PredictionModel():
    def __init__(self):
        pass
    
    def set_models(self):
        # Load weigths froom pretrained model
        autoencoder_model = Autoencoder()
        autoencoder_model.load_weights('ml_models/autoencoder/autoencoder_weights.wg')
        self.autoencoder_model = autoencoder_model
        self.lstm_model = tf.keras.models.load_model(
            'ml_models/lstm/lstm_model.h5')

    def process_symbol_images(self, dataset_raw):

        #0.0 free
        # 0.15 own flagù
        # 0.5 enemies flag
        # 0.45 wall
        # 0.95 padding

        # 0.6 85.5 enemies 0.006 per enemy

        ## 0.606
        ## 0.612
        ##...

        dataset_processed = []
        for sequence in dataset_raw:
            sequence_processed=[]

            current_symbol, current_enemies=sequence[0][1],sequence[0][2]

            if(current_enemies == "upper"):
                dict_values_processing["0.150"]="x"
                dict_values_processing["0.300"]="X"
            else:
                dict_values_processing["0.150"]="X"
                dict_values_processing["0.300"]="x"

            for image,_,_ in sequence:

                this_image = []
                for row in range(len(image)):
                    this_row = []
                    for column in range(len(image[0])):
                        current_cell = image[row][column]

                        # Immettere info per i bonus
                        if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&"):
                            result = 0.45
                        elif(current_cell == "X"):
                            if(current_enemies == "upper"):
                                result = 0.15
                            else:
                                result = 0.30
                        elif(current_cell == "x"):
                            if(current_enemies == "upper"):
                                result = 0.3
                            else:
                                result = 0.15
                        elif(current_cell == current_symbol):
                            result = 0
                        elif(current_cell.isupper() and current_enemies == "upper"):
                            result = 0.6+((0.006)*(ord(current_cell)-65))
                            dict_values_processing[(str(result)+"000")[0:5]]=current_cell
                        elif(current_cell.islower() and current_enemies == "lower"):
                            result = 0.6+((0.006)*(ord(current_cell)-65))
                            dict_values_processing[(str(result)+"000")[0:5]]=current_cell
                        else:
                            result = 0.0
                        this_row.append(result)
                    this_image.append(this_row)
                sequence_processed.append(np.array(this_image))
            dataset_processed.append(sequence_processed)
        dataset_processed = np.array(dataset_processed)
        
        return dataset_processed

    def trim_map(self, map_array, shape):
        # Resize prediction decoded prediction with correct size
        return np.resize(map_array, shape)

    def post_process_image(self, decoded_image):
        # Set number to image based on dictionary
        list_values=[float(key) for key in dict_values_processing]
        symbol_image=[]
        for row in range(len(decoded_image)):
            symbol_row=[]
            for column in range(len(decoded_image[0])):
                current_cell = decoded_image[row][column]
                differences = [abs(current_cell-elem)for elem in list_values]
                result=list_values[differences.index(
                    min(differences))]
                symbol_row.append(dict_values_processing[(str(result)+"000")[0:5]])
            symbol_image.append(symbol_row)
                
                
        return np.array(symbol_image)

    def padding_maps(self,dataset_processed):
        # Pad maps with maximum size
        dataset_processed_generalized=[]
        for sequence in dataset_processed:
            sequence_processed_generalized=[]
            for elem in sequence:
                extension = np.empty((max_map_dimension,max_map_dimension))
                extension.fill(0.95)
                extension[:elem.shape[0],:elem.shape[1]] = elem
                sequence_processed_generalized.append(extension)
            dataset_processed_generalized.append(sequence_processed_generalized)
        return np.array(dataset_processed_generalized)


    def extract_images(self, dataset):
        # Get images from dataset of sequences, useful for autoencoder
        only_images=[]
        for sequence in dataset:
            only_images.extend(sequence)
        return np.array(only_images)

    def training_autoencoder(self,dataset):

        #___________________________________________________________Train autoencoder
        # Get images
        dataset_processed=self.process_symbol_images(dataset)

        #Padding maps
        dataset_processed_padded=self.padding_maps(dataset_processed)

        # Extract images
        autoencoder_dataset=self.extract_images(dataset_processed_padded)


        #Train model
        autoencoder=Autoencoder()
        autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())
        autoencoder.fit(autoencoder_dataset, autoencoder_dataset,
                        epochs=100,
                        shuffle=True)
        # Save weigths
        autoencoder.save_weights('ml_models/autoencoder/autoencoder_weights.wg')
        self.autoencoder_model=autoencoder

    def autoencoder_encode_sequences(self,dataset_sequences):
        x_train_encoded_sequences=[]
        y_train_encoded_sequences=[]
        for current_sequence in dataset_sequences:
            encoded_imgs = self.autoencoder_model.encoder(current_sequence).numpy()
            y_train_encoded_sequences.append(encoded_imgs[-1])
            x_train_encoded_sequences.append(encoded_imgs[:-1])

        x_train=np.array(x_train_encoded_sequences)
        y_train=np.array(y_train_encoded_sequences)

        x_train = tf.keras.preprocessing.sequence.pad_sequences(
            x_train, maxlen=max_len_sequence,padding="post"
        )

        return x_train, y_train
    def training_lstm(self, dataset):
        #____________________________________________________________________Train LSTM

        # Get images
        dataset_processed=self.process_symbol_images(dataset)

        #Padding maps
        dataset_processed_padded=self.padding_maps(dataset_processed)

        #Encode images and padding sequence
        x_lstm_dataset,y_lstm_dataset=self.autoencoder_encode_sequences(dataset_processed_padded)

        # Set LSTM model
        lstm_model = tf.keras.models.Sequential([
            tf.keras.Input(shape=(max_len_sequence, latent_dim_encoder)),
            #tf.keras.layers.Embedding(input_dim=max_len_sequence, output_dim=input_output_dim, mask_zero=True),
            tf.keras.layers.LSTM(num_lstm_cell),
            tf.keras.layers.Dense(units=latent_dim_encoder)
        ])

        # Compile and train
        lstm_model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['mse'])

        lstm_model.fit(x=x_lstm_dataset, y=y_lstm_dataset,epochs=10)

        # Save and load
        lstm_model.save('ml_models/lstm/lstm_model.h5')
        self.lstm_model=lstm_model

    def get_prediction(self, history):
        # From a list of maps get the prediction of the next map

        # Process symbol
        dataset_processed = self.process_symbol_images(np.array([history]))

        #Padding maps
        dataset_processed_padded=self.padding_maps(dataset_processed)

        # Encode images
        encoded_imgs = self.autoencoder_model.encoder(dataset_processed_padded[0]).numpy()
        query = np.array([encoded_imgs])

        # Padding sequence
        query = tf.keras.preprocessing.sequence.pad_sequences(
            query, maxlen=max_len_sequence, padding="post"
        )

        # Predict
        new_encoded_maps = self.lstm_model.predict(query)

        # Decode
        new_map = self.autoencoder_model.decoder(new_encoded_maps).numpy()

        # Trim map
        new_map=self.trim_map(new_map[0], (len(history[0][0]), len(history[0][0][1])))

        # Post Processing
        post_processed=self.post_process_image(new_map)

        return post_processed


if __name__ == "__main__":
    

    # Fake history
    data = [([['c', '.', '.'], ['.', '.', '.']], "A", 'lower'), ([['.', 'c', '.'], [
        '.', '.', '.']], "A", 'lower'), ([['.', '.', 'c'], ['.', '.', '.']], "A", 'lower')]

    data_different= [([['', '.', '.'], ['.', '.', '.'],['c', '.', '.']], "A", 'lower'), ([['.', '.', '.'], [
        'c', '.', '.'],['.', '.', '.']], "A", 'lower'), ([['c', '.', '.'], ['.', '.', '.'],['.', '.', '.']], "A", 'lower')]
    # Fake sequences dataset
    data_training=[data,data,data,data,data]

    new_model = PredictionModel()

    new_model.training_autoencoder(data_training)

    new_model.training_lstm(data_training)

    new_model.set_models()

    print(new_model.get_prediction(data[0:2]))
    print(dict_values_processing)
