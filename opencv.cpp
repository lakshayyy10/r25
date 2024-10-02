#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;

int main() {
    VideoCapture cap(1);
    Mat img;
    while(true){
        cap.read(img);
        imshow("Image",img);
        waitKey(1);
    }
}