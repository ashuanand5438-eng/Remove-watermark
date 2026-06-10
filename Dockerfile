FROM python:3.9
RUN apt-get update && apt-get install -y libgl1-mesa-glx ffmpeg
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "app:app"]
