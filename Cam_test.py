import cv2

# 두 카메라 열기
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

# 원하는 해상도 명시!
width, height = 1280, 720
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 열렸는지 확인
if not cap0.isOpened() or not cap1.isOpened():
    print("카메라 열기 실패")
    exit()

while True:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if not ret0 or not ret1:
        print("프레임 읽기 실패")
        break

    # 각 프레임 보여주기
    cv2.imshow('Camera 0', frame0)
    cv2.imshow('Camera 1', frame1)

    # 'q' 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap0.release()
cap1.release()
cv2.destroyAllWindows()
