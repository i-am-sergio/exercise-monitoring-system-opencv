#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>

// Path to the TFLite model
const char* model_path = "model.tflite";

// Define the connections between the keypoints
const std::vector<std::pair<int, int>> KEYPOINT_EDGES = {
    {0, 1}, {0, 2}, {1, 3}, {2, 4}, {0, 5}, {0, 6}, {5, 7},
    {7, 9}, {6, 8}, {8, 10}, {5, 6}, {5, 11}, {6, 12}, {11, 12}, {11, 13},
    {13, 15}, {12, 14}, {14, 16}
};

cv::Scalar COLOR1 = cv::Scalar(255, 31, 135); // purple
cv::Scalar COLOR2 = cv::Scalar(36, 204, 242); // yellow
cv::Scalar COLOR3 = cv::Scalar(26, 240, 126); // lemon

// Define the colors for the connections
const std::vector<cv::Scalar> EDGE_COLORS = {
    COLOR2, COLOR1, COLOR2,
    COLOR1, COLOR2, COLOR1,
    COLOR2, COLOR2, COLOR1,
    COLOR1, COLOR3, COLOR2,
    COLOR1, COLOR3, COLOR2,
    COLOR3, COLOR1, COLOR1
};

// Function to process a frame
std::vector<float> process_frame(const cv::Mat& frame, tflite::Interpreter* interpreter, int input_index, int output_index, const TfLiteTensor* input_tensor) {
    // Resize the frame to match the input shape of the model
    cv::Mat input_image;
    cv::resize(frame, input_image, cv::Size(input_tensor->dims->data[2], input_tensor->dims->data[1]));

    // Convert the frame to uint8
    input_image.convertTo(input_image, CV_8U);

    // Add a dimension to the frame
    std::vector<int> input_shape = {1, input_tensor->dims->data[1], input_tensor->dims->data[2], input_tensor->dims->data[3]};
    interpreter->ResizeInputTensor(input_index, input_shape);
    interpreter->AllocateTensors();

    // Copy the frame data to the input tensor
    memcpy(interpreter->typed_input_tensor<uint8_t>(input_index), input_image.data, input_image.total() * input_image.elemSize());

    // Run inference
    interpreter->Invoke();

    // Get the keypoints with scores
    const TfLiteTensor* output_tensor = interpreter->tensor(output_index);
    std::vector<float> keypoints_with_scores(output_tensor->data.f, output_tensor->data.f + output_tensor->bytes / sizeof(float));
    // print the keypoints with scores
    // for (float score : keypoints_with_scores) {
    //     std::cout << score << "\n";
    // }
    return keypoints_with_scores;
}

// Function to draw keypoints and edges on the image
cv::Mat draw_predictions_on_image(cv::Mat& image, const std::vector<float>& keypoints_with_scores, float keypoint_threshold = 0.11) {
    int height = image.rows;
    int width = image.cols;

    for (size_t idx = 0; idx < KEYPOINT_EDGES.size(); ++idx) {
        auto [start, end] = KEYPOINT_EDGES[idx];
        cv::Scalar color = EDGE_COLORS[idx];

        float start_score = keypoints_with_scores[start * 3 + 2];
        float end_score = keypoints_with_scores[end * 3 + 2];

        if (start_score > keypoint_threshold && end_score > keypoint_threshold) {
            cv::Point start_point(static_cast<int>(keypoints_with_scores[start * 3 + 1] * width),
                                  static_cast<int>(keypoints_with_scores[start * 3] * height));
            cv::Point end_point(static_cast<int>(keypoints_with_scores[end * 3 + 1] * width),
                                static_cast<int>(keypoints_with_scores[end * 3] * height));
            cv::line(image, start_point, end_point, color, 2);
        }
    }

    for (size_t i = 0; i < keypoints_with_scores.size() / 3; ++i) {
        float score = keypoints_with_scores[i * 3 + 2];
        if (score > keypoint_threshold) {
            cv::Point center(static_cast<int>(keypoints_with_scores[i * 3 + 1] * width),
                             static_cast<int>(keypoints_with_scores[i * 3] * height));
            cv::circle(image, center, 3, cv::Scalar(0, 0, 255), -1);
        }
    }
    
    return image;
}


int main() {
    // Load the TFLite model
    std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile(model_path);
    if (!model) {
        std::cerr << "Failed to load model\n";
        return -1;
    }

    // Build the interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    tflite::InterpreterBuilder(*model, resolver)(&interpreter);
    if (!interpreter) {
        std::cerr << "Failed to build interpreter\n";
        return -1;
    }

    // Allocate tensors
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        std::cerr << "Failed to allocate tensors\n";
        return -1;
    }

    // Get input and output tensor details
    int input_index = interpreter->inputs()[0];
    int output_index = interpreter->outputs()[0];
    const TfLiteTensor* input_tensor = interpreter->tensor(input_index);

    // Video path
    const char* video_path = "sentadilla.mp4";

    // Capture video from the camera
    cv::VideoCapture cap(video_path);
    if (!cap.isOpened()) {
        std::cerr << "Error opening video file\n";
        return -1;
    }

    std::cout<<" Todo bien hasta aqui"<< std::endl;

    while (true) {
        // Read a frame
        cv::Mat frame;
        cap >> frame;
        if (frame.empty()) {
            break;
        }

        // Convert the frame to RGB
        cv::Mat frame_rgb;
        cv::cvtColor(frame, frame_rgb, cv::COLOR_BGR2RGB);

        // Process the frame
        std::vector<float> keypoints_with_scores = process_frame(frame_rgb, interpreter.get(), input_index, output_index, input_tensor);

        // Draw the keypoints and edges on the frame
        cv::Mat processed_frame = draw_predictions_on_image(frame, keypoints_with_scores);

        // Show the processed frame
        cv::imshow("pose estimation", processed_frame);

        // Exit the loop if the 'q' key is pressed or if clicked on the close button
        if (cv::waitKey(1) == 'q') {
            break;
        }
        
    }

    // Release the video capture and close windows
    cap.release();
    cv::destroyAllWindows();

    return 0;
}