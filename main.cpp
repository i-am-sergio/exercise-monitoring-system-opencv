#include <iostream>
#include <opencv2/opencv.hpp>
#include "opencv2/highgui/highgui.hpp"

using namespace cv;
using namespace std;

int main()
{
    cout << CV_VERSION << endl;

    string location = "ichikanakano.jpg";

    Mat im = cv::imread(location, 1);
    if (im.empty())
    {
        cout << "Cannot open image!" << endl;
        return -1;
    }

    // Mostrar tamaño de la imagen en consola
    cout << im.size << endl;

    // Mostrar la imagen en una ventana
    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", im);

    // Esperar a que se presione una tecla
    waitKey(0);

    return 0;
}
