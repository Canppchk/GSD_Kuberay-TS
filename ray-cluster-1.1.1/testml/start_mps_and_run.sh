#!/bin/bash

# Start the MPS control daemon
nvidia-cuda-mps-control -d

# Set MPS environment variables
export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log

# Run the inference script
python3 /opt/inference_script.py

# Keep the container running (optional)
tail -f /dev/null

