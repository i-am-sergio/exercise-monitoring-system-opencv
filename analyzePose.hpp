#ifndef ANALYZE_POSE_H
#define ANALYZE_POSE_H

#include <opencv2/core.hpp>
#include <opencv2/dnn.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <string>
#include <iostream>

using namespace cv;
using namespace cv::dnn;
using namespace std;

const int POSE_PAIRS[20][2] = {
    {1, 2}, {1, 5}, {2, 3}, {3, 4}, {5, 6}, {6, 7}, {1, 8}, {8, 9}, {9, 10}, {1, 11}, {11, 12}, {12, 13}, {1, 0}, {0, 14}, {14, 16}, {0, 15}, {15, 17}};

Mat analyzePose(const string &imgW, int W_in, int H_in, float thresh, float scale)
{
    String modelTxt = "pose_deploy_linevec.prototxt";
    String modelBin = "pose_iter_440000.caffemodel";
    String imageFile = imgW;
    String dataset = "COCO";
    int npairs = 17;
    int nparts = 18;

    Net net = readNet(modelBin, modelTxt);
    Mat img = imread(imageFile);
    if (img.empty())
    {
        cerr << "Can't read image from the file: " << imageFile << endl;
        exit(-1);
    }
    Mat inputBlob = blobFromImage(img, scale, Size(W_in, H_in), Scalar(0, 0, 0), false, false);
    net.setInput(inputBlob);
    Mat result = net.forward();
    int H = result.size[2];
    int W = result.size[3];
    vector<Point> points(nparts);
    for (int n = 0; n < nparts; n++)
    {
        Mat heatMap(H, W, CV_32F, result.ptr(0, n));
        Point p(-1, -1), pm;
        double conf;
        minMaxLoc(heatMap, 0, &conf, 0, &pm);
        if (conf > thresh)
            p = pm;
        points[n] = p;
    }
    float SX = float(img.cols) / W;
    float SY = float(img.rows) / H;
    for (int n = 0; n < npairs; n++)
    {
        Point2f a = points[POSE_PAIRS[n][0]];
        Point2f b = points[POSE_PAIRS[n][1]];
        if (a.x <= 0 || a.y <= 0 || b.x <= 0 || b.y <= 0)
            continue;
        a.x *= SX;
        a.y *= SY;
        b.x *= SX;
        b.y *= SY;
        line(img, a, b, Scalar(0, 200, 0), 2);
        circle(img, a, 3, Scalar(0, 0, 200), -1);
        circle(img, b, 3, Scalar(0, 0, 200), -1);
    }
    return img;
}

#endif // ANALYZE_POSE_H