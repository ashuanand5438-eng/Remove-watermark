from flask import Flask, render_template, request, send_file
import cv2
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def remove_watermark(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # LOGIC: Watermark aksar corner mein hota hai. 
        # Hum bottom-right corner ko blur/inpainting karenge.
        h, w, _ = frame.shape
        roi = frame[h-100:h, w-200:w] # Area define kiya
        blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
        frame[h-100:h, w-200:w] = blurred_roi
        
        out.write(frame)
    
    cap.release()
    out.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['video']
        filename = f"{uuid.uuid4()}.mp4"
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, f"clean_{filename}")
        file.save(input_path)
        
        remove_watermark(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
