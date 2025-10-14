import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

# --- Carregar o modelo ---
try:
    with open('model.p', 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
except FileNotFoundError:
    print("Erro: O arquivo 'model.p' não foi encontrado.")
    exit()

cap = cv2.VideoCapture(0)

# --- INICIALIZAÇÃO CORRETA DO MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

labels_dict = {i: label for i, label in enumerate(model.classes_)}

# --- Variáveis para o controle de fala ---
last_spoken_char = ""
current_char_candidate = ""
confidence_counter = 0
CONFIDENCE_THRESHOLD = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # AQUI ESTÁ A CORREÇÃO: DE BGR PARA RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            data_aux = []
            # (Código para extrair pontos da mão - sem alterações)
            wrist_x = hand_landmarks.landmark[0].x
            wrist_y = hand_landmarks.landmark[0].y
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x - wrist_x)
                data_aux.append(landmark.y - wrist_y)

            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]

            # --- Lógica de Confiança (sem alterações) ---
            if predicted_character == current_char_candidate:
                confidence_counter += 1
            else:
                current_char_candidate = predicted_character
                confidence_counter = 1

            # --- LÓGICA DE FALA MODIFICADA ---
            if confidence_counter >= CONFIDENCE_THRESHOLD:
                if current_char_candidate != last_spoken_char:
                    print(f"Com confiança, detectei: {current_char_candidate}. Preparando para falar...")
                    
                    engine = pyttsx3.init()
                    engine.say(current_char_candidate)
                    engine.runAndWait()
                    engine.stop()
                    
                    last_spoken_char = current_char_candidate

            # --- Desenhar o texto na tela ---
            cv2.putText(frame, predicted_character, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('Reconocimiento de Senas', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()