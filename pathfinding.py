from collections import deque

class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.miniMap
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.getGraph()

    def getPath(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]

        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            curNode = queue.popleft()
            if curNode == goal:
                break
            nextNodes = graph[curNode]

            for nextNode in nextNodes:
                if nextNode not in visited and nextNode not in self.game.objectHandler.npcPositions:
                    queue.append(nextNode)
                    visited[nextNode] = curNode

        return visited

    def getNextNodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.worldMap]

    def getGraph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.getNextNodes(x, y)
