import cv2
import numpy as np

board_pattern = (8, 6)
board_cellsize = 30.0

objp = np.zeros((board_pattern[0] * board_pattern[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:board_pattern[0], 0:board_pattern[1]].T.reshape(-1, 2)
objp *= board_cellsize

objpoints = []
imgpoints = []

cap = cv2.VideoCapture('data/my_chessboard_video.mp4')
frame_count = 0
max_frames = 250
quit_program = False

while True:
    if quit_program:
        break

    ret, frame = cap.read()
    if not ret:
        print("영상 끝")
        break

    frame_count += 1
    if frame_count > max_frames:
        print("프레임 제한 도달")
        break

    if frame_count % 5 != 0:  
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, board_pattern, None)

    if found:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        objpoints.append(objp)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(frame, board_pattern, corners, found)

        print(f"체스보드 인식됨 (프레임 {frame_count})")

    cv2.imshow("Chessboard", frame)

    key = cv2.waitKey(100)  
    if key == ord('q') or key == 27:
        print("종료")
        quit_program = True

cap.release()
cv2.destroyAllWindows()

if len(objpoints) > 0 and len(imgpoints) > 0:
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    fx = K[0, 0]
    fy = K[1, 1]
    cx = K[0, 2]
    cy = K[1, 2]

    print("\n Camera Matrix (K):\n", K)
    print(f"fx: {fx:.2f}, fy: {fy:.2f}, cx: {cx:.2f}, cy: {cy:.2f}")
    print("Distortion Coefficients:", dist.ravel())
    print("RMS Error:", ret)
else:
    print("유효한 체스보드 데이터가 없어 캘리브레이션 실패")
