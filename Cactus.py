import math
from collections import defaultdict

INF = float("inf")

def DFS(v, parent, graph, disc, low, time, S, val, dp):

    time[0] += 1
    disc[v] = low[v] = time[0]

    min_dp = INF

    for u in graph[v]:
        
        flag = False
        if disc[u] == -1:   # not visited
            S.append((v, u))
            DFS(u, v, graph, disc, low, time, S, val, dp)
            flag = True

        elif u != parent:
            low[v] = min(low[v], disc[u])

        if(flag == False or (flag == True and S[-1:] == [(v, u)] and low[u] > disc[v])):
            if low[u] == disc[v] or S[-1:] == [(v, u)]:
                block_edges = []
                while S:
                    e = S.pop()
                    block_edges.append(e)
                    if v in e:
                        break
                       
                # Collect vertices in this block
                C = set([x for edge in block_edges for x in edge if x != v])

                # sum, min1, min2
                valid = [x for x in C if dp[x][1] != -1]
                s = sum(dp[x][1] for x in valid)
                diffs = sorted([dp[x][0] - dp[x][1] for x in valid])

                min1 = diffs[0] if len(diffs) > 0 else 1
                min2 = diffs[1] if len(diffs) > 1 else 1
                
                if len(C) == 1:
                    # single-edge block
                    val[v][0][0] = 1 + s
                    val[v][0][1] = s + min1
                    val[v][1][0] = s
                else:
                    # cycle block
                    val[v][0][0] = 2 + s
                    val[v][0][1] = 1 + s + min1
                    val[v][0][2] = s + min1 + min2
                    val[v][1][0] = 1 + s
                    val[v][1][1] = s + min1

                # update dp[v]
                dp[v][0] += min([val[v][1][0], val[v][1][1] if val[v][1][1] != -1 else INF])
                dp[v][1] += min([val[v][1][0], val[v][1][1] if val[v][1][1] != -1 else INF])

                # update min_dp
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
    """
    Algorithm 1: Compute Z0(G)
    """
    V = list(graph.keys())
    ans = INF

    for root in V:
        S = []
        disc = {v: -1 for v in V}
        low = {v: -1 for v in V}
        time = [0]  # mutable integer
        val = {u: [[-1 for _ in range(3)] for _ in range(2)] for u in V}
        dp = {u: [0, 0] for u in V}

        DFS(root, None, graph, disc, low, time, S, val, dp)
        ans = min(ans, dp[root][0])

    return ans

if __name__ == "__main__":
    # Input format:
    # n m
    # u1 v1
    # u2 v2
    # ...
    # um vm
    n, m = map(int, input("Enter number of vertices and edges (n m): ").split())
    graph = defaultdict(list)

    print("Enter the edges (u v):")
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    # Ensure all vertices are in graph
    for v in range(1, n+1):
        if v not in graph:
            graph[v] = []

    result = compute_Z0(graph)
    print("Z0(G) =", result)