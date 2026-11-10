import cv2 as cv
import os
import csv
def Out_image(img,filename):
    os.makedirs("outputs", exist_ok=True)
    cv.imwrite(f"outputs/{filename}.png",img)
def Create_csv():
    with open("./outputs/data.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["frame_id", "time_s", "candidate_id",
                         "detect_valid", "pnp_valid",
                         "tx_m", "ty_m", "tz_m", "distance_m",
                         "rx_rad", "ry_rad", "rz_rad", "reprojection_error_px"])
def Find_None_Aim(frame_id, time_s):
    with open("./outputs/data.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        list_row = []
        list_row.append(frame_id)
        list_row.append(time_s)
        list_row.append(-1)
        writer.writerow(list_row)
def Get_reprojection_error(aim_points, imagePoints):
    if imagePoints is None:
        return None
    error = 0.0
    for i in range(len(aim_points)):
        u_i, v_i = aim_points[i]
        u_hat_i, v_hat_i = imagePoints[i]
        e_i = ((u_i - u_hat_i) ** 2 + (v_i - v_hat_i) ** 2) ** 0.5
        error += e_i
    reprojection_error_px = error / len(aim_points)
    return reprojection_error_px
#第 i 个原始角点为 (u_i, v_i)，对应的重投影点为 (u_hat_i, v_hat_i)，先计算 e_i = sqrt((u_i-u_hat_i)^2 + (v_i-v_hat_i)^2)，再计算 reprojection_error_px = (e_0+e_1+e_2+e_3)/4
def output_frame_csv(frame_id, time_s,array_detect, array_ret, array_rvec, array_tvec,array_aim_points,array_imagePoints):
    with open("./outputs/data.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for i in range(len(array_ret)):
            list_row = []
            list_row.append(frame_id)
            list_row.append(time_s)
            list_row.append(i)
            list_row.append(array_detect[i])
            list_row.append(array_ret[i])
            if array_ret[i]:
                list_row.append(array_tvec[i][0][0])
                list_row.append(array_tvec[i][1][0])
                list_row.append(array_tvec[i][2][0])
                distance = (array_tvec[i][0][0]**2 + array_tvec[i][1][0]**2 + array_tvec[i][2][0]**2)**0.5
                list_row.append(distance)
                list_row.append(array_rvec[i][0][0])
                list_row.append(array_rvec[i][1][0])
                list_row.append(array_rvec[i][2][0])
                list_row.append(Get_reprojection_error(array_aim_points[i], array_imagePoints[i]))
            writer.writerow(list_row)
# frame_id, time_s, candidate_id,
# detect_valid, pnp_valid,
# tx_m, ty_m, tz_m, distance_m,
# rx_rad, ry_rad, rz_rad, reprojection_error_px
