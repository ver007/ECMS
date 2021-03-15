import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

import cv2
from deepface.mtcnn.core.detect import create_mtcnn_net, MtcnnDetector
import dlib
import csv
import numpy as np
import os


model = dlib.face_recognition_model_v1(
    "deepface//model_store//dlib_face_recognition_resnet_model_v1.dat"
)
predictor = dlib.shape_predictor(
    'deepface//model_store//shape_predictor_68_face_landmarks.dat'
)


def detect_face(img):
    p_model_path = "deepface/model_store/pnet_epoch.pt"
    r_model_path = "deepface/model_store/rnet_epoch.pt"
    o_model_path = "deepface/model_store/onet_epoch.pt"
    pnet, rnet, onet = create_mtcnn_net(p_model_path, r_model_path, o_model_path, use_cuda=True)
    mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)
    bboxs, landmarks = mtcnn_detector.detect_face(img)
    return bboxs, landmarks


def return_features(img, bboxs):
    faces_features = []
    if len(bboxs) != 0:
        for i in bboxs:
            # temp = img[int(i[1]): int(i[3]), int(i[0]): int(i[2])]
            # cv2.imshow('temp', temp)
            rec = dlib.rectangle(int(i[0]), int(i[1]), int(i[2]), int(i[3]))
            shape = predictor(img, rec)
            faces_features.append(model.compute_face_descriptor(img, shape))
    return faces_features


def save_feature(imgpath, savepath):
    img = cv2.imread(imgpath)
    name = os.path.split(imgpath)[-1].split('.')[0]
    bboxs, landmarks = detect_face(img)
    face = return_features(img, bboxs)[0]
    with open(savepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        row = []
        row.append(name)
        for i in face:
            row.append(i)
        writer.writerow(row)


def get_face_database(path):
    import pandas as pd
    name_known_list = []
    features_known_list = []
    csv_rd = pd.read_csv(path, header=None)
    for i in range(csv_rd.shape[0]):
        name_known_list.append(str(int(csv_rd.values[i: i+1][0][0])))
        features_known_list.append(csv_rd.values[i: i+1][0][1:])
    return name_known_list, features_known_list


def contrast(img, face_database_path, threshold):
    bboxs, landmarks = detect_face(img)
    faces = return_features(img, bboxs)
    names, features = get_face_database(face_database_path)
    flags = [0 for i in range(len(names))]
    for i in faces:
        for j, k in enumerate(features):
            dist = np.linalg.norm(i - k)
            if dist <= threshold:
                flags[j] = 1
                break
    return names, flags


if __name__ == "__main__":
    img = cv2.imread("deepface//face_database//class1//img//1170131230.jpg")
    name, flag = contrast(img, "deepface//face_database//class2//faces.csv", 0.45)
    # imgpath = "..//face_database//class1//cl.jpg"
    # save_feature(imgpath, "deepface/face_database/faces.csv")
