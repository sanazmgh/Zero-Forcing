import random
import time
from collections import defaultdict

INF = float("inf")

def dfs(v, parent, graph, disc, low, time, stack, val, dp, seen_edges):

    time[0] += 1
    disc[v] = low[v] = time[0]

    min_dp = INF

    for u in graph[v]:
        
        if ((u,v) in seen_edges or (v,u) in seen_edges):
            continue

        flag = False
        if disc[u] == -1:
            stack.append((v, u))
            dfs(u, v, graph, disc, low, time, stack, val, dp, seen_edges)
            flag = True

        elif u != parent:
            low[v] = min(low[v], disc[u])

        found_cycle = False
        if(flag== True and stack):
            [(a,b)] = stack[-1:]
            if ((a in graph[v] or b in graph[v]) and (a != v and b!=v) and (a!=u or b!=u)):
                found_cycle = True
                seen_edges.append((v, a if a in graph[v] else b))

        if((flag == True and stack[-1:] == [(v, u)] and low[u] > disc[v]) or found_cycle==True):
            if stack[-1:] == [(v, u)] or found_cycle == True:
                block_edges = []
                while stack:
                    e = stack.pop()
                    block_edges.append(e)
                    if v in e:
                        break
                       
                cycle = set([x for edge in block_edges for x in edge if x != v])

                valid = [x for x in cycle if dp[x][1] != -1]
                summation = sum(dp[x][1] for x in valid)
                diffs = sorted([dp[x][0] - dp[x][1] for x in valid])

                min1 = diffs[0] if len(diffs) > 0 else 1
                min2 = diffs[1] if len(diffs) > 1 else 1
                
                if len(C) == 1:
                    val[v][0][0] = 1 + summation
                    val[v][0][1] = summation + min1
                    val[v][1][0] = summation

                    val[v][0][2] = -1
                    val[v][1][1] = -1
                else:
                    val[v][0][0] = 2 + summation
                    val[v][0][1] = 1 + summation + min1
                    val[v][0][2] = summation + min1 + min2
                    val[v][1][0] = 1 + summation
                    val[v][1][1] = summation + min1

                dp[v][0] += min([val[v][1][0], val[v][1][1] if val[v][1][1] != -1 else INF])
                dp[v][1] += min([val[v][1][0], val[v][1][1] if val[v][1][1] != -1 else INF])

                for i in range(3):
                    for j in range(2):
                        if val[v][1][j] != -1 and val[v][0][i] != -1:
                            other = val[v][1][(j + 1) % 2]
                            if val[v][1][j] <= other or other == -1:
                                min_dp = min(min_dp, val[v][0][i] - val[v][1][j])

    if(min_dp == INF):
        min_dp = 0

    dp[v][0] = max([dp[v][0] + min_dp, 1])


def compute_Z0(graph):
    ans = INF
    vertices = list(graph.keys())
    
    for root in vertices:
        stack = []
        disc = {v: -1 for v in vertices}
        low = {v: -1 for v in vertices}
        time = [0]
        val = {u: [[-1 for _ in range(3)] for _ in range(2)] for u in vertices}
        dp = {u: [0, 0] for u in vertices}
        seen_edges = []

        dfs(root, None, graph, disc, low, time, stack, val, dp, seen_edges)
        ans = min(ans, dp[root][0])
        
    return ans

def generate_cactus(n, max_cycles=None, max_attempts=1000):
    if n < 1:
        return defaultdict(list)

    graph = defaultdict(list)

    vertices = list(range(1, n+1))
    connected = [vertices.pop(0)]
    while vertices:
        u = random.choice(connected)
        v = vertices.pop(0)
        graph[u].append(v)
        graph[v].append(u)
        connected.append(v)

    def bfs_parent(root=1):
        parent = {root: None}
        queue = [root]
        while queue:
            curr = queue.pop(0)
            for nei in graph[curr]:
                if nei not in parent:
                    parent[nei] = curr
                    queue.append(nei)
        return parent

    parent = bfs_parent(1)

    edges_in_cycles = set()
    max_cycles = max_cycles or n // 3
    cycles_added = 0
    attempts = 0

    while cycles_added < max_cycles and attempts < max_attempts:
        v = random.randint(1, n)
        current = parent[v]
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]

        added = False
        for anc in path:
            path_edges = []
            x = v
            while x != anc:
                p = parent[x]
                path_edges.append(tuple(sorted((x, p))))
                x = p
                
            if any(e in edges_in_cycles for e in path_edges):
                continue
            if anc in graph[v]:
                continue

            graph[v].append(anc)
            graph[anc].append(v)
            edges_in_cycles.update(path_edges)
            edges_in_cycles.add(tuple(sorted((v, anc))))
            cycles_added += 1
            added = True
            break
        attempts += 1 if not added else 0

    return graph, cycles_added


def run_experiment(n):
    graph, cycles = generate_cactus(n)
    edges = sum(len(neighs) for neighs in graph.values()) // 2

    print("Generated cactus graph:")
    print(f"Vertices (n): {n}")
    print(f"Edges (m): {edges}")
    print(f"Cycles: {cycles}")
    
    start = time.time()
    z0 = compute_Z0(graph)
    end = time.time()
    
    print(f"Z0: {z0}")
    print(f"Running time: {end - start:.6f} seconds")

    return graph, edges, cycles, z0


if __name__ == "__main__":
    for n in [10, 50, 100, 500, 1000, 2000]:
        run_experiment(n)