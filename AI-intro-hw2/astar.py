import csv
import os
import heapq

py_dir = os.path.dirname(os.path.realpath(__file__))
edgeFile = open(py_dir+'\\edges.csv', newline='')
heuristicFile = open(py_dir+'\\heuristic.csv', newline='')
rws = csv.DictReader(edgeFile)

# use dict to store edges 
# key is start. And value is a 2d-list
# [[end, dis, spd_lim], ...]
edges = dict()
lis = list()
prev = -1
for rw in rws:
    # because edges.csv is sorted by start node, this way is okay
    if int(rw['start']) != prev:
        edges[prev] = lis
        prev = int(rw['start'])
        lis = list() # initialize

    lis.append([int(rw['end']), float(rw['distance']), float(rw['speed limit'])])
edgeFile.close() # data are stored in edges, thus close the file

# use dict to store heuristic
# key is the node, value is tuple (dis to id1,2,3)
heu = dict()
rws_heu = csv.DictReader(heuristicFile)
for rwh in rws_heu:
    heu[int(rwh['node'])] = (float(rwh['1079387396']), float(rwh['1737223506']), float(rwh['8513026827']))

# use heapq (priority_queue) storing 
# tuple containing (dis, next_node)
# to get mini distance choice
def astar(start, end):
    # Begin your code (Part 4)
    # to select the testcase
    if end==1079387396: sel=0
    elif end==1737223506: sel=1
    else: sel=2

    # initialize
    ans = dict()
    ans[start] = [0.0, -1]# the distance from start to start is 0
    nw = (0, start) # changed to tuple
    pq = []
    num_vised = 0
    done = False
    path = list()

    while not done:
        for next in edges[nw[1]]: # next is a list [end, dis, spd_lim]
            if next[0] in edges: # if there is edge started from this node
                if next[0] != end and next[0] not in ans:
                    # works when not achieve to final node 
                    # and this node has not been visited yet
                    heapq.heappush(pq, (ans[nw[1]][0]+heu[next[0]][sel], next[0]) )
                    ans[next[0]] = [ans[nw[1]][0] + next[1], nw[1]]# update the distance and num_node
                    num_vised+=1
                elif next[0] in ans and ans[next[0]][0]>=ans[nw[1]][0]+next[1]:
                    # renew to shortest distance
                    heapq.heappush(pq, (ans[nw[1]][0]+next[1], next[0]) )
                    ans[next[0]] = [ans[nw[1]][0] + next[1], nw[1]]
                elif next[0]==end: # reach the end
                    ans[next[0]] = [ans[nw[1]][0] + next[1], nw[1]]
                    # to get the path by reversing back
                    back = end
                    path.append(back)
                    while ans[back][1] != start:
                        path.append(ans[back][1])
                        back = ans[back][1]
                    path.append(start)
                    done = True
                    num_vised+=1
        nw = heapq.heappop(pq)

    return path, ans[end][0], num_vised
    
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
