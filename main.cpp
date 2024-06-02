#include "analyzePose.hpp"
#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/dnn.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
using namespace cv;
using namespace std;

int main(int argc, char **argv)
{
    int W_in = 368;
    int H_in = 368;
    float thresh = 0.1;
    float scale = 0.003922;
    auto estimated_image = analyzePose("fit1.jpg", W_in, H_in, thresh, scale);
    imshow("Estimated Image", estimated_image);
    waitKey(0);
    return 0;
}