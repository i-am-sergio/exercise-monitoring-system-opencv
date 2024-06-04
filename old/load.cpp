#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <iostream>

using namespace cv;
using namespace std;
using namespace cv::dnn;

const int inWidth = 368;
const int inHeight = 368;
const float thr = 0.2;

const std::map<std::string, int> BODY_PARTS = { {"Nose", 0}, {"Neck", 1}, {"RShoulder", 2}, {"RElbow", 3}, {"RWrist", 4},
                                                {"LShoulder", 5}, {"LElbow", 6}, {"LWrist", 7}, {"RHip", 8}, {"RKnee", 9},
                                                {"RAnkle", 10}, {"LHip", 11}, {"LKnee", 12}, {"LAnkle", 13}, {"REye", 14},
                                                {"LEye", 15}, {"REar", 16}, {"LEar", 17}, {"Background", 18} };

const std::vector<std::pair<std::string, std::string>> POSE_PAIRS = { {"Neck", "RShoulder"}, {"Neck", "LShoulder"}, {"RShoulder", "RElbow"},
                                                                      {"RElbow", "RWrist"}, {"LShoulder", "LElbow"}, {"LElbow", "LWrist"},
                                                                      {"Neck", "RHip"}, {"RHip", "RKnee"}, {"RKnee", "RAnkle"}, {"Neck", "LHip"},
                                                                      {"LHip", "LKnee"}, {"LKnee", "LAnkle"}, {"Neck", "Nose"}, {"Nose", "REye"},
                                                                      {"REye", "REar"}, {"Nose", "LEye"}, {"LEye", "LEar"} };

Mat poseEstimation(Mat& frame, Net& net) {
    int frameWidth = frame.cols;
    int frameHeight = frame.rows;
    Mat inputBlob = blobFromImage(frame, 1.0, Size(inWidth, inHeight), Scalar(127.5, 127.5, 127.5), true, false);
    net.setInput(inputBlob);

    Mat out = net.forward();
    out = out.reshape(1, { out.size[1], out.size[2], out.size[3] });

    vector<Point> points(BODY_PARTS.size());

    for (int i = 0; i < BODY_PARTS.size(); ++i) {
        Mat heatMap(out.size[2], out.size[3], CV_32F, out.ptr(0, i));
        Point maxPoint;
        double conf;
        minMaxLoc(heatMap, 0, &conf, 0, &maxPoint);
        int x = (frameWidth * maxPoint.x) / out.size[3];
        int y = (frameHeight * maxPoint.y) / out.size[2];
        points[i] = (conf > thr) ? Point(x, y) : Point(-1, -1);
    }

    for (const auto& pair : POSE_PAIRS) {
        string partFrom = pair.first;
        string partTo = pair.second;
        int idFrom = BODY_PARTS.at(partFrom);
        int idTo = BODY_PARTS.at(partTo);

        if (points[idFrom] != Point(-1, -1) && points[idTo] != Point(-1, -1)) {
            line(frame, points[idFrom], points[idTo], Scalar(0, 255, 0), 3);
            circle(frame, points[idFrom], 3, Scalar(0, 0, 255), FILLED);
            circle(frame, points[idTo], 3, Scalar(0, 0, 255), FILLED);
        }
    }

    double t = (double)getTickCount();
    net.setInput(inputBlob);
    net.forward();
    t = ((double)getTickCount() - t) / getTickFrequency();
    putText(frame, format("%.2fms", t * 1000), Point(10, 20), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 0));

    return frame;
}

int main() {
    Net net = readNetFromTensorflow("graph_opt.pb");

    Mat img = imread("fit1.jpg");
    if (img.empty()) {
        cerr << "Image not found!" << endl;
        return -1;
    }

    cout << img.size << endl;

    Mat estimatedImage = poseEstimation(img, net);

    imshow("Pose Estimation", estimatedImage);
    waitKey(0);

    return 0;
}
