import requests

API_URL = "http://127.0.0.1:5000"

def add_node():
    """ Prompts user for CPU cores and sends request to API server """
    cpu = input("Enter CPU cores for new node: ")
    response = requests.post(f"{API_URL}/add_node", json={"cpu": int(cpu)})
    print(response.json())

def list_nodes():
    """ Fetches and displays all registered nodes """
    response = requests.get(f"{API_URL}/list_nodes")
    print(response.json())

def main():
    while True:
        print("\n1. Add Node\n2. List Nodes\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_node()
        elif choice == "2":
            list_nodes()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
