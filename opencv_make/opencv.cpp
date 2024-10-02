#include<opencv2/imgcodecs.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>
#include<iostream>
using namespace std;
using namespace cv;


int main(){
    string path = "img/cheese.png";
    Mat img = imread(path);
    imshow("Image",img);
    Mat flipimg;
    flip(img,flipimg,1);
    imshow("flippedimage",flipimg);
    waitKey(0);
}

