#recognize.py
import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
from tensorflow.keras.models import load_model  # Ya en uso para LSTM

# --- Cargar ambos modelos ---
try:
    with open('model.p', 'rb') as f:
        static_model_dict = pickle.load(f)
    static_model = static_model_dict['model']  # Modelo RandomForest para estático
except FileNotFoundError:
    print("Error: No se encontró 'model.p'.")
    exit()

try:
    dynamic_model = load_model('action.h5')  # Modelo LSTM para dinámico
except Exception as e:
    print(f"Error al cargar 'action.h5': {e}")
    exit()

cap = cv2.VideoCapture(0)

# --- INICIALIZACIÓN DE MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

labels_dict_static = {i: label for i, label in enumerate(['J', 'K', 'Ñ', 'Q', 'X', 'Z'])}  # Ajusta según tu entrenamiento estático
labels_dict_dynamic = {0: 'J', 1: 'K', 2: 'Ñ', 3: 'Q', 4: 'X', 5: 'Z'}  # Ajusta según tu entrenamiento dinámico

# --- Variables para detección de movimiento y secuencias ---
previous_landmarks = None  # Para comparar movimiento
movement_threshold = 0.0016  # Umbral de movimiento (ajusta según pruebas, e.g., 0.05 para baja variación)
sequence = []  # Para secuencias dinámicas
sequence_length = 30  # Debe coincidir con tu entrenamiento
last_spoken_char = ""
current_char_candidate = ""
confidence_counter = 0
CONFIDENCE_THRESHOLD = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Primer mano detectada
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        current_landmarks = np.array([[lmk.x, lmk.y, lmk.z] for lmk in hand_landmarks.landmark]).flatten()  # Array de 63 elementos
        
        if previous_landmarks is not None:
            # Calcular movimiento: media de diferencias absolutas
            movement = np.mean(np.abs(current_landmarks - previous_landmarks))
            
            if movement < movement_threshold:  # Baja movimiento: Seña estática
                # Predicción estática
                data_aux_static = []  # Extraer keypoints relativos para el modelo estático
                wrist_x = hand_landmarks.landmark[0].x
                wrist_y = hand_landmarks.landmark[0].y
                for landmark in hand_landmarks.landmark:
                    data_aux_static.append(landmark.x - wrist_x)
                    data_aux_static.append(landmark.y - wrist_y)  # Solo x e y, como en tu código original
                
                prediction_static = static_model.predict([np.asarray(data_aux_static)])
                predicted_character = prediction_static[0]  # Asume que es la predicción directa
                
                # Lógica de confianza
                if predicted_character == current_char_candidate:
                    confidence_counter += 1
                else:
                    current_char_candidate = predicted_character
                    confidence_counter = 1
                
                if confidence_counter >= CONFIDENCE_THRESHOLD:
                    if current_char_candidate != last_spoken_char:
                        print(f"Con confianza, detecté (estático): {current_char_candidate}")
                        engine = pyttsx3.init()
                        engine.say(current_char_candidate)
                        engine.runAndWait()
                        engine.stop()
                        last_spoken_char = current_char_candidate
                
                cv2.putText(frame, f"Estático: {predicted_character}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                sequence = []  # Resetear secuencia por si acaso
                
            else:  # Alto movimiento: Seña dinámica
                # Agregar a secuencia para modelo dinámico
                data_aux_dynamic = current_landmarks  # Usar landmarks absolutos (x, y, z)
                sequence.append(data_aux_dynamic)  # Agrega el array de 63 elementos
                
                if len(sequence) > sequence_length:
                    sequence = sequence[-sequence_length:]  # Mantener solo los últimos 30
                    
                if len(sequence) == sequence_length:
                    sequence_array = np.array(sequence).reshape(1, sequence_length, 63)  # Forma para LSTM
                    prediction_dynamic = dynamic_model.predict(sequence_array)
                    predicted_index = np.argmax(prediction_dynamic)
                    predicted_character = labels_dict_dynamic[predicted_index]
                    
                    # Lógica de confianza
                    if predicted_character == current_char_candidate:
                        confidence_counter += 1
                    else:
                        current_char_candidate = predicted_character
                        confidence_counter = 1
                    
                    if confidence_counter >= CONFIDENCE_THRESHOLD:
                        if current_char_candidate != last_spoken_char:
                            print(f"Con confianza, detecté (dinámico): {current_char_candidate}")
                            engine = pyttsx3.init()
                            engine.say(current_char_candidate)
                            engine.runAndWait()
                            engine.stop()
                            last_spoken_char = current_char_candidate
                    
                    cv2.putText(frame, f"Dinámico: {predicted_character}", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        previous_landmarks = current_landmarks  # Actualizar para el próximo frame
    
    cv2.imshow('Reconocimiento de Señas (Estático/Dinámico)', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()