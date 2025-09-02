import time
import random
from collections import defaultdict

def find_blocks(graph):
    
    time = 0
    disc = {v: -1 for v in graph}
    low = {v: -1 for v in graph}
    stack = []
    blocks = []

    def dfs(v, parent):
        nonlocal time
        time += 1
        disc[v] = low[v] = time

        for u in graph[v]:
            if disc[u] == -1:
                stack.append((v, u))
                dfs(u, v)
                low[v] = min(low[v], low[u])

                if low[u] >= disc[v]:
                    block = set()
                    while stack:
                        e = stack.pop()
                        block.update(e)
                        if e == (v, u) or e == (u, v):
                            break
                    blocks.append(block)

            elif u != parent and disc[u] < disc[v]:
                low[v] = min(low[v], disc[u])

    for v in graph:
        dfs(v, None)
        break

    return blocks

def compute_Z(graph):
    blocks = find_blocks(graph)
    colored = {v: 0 for v in graph}
    removed = {v: 0 for v in graph}
    
    ans = 0

    for block in blocks:
        block_size = len(block)
        filled_vertices = sum(colored[v] for v in block)
        shared = None

        for v in block:
            flag = True
            for u in graph[v]:
                if removed[u]==0 and u not in block:
                    flag = False

            if flag == False:
                shared = v
                break

        if filled_vertices == block_size:
            for v in block:
                removed[v] = 1

        elif filled_vertices == block_size -1:
            for v in block:
                removed[v] = 1
                colored[v] = 1
        
        elif filled_vertices == block_size -2:
            for v in block:
                removed[v] = 1

                if(v != shared):
                    colored[v] = 1

            if (shared != None and colored[shared]==1) or shared == None:
                ans += 1
                colored[shared] = 1
        
        else:
            if (shared != None and colored[shared]==1) or shared == None:
                ans += block_size - filled_vertices - 1
            
            elif shared != None and colored[shared]==0:
                ans += block_size - filled_vertices - 2
            

            for v in block:
                removed[v] = 1

                if(v != shared):
                    colored[v] = 1

        if shared != None:
            removed[shared] = 0
    return ans


def generate_block_graph(n, max_blocks=None, max_attempts=1000):
    if n < 1:
        return defaultdict(list), 0

    graph = defaultdict(list)
    vertices = list(range(1, n+1))
    used = set()

    block_size = min(random.randint(2, 4), n)
    block_vertices = vertices[:block_size]
    used.update(block_vertices)

    for i in range(block_size):
        for j in range(i+1, block_size):
            u, v = block_vertices[i], block_vertices[j]
            graph[u].append(v)
            graph[v].append(u)

    max_blocks = max_blocks or n // 2
    blocks_added = 1
    attempts = 0

    while len(used) < n and blocks_added < max_blocks and attempts < max_attempts:
        available = list(set(vertices) - used)
        if not available:
            break

        attach_vertex = random.choice(list(used))
        
        possible_sizes = range(2, len(available) + 2)
        block_size = random.choice(possible_sizes)
        new_vertices = random.sample(available, block_size - 1)
        block_vertices = [attach_vertex] + new_vertices

        if len(new_vertices) == 0:
            attempts += 1
            continue

        for i in range(len(block_vertices)):
            for j in range(i+1, len(block_vertices)):
                u, v = block_vertices[i], block_vertices[j]
                if v not in graph[u]:
                    graph[u].append(v)
                if u not in graph[v]:
                    graph[v].append(u)

        used.update(new_vertices)
        blocks_added += 1
        attempts = 0

    return graph, blocks_added

def run_experiment(n):
    graph, blocks = generate_block_graph(n)

    edges = sum(len(neighs) for neighs in graph.values()) // 2

    print("Generated block graph:")
    print(f"Vertices (n): {n}")
    print(f"Edges (m): {edges}")
    print(f"Blocks: {blocks}")

    start = time.time()
    z = compute_Z(graph)
    end = time.time()

    print(f"Z: {z}")
    print(f"Running time: {end - start:.6f} seconds")

    return graph, edges, z, (end - start)


if __name__ == "__main__":
    for n in [10, 50, 100, 500, 1000]:
        run_experiment(n)
