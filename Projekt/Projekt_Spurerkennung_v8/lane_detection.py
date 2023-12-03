import time
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
import glob


class LaneDetection:
    def __init__(self, video_name='project_video.mp4'):
        self.video_name = video_name
        self.calibration_data = np.load('calibration.npz')
        self.mtx = self.calibration_data['mtx']
        self.dist = self.calibration_data['dist']
        self.rvecs = self.calibration_data['rvecs']
        self.tvecs = self.calibration_data['tvecs']

    def start(self):
        # get video
        cap = cv.VideoCapture('./img/Udacity/' + self.video_name)

        # used to record the time when we processed last frame
        prev_frame_time = 0
        # used to record the time at which we processed current frame
        new_frame_time = 0

        frame_counter = 0
        fps_sum = 0

        # check if video is opened
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            frame_counter += 1
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            font = cv.FONT_HERSHEY_SIMPLEX
            new_frame_time = time.time()

            # operations on the frame come here
            frame = self.undistorted_frame(frame)
            # ToDo: add lane detection for frame

            # calculate fps
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps_sum += fps
            # display fps
            if fps > 20:
                cv.putText(frame, str(fps), (7, 80), font, 3, (100, 255, 0), 3, cv.LINE_AA)
            else:
                cv.putText(frame, str(fps), (7, 80), font, 3, (0, 0, 255), 3, cv.LINE_AA)

            # display fps average
            # ToDo: frame average needed?
            cv.putText(frame, str(int(fps_sum/frame_counter)), (1080, 80), font, 3, (0, 0, 0), 3, cv.LINE_AA)

            # Display the resulting frame
            cv.imshow(self.video_name, frame)
            if cv.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

    def undistorted_frame(self, frame):
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
        undistorted_img = cv.undistort(frame, self.mtx, self.dist, None, new_camera_mtx)

        # crop the image
        x, y, w, h = roi
        return undistorted_img[y:y + h, x:x + w]


if __name__ == '__main__':
    video_name = 'project_video.mp4'
    ld = LaneDetection(video_name)
    ld.start()
