#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
    // Load the image
    string path = "img/image.png";
    Mat src = imread(path);

    if (src.empty()) {
        cout << "Could not open or find the image!" << endl;
        return -1;
    }

    // Convert to grayscale
    Mat gray;
    cvtColor(src, gray, COLOR_BGR2GRAY);

    // Apply Canny edge detection
    Mat edges;
    Canny(gray, edges, 50, 150, 3);

    // Use Hough Line Transform to detect lines
    vector<Vec2f> lines;
    HoughLines(edges, lines, 1, CV_PI / 180, 200);

    // Draw the lines on the original image
    for (size_t i = 0; i < lines.size(); i++) {
        float rho = lines[i][0];
        float theta = lines[i][1];
        double a = cos(theta), b = sin(theta);
        double x0 = a * rho, y0 = b * rho;
        Point pt1(cvRound(x0 + 1000 * (-b)), cvRound(y0 + 1000 * a));
        Point pt2(cvRound(x0 - 1000 * (-b)), cvRound(y0 - 1000 * a));
        line(src, pt1, pt2, Scalar(0, 0, 255), 2, LINE_AA);
    }

    // Display the result
    imshow("Hough Line Detection", src);
    waitKey(0);
    return 0;
}
