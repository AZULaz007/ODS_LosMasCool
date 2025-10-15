# collect_data.py
import os
import cv2

# --- CONFIGURACIÓN ---
# Cambia este valor a la letra o seña que vas a capturar
DATA_DIR = './data'
SIGN_LETTER = 'Y'  # Cambia esto a la letra que deseas capturar
# --- FIN CONFIGURACIÓN ---

# Crear el directorio si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

sign_dir = os.path.join(DATA_DIR, SIGN_LETTER)
if not os.path.exists(sign_dir):
    os.makedirs(sign_dir)

# Contar cuántas imágenes ya existen
counter = len(os.listdir(sign_dir))

# Iniciar la cámara
cap = cv2.VideoCapture(0)

print(f"Preparado para capturar imágenes para la seña: '{SIGN_LETTER}'")
print("Coloca tu mano en posición y presiona 's' para guardar la imagen.")
print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Muestra un rectángulo donde deberías poner la mano
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)
    cv2.putText(frame, f"Capturas para '{SIGN_LETTER}': {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('Recopilacion de Datos', frame)

    key = cv2.waitKey(25)
    if key == ord('q'):
        break
    if key == ord('s'):
        # Guarda la imagen en la carpeta correcta
        cv2.imwrite(os.path.join(sign_dir, f'{counter}.jpg'), frame)
        print(f"Imagen {counter} guardada para la seña '{SIGN_LETTER}'")
        counter += 1

cap.release()
cv2.destroyAllWindows()