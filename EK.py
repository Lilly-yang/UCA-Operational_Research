import copy
from collections import deque


def hasPath(Gf, s, t, path):
    # BFS algorithm
    V = len(Gf)
    visited = list(range(V))
    for i in range(V):
        visited[i] = False
    visited[s] = True
    queue = deque([s])
    while queue:
        temp = queue.popleft()
        if temp == t:
            return True
        for i in range(V):
            if not visited[i] and (Gf[temp][i] > 0):
                queue.append(i)
                visited[i] = True
                path[i] = temp  # record precursor
    return visited[t]


def bfs(adj, start):
    b = []
    if start is None:
        return
    visited = set()
    queue = [start]
    visited.add(start)
    b.append(start)
    while len(queue) > 0:
        cur = queue.pop(0)
        if cur in adj.keys():
            # Visit all its neighbors
            for nex in adj[cur]:
                if nex not in visited:
                    visited.add(nex)
                    b.append(nex)
                    queue.append(nex)
    return b


def max_flow(graph, s, t):
    maxFlow = 0
    Gf = copy.deepcopy(graph)
    V = len(Gf)
    path = list(range(V))
    while hasPath(Gf, s, t, path):
        min_flow = float('inf')
        v = t
        while v != s:
            u = path[v]
            min_flow = min(min_flow, Gf[u][v])
            v = path[v]
        v = t
        while v != s:
            u = path[v]
            Gf[u][v] -= min_flow
            Gf[v][u] += min_flow
            v = path[v]
        maxFlow += min_flow
    print("maxFlow", maxFlow)
    return Gf


f = open("./Flows.txt")
line = f.readlines()
for i, l in enumerate(line):
    line[i] = [int(i) for i in l.split()]

m = line[0][0]  # number of vertexes
capacity = [[0 for i in range(m)] for j in range(m)]  # residual flow
for l in line[1:]:
    capacity[l[0]][l[1]] = l[2]

s = line[0][2]  # s is emanatingNode
t = line[0][3]  # t is terminatingNode
GF = copy.deepcopy(max_flow(capacity, s, t))

##  Define a dictionary to access the adjacency list structure of the residual graph
g = {}
#### Used to store bfs traversed points
c_bfs = []
#### Used to store points that bfs has not traversed
c_notbfs = []

##  Store the access residual graph into the adjacency list structure into g
for i in range(len(GF)):
    a = []
    for j in range(len(GF)):
        if GF[i][j] != 0:
            a.append(j)
            g[i] = a

# Define an identifier for judgment
dd = 0
c_bfs = bfs(g, s)

# Find the points that bfs has not traversed and store them in the array c_notbfs
for i in range(len(GF)):
    for j in range(len(c_bfs)):
        if i == c_bfs[j]:
            dd = 1
    if dd == 0:
        c_notbfs.append(i)
    dd = 0

# print min-cut
print('arcs of min cut:')
for i in c_bfs:
    for j in c_notbfs:
        if capacity[i][j] != 0:
            print(i, '->', j)
