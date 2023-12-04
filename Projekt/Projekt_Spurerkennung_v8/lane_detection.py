import time
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
import glob
import concurrent.futures


class LaneDetection:
    def __init__(self, video_name='project_video.mp4'):
        self.video_name = video_name
        self.calibration_data = np.load('calibration.npz')
        self.mtx = self.calibration_data['mtx']
        self.dist = self.calibration_data['dist']
        self.rvecs = self.calibration_data['rvecs']
        self.tvecs = self.calibration_data['tvecs']
        self.last_stable_frame = None

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
            print("Cannot open video")
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
            cropped_frame = self.crop_image(frame)
            transformed_frame = self.transform_perspective(cropped_frame)
            filtered_frame = self.filter_frame(transformed_frame)
            thresholded_frame = self.threshold_frame(filtered_frame)
            curve_fitted_frame = self.fit_curve(thresholded_frame, frame)
            if curve_fitted_frame is None:
                frame = self.last_stable_frame
            else:
                frame = curve_fitted_frame
                self.last_stable_frame = curve_fitted_frame
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
            cv.putText(frame, str(int(fps_sum / frame_counter)), (1080, 80), font, 3, (0, 0, 0), 3, cv.LINE_AA)

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

    def crop_image(self, frame):
        # zuschneiden des Bildes
        # print(frame.shape)
        return frame[370:, 200:1080]

    def transform_perspective(self, cropped_frame):
        # get the height and width of the images
        h, w = cropped_frame.shape[:2]

        # define the source and destination points for the perspective transformation
        src = np.float32([[340, 40], [540, 40], [870, 240], [10, 240]])
        dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

        # get the perspective transformation matrix
        M = cv.getPerspectiveTransform(src, dst)
        # warp the image to get a bird view
        warped_frame = cv.warpPerspective(cropped_frame, M, (cropped_frame.shape[1], cropped_frame.shape[0]))

        return warped_frame

    def filter_color_range(self, img, lower, upper):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        filtered_img = cv.bitwise_and(img, img, mask=mask)
        return filtered_img

    def filter_frame_without_threading(self, frame):
        # not in use
        # Farbbereiche definieren
        yellow_range = (np.array([20, 100, 20]), np.array([30, 255, 255]))
        white_range = (np.array([0, 0, 200]), np.array([255, 30, 255]))

        img_filtered_yellow = self.filter_color_range(frame, *yellow_range)
        img_filtered_white = self.filter_color_range(frame, *white_range)
        img_filtered = cv.addWeighted(img_filtered_yellow, 1, img_filtered_white, 1, 0)
        return img_filtered

    def filter_frame(self, frame):
        # Farbbereiche definieren
        yellow_range = (np.array([20, 100, 20]), np.array([30, 255, 255]))
        white_range = (np.array([0, 0, 200]), np.array([255, 30, 255]))

        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the tasks for yellow and white color filtering
            yellow_future = executor.submit(self.filter_color_range, frame, *yellow_range)
            white_future = executor.submit(self.filter_color_range, frame, *white_range)

            # Wait for the results
            img_filtered_yellow = yellow_future.result()
            img_filtered_white = white_future.result()

        # Combine the results using addWeighted
        img_filtered = cv.addWeighted(img_filtered_yellow, 1, img_filtered_white, 1, 0)

        # Delete variables to free up memory
        del img_filtered_yellow, img_filtered_white

        return img_filtered

    def threshold_frame(self, frame):
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # add thresholding
        _, binary_image = cv.threshold(img_gray, 180, 255, cv.THRESH_BINARY)

        return binary_image

    def generate_curve_function(self, params):
        return lambda x: params[0] * x ** 2 + params[1] * x + params[2]

    def opening_frame(self, frame):
        kernel_ver = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]], 'uint8')
        opening_frame = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel_ver, iterations=5)
        return opening_frame

    def fit_curve(self, frame_warp, original_frame):
        """
        Fits a curve to the lane lines
        :param frame_warp: image in grayscale (cropped, warped and with thresholding)
        :param original_frame: original image (only undistorted)
        :return: original image with curve in red
        """
        # opening not needed, because the thresholding is already good enough
        # if opening is needed for one of the harder videos, use the following lines instead
        # opened_frame = self.opening_frame(frame_warp)
        # half_y = int(opened_frame.shape[1] / 2)
        # left_x, left_y = np.where(opened_frame[:, :half_y] == 255)
        # right_x, right_y = np.where(opened_frame[:, half_y:] == 255)

        # curve fitting for left and right lane
        half_x = int(frame_warp.shape[1] / 2)
        left_x, left_y = np.where(frame_warp[:, :half_x] == 255)
        right_x, right_y = np.where(frame_warp[:, half_x:] == 255)

        if len(left_x) == 0 or len(right_x) == 0:
            return None
        left_fit = np.polyfit(left_x, left_y, 2)
        right_fit = np.polyfit(right_x, right_y, 2)

        # Erzeuge eine Liste von x-Werten
        x_values_left = np.linspace(0, 800, 100)
        x_values_right = np.linspace(0, 800, 100)

        # Erzeuge die y-Werte basierend auf der Funktion
        curve_function_left = self.generate_curve_function(left_fit)
        y_values_left = curve_function_left(x_values_left)
        curve_function_right = self.generate_curve_function(right_fit)
        y_values_right = curve_function_right(x_values_right)

        # create image from curve function
        frame_lanes = np.zeros_like(frame_warp)
        for i in range(len(x_values_left) - 1):
            cv.line(frame_lanes, (int(y_values_left[i]), int(x_values_left[i])),
                    (int(y_values_left[i + 1]), int(x_values_left[i + 1])), (255, 255, 255), 20)
            cv.line(frame_lanes, (int(y_values_right[i]) + int(frame_lanes.shape[1] / 2), int(x_values_right[i])),
                    (int(y_values_right[i + 1]) + int(frame_lanes.shape[1] / 2), int(x_values_right[i + 1])),
                    (255, 255, 255),
                    20)

        h, w = frame_warp.shape[:2]
        # Rücktransformation der Vogelperspektive bei Funktionen
        # Die Quell- und Ziel-Punkte für die Perspektivtransformation definieren
        src = np.float32([[340, 40], [540, 40], [870, 240], [10, 240]])
        dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

        # Die inverse Transformationsmatrix berechnen
        M_inv = cv.getPerspectiveTransform(dst, src)

        # Die Rücktransformation der Vogelperspektive zum Originalbild durchführen
        mask_warp_size_inv = cv.warpPerspective(frame_lanes, M_inv, (w, h))

        # create mask for lanes in original frame to fit the curve to the original frame
        mask_original_size = np.zeros_like(original_frame)
        h_o, w_o = original_frame.shape[:2]
        a = w_o / 2 - w / 2 + 35
        b = w_o / 2 + w / 2 + 35

        mask_original_size[h_o - h:h_o, int(a):int(b), 0] = mask_warp_size_inv

        # Erzeuge ein boolean-Array für die Pixel, die in der Maske gesetzt sind
        mask_bool_pixels = mask_original_size[:, :, 0] == 255

        # Setze die Farbwerte für die Pixel in img_original, wo die Maske gesetzt ist
        original_frame[mask_bool_pixels] = [0, 0, 255]

        return original_frame


if __name__ == '__main__':
    video_name = 'project_video.mp4'
    ld = LaneDetection(video_name)
    ld.start()
