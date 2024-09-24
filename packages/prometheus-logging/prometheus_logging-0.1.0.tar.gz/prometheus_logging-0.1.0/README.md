# Prometheus Logging

A simple logging library for ML projects using Prometheus.

## Installation

```bash
pip install prometheus_logging
```

## Usage
```python
from prometheus_logging import init_logging, log_model_loss, start_metrics_server
import threading

# Initialize logging
init_logging(
project="my_project",
config={"batch_size": 32, "learning_rate": 0.001},
notes="Training run",
name="experiment_1",
fake_gpu=True
)

# Start metrics server in a separate thread
threading.Thread(target=start_metrics_server, daemon=True).start()

# In your training loop
for epoch in range(num_epochs):
for batch in dataloader:
# ... training logic ...
loss = model(batch)
log_model_loss(loss.item())

# Make sure Prometheus is configured to scrape metrics from `localhost:8000`.
```


