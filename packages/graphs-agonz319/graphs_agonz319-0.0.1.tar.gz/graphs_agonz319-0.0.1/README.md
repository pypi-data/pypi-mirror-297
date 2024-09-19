# Graphs Library

# Description
This is a Python library that provides a collection of algorithms and data structures for working with graphs, including an implementation of Dijkstra's shortest path algorithm module that uses methods from the heap queue algorithm. Heaps are useful data structures for implementing priority queues efficiently, which are often used in algorithms like Dijkstra's shortest path, where you need to quickly find and remove the smallest (or largest) element. This library can be used in graph-related projects.

# Features
**Shortest Path (SP)**:
  - Implementation of Dijkstra's algorithm for finding the shortest path in a weighted graph.

# SP Implementation
To begin finding the shortest path, import the **sp** module from this package into a python file with the code below following it: 

```
import sys

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print(f'Use: {sys.argv[0]} graph_file')
        sys.exit(1)

    graph = {}
    with open(sys.argv[1], 'rt') as f:
        f.readline() # skip first line
        for line in f:
            line = line.strip()
            s, d, w = line.split()
            s = int(s)
            d = int(d)
            w = int(w)
            if s not in graph:
                graph[s] = {}
            graph[s][d] = w
    
    s = 0
    dist, path = sp.dijkstra(graph, s)
    print(f'Shortest distances from {s}:')
    print(dist)
    for d in path: 
        print(f'spf to {d}: {path[d]}')
```

This file will calculate the shortest path by opening and reading from a graph file passed through the command line using the **sys** module. It takes only the path of the file it is in and path of the graph file as its arguements. Below is a format to use as an example:

```
python3 /path/to/current/file /path/to/graph/file
```

# Example 
The shortest path from 0 needs to be calculated from the following **graph.txt** file:

```
9
0 1 4
0 7 8
1 0 4
1 2 8
1 7 11
2 1 8
2 3 7
2 8 2
2 5 4
3 2 7
3 4 9
3 5 14
4 3 9
4 5 10
5 2 4
5 3 14
5 4 10
5 6 2
6 5 2
6 8 6
6 7 1
7 0 8
7 1 11
7 6 1
7 8 7
8 2 2
8 6 6
8 7 7
```

To do so, the code in the implementation section is inserted into a new python file in the projects directory.

Next, using the format given, the line to execute in the command-line is as shown:

```
python3 /Users/JohnDoe/Documents/Example/src/test.py /Users/JohnDoe/Documents/Example/graph.txt
```

Which displays the following output:

```
Shortest distances from 0:
[0, 4, 12, 19, 21, 11, 9, 8, 14]
spf to 0: []
spf to 1: [0]
spf to 7: [0]
spf to 2: [0, 1]
spf to 6: [0, 7]
spf to 8: [0, 1, 2]
spf to 5: [0, 7, 6]
spf to 3: [0, 1, 2]
spf to 4: [0, 7, 6, 5]
```
