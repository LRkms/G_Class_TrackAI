from flask import Flask, render_template_string, Response, request
import cv2
import serial
import threading

# UART 설정 (Jetson → STM32)
ser = serial.Serial('/dev/ttyTHS1', 115200, timeout=1)

# 카메라 설정
camera0 = cv2.VideoCapture(0)
camera1 = cv2.VideoCapture(1)
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
  <div style="display: flex; gap: 20px;">
      <div>
        <h3>Camera 1</h3>
        <img src="/video_feed0" width="480">
      </div>
      <div>
        <h3>Camera 2</h3>
        <img src="/video_feed1" width="480">
      </div>
    </div>
  <button onclick="sendCmd('F')">전진 (F)</button>
  <button onclick="sendCmd('B')">후진 (B)</button>
  <button onclick="sendCmd('L')">좌회전 (L)</button>
  <button onclick="sendCmd('R')">우회전 (R)</button>
  <button onclick="sendCmd('S')">정지 (S)</button>

  <p><b>키보드 조작:</b> W/A/S/D 또는 ↑ ↓ ← →</p>

  <script>
    document.addEventListener("keydown", function(event) {
      let key = event.key.toLowerCase();
      let cmd = null;

      if (key === 'w' || event.key === 'ArrowUp') cmd = 'F';
      else if (key === 's' || event.key === 'ArrowDown') cmd = 'B';
      else if (key === 'a' || event.key === 'ArrowLeft') cmd = 'L';
      else if (key === 'd' || event.key === 'ArrowRight') cmd = 'R';
      else if (key === ' ') cmd = 'S';  // space = stop

      if (cmd) {
        fetch("/control?cmd=" + cmd)
          .then(res => console.log("키 입력:", cmd));
      }
    });

    function sendCmd(cmd) {
      fetch("/control?cmd=" + cmd)
        .then(res => console.log("버튼 클릭:", cmd));
    }
  </script>
</body>
</html>
'''

# 영상 스트리밍 함수
def gen_frames0():
    while True:
        success, frame = camera0.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_frames1():
    while True:
        success, frame = camera1.read()
        if not success:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# 루트 페이지
@app.route('/')
def index():
    return render_template_string(html_template)

# 영상 피드
@app.route('/video_feed0')
def video_feed0():
    return Response(gen_frames0(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

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