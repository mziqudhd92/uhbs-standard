FROM python:3.11-slim-bookworm
WORKDIR /app
RUN pip install --no-cache-dir python-snap7
COPY s7_snap7_server.py /app/s7_snap7_server.py
EXPOSE 102
CMD ["python", "-u", "/app/s7_snap7_server.py", "--host", "0.0.0.0", "--port", "102"]
