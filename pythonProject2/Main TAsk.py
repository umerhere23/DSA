from heapq import *
from TAsk2 import read_uav_data, display_shortest_path
from main import graph


class Graph:
    def __init__(self):
        self.graph = []

    def create_graph(self, input_file):
        with open(input_file, 'r') as file:
            num_vertices, num_edges = map(int, file.readline().split())
            self.graph = [[] for _ in range(num_vertices)]  # Create an empty adjacency list

            for _ in range(num_edges):
                line = file.readline().split()
                start_vertex = ord(line[0]) - ord('A')  # Convert the alphabetic character to vertex index
                end_vertex = ord(line[1]) - ord('A')
                weight = int(line[2])

                self.graph[start_vertex].append((end_vertex, weight))  # Add the edge to the adjacency list

    def display_adjacency_list(self):
        num_vertices = len(self.graph)

        for vertex in range(num_vertices):
            print(f"Vertex {chr(vertex + ord('A'))}:", end=' ')

            for edge in self.graph[vertex]:
                end_vertex, weight = edge
                print(f"{chr(end_vertex + ord('A'))}({weight})", end=' ')

            print()


class LocationHashTable:
    def __init__(self):
        self.hash_table = {}

    def create_location_hash_table(self, data):
        for line in data:
            values = line.split()
            location = values[0]
            if len(values) == 4:
                temperature = int(values[1])
                humidity = int(values[2])
                wind_speed = int(values[3])
            else:
                temperature = 0
                humidity = 0
                wind_speed = 0
            self.hash_table[location] = (temperature, humidity, wind_speed)

    def search_location(self, location):
        vertex = ord(location) - ord('A')
        neighbors = [chr(v + ord('A')) for v, _ in graph[vertex]]
        return neighbors


class Itinerary:
    def __init__(self):
        self.risk_heap = []

    def update_risk(self, location, new_risk):
        for i, (old_risk, loc) in enumerate(self.risk_heap):
            if loc == location:
                self.risk_heap[i] = (new_risk, loc)
                heapify(self.risk_heap)
                return

        # If the location is not found in the heap, add it with the new risk value
        heappush(self.risk_heap, (new_risk, location))

    def provide_itinerary(self):
        itinerary = []

        while self.risk_heap:
            risk, location = heappop(self.risk_heap)
            itinerary.append(location)

        return itinerary


class Location:
    @staticmethod
    def get_risk_level(temperature, humidity, wind_speed):
        temperature_levels = ['low', 'medium', 'high']
        humidity_levels = ['high', 'medium', 'low']
        wind_speed_levels = ['low', 'medium', 'high']

        temperature_thresholds = [32, 40]
        humidity_thresholds = [30, 50]
        wind_speed_thresholds = [40, 55]

        temperature_risk_level = temperature_levels[sum(temperature > threshold for threshold in temperature_thresholds)]
        humidity_risk_level = humidity_levels[sum(humidity > threshold for threshold in humidity_thresholds)]
        wind_speed_risk_level = wind_speed_levels[sum(wind_speed > threshold for threshold in wind_speed_thresholds)]

        return temperature_risk_level, humidity_risk_level, wind_speed_risk_level


class Menu:
    def __init__(self):
        self.graph = Graph()
        self.uav_data = []
        self.location_hash_table = LocationHashTable()
        self.itinerary = Itinerary()

    def read_uav_data(self, file_name):
        with open(file_name, 'r') as file:
            self.uav_data = file.readlines()

    def insert_location(self):
        start_location = input("Enter the start location (A-J): ")
        end_location = input("Enter the end location (A-J): ")
        weight = int(input("Enter the weight of the edge: "))
        self.graph.insert_location(ord(start_location) - ord('A'), ord(end_location) - ord('A'), weight)
        print("Location and edge inserted.")

    def delete_location(self):
        location = input("Enter the location to delete (A-J): ")
        self.graph.delete_location(ord(location) - ord('A'))
        print("Location deleted.")

    def search_location(self):
        location = input("Enter the location to search for (A-J): ")
        neighbors = self.location_hash_table.search_location(location)
        print(f"Neighbors of {location}: {' '.join(neighbors)}")

    def display_adjacency_list(self):
        self.graph.display_adjacency_list()

    def shortest_path(self):
        start_location = input("Enter the start location (A-J): ")
        end_location = input("Enter the end location (A-J): ")
        display_shortest_path(self.graph.graph, start_location, end_location, self.uav_data)

    def update_risk_value(self):
        location = input("Enter the location to update risk value: ")
        temperature, humidity, wind_speed = self.location_hash_table.hash_table.get(location, (0, 0, 0))
        temperature_risk, humidity_risk, wind_speed_risk = Location.get_risk_level(temperature, humidity, wind_speed)
        new_risk = max(temperature_risk, humidity_risk, wind_speed_risk)
        self.itinerary.update_risk(location, new_risk)
        print("Risk value updated.")

    def provide_itinerary(self):
        itinerary = self.itinerary.provide_itinerary()
        print("Itinerary:")
        print(' -> '.join(itinerary))

    def main_menu(self):
        while True:
            print("\n--- MENU ---")
            print("1. Insert a location and edge")
            print("2. Delete a location")
            print("3. Search for a location")
            print("4. Display adjacency list")
            print("5. Shortest path between two locations")
            print("6. Update risk value")
            print("7. Provide itinerary")
            print("8. Exit")

            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                self.insert_location()

            elif choice == "2":
                self.delete_location()

            elif choice == "3":
                self.search_location()

            elif choice == "4":
                self.display_adjacency_list()

            elif choice == "5":
                self.shortest_path()

            elif choice == "6":
                self.update_risk_value()

            elif choice == "7":
                self.provide_itinerary()

            elif choice == "8":
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == '__main__':
    menu = Menu()
    menu.graph.create_graph("location.txt")
    menu.read_uav_data("UAVdata.txt")
    menu.location_hash_table.create_location_hash_table(menu.uav_data)
    menu.main_menu()
