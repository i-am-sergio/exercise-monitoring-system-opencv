#include <iostream>
#include <opencv2/opencv.hpp>
#include "opencv2/highgui/highgui.hpp"

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
        imshow("Webcam", frame);
        if (waitKey(30) == 'q') // Esperar 30 ms y salir si se presiona la tecla 'q'
        {
            break;
        }
    }
    cap.release();
    destroyAllWindows();
    return 0;
}
