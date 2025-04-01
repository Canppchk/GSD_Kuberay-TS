# Base image with CUDA and cuDNN support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118

# Copy the inference script and MPS start script into the image
COPY inference_script.py /opt/inference_script.py
COPY start_mps_and_run.sh /opt/start_mps_and_run.sh
RUN chmod +x /opt/start_mps_and_run.sh

# Set the entrypoint to the MPS start script
ENTRYPOINT ["/opt/start_mps_and_run.sh"]

