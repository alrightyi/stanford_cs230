# stanford_cs230
CS230 Deep Learning project

Use YOLOv2 model to detect qualified passenger vehicales in HOV lane in California.

Code adapted from Coursera assignment on YOLOv2:
https://www.coursera.org/learn/convolutional-neural-networks/notebook/bbBOL/car-detection-with-yolov2

Also updated yad2k from latest on Github:
https://github.com/allanzelener/YAD2K

How to run:

1) git clone https://github.com/alrightyi/stanford_cs230.git
2) 
virtualenv -p python3 .env

source .env/bin/activate

pip install -r requirements.txt

3) python yolo.py <image_file_name> from "images/" folder


Experiemented by changing number of classes, anchors in 


Datasets for Bumpers, Stickers are in "images/".

Attempting to use retrain_yolo.py to retrain the model to recognize bumpers and stickers, in addition to cars and persons.

Still no success yet.  Main issue is that the dataset does not have proper boxes.

Still WIP.


