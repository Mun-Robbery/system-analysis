import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

TEST_STRING = """
    {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }
"""

@dataclass
class GraphNode:
    children: List[int]
    parent: Optional[str]
    relations: List[int] = field(default_factory=lambda: [0] * 5)

    def __str__(self) -> str:
        return f"{self.children}, {self.parent}, {self.relations}"


class GraphAnalyzer:
    def __init__(self, json_string: str):
        self.graph_data = json.loads(json_string)
        self.graph_repr: Dict[str, GraphNode] = {}

    def analyze(self) -> tuple[Dict[str, GraphNode], float]:
        self._build_graph()
        self._calculate_relations()
        sorted_graph = self._sort_graph()
        entropy = self._calculate_entropy([node.relations for node in sorted_graph.values()])
        return sorted_graph, entropy

    def _build_graph(self) -> None:
        self._recursive_parse(self.graph_data)

    def _recursive_parse(self, graph: Dict[str, Dict], parent: Optional[str] = None) -> None:
        for node_id, children in graph.items():
            child_nodes = []
            if isinstance(children, dict) and children:
                self._recursive_parse(children, node_id)
                child_nodes = list(children.keys())

            node = GraphNode(child_nodes, parent)
            node.relations[0] = len(child_nodes)
            node.relations[1] = 1 if parent is not None else 0
            self.graph_repr[node_id] = node

    def _calculate_relations(self) -> None:
        for node_id, node in self.graph_repr.items():
            if node.parent is not None:
                parent = self.graph_repr[node.parent]
                node.relations[4] += len(parent.children) - 1
                if parent.parent is not None:
                    node.relations[3] += 1

            for child_id in node.children:
                child = self.graph_repr[str(child_id)]
                node.relations[2] += child.relations[2] + len(child.children)
                child.relations[3] += node.relations[3]

    def _sort_graph(self) -> Dict[str, GraphNode]:
        return dict(sorted(self.graph_repr.items(), key=lambda x: x[0]))

    @staticmethod
    def _calculate_entropy(matrix: List[List[int]]) -> float:
        if not matrix:
            return 0.0

        column_entropy = [0.0] * len(matrix[0])
        for row in matrix:
            row_sum = len(row) - 1
            for i, value in enumerate(row):
                if value == 0:
                    continue
                probability = value / row_sum
                column_entropy[i] -= probability * math.log2(probability)

        return sum(column_entropy)


def main(input_string: str) -> None:
    analyzer = GraphAnalyzer(input_string)
    graph, entropy = analyzer.analyze()

    for node_id, node in graph.items():
        print(f"{node_id}: {node.relations}")
    print(entropy)


if __name__ == "__main__":
    main(TEST_STRING)