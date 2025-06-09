from flask import Flask, request, jsonify
import threading
import time
import docker

app = Flask(__name__)
client = docker.from_env()

# Cluster Data
nodes = {}  # {node_id: {"cpu": 2, "pods": [], "status": "healthy"}}
pods = {}   # {pod_id: {"cpu": 1, "node": node_id}}
node_heartbeats = {}  # {node_id: last_heartbeat_time}

HEARTBEAT_INTERVAL = 10  # 10 seconds timeout for node failures

# 🟢 Add Node (Launch Docker Container)
@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    cpu_cores = data.get("cpu")

    # Launch a container as a new node
    container = client.containers.run("python:3.9", "sleep infinity", detach=True)
    node_id = container.id[:10]  # Shortened container ID

    nodes[node_id] = {"cpu": cpu_cores, "pods": [], "status": "healthy"}
    node_heartbeats[node_id] = time.time()
    
    return jsonify({"message": "Node added", "node_id": node_id})

# 🟢 List All Nodes
@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(nodes)

# 🟢 Launch Pod (Assign to a Node)
@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    data = request.json
    pod_id = f"pod-{len(pods) + 1}"
    cpu_req = data.get("cpu")

    # Find a node with enough CPU
    for node_id, info in nodes.items():
        if info["cpu"] >= cpu_req:
            nodes[node_id]["pods"].append(pod_id)
            nodes[node_id]["cpu"] -= cpu_req  # Reserve CPU
            pods[pod_id] = {"cpu": cpu_req, "node": node_id}
            return jsonify({"message": "Pod launched", "pod_id": pod_id, "node": node_id})

    return jsonify({"error": "No available node with enough CPU"}), 400

# 🟢 Node Heartbeat (Health Check)
@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node_id = data.get("node_id")

    if node_id in nodes:
        node_heartbeats[node_id] = time.time()
        nodes[node_id]["status"] = "healthy" 
        return jsonify({"message": "Heartbeat received"})
    else:
        return jsonify({"error": "Node not found"}), 404

# 🟢 Monitor Node Health (Detect Failures)
def monitor_health():
    while True:
        time.sleep(5)  # Check every 5 seconds
        current_time = time.time()

        for node_id, last_hb in node_heartbeats.items():
            if current_time - last_hb > HEARTBEAT_INTERVAL:
                print(f" Node {node_id} failed! Rescheduling pods...")
                nodes[node_id]["status"] = "failed"

                # Reschedule pods
                for pod in nodes[node_id]["pods"]:
                    for new_node in nodes:
                        if nodes[new_node]["cpu"] >= pods[pod]["cpu"]:
                            nodes[new_node]["pods"].append(pod)
                            nodes[new_node]["cpu"] -= pods[pod]["cpu"]
                            pods[pod]["node"] = new_node
                            break
                
                nodes[node_id]["pods"] = []  # Clear pods from failed node

# Start Health Monitoring Thread
threading.Thread(target=monitor_health, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
