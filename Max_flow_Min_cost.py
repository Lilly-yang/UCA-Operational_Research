from ortools.graph import pywrapgraph

# between each pair. For instance, the arc from node s to node 1 has capacity of 16 and a unit cost of 58.
start_nodes = []
end_nodes = []
capacities = []
unit_costs = []

f = open("./Flows.txt")
line = f.readlines()
for i, l in enumerate(line):
    line[i] = [int(i) for i in l.split()]

for l in line[1:]:
    start_nodes.append(l[0])
    end_nodes.append(l[1])
    capacities.append(l[2])
    unit_costs.append(l[3])

# Define an array of supplies at each node.
supplies = [24, 0, 0, 0, 0, 0, -24]

# Instantiate a SimpleMinCostFlow solver.
min_cost_flow = pywrapgraph.SimpleMinCostFlow()
# Add each arc.
for i in range(0, len(start_nodes)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i], capacities[i], unit_costs[i])
# Add node supplies.
for i in range(0, len(supplies)):
    min_cost_flow.SetNodeSupply(i, supplies[i])
# Find the minimum cost flow between node s and node t.
if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
    print('Maximum flow:', min_cost_flow.MaximumFlow())
    print('Minimum cost:', min_cost_flow.OptimalCost(), '\n')
    print('  Arc    Flow / Capacity  Cost')
    for i in range(min_cost_flow.NumArcs()):
        cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
        print('%1s -> %1s   %3s  / %3s       %3s' % (
            min_cost_flow.Tail(i),
            min_cost_flow.Head(i),
            min_cost_flow.Flow(i),
            min_cost_flow.Capacity(i),
            cost))
else:
    print('There was an issue with the min cost flow input.')
