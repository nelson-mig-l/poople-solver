from collections import deque
from typing import Optional, List, Dict

def solve(graph: Dict[str, List[str]], start: str, end: str = "POOP") -> Optional[List[str]]:
    queue = deque([[start]])
    visited = set([start])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None
