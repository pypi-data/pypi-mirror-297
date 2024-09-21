import collections

def bfs(graph, startnode):
    seen, queue = set([startnode]), collections.deque([startnode])
    while queue:
        vertex = queue.popleft()
        yield vertex
        for node in graph[vertex]:
            if node not in seen:
                seen.add(node)
                queue.append(node)

# Example usage
if __name__ == "__main__":
    gdict = {
        "a": set(["b", "c"]),
        "b": set(["a", "d"]),
        "c": set(["a", "d"]),
        "d": set(["e"]),
        "e": set(["a"])
    }
    print(list(bfs(gdict, "a")))