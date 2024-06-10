from detection.movenet_thunder import ShowWindow
import numpy as np

class AbdominalController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/abdominal.mp4')
        self.rep_count = 0
        self.is_crunch_correct = False
        self.angle_attempt=100
        self.angle_correct=30
        self.angle_perfect=15
    
    def __del__(self):
        super().__del__()
        
    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle
    
    def check_exercise(self, keypoints):
        # Left hip (11), left shoulder (5), and left knee (13)
        hip_left = keypoints[11]
        shoulder_left = keypoints[5]
        knee_left = keypoints[13]
        
        crunch_angle = self.calculate_angle(knee_left, hip_left, shoulder_left)

        #Calcular score y color
        score_percent, color = self.calculate_score_and_color(crunch_angle)
        # Verificar si las piernas están juntas
        are_legs_together = self.check_legs_together(keypoints, 0.10, 0.20)
        # Verificar si los pies están juntos
        are_ankle_together = self.check_ankle_together(keypoints, 0.10, 0.20)

        # Crear las indicaciones con el mensaje descriptivo
        indications = [
            {"name": "Precision: " + str(round(score_percent, 2)) + "%", "color": color},
            {"name": "Piernas Recogidas" if crunch_angle < 30 else "Recoja las piernas", "color": "green" if crunch_angle < 30 else "red"},
            {"name": "Pies Juntos" if are_ankle_together else "Junte los pies", "color": "green" if are_ankle_together else "red"},
            {"name": "Piernas juntas" if are_legs_together else "Junte las piernas", "color": "green" if are_legs_together else "red"}
        ]
        
        # Llamamos a la función show_indications para mostrar las indicaciones
        self.show_indications(indications)

        return crunch_angle < self.angle_correct  # Reduced threshold angle for crunch detection
    
    def calculate_score_and_color(self, crunch_angle):
        # Ejemplo de indicaciones aleatorias con precisión
        score = (1 - abs(self.angle_perfect - crunch_angle) / self.angle_correct ) * 100 
        score = score if score >= 0 else 0

        # Determinar el color basado en la precisión
        if score > 80:
            color = "blue"
        elif 1 <= score <= 80:
            color = "green"
        else:
            color = "red"

        return score, color

    def check_attempt(self, keypoints):
        # Left hip (11), left shoulder (5), and left knee (13)
        hip_left = keypoints[11]
        shoulder_left = keypoints[5]
        knee_left = keypoints[13]
        
        crunch_angle = self.calculate_angle(knee_left, hip_left, shoulder_left)
        return crunch_angle < self.angle_attempt
    
    def check_legs_together(self, keypoints, x_max_distance, y_max_distance):
        # Definir los índices para los puntos de referencia de las caderas, rodillas y tobillos
        knee_left = keypoints[13]
        knee_right = keypoints[14]

        #Calcular distancia en ejex y ejey
        x_horizontal_displacement = abs(knee_left[1] - knee_right[1])
        y_horizontal_displacement = abs(knee_left[0] - knee_right[0])
        return (x_horizontal_displacement < x_max_distance) and (y_horizontal_displacement < y_max_distance) 

    def check_ankle_together(self, keypoints, x_max_distance, y_max_distance):
        # Definir los índices para los puntos de referencia de las caderas, rodillas y tobillos
        ankle_left = keypoints[15]
        ankle_right = keypoints[16]

        #Calcular distancia en ejex y ejey
        x_horizontal_displacement = abs(ankle_left[1] - ankle_right[1])
        y_horizontal_displacement = abs(ankle_left[0] - ankle_right[0])
        return (x_horizontal_displacement < x_max_distance) and (y_horizontal_displacement < y_max_distance) 
