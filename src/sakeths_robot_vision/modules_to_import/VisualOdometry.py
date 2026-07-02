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
        """Initialize camera settings and feature-matching components for VO."""
        self._CAMERA_WIDTH = camera_width
        self._CAMERA_HEIGHT = camera_height
        self.K = K  # camera matrix
        self.show_matched_features = show_matched_features

        self.orb_detector = cv.ORB_create(nfeatures=2000)
        self.matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)

    def _prepare_image(self, image):
        """Convert color images to grayscale so the detector uses a simpler representation."""
        if image is None:
            raise ValueError("Image cannot be None")
        if len(image.shape) == 3:
            return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        return image

    def get_pose_estimate(self, I_0, I_1):
        """Estimate the relative pose between two consecutive frames.

        Returns a tuple of (rotation_matrix, translation_vector) when enough inlier
        correspondences are found. Returns (None, None) if the motion estimate is not reliable.
        """
        img0 = self._prepare_image(I_0)
        img1 = self._prepare_image(I_1)

        keypoints_1, descriptors_1 = self.orb_detector.detectAndCompute(img0, None)
        keypoints_2, descriptors_2 = self.orb_detector.detectAndCompute(img1, None)

        if descriptors_1 is None or descriptors_2 is None:
            return None, None

        if len(descriptors_1) < 2 or len(descriptors_2) < 2:
            return None, None

        # # Use k-NN matching and keep only strong correspondences before estimating pose.
        # raw_matches = self.matcher.knnMatch(descriptors_1, descriptors_2, k=2)
        # good_matches = []
        # for match_pair in raw_matches:
        #     if len(match_pair) < 2:
        #         continue
        #     m, n = match_pair
        #     if m.distance < 0.75 * n.distance:
        #         good_matches.append(m)

        # if len(good_matches) < 8:
        #     return None, None

        matches = self.matcher.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key = lambda x : x.distance) # sorts matches based on distance (farther ones may match to wrong points)

        # showing matched features across camera frames
        if self.show_matched_features:
            output_image = cv.drawMatches(
                img0, keypoints_1,
                img1, keypoints_2,
                matches[:50], None, flags=2
            ) # shows 50 best features.
            cv.imshow("Matched Features", output_image)
            cv.waitKey(1)

        src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in matches])
        dst_pts = np.float32([keypoints_2[m.trainIdx].pt for m in matches])

        # Use the calibrated camera intrinsics supplied by the caller.
        K = np.asarray(self.K, dtype=np.float64).reshape(3, 3)
        E, mask = cv.findEssentialMat(src_pts, dst_pts, K, cv.RANSAC)
        if E is None or mask is None:
            return None, None

        # # Keep only the inlier correspondences that support the estimated essential matrix.
        # inlier_mask = mask.ravel().astype(bool)
        # src_pts = src_pts[inlier_mask]
        # dst_pts = dst_pts[inlier_mask]
        # if len(src_pts) < 5:
        #     return None, None

        _, R, t, _ = cv.recoverPose(E, src_pts, dst_pts, K, mask)
        if R is None or t is None:
            return None, None

        return R, t