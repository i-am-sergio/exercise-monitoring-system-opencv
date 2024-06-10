# exercise-monitoring-system-opencv

[**Click Here for project settings**](SETTINGS.md)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![CMake](https://img.shields.io/badge/CMake-%23008FBA.svg?style=for-the-badge&logo=cmake&logoColor=white)

## Description

This project is an exercise monitoring system that uses OpenCV for video capture and processing, NumPy for data processing, and is implemented in both C++ and Python. The system captures video from a camera, processes the frames to monitor exercises, and displays the results in real-time.

## Preview

<p align="center">
  <img src="resources/img/screen1.png" alt="Screen1" width="600px" />
</p>

<p align="center">
  <img src="resources/img/screen2.png" alt="Screen2" width="600px" />
</p>

## Requirements

1. **Real-Time Video Capture:** The system should be able to capture video from a camera in real-time to monitor exercises as they are being performed.

2. **Exercise Detection:** The system should be capable of detecting and identifying specific exercises or movements within the captured video stream.

3. **On-Screen Visualization:** Detected exercises or movements should be visually displayed in real-time on the screen, providing immediate feedback to the user.

4. **Multi-Platform Support:** The software should be compatible with multiple platforms, including Windows, Linux, and macOS, to ensure accessibility for a wide range of users.

5. **Modular Architecture:** The system's architecture should be modular, allowing for easy extension and customization of exercise detection algorithms and integration of additional features in the future.

## Structure

4. **Project Structure:**

```
exercise-monitoring-system/
├── controllers
│   ├── abdominal_controller.py
│   ├── biceps_controller.py
│   ├── elevaciones_controller.py
│   ├── estocada_controller.py
│   ├── jumps_controller.py
│   ├── main_controller.py
│   ├── plancha_controller.py
│   ├── puente_controller.py
│   └── sentadilla_controller.py
|
├── detection
│   ├── abdominal.mp4
│   ├── bicep.mp4
│   ├── estocada.mp4
│   ├── flexion.mp4
│   ├── jumping_jack.mp4
│   ├── movenet_thunder.py
│   └── sentadilla.mp4
|
├── resources
│   ├── 1_sentadilla_btn.png
│   ├── 2_lunge_btn.png
│   ├── 3_biceps_btn.png
│   ├── 4_jumping_jacks_btn.png
│   ├── 5_flexion_btn.png
│   ├── 6_abdominal_btn.png
│   ├── img
│   │   ├── 1_sentadilla.png
│   │   ├── 2_stocada.png
│   │   ├── 3_biceps.png
│   │   ├── 4_puente.png
│   │   ├── 5_elevaciones.png
│   │   └── 6_plancha.png
│   └── models
│       └── model.tflite
|
├── ui
│   └── main_window.ui
|
├── utils
│   └── download_vid.py
|
├── views
|   └── main_window.py
|
├── main.py
├── test.py
├── README.md
├── SETTINGS.md
└── requirements.txt


```

### Tecnologies and tools

- Python >= 3.10
- OpenCV
- Tensorflow
- NumPy
- MinGW (for C++ compilation)
- GCC
- CMake
- Ninja (optional, for generating build files with CMake)

## Movement Detection
### Descripción del Modelo y Código
Modelo `model.tflite` (COCO model)
El modelo model.tflite es una versión optimizada para dispositivos móviles del modelo de detección de objetos COCO (Common Objects in Context). Este modelo ha sido entrenado en el conjunto de datos COCO, que contiene 80 clases de objetos comunes. Su objetivo principal es identificar y localizar objetos dentro de una imagen, proporcionando las coordenadas de los cuadros delimitadores (bounding boxes) y las etiquetas de clase correspondientes para cada objeto detectado.
<p align="center">
  <img src="docs/model/coco_model.png" alt="Screen2" width="600px" />
</p>

``` python
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

```

### Descripción de las funciones

Se hace uso de OpenCV y PyQt5 para la visualización y manipulación de video, junto con la detección de poses utilizando un modelo de TensorFlow Lite.

#### Constructor
```python
def __init__(self, model_path="resources/models/model.tflite", video_path=0):
    self.window = QMainWindow()
    self.window.setWindowTitle("Ejercicios Opencv + Qt")
    self.window.resize(1200, 700)
    central_widget = QWidget()
    self.window.setCentralWidget(central_widget)  
    .
    .
    .
```
El constructor `__init__` de la clase `ShowWindow` inicializa la interfaz de usuario y los componentes necesarios para la visualización de video y detección de poses. Crea una ventana principal utilizando PyQt5, establece su título y dimensiones, y organiza los diferentes widgets utilizando un `QGridLayout`. Se definen etiquetas y botones con estilos específicos, así como grupos de etiquetas para mostrar contadores y mensajes de estado. Además, se carga el modelo de TensorFlow Lite para la detección de poses y se inicializan las variables relacionadas con el seguimiento de repeticiones correctas e incorrectas.

#### Destructor
```python
def __del__(self):
    try:
        self.cap.release()
    except AttributeError:
        pass
    try:
        self.timer.stop()
    except AttributeError:
        pass
```
El método destructor `__del__` garantiza que los recursos de captura de video y el temporizador se liberen correctamente cuando la instancia de `ShowWindow` es destruida.


#### Cierra de ventan de ejercicio

```python
def exit_application(self):
    self.cap.release()
    self.timer.stop()
    self.window.close()
```
La función `exit_application` se encarga de liberar los recursos de captura de video y detener el temporizador antes de cerrar la ventana de la aplicación.


#### Captura del video en QT container
```python
def show(self):
    self.cap = cv2.VideoCapture(self.video_path)
    if not self.cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return
    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
    self.frame_duration = 1.0 / self.fps
    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
    self.frame_duration = 1.0 / self.fps
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_window)
    self.timer.start(16)
```
El método `show` inicializa la captura de video desde el `video_path` especificado, establece el temporizador para actualizar la ventana a intervalos regulares y maneja los errores en caso de que no se pueda abrir el video.

#### Obtención de lo keypoints
```python
def get_keypoints(self, image):
    input_image = tf.image.resize(image, (self.input_shape[1], self.input_shape[2]))
    input_image = tf.cast(input_image, dtype=tf.uint8)
    input_image = tf.expand_dims(input_image, axis=0)
    self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], input_image)
    self.interpreter.invoke()
    keypoints_with_scores = self.interpreter.get_tensor(self.interpreter.get_output_details()[0]['index'])
    return keypoints_with_scores
```
La función `get_keypoints` procesa la imagen de entrada para ajustarla al tamaño requerido por el modelo de TensorFlow Lite, ejecuta el modelo para obtener los puntos clave (keypoints) y sus puntuaciones.

#### Graficar los keypoints

```python
def draw_predictions_on_image(self, image, keypoints_with_scores, keypoint_threshold=0.11):
    height, width, _ = image.shape
    keypoints = keypoints_with_scores[0, 0, :, :2]
    keypoints_scores = keypoints_with_scores[0, 0, :, 2]

    for idx, ((start, end), color) in enumerate(zip(self.edges, self.edge_colors)):
        if keypoints_scores[start] > keypoint_threshold and keypoints_scores[end] > keypoint_threshold:
            start_point = (int(keypoints[start, 1] * width), int(keypoints[start, 0] * height))
            end_point = (int(keypoints[end, 1] * width), int(keypoints[end, 0] * height))
            cv2.line(image, start_point, end_point, color, 2)
    for i in range(keypoints.shape[0]):
        if keypoints_scores[i] > keypoint

_threshold:
            center = (int(keypoints[i, 1] * width), int(keypoints[i, 0] * height))
            cv2.circle(image, center, 3, (0, 0, 255), -1)
    return image
```
La función `draw_predictions_on_image` dibuja las predicciones sobre la imagen original utilizando los puntos clave y sus puntuaciones. Las líneas se dibujan entre los puntos clave según los colores definidos en `edge_colors`.

#### Actualización de frames
```python
def update_window(self):
    ret, frame = self.cap.read()
    if not ret:
        self.timer.stop()
        self.cap.release()
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    keypoints_with_scores = self.get_keypoints(frame_rgb)
    keypoints = keypoints_with_scores[0][0]
    is_attempt = self.check_attempt(keypoints)
    is_correct = self.check_exercise(keypoints)

    if self.previous_state is None:
        self.previous_state = is_attempt

    if self.previous_state != is_attempt:
        if is_attempt:
            self.correct_state = False
        else:
            if self.correct_state:
                self.correct_repetitions += 1
            else:
                self.incorrect_repetitions += 1
        self.previous_state = is_attempt

    elif is_attempt:
        if is_correct and not self.correct_state:
            self.correct_state = True

    self.show_feedback(is_attempt)
    output_overlay = self.draw_predictions_on_image(frame, keypoints_with_scores)
    self.show_image(output_overlay)
```
El método `update_window` se ejecuta en cada intervalo del temporizador, captura el siguiente cuadro del video, procesa los puntos clave, determina el estado del intento del usuario, actualiza los contadores de repeticiones y muestra las predicciones sobre la imagen original.

#### Verificación de Intento y Corrección

La verificación del intento y corrección se realiza mediante dos métodos: `self.check_attempt(keypoints)` y `self.check_exercise(keypoints)`. El primero determina si el usuario está intentando un ejercicio basado en los puntos clave, mientras que el segundo verifica si el intento actual es correcto según criterios predefinidos.

#### Actualización del Estado y Contadores

1. **Inicialización del Estado Anterior**:
   - Si `self.previous_state` es `None` (primera iteración), se inicializa con el estado actual de intento (`is_attempt`).

2. **Cambio de Estado**:
   - Si el estado actual de intento (`is_attempt`) difiere del estado anterior (`self.previous_state`):
     - **Inicio de un Nuevo Intento**: Si `is_attempt` es `True`, se marca `self.correct_state` como `False` (nuevo intento en curso).
     - **Fin de un Intento**: Si `is_attempt` es `False`:
       - **Actualización de Contadores**:
         - **Intento Correcto**: Si `self.correct_state` es `True`, se incrementa `self.correct_repetitions`.
         - **Intento Incorrecto**: Si `self.correct_state` es `False`, se incrementa `self.incorrect_repetitions`.
     - Actualización del Estado Anterior: Se actualiza `self.previous_state` con el estado actual (`is_attempt`).

3. **Durante un Intento**:
   - Si `is_attempt` es `True`:
     - **Verificación de Corrección**: Si el intento es correcto (`is_correct` es `True`) y `self.correct_state` es `False`, se marca `self.correct_state` como `True`.

#### Retroalimentación y Visualización

- **Mostrar Retroalimentación**: Se proporciona retroalimentación visual basada en el estado de intento actual mediante `self.show_feedback(is_attempt)`.
- **Dibujo de Predicciones**: Se llama a `self.draw_predictions_on_image(frame, keypoints_with_scores)` para dibujar los puntos clave y las conexiones sobre el cuadro original.
- **Mostrar Imagen**: Se muestra el cuadro procesado con las predicciones superpuestas. 



## Controllers:



### Sentadilla Controller:

**Descripcion:**

El Sentadilla Controller es un controlador que usa el sistema para analizar y evaluar la correcta ejecución de las sentadillas, un ejercicio fundamental para el fortalecimiento de piernas y glúteos. Este sistema utiliza un modelo de detección de poses basado en TensorFlow Lite y una cámara para capturar los movimientos del usuario. Su objetivo es garantizar que las sentadillas se realicen con la técnica adecuada para maximizar los beneficios y reducir el riesgo de lesiones.

Incluye funciones para verificar varios aspectos de la ejecución de las sentadillas. Por ejemplo, verifica la profundidad de la sentadilla, asegurando que la cadera descienda al menos hasta la altura de las rodillas. También verifica el ángulo de la cadera, asegurando que esté por debajo de los 90 grados, y el ángulo de las rodillas, para garantizar una alineación adecuada y evitar tensiones innecesarias en las articulaciones.
...

<p align="center">
  <img src="docs/sentadilla/example.png" alt="Ejemplo Sentadilla" width="600px" />
</p>

#### Funciones:

- **Verificación Completa de la Sentadilla:**

    Esta función analiza exhaustivamente la ejecución de la sentadilla, evaluando diversos aspectos como la profundidad, la alineación de la cadera y las rodillas, y la distribución del peso corporal. Si todos los criterios se satisfacen, se determina que la sentadilla se ha realizado correctamente.

    ```python
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

    ```

- **Verificar Intento de Sentadilla:**
    Esta función determina si el usuario está intentando realizar una sentadilla, evaluando la posición de las articulaciones relevantes, como las caderas, rodillas y tobillos. Se basa en la detección de un ángulo específico en las rodillas y la distancia entre los hombros y las rodillas para identificar el intento de realizar el ejercicio.

    ```python
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
    ```

- **Verificar Profundidad de la Sentadilla:**
    Esta función comprueba si la profundidad de la sentadilla es adecuada, considerando la diferencia vertical entre las caderas y las rodillas cuando se flexionan. Se establece un umbral mínimo para garantizar que la sentadilla alcance una profundidad suficiente para ser efectiva.

    ```python
    def check_depth_squat(self, keypoints):
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]

        # Toma en cuenta el eje y para determinar la profundidad de la sentadilla, la diferencia entre la cadera y la rodilla cuando se flexiona debe ser menor a 0.1
        left_y_diff = abs(left_hip[1] - left_knee[1])
        right_y_diff = abs(right_hip[1] - right_knee[1])

        return left_y_diff < 0.1 and right_y_diff < 0.1

    ```

- **Verificar Ángulo de la Cadera:**
    Esta función verifica que el ángulo formado por la cadera, la rodilla y el tobillo esté dentro de un rango óptimo durante la ejecución de la sentadilla. Un ángulo de cadera apropiado es fundamental para mantener una postura correcta y prevenir lesiones.

    ```python
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
    ```

- **Verificar Ángulo de las Rodillas:**
    Esta función evalúa el ángulo formado por la articulación de la cadera, la rodilla y el tobillo para cada pierna durante la sentadilla. Un ángulo de rodilla adecuado es esencial para garantizar una distribución equilibrada del peso corporal y evitar tensiones indebidas en las articulaciones.

    ```python
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
    ```

- **Calcular Puntuación de Ejecución:**
    Esta función calcula una puntuación que refleja la calidad de la ejecución de la sentadilla, basada en la precisión de los ángulos de las articulaciones y otros factores relevantes. La puntuación proporciona una medida objetiva del rendimiento del usuario durante el ejercicio.

    ```python
    def calculate_score(self, angle):
        return (1 - abs(90 - angle) / 90) * 100
    ```

- **Calcular Puntuación y Color:**
    Esta función determina el color de las indicaciones visuales mostradas al usuario durante la evaluación de la sentadilla, en función de la puntuación obtenida.

    ```python
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
    ```

- **Crear Indicaciones Visuales:**
    Esta función genera indicaciones visuales para guiar al usuario durante la realización de la sentadilla, incluyendo información sobre la precisión de la ejecución y posibles correcciones que se deben realizar. Las indicaciones se presentan de manera intuitiva para facilitar la comprensión y el seguimiento del usuario.
    ```python
    def create_indications(self, score_percent, color, correct_hip_angle, correct_knee_angle):
        return [
            {"name": "Precision: " + str(round(score_percent, 2)) + "%", "color": color },
            {"name": "Cadera correcta" if correct_hip_angle else "Corrige Cadera", "color": "green" if correct_hip_angle else "red"},
            {"name": "Rodilla correcta" if correct_knee_angle else "Agachate Mas", "color": "green" if correct_knee_angle else "red"}
        ]
    ```





### Estocada Controller:

**Descripción:**

El Estocada Controller es un sistema diseñado para analizar y evaluar la correcta ejecución de las estocadas, un ejercicio común en entrenamientos de fuerza y acondicionamiento físico. Este sistema utiliza un modelo de detección de poses basado en TensorFlow Lite y una cámara para capturar los movimientos del usuario, asegurando que las estocadas se realicen con la técnica adecuada para maximizar los beneficios y minimizar el riesgo de lesiones.

<p align="center">
  <img src="docs/estocada/example.png" alt="Ejemplo Estocada" width="600px" />
</p>

#### Funciones:

- **Verificar Ejercicio Completo:**

  Esta función verifica si la ejecución de la estocada es correcta evaluando varios factores como los ángulos de las rodillas y el desplazamiento horizontal de las piernas. Si todas las condiciones se cumplen, se considera que la estocada está bien realizada.

  ```python
  def check_exercise(self, keypoints):
      left_hip, left_knee, left_ankle = keypoints[11][:2], keypoints[13][:2], keypoints[15][:2]
      right_hip, right_knee, right_ankle = keypoints[12][:2], keypoints[14][:2], keypoints[16][:2]

      front_leg_knee_angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
      front_leg_knee_angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

      back_leg_angle_left = self.calculate_angle(right_knee, left_knee, left_ankle)
      back_leg_angle_right = self.calculate_angle(left_knee, right_knee, right_ankle)

      horizontal_displacement = abs(left_knee[1] - right_knee[1])
      sufficient_displacement = self.check_sufficient_displacement(horizontal_displacement)

      correct_front_leg_angle_left = self.check_front_leg_angle(front_leg_knee_angle_left)
      correct_front_leg_angle_right = self.check_front_leg_angle(front_leg_knee_angle_right)

      correct_back_leg_angle_right = self.check_back_leg_angle(back_leg_angle_right)
      correct_back_leg_angle_left = self.check_back_leg_angle(back_leg_angle_left)

      correct_position_left = correct_front_leg_angle_left and correct_back_leg_angle_right
      correct_position_right = correct_front_leg_angle_right and correct_back_leg_angle_left

      score_left = self.calculate_score(front_leg_knee_angle_left)
      score_right = self.calculate_score(front_leg_knee_angle_right)

      score_percent, color = self.calculate_score_and_color(score_left, score_right)

      indications = self.create_indications(score_percent, color, correct_position_left, correct_position_right,
                                          correct_front_leg_angle_left, correct_front_leg_angle_right,
                                          correct_back_leg_angle_right, correct_back_leg_angle_left)

      self.show_indications(indications)

      return (correct_position_left or correct_position_right) and sufficient_displacement
  ```

- **Verificar Desplazamiento Suficiente:**

  Esta función asegura que el desplazamiento horizontal entre las rodillas sea suficiente para considerar que la estocada se realizó correctamente.

  ```python
  def check_sufficient_displacement(self, displacement):
      return displacement > 0.05
  ```

- **Verificar Ángulo de la Pierna Delantera:**

  Esta función verifica si el ángulo de la rodilla de la pierna delantera está dentro del rango correcto.

  ```python
  def check_front_leg_angle(self, angle):
      return 70 <= angle <= 120
  ```

- **Verificar Ángulo de la Pierna Trasera:**

  Esta función verifica si el ángulo de la rodilla de la pierna trasera está dentro del rango correcto.

  ```python
  def check_back_leg_angle(self, angle):
      return angle > 130
  ```

- **Calcular Puntuación:**

  Esta función calcula una puntuación basada en la diferencia del ángulo de la rodilla de la pierna delantera respecto al ideal de 90 grados.

  ```python
  def calculate_score(self, angle):
      return (1 - abs(90 - angle) / 90) * 100
  ```

- **Calcular Puntuación Promedio:**

  Esta función calcula la puntuación promedio de ambos ángulos de las rodillas de las piernas delanteras y determina el color asociado a esa puntuación.

  ```python
  def calculate_score_and_color(self, score_left, score_right):
      score = np.mean([score_left, score_right])
      score_percent = score if score >= 0 else 0

      if score >= 80:
          color = "blue"
      elif 1 <= score <= 80:
          color = "green"
      else:
          color = "red"

      return score_percent, color
  ```

- **Crear Sugerencias:**

  Esta función crea una lista de indicaciones basadas en la precisión y la posición correcta de las piernas.

  ```python
  def create_indications(self, score_percent, color, correct_position_left, correct_position_right,
                      correct_front_leg_angle_left, correct_front_leg_angle_right,
                      correct_back_leg_angle_right, correct_back_leg_angle_left):
      return [
          {"name": "Precisión: " + str(round(score_percent, 2)) + "%", "color": color},
          {"name": "Piernas dobladas" if correct_position_left or correct_position_right else "Doble las piernas", "color": "green" if correct_position_left or correct_position_right else "red"},
          {"name": "Pierna delantera" if correct_front_leg_angle_left or correct_front_leg_angle_right else "Doble pierna delantera", "color": "green" if correct_front_leg_angle_left or correct_front_leg_angle_right else "red"},
          {"name": "Pierna trasera" if correct_back_leg_angle_right or correct_back_leg_angle_left else "Doble pierna trasera", "color": "green" if correct_back_leg_angle_right or correct_back_leg_angle_left else "red"}
      ]
  ```

### Polichinela Controller:

**Descripción:**

El Polichinela Controller es un sistema diseñado para analizar y evaluar la correcta ejecución de los saltos de tijera (jumping jacks) o polichinela, un ejercicio aeróbico popular. Utiliza un modelo de detección de poses basado en TensorFlow Lite y una cámara para capturar los movimientos del usuario, asegurando que los saltos de tijera se realicen con la técnica adecuada para maximizar los beneficios y minimizar el riesgo de lesiones.

<p align="center">
  <img src="docs/polichinela/example.png" alt="Ejemplo Estocada" width="600px" />
</p>

#### Funciones:

- **Calcular Distancia:**

  Esta función calcula la distancia euclidiana entre dos puntos, que en este contexto son las coordenadas de los puntos clave del cuerpo.

  ```python
  def calculate_distance(self, point1, point2):
      return np.linalg.norm(np.array(point1) - np.array(point2))
  ```

- **Verificar Ejercicio Completo:**

  Esta función verifica si la ejecución de los saltos de tijera es correcta evaluando las distancias entre los tobillos y el movimiento vertical de las muñecas, utilizando tanto umbrales estrictos como tolerantes.

  ```python
  def check_exercise(self, keypoints):
      # Define threshold distances for the exercise
      ankle_distance_threshold = 0.05
      wrist_vertical_threshold = 0.05
      ankle_distance_tolerance = 0.07
      wrist_vertical_tolerance = 0.07

      # Get the coordinates of the ankles and wrists
      left_ankle, right_ankle = keypoints[15][:2], keypoints[16][:2]
      left_wrist, right_wrist = keypoints[9][:2], keypoints[10][:2]

      # Calculate the distance between the ankles and the vertical movement of the wrists
      ankle_distance = self.calculate_distance(left_ankle, right_ankle)
      left_wrist_vertical_movement = abs(left_wrist[0])
      right_wrist_vertical_movement = abs(right_wrist[0])

      # Check the state of the exercise with original and tolerant thresholds
      is_correct = self.is_exercise_correct(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_threshold, wrist_vertical_threshold)
      is_correct_tolerant = self.is_exercise_correct(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_tolerance, wrist_vertical_tolerance)

      # Calculate scores based on original and tolerant thresholds
      score = self.calculate_score(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_threshold, wrist_vertical_threshold)
      score_tolerant = self.calculate_score(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_tolerance, wrist_vertical_tolerance)

      # Determine the final score percent and color
      score_percent = max(score, score_tolerant) if max(score, score_tolerant) >= 0 else 0
      color = self.determine_color(score_percent)

      # Create the indications with descriptive messages
      indications = self.create_indications(score_percent, color, is_correct, is_correct_tolerant, wrist_vertical_threshold, left_wrist_vertical_movement, right_wrist_vertical_movement)

      self.show_indications(indications)
      return is_correct
  ```

- **Verificar Ejercicio Correcto:**

  Esta función verifica si las distancias entre los tobillos y el movimiento vertical de las muñecas cumplen con los umbrales especificados.

  ```python
  def is_exercise_correct(self, ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_threshold, wrist_threshold):
      return (ankle_distance > ankle_threshold) and (left_wrist_vertical_movement < wrist_threshold or right_wrist_vertical_movement < wrist_threshold)
  ```

- **Calcular Puntuación:**

  Esta función calcula una puntuación basada en la distancia entre los tobillos y el movimiento vertical de las muñecas, en relación con los umbrales dados.

  ```python
  def calculate_score(self, ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_threshold, wrist_threshold):
      score_ankle_distance = min((ankle_distance / ankle_threshold) * 100, 100)
      score_wrist_vertical_movement = min((wrist_threshold - min(left_wrist_vertical_movement, right_wrist_vertical_movement)) / wrist_threshold * 100, 100)
      return np.mean([score_ankle_distance, score_wrist_vertical_movement])
  ```

- **Determinar Color:**

  Esta función determina el color asociado a la puntuación calculada para proporcionar una retroalimentación visual clara.

  ```python
  def determine_color(self, score_percent):
      if score_percent > 80:
          return "blue"
      elif 1 <= score_percent <= 80:
          return "green"
      else:
          return "red"
  ```

- **Crear Indicaciones:**

  Esta función crea una lista de indicaciones basadas en la precisión y la posición correcta de las piernas y brazos durante el ejercicio.

  ```python
  def create_indications(self, score_percent, color, is_correct, is_correct_tolerant, wrist_vertical_threshold, left_wrist_vertical_movement, right_wrist_vertical_movement):
      return [
          {"name": "Precisión: " + str(round(score_percent, 2)) + "%", "color": color},
          {"name": "Piernas estiradas" if is_correct or is_correct_tolerant else "Estira piernas", "color": "green" if is_correct or is_correct_tolerant else "red"},
          {"name": "Brazos estirados" if left_wrist_vertical_movement < wrist_vertical_threshold or right_wrist_vertical_movement < wrist_vertical_threshold else "Levante los brazos", "color": "green" if left_wrist_vertical_movement < wrist_vertical_threshold or right_wrist_vertical_movement < wrist_vertical_threshold else "red"}
      ]
  ```
### **Curl Bicep Controller**

El Controlador de Curl de Bíceps es un componente crucial en un sistema de asistencia para ejercicios físicos basado en visión por computadora. Este informe detalla su diseño, funcionamiento y los criterios utilizados para evaluar la postura del usuario durante el ejercicio.
<p align="center">
  <img src="docs/bicep/bicep_star.png" alt="Ejemplo Estocada" width="600px" />
</p>

#### Diseño del Controlador

El Controlador de Curl de Bíceps se implementa en Python, utilizando el modelo TFLite para la detección de puntos clave (keypoints) del cuerpo humano. La detección de postura y la retroalimentación visual se llevan a cabo en tiempo real, permitiendo una corrección inmediata durante la ejecución del ejercicio.

#### Funcionamiento

El controlador sigue un proceso secuencial durante la ejecución del ejercicio:

##### 1. Inicialización

El controlador se inicializa con la ruta del modelo y el vídeo de detección.

```python
class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__(model_path="resources/models/model.tflite", video_path="detection/flexion.mp4")
        # Otros atributos y configuraciones
```

##### 2. Incio del ejercicio

La función `check_temp` se encarga de verificar si el usuario está en la posición inicial del ejercicio de curl de bíceps. Comprueba si los keypoints detectados muestran una postura inicial válida.

```python
def check_temp(self, keypoints):
    curl_angle_left, curl_angle_right = self.check_curl_angles(keypoints)

        is_attempt_left = curl_angle_left <= self.attempt_angle_threshold
        is_attempt_right = curl_angle_right <= self.attempt_angle_threshold

        return is_attempt_left or is_attempt_right
```

##### 3. Criterios de Verificación

La función `check_exercise` evalúa si el usuario está realizando correctamente el ejercicio de curl de bíceps. Para ello, verifica varios criterios, incluyendo:
```python
def check_exercise(self, keypoints):
    # Verifica la ejecución correcta del ejercicio de curl de bíceps
```
###### 3.1 Alineación de la Espalda: 

Otro aspecto crucial de la verificación implica evaluar los ángulos entre los keypoints de los hombros, caderas y tobillos. Esta evaluación permite determinar si la espalda del usuario se mantiene recta durante la ejecución del ejercicio. Se considera que la espalda está alineada de manera adecuada si los ángulos entre los keypoints de los hombros, caderas y tobillos están dentro de un rango establecido y aceptable. Esto es vital para prevenir lesiones y garantizar una postura correcta durante el ejercicio.
```python
...
        back_straight_left = 150 <= back_angle_left <= 180
        back_straight_right = 150 <= back_angle_right <= 180
...
```

###### 3.2 Ángulos de Curl de Bíceps

 En esta etapa, se calculan los ángulos entre los keypoints correspondientes a los hombros, codos y muñecas tanto izquierdo como derecho. Estos ángulos son fundamentales para determinar la adecuación del movimiento del brazo durante el ejercicio. Se considera que el ejercicio es ejecutado correctamente si los ángulos de curl de bíceps son menores o iguales al umbral establecido (exercise_angle_threshold). Esto garantiza una ejecución precisa y efectiva del ejercicio.

   
```python
...
      is_correct = (curl_angle_left <= self.exercise_angle_threshold and 
      curl_angle_right <= self.exercise_angle_threshold and 
      back_straight_left and back_straight_right)

....
```
###### 3.3 Cálculo del Puntaje de Precisión

Este código evalúa la precisión en la ejecución del ejercicio de curl de bíceps. Para cada brazo, los puntajes de precisión `score_left y score_right` se calculan restando el ángulo de curl medido del umbral establecido, dividiendo esta diferencia por el umbral y restando el resultado de 1. El puntaje final se determina promediando estos puntajes para ambos brazos `score`. Además, se garantiza que el puntaje final esté dentro del rango de 0 a 100 `score_percent`, lo que proporciona una evaluación clara de la técnica del usuario y facilita el monitoreo y la mejora de la ejecución del ejercicio.
  ```python
  score_left = (1 - abs(self.exercise_angle_threshold - curl_angle_left) / self.exercise_angle_threshold) * 100
        score_right = (1 - abs(self.exercise_angle_threshold - curl_angle_right) / self.exercise_angle_threshold) * 100
        score = np.mean([score_left, score_right])
        score_percent = score if score >= 0 else 0
  ```
##### 4. Generación del FeedBack

La función `generate_indications` se encarga de generar las indicaciones visuales basadas en los resultados de la evaluación del ejercicio. Las indicaciones incluyen información sobre la precisión del movimiento, la alineación de la espalda y la ejecución correcta de los curls de bíceps.

```python
indications = [
            {"name": "Precision: " + str(round(score_percent, 2)) + "%", "color": self.determine_color(score_percent)},
            {"name": "Espalda recta" if back_straight_left and back_straight_right else "Corrige espalda", "color": "green" if back_straight_left and back_straight_right else "red"},
            {"name": "Curl brazo izquierdo" if curl_angle_left <= self.exercise_angle_threshold else "Corrige brazo izquierdo", "color": "green" if curl_angle_left <= self.exercise_angle_threshold else "red"},
            {"name": "Curl brazo derecho" if curl_angle_right <= self.exercise_angle_threshold else "Corrige brazo derecho", "color": "green" if curl_angle_right <= self.exercise_angle_threshold else "red"}
        ]
        return indications
```
Determinar Color

  Esta función determina el color asociado a la puntuación calculada para proporcionar una retroalimentación visual clara.

  ```python
  def determine_color(self, score_percent):
      if score_percent > 80:
          return "blue"
      elif 1 <= score_percent <= 80:
          return "green"
      else:
          return "red"
  ```

Estas funciones del Controlador de Curl de Bíceps trabajan en conjunto para proporcionar una evaluación detallada de la postura y la ejecución del ejercicio. La función `check_exercise` utiliza criterios específicos para verificar la correcta realización del curl de bíceps, mientras que `generate_indications` se encarga de proporcionar retroalimentación visual al usuario.

#### Resultado
##### Correcto
<p align="center">
  <img src="docs/bicep/bicep_correct.png" alt="Ejemplo Estocada" width="600px" />
</p>

##### Incorrecto
<p align="center">
  <img src="docs/bicep/bicep_incorrect.png" alt="Ejemplo Estocada" width="600px" />
</p>