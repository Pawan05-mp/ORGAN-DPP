FROM pytorch/pytorch:2.2.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# Copy project
COPY . /app

# Use pip to install requirements; RDKit is best installed via conda in GPU images
RUN pip install --upgrade pip && pip install -r backend/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
