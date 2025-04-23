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
last_pose_frame = time.time()
falling_detected = False

# Abre webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (500, 500))
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        last_pose_frame = time.time()
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        points = result.pose_landmarks.landmark
        y_head = points[0].y
        y_hip = points[24].y

        # Critério de queda: cabeça está muito baixa (quase ao nível do quadril ou fora da tela)
        if y_head > 0.8 or abs(y_head - y_hip) < 0.05:
            falling_detected = True
        else:
            falling_detected = False

    else:
        # Sem detecção por mais de 3 segundos
        if time.time() - last_pose_frame > 3:
            falling_detected = True

    if falling_detected:
        cv2.putText(frame, "QUEDA DETECTADA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        # arduino.write(b'1')
        falling_detected = False  # Previne múltiplos alertas

    cv2.imshow("Monitor de Queda", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza
cap.release()
cv2.destroyAllWindows()
# arduino.close()
