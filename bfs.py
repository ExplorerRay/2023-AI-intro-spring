import csv
import os
import queue

# please put this python in the same folder as edges.csv
py_dir = os.path.dirname(os.path.realpath(__file__))
edgeFile = open(py_dir+'\\edges.csv', newline='')
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


# use dict to store path (ans)
# key is the end node, value is a list
# distance from start to this node and the previous node in this path
def bfs(start, end):
    # Begin your code (Part 1)

    # initialize
    ans = dict()
    ans[start] = [0.0, 1]# the distance from start to start is 0
    nw = start
    q = queue.SimpleQueue()
    num_vised = 0
    done = False
    path = list()

    while not done:
        for next in edges[nw]: # next is a list [end, dis, spd_lim]
            if next[0] in edges: # if there is edge started from this node
                if next[0] != end and next[0] not in ans:
                    # works when not achieve to final node 
                    # and this node has not been visited yet
                    q.put(next[0])
                    ans[next[0]] = [ans[nw][0] + next[1], nw]# update the distance and num_node
                    num_vised+=1
                elif next[0]==end: # reach the end
                    ans[next[0]] = [ans[nw][0] + next[1], nw]
                    # to get the path by reversing back
                    back = end
                    path.append(back)
                    while ans[back][1] != start:
                        path.append(ans[back][1])
                        back = ans[back][1]
                    path.append(start)
                    done = True
                    num_vised+=1
        nw = q.get()

    return path, ans[end][0], num_vised
    # End your code (Part 1)

if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
