import cv2 as cv
import os
import sys
import numpy as np
import argparse
import Const
import input
import output
import projectPoints
import Find_Aim
import Solve_PnP
def image_process(frame_id, time_s, img):
    img=cv.resize(img,(Const.image_width, Const.image_height))
    array_aim_points=Find_Aim.Dispose_image_inRange(img)
    if len(array_aim_points)==0:
        output.Find_None_Aim(frame_id, time_s)
        return img
    array_ret, array_rvec, array_tvec = Solve_PnP.PnP_img(array_aim_points)
    result=img.copy()
    array_imagePoints=projectPoints.project_points_img(array_ret, array_rvec, array_tvec, result)
    output.output_frame_csv(frame_id, time_s, array_aim_points, array_ret, array_rvec, array_tvec,array_aim_points,array_imagePoints)
    # result=cv.drawContours(result, array_aim_points, -1, (0, 255, 0), 3)
    return result
    # cv.imshow("result", result)
    # cv.waitKey(0)
def video_process(video_path):
    cap=cv.VideoCapture(video_path)
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    out = cv.VideoWriter(
    "./outputs/Output_video.avi",
    fourcc,
    120.0,
    (Const.image_width, Const.image_height)
    )
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    output.Create_csv()
    frame_id=1
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        time_s=cap.get(cv.CAP_PROP_POS_MSEC)/1000.0
        result=image_process(frame_id, time_s, frame)
        out.write(result)
        frame_id+=1
    cap.release()
    out.release()
    cv.destroyAllWindows()
if __name__=="__main__":
    video_process("./input/video.avi")
    # result=image_process(1, 0, input.Input_image("./input/img_0.png"))
    # cv.imshow("result", result)
    # cv.waitKey(0)