import requests

API_SERVER = "http://127.0.0.1:5000"

def add_node():
    cpu = int(input("Enter CPU cores for the new node: "))
    response = requests.post(f"{API_SERVER}/add_node", json={"cpu": cpu})
    print(response.json())

def list_nodes():
    response = requests.get(f"{API_SERVER}/list_nodes")
    print(response.json())

def launch_pod():
    cpu = int(input("Enter CPU required for pod: "))
    response = requests.post(f"{API_SERVER}/launch_pod", json={"cpu": cpu})
    print(response.json())

def main():
    while True:
        print("\n1. Add Node\n2. List Nodes\n3. Launch Pod\n4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_node()
        elif choice == "2":
            list_nodes()
        elif choice == "3":
            launch_pod()
        elif choice == "4":
            break
        else:
            print(" Invalid choice, try again.")

if __name__ == "__main__":
    main()
