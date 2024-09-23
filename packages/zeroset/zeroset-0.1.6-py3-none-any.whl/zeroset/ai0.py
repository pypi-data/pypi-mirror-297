import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# pip install tensorflow-cpu
# pip install deepface
# pip install tf-keras
# https://github.com/serengil/deepface
from deepface import DeepFace

model_names = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace", ]
detector_backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
distance_metrics = ["cosine", "euclidean", "euclidean_l2"]
import cv0
import py0
import cv2

filename1 = "../data/my_04.jpg"
filename2 = "../data/my_02.jpg"

img1 = cv0.imread(filename1)
img2 = cv0.imread(filename2)

results = DeepFace.verify(img1, img2,
                          model_name="Facenet",
                          detector_backend="retinaface",
                          distance_metric="cosine"
                          )


def get_face_rect(key):
    x = results["facial_areas"][key]["x"]
    y = results["facial_areas"][key]["y"]
    w = results["facial_areas"][key]["w"]
    h = results["facial_areas"][key]["h"]
    eye_x, eye_y = results["facial_areas"][key]["left_eye"]
    return {
        "opencv": {
            "tl": (x, y),
            "br": (x + w, y + h),
        }
    }


rect1 = get_face_rect("img1")
rect2 = get_face_rect("img2")

img1 = cv2.rectangle(img1, rect1["opencv"]["tl"], rect1["opencv"]["br"], (0, 255, 0), 2)
img2 = cv2.rectangle(img2, rect2["opencv"]["tl"], rect2["opencv"]["br"], (0, 255, 0), 2)

py0.print.print_auto(results)

img_all = cv0.hconcat(img1, img2)
cv0.imshow("image", img_all).waitKey()
