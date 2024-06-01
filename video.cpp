#include <iostream>
#include <opencv2/opencv.hpp>
#include "opencv2/highgui/highgui.hpp"

using namespace cv;
using namespace std;

int main()
{
    VideoCapture cap;
    
    // Intentar abrir la cámara frontal (usualmente 1)
    if (!cap.open(1))
    {
        // Si no se puede abrir la cámara frontal, usar la cámara por defecto (0)
        if (!cap.open(0))
        {
            cout << "Error al abrir la cámara!" << endl;
            return -1;
        }
    }

    // Crear una ventana
    namedWindow("Webcam", WINDOW_AUTOSIZE);

    while (true)
    {
        Mat frame;
        // Capturar el frame
        cap >> frame;
        if (frame.empty())
        {
            cout << "No se puede capturar el frame!" << endl;
            break;
        }

        // Mostrar el frame en la ventana
        imshow("Webcam", frame);

        // Esperar 30 ms y salir si se presiona la tecla 'q'
        if (waitKey(30) == 'q')
        {
            break;
        }
    }

    // Liberar el objeto VideoCapture
    cap.release();
    // Destruir todas las ventanas
    destroyAllWindows();

    return 0;
}
