# Base image
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Set up environment variables
ENV CONDA_DIR=/opt/conda \
    PATH=/opt/conda/bin:$PATH \
    RAY_DEBUG_BUILD=tsan

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        clang-12 \
        pkg-config \
        psmisc \
        unzip \
        git && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN curl -sSLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh && \
    conda clean -afy

# Create a new conda environment and activate it
RUN conda create -n myenv -c conda-forge python=3.9 && \
    echo "source activate myenv" >> ~/.bashrc

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Activate the environment
RUN source activate myenv

# Clone Ray project
RUN git clone https://github.com/ray-project/ray.git /ray

# Install Bazelisk
RUN cd /ray && ./ci/env/install-bazel.sh

# Install NodeJS version 14 using NVM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    nvm install 14 && \
    nvm use 14

# Build the Ray dashboard client
RUN export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    cd /ray/python/ray/dashboard/client && \
    npm ci && \
    npm run build

# Create .bazelrc file to limit RAM and CPU usage before pip install
RUN echo 'build --local_ram_resources=HOST_RAM*.5 --local_cpu_resources=4' >> /ray/.bazelrc

# Install Ray with debug options
RUN cd /ray/python && \
    pip install -r requirements.txt && \ 
    pip install -e . --verbose

# Export the Ray port
EXPOSE 6379 8265 10001

# Start the container with the correct environment
CMD ["bash"]

