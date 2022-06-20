import os
import numpy as np
from datetime import datetime
from detect_box_yolo import detect_box
from logic import *
from threading import Thread


def is_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Creating {}...'.format(path))


def draw_roi(frame, rois, color_box):

    for roi in rois:

        # creating the centroid
        center = (int((roi[0] + roi[2]) / 2), int((roi[1] + roi[3]) / 2))
        cv2.circle(frame, center, 2, (0, 0, 255), 1)

        if roi[4] == 0:  # box
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), color_box, thickness=2)
            bbox_message = 'class0'

        if roi[4] == 1:  # box
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), color_box, thickness=2)
            bbox_message = 'class1'
        

        cv2.putText(frame, bbox_message, (roi[0] +30 , roi[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)


def make_vid(output_path, filename, fps=15):
    image_list = []
    image_path_list = os.listdir(output_path)
    image_path_list = sorted(image_path_list, key=lambda x: int(x[:len(x) - 4]))

    for image in image_path_list:
        img = cv2.imread(os.path.join(output_path, image))
        h, w, _ = img.shape
        size = (w, h)
        image_list.append(img)

    video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(image_list)):
        video.write(image_list[i])

    video.release()
    print('Video Saved')


def videoshow(data_path, filename):
    return cv2.VideoCapture(os.path.join(data_path, filename))

def process_lines(data_path, filename, out_folder, draw_bottles=True, videoout=True):
    # color = (B,G,R)

    color_box = (0,0,255)
    fpers = None                                                                                                                                                      
    frame_no = 1
    # logo = cv2.imread(logo_path)

    cap = videoshow(data_path, filename)

    while cap.isOpened():
        ret, frame = cap.read()
        start_time = time.time()

        if ret:
            if frame_no % 1 == 0:
                # frame = cv2.resize(frame,(1080,1920))
                # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                st_time = time.time()
                rois = detect_box(frame, 0.25)
                analysis, frame, rois, frame_no   = analyse(frame, rois, frame_no)
                if draw_bottles:
                    draw_roi(frame, rois, color_box)
                # frame = add_area(frame,logo)
                write_analysis(frame,analysis)
                print('Frame no: {}'.format(frame_no))
                cv2.imwrite(os.path.join(out_folder, str(frame_no) + '.jpg'), frame)
                if videoout:
                    output_frames(frame)

        else:
            cap.release()

        frame_no += 1

        if (time.time() - start_time) != 0:
            fpers = round(1.0 / (time.time() - start_time), 2)
        else:
            fpers = 0
        cv2.putText(frame, "FPS" + ":" + str(fpers), (10, 90), 0, 0.75, (255, 255, 255), 3)
        cv2.putText(frame, "FPS" + ":" + str(fpers), (10, 90), 0, 0.75, (0, 0, 0), 2)
        print("FPS :", fpers)
    #make_vid(out_folder,out_filename,fps=15)
    print('Done!')

def output_frames(frame):
    
    # cv2.resize(frame, (360, 640))
    # frame = cv2.resize(frame, (960, 540))
    cv2.imshow("output", frame)
    cv2.waitKey(10)

def add_area(frame,logo):
    # image.shape = (352,640,3)
    # right side area (horizontal stack)
    black_area = np.zeros([512, 400, 3], dtype=np.uint8)
    black_area.fill(255)
    frame = np.concatenate((frame, black_area), axis=1)
    # top area (vertical stack)
    # black_area = np.zeros([50,910,3], dtype=np.uint8)
    # black_area.fill(175)
    # frame = np.concatenate((black_area, frame), axis=0)
    frame[0:logo.shape[0], frame.shape[1] - logo.shape[1]:frame.shape[1]] = logo
    return frame
        


if __name__ == "__main__":

    # logo_path = "logo_new2.jpg"
    data_path = os.path.join('video_data')
    processed_frames_path = 'inference_out'
    is_dir(processed_frames_path)

    result_video_path = 'result_vid'
    is_dir(result_video_path)

    locations = os.listdir(data_path)
    print(locations)
    for location in locations:
        #video_files = os.listdir(os.path.join(data_path,location))
        video_files = ["Amina-12ml.avi"]
        print(video_files)

        for video_file in video_files:
            out_filename = os.path.join(result_video_path, 'result_' + '_' + video_file)

            out_folder = f"inference_out/{video_files[0][0:-4]}"
            is_dir(out_folder)
            start = datetime.now()
            process_lines("video_data", video_file, out_folder)
            y = Thread(target=process_lines)
            z = Thread(target=output_frames)
            y.start()
            z.start() 
            y.join()
            z.join()
           
            # make_vid(out_folder, out_filename, fps=20)
            stop = datetime.now()
            print('Time Taken: {}'.format(stop - start))

