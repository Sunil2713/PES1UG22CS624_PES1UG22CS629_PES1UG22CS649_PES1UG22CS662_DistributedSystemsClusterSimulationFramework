from flask import Flask, request, jsonify
import docker

app = Flask(__name__)

# In-memory storage for nodes
nodes = {}
node_id_counter = 1

# Initialize Docker client
docker_client = docker.from_env()

@app.route("/add_node", methods=["POST"])
def add_node():
    """ Adds a node to the cluster and launches a container """
    global node_id_counter
    data = request.json
    cpu_cores = data.get("cpu")

    if not cpu_cores:
        return jsonify({"error": "CPU cores required"}), 400

    node_id = f"node-{node_id_counter}"
    node_id_counter += 1

    # Launch Docker container for the node
    container = docker_client.containers.run(
        "python:3.9",
        command="sleep infinity",
        detach=True,
        name=node_id
    )

    # Store node details
    nodes[node_id] = {
        "cpu": cpu_cores,
        "container_id": container.id,
        "status": "running"
    }

    return jsonify({"message": f"Node {node_id} added", "node": nodes[node_id]})

@app.route("/list_nodes", methods=["GET"])
def list_nodes():
    """ Lists all active nodes """
    return jsonify(nodes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
