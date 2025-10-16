#collect_dynamic_data.py
import cv2
import numpy as np
import os
import mediapipe as mp

# --- INICIALIZAÇÃO CORRETA DO MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- CONFIGURAÇÃO ---
DATA_PATH = os.path.join('dynamic_data') # Diretório para salvar os dados
actions = np.array(['J', 'K', 'Ñ','Q','X','Z']) # Ações (gestos) que vamos gravar
no_sequences = 30 # 30 "vídeos" de cada gesto
sequence_length = 30 # 30 frames por "vídeo"
# --- FIM DA CONFIGURAÇÃO ---

# Criar as pastas para cada ação
for action in actions:
    for sequence in range(no_sequences):
        try:
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Tente 1 ou 2 se o 0 não funcionar
# VERIFICA SE A CÂMERA ABRIU CORRETAMENTE
if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# Loop principal para coletar dados
for action in actions:
    # Loop através das sequências (vídeos)
    for sequence in range(no_sequences):
        # Loop através dos frames da sequência
        for frame_num in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                print("Erro: Falha ao capturar o frame.")
                cap.release()
                cv2.destroyAllWindows()
                exit()

            # Processar o frame com MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Desenhar os pontos na mão
            if results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            # Lógica de espera e texto na tela
            if frame_num == 0:
                cv2.putText(frame, 'INICIANDO COLETA', (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                cv2.putText(frame, f'Coletando frames para {action} - Video No. {sequence}', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('Coleta de Dados Dinamicos', frame)
                cv2.waitKey(2000) # Espera 2 segundos
            else:
                cv2.putText(frame, f'Coletando frames para {action} - Video No. {sequence}', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('Coleta de Dados Dinamicos', frame)
            
            # LÓGICA DE SALVAR OS DADOS
            keypoints = np.array([[res.x, res.y, res.z] for res in results.multi_hand_landmarks[0].landmark]).flatten() if results.multi_hand_landmarks else np.zeros(21*3)
            npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
            np.save(npy_path, keypoints)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()

print("Coleta de dados finalizada.")
cap.release()
cv2.destroyAllWindows()