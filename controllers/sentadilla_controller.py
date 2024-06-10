import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class SentadillaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/sentadilla.mp4')
        self.rep_count = 0
        self.initiated = False
        self.angle_knee_attempt = 130
    
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

    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))
    
    # Check if the person is squatting
    # Check if angle between hips, knees and ankles is correct
    def check_exercise(self, keypoints):

        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]

        correct_depth_squat = self.check_depth_squat(keypoints)
        correct_hip_angle = self.check_hip_angle(keypoints)
        correct_knee_angle = self.check_knee_angle(keypoints)

        # Ángulo de la cadera
        hip_angle_left = self.calculate_angle(left_shoulder, left_hip, left_knee)
        hip_angle_right = self.calculate_angle(right_shoulder, right_hip, right_knee)

        score_left = self.calculate_score(hip_angle_left)
        score_right = self.calculate_score(hip_angle_right)

        score_percent, color = self.calculate_score_and_color(score_left, score_right)


        indications = self.create_indications(score_percent, color, correct_hip_angle, correct_knee_angle)
        
        self.show_indications(indications)

        return correct_depth_squat and correct_hip_angle and correct_knee_angle

    # Check if the person is attempting to squat
    def check_attempt(self, keypoints):
        # Extract relevant keypoints
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]
        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]
        
        angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        # distance between shoulders and knees
        distance_left = self.calculate_distance(left_shoulder, left_knee)
        distance_right = self.calculate_distance(right_shoulder, right_knee)

        # if distances < 0.3 is attempting
        if distance_left < 0.3 and distance_right < 0.3:
            return angle_left < self.angle_knee_attempt and angle_right < self.angle_knee_attempt
        else:
            return False


    # la cadera debe descender hasta alcanzar al menos la altura de las rodillas,
    def check_depth_squat(self, keypoints):
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]

        # Toma en cuenta el eje y para determinar la profundidad de la sentadilla, la diferencia entre la cadera y la rodilla cuando se flexiona debe ser menor a 0.1
        left_y_diff = abs(left_hip[1] - left_knee[1])
        right_y_diff = abs(right_hip[1] - right_knee[1])

        return left_y_diff < 0.1 and right_y_diff < 0.1
    
    # Verifica que el ángulo de la cadera sea menor a 90 grados
    def check_hip_angle(self, keypoints):
        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]

        # Ángulo de la cadera
        hip_angle_left = self.calculate_angle(left_shoulder, left_hip, left_knee)
        hip_angle_right = self.calculate_angle(right_shoulder, right_hip, right_knee)

        return hip_angle_left < 90 and hip_angle_right < 90
    
    # Verifica el angulo de la rodilla
    def check_knee_angle(self, keypoints):
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]

        # Ángulo de la rodilla
        knee_angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        knee_angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        # print("Knee Left: ", knee_angle_left, "  -  Knee Right: ", knee_angle_right)

        return knee_angle_left < 100 and knee_angle_right < 100
    
    def calculate_score(self, angle):
        return (1 - abs(90 - angle) / 90) * 100
    
    def calculate_score_and_color(self, score_left, score_right):
        score = np.mean([score_left, score_right])
        score_percent = score if score >= 0 else 0
        
        if score >= 80:
            color = "blue"
        elif 1 <= score < 80:
            color = "green"
        else:
            color = "red"
        
        return score_percent, color

    def create_indications(self, score_percent, color, correct_hip_angle, correct_knee_angle):
        return [
            {"name": "Precision: " + str(round(score_percent, 2)) + "%", "color": color },
            {"name": "Cadera correcta" if correct_hip_angle else "Corrige Cadera", "color": "green" if correct_hip_angle else "red"},
            {"name": "Rodilla correcta" if correct_knee_angle else "Agachate Mas", "color": "green" if correct_knee_angle else "red"}
        ]
        