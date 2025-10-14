# train_lstm_model.py
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

# --- CONFIGURAÇÃO (deve ser a mesma do script de coleta) ---
DATA_PATH = os.path.join('dynamic_data')
actions = np.array(['J', 'Z', 'Ola']) # As mesmas ações que você gravou
no_sequences = 30 # As mesmas 30 sequências
sequence_length = 30 # Os mesmos 30 frames
# --- FIM DA CONFIGURAÇÃO ---

label_map = {label: num for num, label in enumerate(actions)}
sequences, labels = [], []

print("Carregando dados...")
# Carregar os dados salvos
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy"))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

print("Dados carregados com sucesso.")

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1) # Aumentei o teste para 10%

print(f"Iniciando o treinamento do modelo... Shape dos dados de treino: {X_train.shape}")

# Construir o modelo LSTM
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(sequence_length, 21*3)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test)) # Reduzi as épocas para 100, um bom começo

model.summary()

# Salvar o modelo
print("Salvando o modelo treinado...")
model.save('action.h5')
print("Modelo salvo como 'action.h5'")