#Mememan-izator

**The project is hosted on [https://mememan-izator.herokuapp.com/](https://mememan-izator.herokuapp.com/)**

This is a simple project I made in order to improve my dash skills and to discover OpenCV.
This project is a web interface allowing a user to replace all the faces on an image by mememan's one.

In order to use this project locally, you can clone this repo then run:
```pip install -r requirements.txt```

It is possible to have a conflict when installing OpenCV (cv2), then I would recommend to remove ```opencv-python-headless==4.5.1.48``` from requirements.txt and run ```pip install opencv-python``` 

Then simply run ```python app.py```