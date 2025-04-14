import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import sys

# Function to split a binary file into packets and assign IDs, saving them to a directory
def split_binary_file(file_path, packet_size, output_dir):
    packets = []
    packet_id = 0
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, "rb") as f:
        while chunk := f.read(packet_size):
            packets.append((packet_id, chunk))  # Store packet ID with data
            # Save each packet as a separate file in the output directory
            packet_file_path = os.path.join(output_dir, f"packet_{packet_id}.bin")
            with open(packet_file_path, "wb") as packet_file:
                packet_file.write(chunk)
            packet_id += 1

    return packets

# Function to perform BFS and find an augmenting path
def bfs(graph, residual_graph, source, sink, parent):
    visited = [False] * len(graph)
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(len(graph)):
            if not visited[v] and residual_graph[u][v] > 0:  # Check for capacity in residual graph
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

# Ford-Fulkerson algorithm to calculate max flow and determine paths
def ford_fulkerson(graph, source, sink):
    residual_graph = [row[:] for row in graph]  # Create residual graph as a copy of original graph
    parent = [-1] * len(graph)  # Array to store path information
    max_flow = 0
    paths = []  # To store all paths for visualization

    while bfs(graph, residual_graph, source, sink, parent):
        # Find the maximum flow through the path found by BFS
        path_flow = float('Inf')
        s = sink
        path = []  # Store the current path for this iteration

        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            path.append(s)
            s = parent[s]
        path.append(source)
        paths.append(path[::-1])  # Reverse the path to get source-to-sink order

        # Update residual capacities of edges and reverse edges along the path
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow, paths

# Visualization of the graph and flow paths for packets
def visualize_packet_paths(paths, packet_to_path_mapping):
    print("\nPacket Flow Paths:")
    for i, path in enumerate(paths):
        print(f"Path {i}: {' -> '.join(map(str, path))}")
    
    print("\nPacket-to-Path Mapping:")
    for packet_id, path_id in packet_to_path_mapping.items():
        print(f"Packet ID {packet_id} uses Path {path_id}")

# Visualization of the graph structure using NetworkX and save it as PNG
def visualize_graph(graph, source, sink, paths, output_dir):
    # Ensure output directory exists for saving the graph visualization
    os.makedirs(output_dir, exist_ok=True)

    G = nx.DiGraph()
    for u in range(len(graph)):
        for v in range(len(graph[u])):
            if graph[u][v] > 0:
                G.add_edge(u, v, capacity=graph[u][v])

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'capacity')
    plt.figure(figsize=(8, 6))  # Create a new figure for this plot
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight source and sink nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', node_size=2000)
    nx.draw_networkx_nodes(G, pos, nodelist=[sink], node_color='red', node_size=2000)

    # Label source and sink nodes
    plt.text(pos[source][0], pos[source][1] - 0.1, 'Source', ha='center', fontsize=10)
    plt.text(pos[sink][0], pos[sink][1] - 0.1, 'Sink', ha='center', fontsize=10)

    # Highlight paths used by packets
    for path in paths:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

    plt.title("Flow Network")
    
    # Save visualization as PNG file in the specified directory
    viz_file_path = os.path.join(output_dir, f"VIZ_{os.path.basename(output_dir)}.png")
    plt.savefig(viz_file_path)
    
    plt.close()  # Close this plot to prevent overlap with the next one

# Animated visualization of packet movement along paths
def animate_packet_movement(graph, source, sink, paths, packet_to_path_mapping, output_dir):
    G = nx.DiGraph()
    
    for u in range(len(graph)):
        for v in range(len(graph[u])):
            if graph[u][v] > 0:
                G.add_edge(u, v)

    pos = nx.spring_layout(G)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    def update(frame):
        ax.clear()
        
        # Draw base graph structure with nodes and edges
        nx.draw(G,
                pos,
                with_labels=True,
                node_color="lightblue",
                node_size=2000,
                ax=ax)
        
        # Highlight source and sink nodes
        nx.draw_networkx_nodes(G,
                               pos,
                               nodelist=[source],
                               node_color="green",
                               node_size=2000,
                               ax=ax)
        nx.draw_networkx_nodes(G,
                               pos,
                               nodelist=[sink],
                               node_color="red",
                               node_size=2000,
                               ax=ax)

        # Animate packet movement along one of the paths (cycling through frames)
        packet_id = frame // len(paths)  # Cycle through packets
        path_id = packet_to_path_mapping[packet_id]
        current_path = paths[path_id]
        
        edge_list = list(zip(current_path[:-1], current_path[1:]))
        
        # Highlight the entire path for the current packet
        nx.draw_networkx_edges(G,
                               pos,
                               edgelist=edge_list,
                               edge_color="orange",
                               width=2.5,
                               ax=ax)
        
        # Highlight the current position of the packet along the path
        current_node_index = frame % len(current_path)
        current_node = current_path[current_node_index]
        
        ax.text(pos[current_node][0], pos[current_node][1] - 0.1,
                f"Packet {packet_id}", ha='center', fontsize=10)

        ax.set_title(f"Packet Movement Animation\nCurrent Packet: {packet_id}")

    ani = FuncAnimation(fig,
                        update,
                        frames=len(packet_to_path_mapping) * len(paths),
                        interval=1000,  # Slow down the animation
                        repeat=True)

    # Save the animation as an APNG file in the output directory
    ani_file_path = os.path.join(output_dir, f"ANI_{os.path.basename(output_dir)}.gif")
    ani.save(ani_file_path, writer='pillow', fps=1)  # Adjust fps for smoother/slower playback

    plt.show()

if __name__ == "__main__":
    # Check if output directory name is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <output_directory_name>")
        sys.exit(1)

    output_dir_name = sys.argv[1]

    # Example graph represented as an adjacency matrix (capacity graph)
    capacities = [
        [0, 16, 13, 0, 0],
        [0, 0, 10, 12, 0],
        [0, 4, 0, 0, 14],
        [0, 0, 9, 0, 20],
        [0, 0, 0, 7, 0]
    ]

    source = 0   # Define Node 0 as Source
    sink = 4     # Define Node 4 as Sink

    # Calculate maximum flow and paths using Ford-Fulkerson algorithm
    max_flow_value, paths = ford_fulkerson(capacities, source, sink)
    print(f"The maximum possible flow is {max_flow_value}")

    # Specify the path to the encrypted.bin file (update this path accordingly)
    file_path = "encrypted.bin"

    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
    else:
        # Split the encrypted binary file into packets and save them to the output directory
        packet_size = 1024  # Size of each packet in bytes
        packets = split_binary_file(file_path=file_path,
                                    packet_size=packet_size,
                                    output_dir=output_dir_name)

        print(f"Split {len(packets)} packets from {file_path} into directory '{output_dir_name}'.")

        # Map each packet to a specific path (cycling through available paths)
        packet_to_path_mapping = {}
        for packet_id in range(len(packets)):
            path_id = packet_id % len(paths)  # Cycle through available paths
            packet_to_path_mapping[packet_id] = path_id

        # Display all paths and their associated packets
        visualize_packet_paths(paths, packet_to_path_mapping)

        # Visualize the graph with highlighted paths and source/sink nodes
        visualize_graph(capacities,
                        source,
                        sink,
                        paths,
                        output_dir_name)

        # Animate packet movement along their respective paths in the graph
        animate_packet_movement(capacities,
                                source,
                                sink,
                                paths,
                                packet_to_path_mapping,
                                output_dir_name)
