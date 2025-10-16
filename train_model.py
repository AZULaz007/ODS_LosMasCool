# train_model.py
import os
import pickle
import mediapipe as mp
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

DATA_DIR = './data'
data = []
labels = []

print("Procesando imágenes y extrayendo puntos clave...")

# Iterar sobre cada carpeta de señas en el directorio de datos
for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)
    if not os.path.isdir(dir_path):
        continue
    
    print(f'Procesando clase: {dir_}')
    # Iterar sobre cada imagen en la carpeta de la seña
    for img_path in os.listdir(dir_path):
        img_full_path = os.path.join(dir_path, img_path)
        img_data = []
        
        # Leer la imagen
        img = cv2.imread(img_full_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Procesar con MediaPipe
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            # Normalizar los puntos relativos a la muñeca
            wrist_x = hand_landmarks.landmark[0].x
            wrist_y = hand_landmarks.landmark[0].y
            for landmark in hand_landmarks.landmark:
                img_data.append(landmark.x - wrist_x)
                img_data.append(landmark.y - wrist_y)
            
            data.append(img_data)
            labels.append(dir_)

print("Entrenamiento del modelo iniciado...")

# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Entrenar un clasificador de Bosque Aleatorio (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Evaluar el modelo
y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)

print(f'Modelo entrenado con una precisión de: {score * 100:.2f}%')

# Guardar el modelo entrenado en un archivo
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)

print("¡Modelo guardado exitosamente como 'model.p'!")