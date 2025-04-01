# Base image with CUDA and cuDNN support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

USER root

# Install basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    sudo \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ray from PyPI
RUN pip3 install --upgrade pip \
    && pip3 install ray[default]

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118

# Copy the inference script and MPS start script into the image
COPY inference_script.py /opt/inference_script.py
COPY start_mps_and_run.sh /opt/start_mps_and_run.sh
RUN chmod +x /opt/start_mps_and_run.sh

# Set the entrypoint to the MPS start script
ENTRYPOINT ["/opt/start_mps_and_run.sh"]

# Set the working directory
WORKDIR /app

# Expose ports for Ray head node (if needed)
EXPOSE 6379 6380 8265
