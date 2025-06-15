# Cluster Simulator

This project simulates a distributed cluster system using a Flask API server, node heartbeats, and a client CLI.

## Components

- **api_server.py**: A Flask API server that manages nodes and pods. It provides endpoints to add nodes, list nodes, launch pods, and monitor node health via heartbeats.
- **node.py**: Simulates a node that sends heartbeats to the API server every 5 seconds.
- **client.py**: A command-line interface (CLI) for interacting with the cluster. It allows you to add nodes, list nodes, and launch pods.
- **Dockerfile.txt**: Contains instructions to build a Docker image for running the API server and node.

## Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Sunil2713/PES1UG22CS624_PES1UG22CS629_PES1UG22CS649_PES1UG22CS662_DistributedSystemsClusterSimulationFramework.git
   cd PES1UG22CS624_PES1UG22CS629_PES1UG22CS649_PES1UG22CS662_DistributedSystemsClusterSimulationFramework
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.9 installed. Install the required packages:
   ```sh
   pip install flask docker requests
   ```

3. **Run the API Server**:
   ```sh
   python api_server.py
   ```

4. **Run the Node Simulator**:
   In a separate terminal, run:
   ```sh
   python node.py
   ```

5. **Use the Client CLI**:
   In another terminal, run:
   ```sh
   python client.py
   ```

## Docker Setup

To run the project using Docker, build the image using the provided Dockerfile:
```sh
docker build -t cluster-simulator -f Dockerfile.txt .
docker run -p 5000:5000 cluster-simulator
```

## Notes

- The API server runs on `http://127.0.0.1:5000`.
- Ensure that the `NODE_ID` environment variable is set when running `node.py`.
- Sensitive files (like API keys) are excluded from git tracking via `.gitignore`. 