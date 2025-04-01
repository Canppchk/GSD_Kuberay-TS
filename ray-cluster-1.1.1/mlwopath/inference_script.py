import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import multiprocessing

def inference_task(task_id):
    # Set MPS environment variables
    os.environ['CUDA_MPS_PIPE_DIRECTORY'] = '/tmp/nvidia-mps'
    os.environ['CUDA_MPS_LOG_DIRECTORY'] = '/tmp/nvidia-log'

    # Set the device to GPU
    device = torch.device('cuda:0')

    # Load the pre-trained model (ResNet-50)
    model = models.resnet50(pretrained=True).to(device)
    model.eval()

    # Prepare a dummy input image
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])

    # Create a random image tensor
    input_tensor = torch.randn(1, 3, 224, 224, device=device)

    # Run inference multiple times
    for i in range(5):
        with torch.no_grad():
            output = model(input_tensor)
        torch.cuda.synchronize()
        print(f"Task {task_id}, Iteration {i+1}: Inference completed.")

if __name__ == "__main__":
    num_processes = 2  # Number of concurrent inference tasks
    processes = []

    for i in range(num_processes):
        p = multiprocessing.Process(target=inference_task, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

