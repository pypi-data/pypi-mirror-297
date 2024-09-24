from prometheus_client import start_http_server, Gauge
import subprocess
import time
import psutil
import re
import random
import platform

cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage (%)')
gpu_usage = Gauge('gpu_usage_percent', 'GPU Usage (%)')
memory_usage = Gauge('memory_usage_percent', 'Memory Usage (%)')
gpu_temp = Gauge('gpu_temp_celsius', 'GPU Temperature (°C)')
gpu_memory_access = Gauge('gpu_memory_access_percent', 'GPU Time Spent Accessing Memory (%)')
gpu_memory_allocated = Gauge('gpu_memory_allocated_bytes', 'GPU Memory Allocated (bytes)')
gpu_power_usage_percent = Gauge('gpu_power_usage_percent', 'GPU Power Usage (%)')
gpu_power_usage_watts = Gauge('gpu_power_usage_watts', 'GPU Power Usage (W)')
model_loss = Gauge('model_loss', 'Model Training Loss')

config_storage = {}
use_fake_gpu_data = False

def init_logging(project, config=None, notes=None, name=None, fake_gpu=False):
    """
    Initialize logging configuration.
    """
    global config_storage, use_fake_gpu_data
    config_storage = {
        'project': project,
        'config': config or {},
        'notes': notes,
        'name': name
    }
    use_fake_gpu_data = fake_gpu or platform.system() == 'Darwin'
    
    # Store configuration as Prometheus metrics
    Gauge('project_info', 'Project Information', ['project', 'notes', 'name']).labels(
        project=project, notes=notes or '', name=name or '').set(1)
    if config:
        for key, value in config.items():
            Gauge(f'config_{key}', f'Configuration: {key}').set(value if isinstance(value, (int, float)) else 1)

def get_fake_gpu_data():
    return {
        'gpu_usage': random.uniform(0, 100),
        'gpu_temp': random.uniform(30, 80),
        'gpu_memory_access': random.uniform(0, 100),
        'gpu_memory_allocated': random.randint(0, 8 * 1024 * 1024 * 1024),  # Up to 8 GB
        'gpu_power_percent': random.uniform(0, 100),
        'gpu_power_watts': random.uniform(0, 300)
    }


def get_system_info():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    if use_fake_gpu_data:
        gpu_data = get_fake_gpu_data()
        return (cpu_percent, gpu_data['gpu_usage'], memory_percent, 
                gpu_data['gpu_temp'], gpu_data['gpu_memory_access'], 
                gpu_data['gpu_memory_allocated'], gpu_data['gpu_power_percent'], 
                gpu_data['gpu_power_watts'])
    else:
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Assuming single GPU setup
                return (cpu_percent, gpu.load * 100, memory_percent, gpu.temperature, 
                        gpu.memoryUtil * 100, gpu.memoryUsed * 1024 * 1024, 
                        gpu.load * 100, gpu.powerUsage)
        except ImportError:
            print("GPUtil not available. Using fake GPU data.")
            return get_fake_gpu_data()

    return cpu_percent, None, memory_percent, None, None, None, None, None

def log_system_metrics():
    cpu, gpu, memory, gpu_temp_val, gpu_mem_access, gpu_mem_alloc, gpu_power_percent, gpu_power_watts = get_system_info()
    if cpu is not None:
        cpu_usage.set(cpu)
    if gpu is not None:
        gpu_usage.set(gpu)
    if memory is not None:
        memory_usage.set(memory)
    if gpu_temp_val is not None:
        gpu_temp.set(gpu_temp_val)
    if gpu_mem_access is not None:
        gpu_memory_access.set(gpu_mem_access)
    if gpu_mem_alloc is not None:
        gpu_memory_allocated.set(gpu_mem_alloc)
    if gpu_power_percent is not None:
        gpu_power_usage_percent.set(gpu_power_percent)
    if gpu_power_watts is not None:
        gpu_power_usage_watts.set(gpu_power_watts)

def log_model_loss(loss_value):
    """
    Log the model loss.
    """
    model_loss.set(loss_value)

def start_metrics_server(port=8000, log_interval=5):
    start_http_server(port)
    print(f"Metrics server started on port {port}")
    while True:
        log_system_metrics()
        time.sleep(log_interval)

if __name__ == '__main__':
    init_logging("example_project", config={"batch_size": 32}, notes="Test run", name="experiment_1", fake_gpu=True)
    start_metrics_server()