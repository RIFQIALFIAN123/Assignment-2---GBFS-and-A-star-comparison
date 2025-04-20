import time
from queue import PriorityQueue
import numpy as np

def manhattan_distance(a, b):
    """Menghitung jarak Manhattan antara dua titik a dan b"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(grid, node):
    """Mendapatkan tetangga yang valid (dapat dilalui) dari suatu node"""
    rows, cols = grid.shape
    x, y = node
    neighbors = []
    
    # Periksa 4 arah (atas, kanan, bawah, kiri)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Periksa batas dan rintangan
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    
    return neighbors

def reconstruct_path(came_from, current):
    """Merekonstruksi jalur dari titik awal ke titik akhir"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # Balikan untuk mendapatkan jalur dari awal ke akhir

def a_star(grid, start, goal):
    """Implementasi algoritma A* pada grid"""
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    open_set_hash = {start}  # Untuk memeriksa apakah node ada di open set
    
    nodes_explored = 0
    
    while not open_set.empty():
        _, current = open_set.get()
        open_set_hash.remove(current)
        nodes_explored += 1
        
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, nodes_explored
        
        for neighbor in get_neighbors(grid, current):
            # g adalah jarak sebenarnya dari awal ke neighbor melalui current
            tentative_g_score = g_score[current] + 1
            
            # Jika ini adalah jalur yang lebih baik ke neighbor
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    return None, nodes_explored  # Tidak ada jalur yang ditemukan

def run_astar_experiment(grid, start, goal):
    """Menjalankan eksperimen A* dan mengukur waktu"""
    start_time = time.time()
    path, nodes_explored = a_star(grid, start, goal)
    execution_time = (time.time() - start_time) * 1000  # Konversi ke milidetik
    
    result = {
        'time_ms': execution_time,
        'path_length': len(path) if path else 0,
        'nodes_explored': nodes_explored,
        'path': path
    }
    
    return result

if __name__ == "__main__":
    # Contoh penggunaan
    # Buat grid 5x5 sederhana dengan beberapa rintangan
    grid = np.zeros((5, 5), dtype=int)
    
    # Tetapkan beberapa rintangan (nilai 1)
    grid[0, 3] = 1  # Rintangan di (0,3)
    grid[1, 0] = 1  # Rintangan di (1,0)
    grid[1, 1] = 1  # Rintangan di (1,1)
    grid[1, 3] = 1  # Rintangan di (1,3)
    grid[2, 3] = 1  # Rintangan di (2,3)
    grid[3, 1] = 1  # Rintangan di (3,1)
    grid[3, 2] = 1  # Rintangan di (3,2)
    
    start = (0, 0)  # Posisi awal S
    goal = (4, 4)   # Posisi tujuan G
    
    print("Grid:")
    for row in grid:
        print(" ".join(["#" if cell == 1 else "." for cell in row]))
    
    result = run_astar_experiment(grid, start, goal)
    
    print(f"\nHasil A*:")
    print(f"Waktu Eksekusi: {result['time_ms']:.2f} ms")
    print(f"Panjang Jalur: {result['path_length']} node")
    print(f"Node yang Dieksplorasi: {result['nodes_explored']}")
    print(f"Jalur: {result['path']}")