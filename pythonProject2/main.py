def create_graph(input_file):
    with open(input_file, 'r') as file:
        num_vertices, num_edges = map(int, file.readline().split())
        graph = [[] for _ in range(num_vertices)]  # Create an empty adjacency list

        for _ in range(num_edges):
            line = file.readline().split()
            start_vertex = ord(line[0]) - ord('A')  # Convert the alphabetic character to vertex index
            end_vertex = ord(line[1]) - ord('A')
            weight = int(line[2])

            graph[start_vertex].append((end_vertex, weight))  # Add the edge to the adjacency list

    return graph


def display_adjacency_list(graph):
    num_vertices = len(graph)

    for vertex in range(num_vertices):
        print(f"Vertex {chr(vertex + ord('A'))}:", end=' ')

        for edge in graph[vertex]:
            end_vertex, weight = edge
            print(f"{chr(end_vertex + ord('A'))}({weight})", end=' ')

        print()


graph = create_graph("location.txt")
display_adjacency_list(graph)
