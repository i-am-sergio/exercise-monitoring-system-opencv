from detection.movenet_thunder import ShowWindow
import cv2


# Hereda de la clase ShowWindow
class AbdominalController(ShowWindow):
    def __init__(self):
        super().__init__()
    
    def __del__(self):
        super().__del__()
    
    def show(self):
        super().show()
        self.cap.release()
        cv2.destroyAllWindows()
    
    def calculate_reps(self):
        pass

    def calculate_time(self):
        pass

    def calculate_speed(self):
        pass


