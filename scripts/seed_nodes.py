#!/usr/bin/env python3
"""
Seed Nodes Generator for Project404
Generates a specified number of test 'capture' nodes in the graph YAML.
Usage:
  python scripts/seed_nodes.py --count N
"""
"""
Создал скрипт scripts/seed_nodes.py для генерации тестовых точек боли. Он:
- Загружает project404.graph.yaml, оборачивая список в dict, если нужно.
- Добавляет --count новых узлов capture/seed-XX со стандартной metadata.
- Пишет новые nodes и edges обратно в YAML.
Теперь make seed будет работать. Не забудь добавить scripts/seed_nodes.py в репозиторий:

```bash
git add scripts/seed_nodes.py
git commit -m "feat: add seed_nodes.py for capture node generation"```
"""

import os
import sys
import yaml
import argparse
from datetime import date

def load_graph(path):
    if not os.path.exists(path):
        print(f"Graph file '{path}' not found.")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # If root is list, wrap into dict
    if isinstance(data, list):
        data = {'nodes': data, 'edges': []}
    return data


def save_graph(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Saved updated graph to {path}")


def generate_seed_nodes(graph, count):
    """Append 'count' seed capture nodes to graph."""
    today = date.today().isoformat()
    root_id = 'project404.root'
    existing_ids = {n['id'] for n in graph.get('nodes', [])}
    new_nodes = []
    new_edges = []
    start_idx = 1
    # Determine next available index
    while f"capture/seed-{start_idx:02d}" in existing_ids:
        start_idx += 1
    for i in range(count):
        idx = start_idx + i
        node_id = f"capture/seed-{idx:02d}"
        node = {
            'id': node_id,
            'ver': '0.0.1',
            'parent': root_id,
            'hash': '',
            'updated': today,
            'stage': 'capture',
            'processed': False,
            'data': {
                'reporter': 'seed',
                'title': f'Seed point {idx}',
                'description': 'Auto-generated seed point for testing',
                'severity': 'low'
            }
        }
        new_nodes.append(node)
        new_edges.append({'parent': root_id, 'child': node_id})
    graph['nodes'].extend(new_nodes)
    graph.setdefault('edges', []).extend(new_edges)
    print(f"Generated {count} seed nodes.")


def main():
    parser = argparse.ArgumentParser(description='Generate seed capture nodes')
    parser.add_argument('--count', type=int, default=1, help='Number of seed nodes to create')
    args = parser.parse_args()
    graph_file = 'project404.graph.yaml'

    graph = load_graph(graph_file)
    generate_seed_nodes(graph, args.count)
    save_graph(graph, graph_file)

if __name__ == '__main__':
    main()
