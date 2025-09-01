from collections import defaultdict

def find_blocks(graph):
    
    time = 0
    disc = {v: -1 for v in graph}
    low = {v: -1 for v in graph}
    S = []  # stack of edges
    blocks = []

    def dfs(v, parent):
        nonlocal time
        time += 1
        disc[v] = low[v] = time

        for u in graph[v]:
            if disc[u] == -1:  # tree edge
                S.append((v, u))
                dfs(u, v)
                low[v] = min(low[v], low[u])

                if low[u] >= disc[v]:
                    block = set()
                    while S:
                        e = S.pop()
                        block.update(e)
                        if e == (v, u) or e == (u, v):
                            break
                    blocks.append(block)

            elif u != parent and disc[u] < disc[v]:  # back edge
                low[v] = min(low[v], disc[u])

    for v in graph:
        dfs(v, None)
        break

    return blocks

def calcZ(blocks, colored, removed, graph):
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


if __name__ == "__main__":
    n, m = map(int, input("Enter n m: ").split())
    graph = defaultdict(list)
    for _ in range(m):
        u, v = input().split()
        graph[u].append(v)
        graph[v].append(u)
        
    blocks = find_blocks(graph)
    print("Blocks (biconnected components):")
    for i, block in enumerate(blocks, 1):
        print(f"Block {i}: {block}")
    
    colored = {v: 0 for v in graph}
    removed = {v: 0 for v in graph}
    Z = calcZ(blocks, colored, removed, graph)
    print("Z(G) = ", Z)
