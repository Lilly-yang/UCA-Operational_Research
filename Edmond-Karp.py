# -*- encoding:gbk -*-
from queue import Queue
import copy

q = Queue()  # for finding augmented path

f = open("./Flows.txt")
line = f.readlines()
for i, l in enumerate(line):
    line[i] = [int(i) for i in l.split()]

m = line[0][0]  # number of vertex
n = line[0][1]  # number of edges

residual = [[0 for i in range(m)] for j in range(m)]  # residual flow of residual graph
maxflowgraph = [[0 for i in range(m)] for j in range(m)]  # for recording the max-flow, initial is 0
flow = [0 for i in range(m)]  # recording min-flow of edges for each augmented path
pre = [float('inf') for i in range(m)]  # Record the precursor of each node of the augmented path

# Set the initial flow of the graph
for l in line[1:]:
    residual[l[0]][l[1]] = l[2]

graph = copy.deepcopy(residual)


def BFS(source, sink):
    q.empty()  # empty the queen

    for i in range(m):
        pre[i] = float('inf')

    # important! otherwise the funded flow will always be 0.
    # But only source, no need empty other nodes.
    flow[source] = float('inf')
    q.put(source)
    while not q.empty():
        index = q.get()
        if index == sink:
            break
        for i in range(m):
            if (i != source) & (residual[index][i] > 0) & (pre[i] == float('inf')):
                # i!=source，no deed to analysis flow from source to itself
                # residual[index][i]>0，flow can traver the arc
                # pre[i]==float('inf')，it's means BFS is not reach this node yet
                pre[i] = index
                flow[i] = min(flow[index], residual[index][i])
                q.put(i)
    if pre[sink] == float('inf'):
        # The precursor of the meeting point is still the initial value
        # indicating that there is no augmenting path
        return -1
    else:
        return flow[sink]


def maxflow(source, sink):
    sumflow = 0  # Record the maximum stream and keep accumulating
    # augmentflow = 0 #The minimum passing flow of the augmented path currently found
    while True:
        augmentflow = BFS(source, sink)
        if augmentflow == -1:
            # no augmented path
            break
        k = sink
        while k != source:  # stop while if k goes back to the starting point
            prev = pre[k]  # from prev to k
            maxflowgraph[prev][k] += augmentflow
            residual[prev][k] -= augmentflow  # The direction of travel is consumed
            residual[k][prev] += augmentflow  # reverse arc
            k = prev
        sumflow += augmentflow
    return sumflow


result = maxflow(0, m - 1)
print('Maximum flow:', result, '\n')
print('  Arc    Flow / Capacity')
for e, arc in enumerate(maxflowgraph):
    for t, flow in enumerate(arc):
        if flow != 0:
            print('%1s -> %1s   %3s  / %3s' % (e, t, flow, graph[e][t]))
