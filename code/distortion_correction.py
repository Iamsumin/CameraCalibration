import cv2
import numpy as np

K = np.load('data/camera_matrix.npy')
dist_coeff = np.load('data/dist_coeffs.npy')

video_file = 'data/my_chessboard_video.mp4'
cap = cv2.VideoCapture(video_file)

map1, map2 = None, None
new_K = None
roi = None

while True:
    valid, original_img = cap.read()
    if not valid:
        print("영상 끝")
        break

    h, w = original_img.shape[:2]

    if map1 is None or map2 is None:
        new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist_coeff, (w, h), 1)
        map1, map2 = cv2.initUndistortRectifyMap(K, dist_coeff, None, new_K, (w, h), cv2.CV_32FC1)

    corrected_img = cv2.remap(original_img, map1, map2, interpolation=cv2.INTER_LINEAR)

    x, y, rw, rh = roi
    corrected_img = corrected_img[y:y+rh, x:x+rw]
    cropped_original = original_img[y:y+rh, x:x+rw]

    combined = np.hstack((cropped_original, corrected_img))
    cv2.putText(combined, "Original", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.putText(combined, "Rectified", (rw + 30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("Original vs Rectified", combined)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        print("종료")
        break

cap.release()
cv2.destroyAllWindows()
