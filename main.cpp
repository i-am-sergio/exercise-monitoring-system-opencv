#include <opencv2/dnn.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>

using namespace cv;
using namespace cv::dnn;
using namespace std;

const int POSE_PAIRS[3][20][2] = {
    {// COCO body
     {1, 2},
     {1, 5},
     {2, 3},
     {3, 4},
     {5, 6},
     {6, 7},
     {1, 8},
     {8, 9},
     {9, 10},
     {1, 11},
     {11, 12},
     {12, 13},
     {1, 0},
     {0, 14},
     {14, 16},
     {0, 15},
     {15, 17}},
    {// MPI body
     {0, 1},
     {1, 2},
     {2, 3},
     {3, 4},
     {1, 5},
     {5, 6},
     {6, 7},
     {1, 14},
     {14, 8},
     {8, 9},
     {9, 10},
     {14, 11},
     {11, 12},
     {12, 13}},
    {
        // hand
        {0, 1},
        {1, 2},
        {2, 3},
        {3, 4}, // thumb
        {0, 5},
        {5, 6},
        {6, 7},
        {7, 8}, // pinkie
        {0, 9},
        {9, 10},
        {10, 11},
        {11, 12}, // middle
        {0, 13},
        {13, 14},
        {14, 15},
        {15, 16}, // ring
        {0, 17},
        {17, 18},
        {18, 19},
        {19, 20} // small
    }};

mutex mtx_capture;
mutex mtx_process;
condition_variable cv_frame;
queue<Mat> frame_queue;
queue<Mat> processed_queue;
bool stop = false;

void capture_frame(VideoCapture &cap) {
    while (true) {
        Mat frame;
        cap >> frame;
        if (frame.empty())
            break;
        {
            lock_guard<mutex> lock(mtx_capture);
            frame_queue.push(frame);
        }
        cv_frame.notify_all();
        this_thread::sleep_for(chrono::milliseconds(200)); // Espera 200ms (5 fps)
        if (stop) break;
    }
}

void process_frame(Net &net, const int W_in, const int H_in, const float scale, const float thresh) {
    while (true) {
        Mat frame;
        {
            unique_lock<mutex> lock(mtx_capture);
            cv_frame.wait(lock, []{ return !frame_queue.empty() || stop; });
            if (stop && frame_queue.empty()) break;
            frame = frame_queue.front();
            frame_queue.pop();
        }

        Mat inputBlob = blobFromImage(frame, scale, Size(W_in, H_in), Scalar(0, 0, 0), false, false);
        net.setInput(inputBlob);
        Mat result = net.forward();

        int H = result.size[2];
        int W = result.size[3];

        vector<Point> points(22);
        for (int n = 0; n < 18; n++)
        {
            Mat heatMap(H, W, CV_32F, result.ptr(0, n));
            Point p(-1, -1), pm;
            double conf;
            minMaxLoc(heatMap, 0, &conf, 0, &pm);
            if (conf > thresh)
                p = pm;
            points[n] = p;
        }

        float SX = float(frame.cols) / W;
        float SY = float(frame.rows) / H;
        for (int n = 0; n < 17; n++)
        {
            Point2f a = points[POSE_PAIRS[0][n][0]];
            Point2f b = points[POSE_PAIRS[0][n][1]];

            if (a.x <= 0 || a.y <= 0 || b.x <= 0 || b.y <= 0)
                continue;

            a.x *= SX;
            a.y *= SY;
            b.x *= SX;
            b.y *= SY;

            line(frame, a, b, Scalar(0, 200, 0), 2);
            circle(frame, a, 3, Scalar(0, 0, 200), -1);
            circle(frame, b, 3, Scalar(0, 0, 200), -1);
        }

        {
            lock_guard<mutex> lock(mtx_process);
            processed_queue.push(frame);
        }
    }
}

void display_frame() {
    while (true) {
        Mat frame;
        {
            unique_lock<mutex> lock(mtx_process);
            if (processed_queue.empty()) continue;
            frame = processed_queue.front();
            processed_queue.pop();
        }

        imshow("OpenPose", frame);
        if (waitKey(1) == 27) { // Presiona 'ESC' para salir
            stop = true;
            break;
        }
    }
}

int main(int argc, char **argv)
{
    const string modelTxt = "pose_deploy_linevec.prototxt";
    const string modelBin = "pose_iter_440000.caffemodel";
    const int W_in = 368;
    const int H_in = 368;
    const float thresh = 0.1;
    const float scale = 0.003922;

    Net net = readNet(modelBin, modelTxt);

    VideoCapture cap(0); // Abre la cámara predeterminada (0).
    if (!cap.isOpened())
    {
        cerr << "Error opening camera" << endl;
        return -1;
    }

    thread t1(capture_frame, ref(cap));
    thread t2(process_frame, ref(net), W_in, H_in, scale, thresh);
    thread t3(display_frame);

    t1.join();
    t2.join();
    t3.join();

    cap.release();
    destroyAllWindows();
    return 0;
}
