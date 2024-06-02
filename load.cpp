#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>

using namespace cv;
using namespace cv::dnn;

const int inWidth = 368;
const int inHeight = 368;
const float thr = 0.2;

const std::map<std::string, int> BODY_PARTS = {{"Nose", 0}, {"Neck", 1}, {"RShoulder", 2}, {"RElbow", 3}, {"RWrist", 4},
                                                {"LShoulder", 5}, {"LElbow", 6}, {"LWrist", 7}, {"RHip", 8}, {"RKnee", 9},
                                                {"RAnkle", 10}, {"LHip", 11}, {"LKnee", 12}, {"LAnkle", 13}, {"REye", 14},
                                                {"LEye", 15}, {"REar", 16}, {"LEar", 17}, {"Background", 18}};

const std::vector<std::vector<std::string>> POSE_PAIRS = {{"Neck", "RShoulder"}, {"Neck", "LShoulder"}, {"RShoulder", "RElbow"},
                                                          {"RElbow", "RWrist"}, {"LShoulder", "LElbow"}, {"LElbow", "LWrist"},
                                                          {"Neck", "RHip"}, {"RHip", "RKnee"}, {"RKnee", "RAnkle"}, {"Neck", "LHip"},
                                                          {"LHip", "LKnee"}, {"LKnee", "LAnkle"}, {"Neck", "Nose"}, {"Nose", "REye"},
                                                          {"REye", "REar"}, {"Nose", "LEye"}, {"LEye", "LEar"}};

cv::Mat pose_estimation(cv::Mat& frame, Net& net) {
    int frame_width = frame.cols;
    int frame_height = frame.rows;

    Mat blob = blobFromImage(frame, 1.0, Size(inWidth, inHeight), Scalar(127.5, 127.5, 127.5), true, false);
    net.setInput(blob);
    Mat out = net.forward();

    out = out(Rect(0, 0, 19, out.size[2]));  // MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(BODY_PARTS.size() == out.size[1]);

    std::vector<Point> points;

    for (int i = 0; i < BODY_PARTS.size(); i++) {
        Mat heat_map = out.col(i).reshape(1, out.size[2]);
        Point max_loc;
        double max_val;
        minMaxLoc(heat_map, nullptr, &max_val, nullptr, &max_loc);
        int x = static_cast<int>((frame_width * max_loc.x) / out.size[3]);
        int y = static_cast<int>((frame_height * max_loc.y) / out.size[2]);
        // Add a point if it's confidence is higher than threshold.
        if (max_val > thr)
            points.push_back(Point(x, y));
        else
            points.push_back(Point(-1, -1));  // Invalid point
    }

    for (const auto& pair : POSE_PAIRS) {
        std::string part_from = pair[0];
        std::string part_to = pair[1];
        int id_from = BODY_PARTS.at(part_from);
        int id_to = BODY_PARTS.at(part_to);

        if (points[id_from] != Point(-1, -1) && points[id_to] != Point(-1, -1)) {
            line(frame, points[id_from], points[id_to], Scalar(0, 255, 0), 3);
            circle(frame, points[id_from], 3, Scalar(0, 0, 255), -1);
            circle(frame, points[id_to], 3, Scalar(0, 0, 255), -1);
        }
    }

    return frame;
}

int main() {
    Net net = readNetFromTensorflow("graph_opt.pb");

    Mat img = imread("fit3.jpg");
    Mat estimated_image = pose_estimation(img, net);

    imshow("Estimated Image", estimated_image);
    waitKey(0);
    return 0;
}
