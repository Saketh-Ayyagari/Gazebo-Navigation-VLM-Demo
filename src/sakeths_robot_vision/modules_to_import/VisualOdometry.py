import cv2 as cv
import numpy as np
'''
A visual odometry class that will take in camera frames and return a camera's pose estimate.
'''
class VisualOdometry:
    '''
    Implementing VisualOdometry object with monocular visual odometry using ORB detection. 

    @params
    camera_width: width of the camera frame
    camera_height: height of the camera frame
    K: camera matrix (intrinsic parameters)
    show_matched_features: boolean to show matched features between frames. Used for debugging
    '''
    def __init__(self, camera_width, camera_height, K, show_matched_features=False):
        self._CAMERA_WIDTH = camera_width
        self._CAMERA_HEIGHT = camera_height
        self.K = K # camera matrix
        self.show_matched_features = show_matched_features

        self.orb_detector = cv.ORB_create(nfeatures=2000)
        self.matcher = cv.BFMatcher(cv.NORM_HAMMING,crossCheck=True)
        
    '''
    Given a current and previous image/frame, return relative rotation matrix and translation vector
    '''
    def get_pose_estimate(self, I_0, I_1): # Detecting specific features and descriptors
        keypoints_1, descriptors_1 = self.orb_detector.detectAndCompute(I_0, None)
        keypoints_2, descriptors_2 = self.orb_detector.detectAndCompute(I_1, None)

        # matching features
        matches = self.matcher.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key = lambda x : x.distance) # sorts matches based on distance (farther ones may match to wrong points)

        # converting keypoints to numpy arrays to find essential matrix and recovering pose. 
        kp1 = np.float32([keypoints_1[m.queryIdx].pt for m in matches])
        kp2 = np.float32([keypoints_2[m.trainIdx].pt for m in matches])

        center_point = (self._CAMERA_WIDTH // 2, self._CAMERA_HEIGHT // 2)
        # now calculating essential matrix E given intrinsic matrix K and the previous rotation matrix and
        # translation vector R, t. 
        cx, cy = center_point
        fx = (self._CAMERA_WIDTH / 2) / np.arctan(np.deg2rad(78) / 2)
        fy = fx
        K = np.array([[fx, 0, cx],
                      [0, fy, cy],
                      [0, 0, 1]])
        
        E, mask = cv.findEssentialMat(kp1, kp2, K, cv.RANSAC)
        
        # given essential matrix E, calculate the rotation matrix and translation vector R, t
        ret_transform, R, t, _ = cv.recoverPose(E, kp1, kp2, K)