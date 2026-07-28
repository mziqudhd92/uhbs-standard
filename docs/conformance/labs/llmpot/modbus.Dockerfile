FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir 'torch' 'transformers' --extra-index-url https://download.pytorch.org/whl/cpu
COPY modbus_hf_server.py /app/modbus_hf_server.py
ENV LLMPOT_MODEL=cv43/llmpot
EXPOSE 5020
CMD ["python", "-u", "/app/modbus_hf_server.py", "--host", "0.0.0.0", "--port", "5020"]
