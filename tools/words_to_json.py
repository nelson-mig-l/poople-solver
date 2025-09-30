import json
import sys
from typing import List, Dict


def load_nodes(file_path: str) -> List[str]:
    nodes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            nodes.append(line.strip())
    return nodes


def is_one_char_diff(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    diff_count = sum(c1 != c2 for c1, c2 in zip(word1, word2))
    return diff_count == 1


def build_graph(nodes: List[str]) -> Dict[str, List[str]]:
    graph = {node: [] for node in nodes}
    for i, word1 in enumerate(nodes):
        for word2 in nodes[i + 1:]:
            if is_one_char_diff(word1, word2):
                graph[word1].append(word2)
                graph[word2].append(word1)
    return graph


def convert(input_file: str, output_file: str):
    print("Converting words to JSON...")
    nodes = load_nodes(input_file)
    data = build_graph(nodes)
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=2)
    print("Done.")


if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) != 2:
        print("Usage: python words_to_json.py <input_txt_file> <output_json_file>")
        sys.exit(1)
    convert(params[0], params[1])
