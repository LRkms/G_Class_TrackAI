from flask import Flask, render_template_string, Response, request
import cv2
import serial
import threading

# UART 설정 (Jetson → STM32)
ser = serial.Serial('/dev/ttyTHS1', 115200, timeout=1)

# 카메라 설정
camera = cv2.VideoCapture(0)

app = Flask(__name__)

# HTML 페이지 템플릿
html_template = '''
<!DOCTYPE html>
<html>
<head>
  <title>Smart RC Car Control</title>
</head>
<body>
  <h1>📷 실시간 영상 & 🚗 조작</h1>
  <img src="/video_feed" width="640"><br><br>
  <button onclick="sendCmd('F')">전진 (F)</button>
  <button onclick="sendCmd('B')">후진 (B)</button>
  <button onclick="sendCmd('L')">좌회전 (L)</button>
  <button onclick="sendCmd('R')">우회전 (R)</button>
  <button onclick="sendCmd('S')">정지 (S)</button>

  <script>
    function sendCmd(cmd) {
      fetch("/control?cmd=" + cmd)
        .then(res => console.log("보냄:", cmd));
    }
  </script>
</body>
</html>
'''

# 영상 스트리밍 함수
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 루트 페이지
@app.route('/')
def index():
    return render_template_string(html_template)

# 영상 피드
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# UART 명령 전송
@app.route('/control')
def control():
    cmd = request.args.get('cmd')
    if cmd in ['F', 'B', 'L', 'R', 'S']:
        ser.write(cmd.encode())
        return f"전송됨: {cmd}"
    return "잘못된 명령"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)