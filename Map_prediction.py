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
max_len_sequence=3
num_lstm_cell=10

# Constant
max_map_dimension = 3
latent_dim_decoder = max_map_dimension*max_map_dimension



# Post processing
dict_enemies_position={}

dict_values_processing={
    "0.000":".",
    "0.001":"e",
    "0.003":"nan",
    "0.004":"#",
    "0.006":"nan"
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
        # 0.2 enemies flag
        # 0.45 wall
        # 0.95 padding

        # 0.60 enmy

        dataset_processed = []
        for sequence in dataset_raw:
            sequence_processed=[]

            current_symbol, current_enemies=sequence[0][1],sequence[0][2]

            if(current_enemies == "upper"):
                dict_values_processing["0.006"]="x"
                dict_values_processing["0.003"]="X"
            else:
                dict_values_processing["0.006"]="X"
                dict_values_processing["0.003"]="x"

            for image,_,_ in sequence:

                this_image = []
                for row in range(len(image)):
                    this_row = []
                    for column in range(len(image[0])):
                        current_cell = image[row][column]

                        # Immettere info per i bonus
                        if(current_cell == "#" or current_cell == "@" or current_cell == "!" or current_cell == "&"):
                            result = 0.004
                        elif(current_cell == "X"):
                            if(current_enemies == "upper"):
                                result = 0.006
                            else:
                                result = 0.003
                        elif(current_cell == "x"):
                            if(current_enemies == "upper"):
                                result = 0.003
                            else:
                                result = 0.006
                        elif(current_cell == current_symbol):
                            result = 0
                        elif(current_cell.isupper() and current_enemies == "upper"):
                            result = 0.001
                            dict_enemies_position[current_cell]=(row,column)
                        elif(current_cell.islower() and current_enemies == "lower"):
                            result = 0.001
                            dict_enemies_position[current_cell]=(row,column)
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
        return map_array[:shape[0],:shape[1]]

    def post_process_image(self, decoded_image, enemy):
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
                
        symbol_image=np.array(symbol_image)
        symbol_image[symbol_image=="e"]=enemy
        return symbol_image

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
        autoencoder.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss=losses.MeanSquaredError())
        autoencoder.fit(autoencoder_dataset, autoencoder_dataset,
                        epochs=10000,
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
            x_train, maxlen=max_len_sequence,padding="post", value=0.95
        )

        return x_train, y_train
    
    def multiply_foreach_enemy(self,dataset):
        dataset_processed = []
        for sequence in dataset:
            sequence_processed=[]

            current_symbol, current_enemies=sequence[0][1],sequence[0][2]
            sequence_list_images=[]
            for image,_,_ in sequence:
                sequence_list_images.append(image)

            enemies=[]
            allies=[]

            for elem in np.unique(np.array(sequence_list_images)):
                if(elem.isupper() and current_enemies == "upper"):
                    enemies.append(elem)
                if(elem.islower() and current_enemies == "lower"):
                    enemies.append(elem)
                if(elem.islower() and current_enemies == "upper"):
                    allies.append(elem)
                if(elem.isupper() and current_enemies == "lower"):
                    allies.append(elem)


            for enemy in enemies:
                local_sequence=np.array(sequence_list_images)
                #Elimina altri amici
                for friend in allies:
                    local_sequence[local_sequence==friend]="."

                #Elimina altri nemici
                for local_enemy in enemies:
                    if(local_enemy!=enemy):
                        local_sequence[local_sequence==local_enemy]="."

                # Aggiungi informazioni
                add_information_sequence=[]
                for elem in local_sequence:
                    add_information_sequence.append((elem,current_symbol,current_enemies))
                # Aggiungi al dataset
                dataset_processed.append(add_information_sequence)
        return dataset_processed

    def training_lstm(self, dataset):
        #____________________________________________________________________Train LSTM
 
        # Multiply sequence for each enemyes
        multiplied_dataset= self.multiply_foreach_enemy(dataset)
 
        # Get images
        dataset_processed=self.process_symbol_images(multiplied_dataset)

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
        lstm_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['mse'])

        lstm_model.fit(x=x_lstm_dataset, y=y_lstm_dataset,epochs=10000)

        # Save and load
        lstm_model.save('ml_models/lstm/lstm_model.h5')
        self.lstm_model=lstm_model

    def process_enemies(self,dataset_padded, enemy):
        current_pos_row,current_pos_col=dict_enemies_position[enemy]
        dataset_padded_copy=dataset_padded
        for image in dataset_padded_copy:
            image[image==0.6]=0
            image[current_pos_row][current_pos_col]=0.6
        return dataset_padded_copy

    def get_prediction(self, history):
        # From a list of maps get the prediction of the next map
        current_symbol, current_enemies=history[0][1],history[0][2]

        multiplied_dataset= self.multiply_foreach_enemy(np.array([history]))

        sequence_list_images=[]
        for image,_,_ in history:
            sequence_list_images.append(image)
        enemies=[]
        allies=[]

        for elem in np.unique(np.array(sequence_list_images)):
            if(elem.isupper() and current_enemies == "upper"):
                enemies.append(elem)
            if(elem.islower() and current_enemies == "lower"):
                enemies.append(elem)
            if(elem.islower() and current_enemies == "upper"):
                allies.append(elem)
            if(elem.isupper() and current_enemies == "lower"):
                allies.append(elem)

        print(enemies)
        list_post_processed=[]
        for i,current_sequence in enumerate(multiplied_dataset):

            # Process symbol
            dataset_processed = self.process_symbol_images(np.array([current_sequence]))
            
            #Padding maps
            dataset_processed_padded=self.padding_maps(dataset_processed)
            
            print(dataset_processed_padded[0])

            # Encode images
            encoded_imgs = self.autoencoder_model.encoder(dataset_processed_padded[0]).numpy()
            query = np.array([encoded_imgs])

            # Padding sequence
            query = tf.keras.preprocessing.sequence.pad_sequences(
                query, maxlen=max_len_sequence, padding="post", value=0.95
            )

            # Predict
            new_encoded_maps = self.lstm_model.predict(query)

            # Decode
            new_map = self.autoencoder_model.decoder(new_encoded_maps).numpy()
            print(new_map)
            # Trim map
            new_map=self.trim_map(new_map[0], (len(history[0][0]), len(history[0][0][1])))

            # Post Processing
            post_processed=self.post_process_image(new_map,enemies[i])
            list_post_processed.append(post_processed)
        
        return list_post_processed
        
    def grid_lstm(self,dataset):
        dict_model={}
        grid_params = {
                'learning_rate': [1e-4,1e-3,1e-6, 1e-5, 1e-7],
                'num_cell': [2,10,20,30]
            }
        keys, values = zip(*grid_params.items())
        params_list = [dict(zip(keys, v)) for v in product(*values)]

        for configuration in params_list:
            #Parametri

            learning_rate = configuration['learning_rate']
            num_cell = configuration['num_cell']

            # Set LSTM model
            lstm_model = tf.keras.models.Sequential([
                tf.keras.Input(shape=(max_len_sequence, latent_dim_encoder)),
                #tf.keras.layers.Embedding(input_dim=max_len_sequence, output_dim=input_output_dim, mask_zero=True),
                tf.keras.layers.LSTM(num_cell),
                tf.keras.layers.Dense(units=latent_dim_encoder)
            ])

            # Compile and train
            lstm_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                loss=tf.keras.losses.MeanSquaredError(),
                metrics=['mse'])

            history=lstm_model.fit(x=dataset[0], y=dataset[1],epochs=10000)
            val_acc = history.history['val_accuracy']
            dict_model[str(configuration)]=val_acc[-1]
        print(dict_model)

    def prepare_data_autoencoder(self,dataset):
        # Get images
        dataset_processed=self.process_symbol_images(dataset)
        print("Image processed")
        #Padding maps
        dataset_processed_padded=self.padding_maps(dataset_processed)
        print("image padding")
        # Extract images
        autoencoder_dataset=self.extract_images(dataset_processed_padded)
        print("extraction")
        filehandler = open("./map_prediction_datasets/data_processed_autoencoder.pickle","wb")
        pickle.dump(autoencoder_dataset,filehandler,protocol=4)

    def prepare_data_lstm(self, dataset):
        # Multiply sequence for each enemyes
        multiplied_dataset= self.multiply_foreach_enemy(dataset)
        print("multiplied")
        # Get images
        dataset_processed=self.process_symbol_images(multiplied_dataset)
        print("process")
        #Padding maps
        dataset_processed_padded=self.padding_maps(dataset_processed)
        print("padding")
        #Encode images and padding sequence
        #x_lstm_dataset,y_lstm_dataset=self.autoencoder_encode_sequences(dataset_processed_padded)

        

    def grid_autoencoder(self,dataset):
        dict_model= {}
        grid_params = {
                'learning_rate': [1e-4,1e-3,1e-6, 1e-5, 1e-7],
                'optimizer': [tf.keras.optimizers.Adam]
            }
        keys, values = zip(*grid_params.items())
        params_list = [dict(zip(keys, v)) for v in product(*values)]

        for configuration in params_list:
            #Parametri
            
            learning_rate = configuration['learning_rate']
            optimizer = configuration['optimizer']

            autoencoder=Autoencoder()
            autoencoder.compile(optimizer=optimizer(learning_rate=learning_rate), loss=losses.MeanSquaredError())
            history=autoencoder.fit(dataset, dataset,validation_split=0.2,
                            epochs=10000,
                            shuffle=True)
            
            val_acc = history.history['val_accuracy']
            dict_model[str(configuration)]=val_acc[-1]
        print(dict_model)

if __name__ == "__main__":
    

    # Fake history
    data = [([['c', '.', '.'], ['.', '.', 'd']], "A", 'lower'), ([['.', 'c', '.'], [
        '.', 'd', '.']], "A", 'lower'), ([['.', '.', 'c'], ['d', '.', '.']], "A", 'lower')]

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
