#include <iostream>
#include <opencv2/opencv.hpp>
#include "opencv2/highgui/highgui.hpp"
#include "analyzePose.hpp"
using namespace cv;
using namespace std;

int main()
{
    VideoCapture cap;
    if (!cap.open(0)) // Intentar abrir la cámara frontal (usualmente 1)
    {
        if (!cap.open(0))
        {
            cout << "Error al abrir la cámara!" << endl;
            return -1;
        }
    }
    namedWindow("Webcam", WINDOW_AUTOSIZE);
    while (true)
    {
        Mat frame;
        cap >> frame;
        if (frame.empty())
        {
            cout << "No se puede capturar el frame!" << endl;
            break;
        }
        int W_in = 368;         // Ancho para el preprocesamiento de la imagen
        int H_in = 368;         // Alto para el preprocesamiento de la imagen
        float thresh = 0.1;     // Umbral de confianza para el mapa de calor
        float scale = 0.003922; // Escala para el blob
        Mat result = analyzePose(frame, W_in, H_in, thresh, scale);
        imshow("Webcam", result);
        if (waitKey(30) == 'q') // Esperar 30 ms y salir si se presiona la tecla 'q'
        {
            break;
        }
    }
    cap.release();
    destroyAllWindows();
    return 0;
}
