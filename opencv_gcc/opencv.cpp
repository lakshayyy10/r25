#include <opencv2/opencv.hpp>
#include <iostream>
int main() {
    // Open the default camera (usually the webcam)
    cv::VideoCapture cap(0); 
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open camera!" << std::endl;
        return -1;
    }

    cv::Mat frame, flippedFrame;

    // Capture a frame from the camera
    cap >> frame;

    // Check if frame is empty
    if (frame.empty()) {
        std::cerr << "Error: Could not capture image!" << std::endl;
        return -1;
    }

    // Flip the image vertically (change flipCode as needed)
    cv::flip(frame, flippedFrame, -1);

    // Display the original and flipped images
    cv::imshow("Original Image", frame);
    cv::imshow("Flipped Image", flippedFrame);

    // Wait until a key is pressed
    cv::waitKey(0);

    // Optionally save the flipped image
    cv::imwrite("flipped_image.jpg", flippedFrame);

    // Release the camera
    cap.release();
    return 0;
}
