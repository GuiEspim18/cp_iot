import cv2
import mediapipe as mp
import numpy as np
import time
# import serial

# Configurar porta serial (ajuste para a sua porta)
# arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# Inicializa MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Variáveis de controle
ultimo_frame_pose = time.time()
queda_detectada = False

# Abre webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (500, 500))
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = pose.process(rgb)

    if resultado.pose_landmarks:
        ultimo_frame_pose = time.time()
        mp_draw.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        pontos = resultado.pose_landmarks.landmark
        y_cabeca = pontos[0].y
        y_quadril = pontos[24].y

        # Critério de queda: cabeça está muito baixa (quase ao nível do quadril ou fora da tela)
        if y_cabeca > 0.8 or abs(y_cabeca - y_quadril) < 0.05:
            queda_detectada = True
        else:
            queda_detectada = False

    else:
        # Sem detecção por mais de 3 segundos
        if time.time() - ultimo_frame_pose > 3:
            queda_detectada = True

    if queda_detectada:
        cv2.putText(frame, "QUEDA DETECTADA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        # arduino.write(b'1')
        queda_detectada = False  # Previne múltiplos alertas

    cv2.imshow("Monitor de Queda", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza
cap.release()
cv2.destroyAllWindows()
# arduino.close()
