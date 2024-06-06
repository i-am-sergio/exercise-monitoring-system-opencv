import cv2
imagen = cv2.imread('./media/fit1.jpg') 
print(imagen.shape)
cv2.imshow('Logo OpenCV',imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()