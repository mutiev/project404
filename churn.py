#!/usr/bin/env python3
"""
Churn Chef Agent Script for Project404
Loads the single-file graph, finds the next Questions-stage node,
generates a patch via OpenAI, logs reasoning, and updates the graph.
"""
import os
import yaml
import openai
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set. Please define it in .env")

GRAPH_PATH = "project404.graph.yaml"
CONCLUSIONS_DIR = os.path.join("action", "conclusions")
os.makedirs(CONCLUSIONS_DIR, exist_ok=True)


def load_graph(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_graph(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def find_next_question_node(graph):
    # Look for nodes marked for Questions and not yet processed
    for node in graph.get('nodes', []):
        if node.get('stage') == 'questions' and not node.get('processed', False):
            return node
    return None


def patch_node_with_ai(node):
    prompt = (
        f"Предложи точечный патч для узла `{node['id']}`.\n"
        f"Данные узла: {node.get('data', {})}\n"
        "Готовь ответ в формате YAML-diff или описания изменений."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты помощник для обновления DBQA Pipeline."},
            {"role": "user", "content": prompt}
        ]
    )
    patch = response.choices[0].message.content.strip()
    node.setdefault('patches', []).append({
        'timestamp': datetime.utcnow().isoformat(),
        'patch': patch
    })
    node['processed'] = True
    return patch


def main():
    graph = load_graph(GRAPH_PATH)

    # Debug output
    print(f"Всего узлов: {len(graph.get('nodes', []))}")
    for n in graph.get('nodes', []):
        print(f"- {n['id']}: stage={n.get('stage')} processed={n.get('processed')}")

    node = find_next_question_node(graph)
    if not node:
        print("Не найден узел на этапе Questions для обработки.")
        return

    print(f"Патчим узел: {node['id']}")
    patch = patch_node_with_ai(node)

    # Write conclusion file
    now = datetime.utcnow().strftime("%Y%m%d-%H%M")
    conclusion_path = os.path.join(CONCLUSIONS_DIR, f"{now}.md")
    with open(conclusion_path, 'w', encoding='utf-8') as f:
        f.write(f"# Conclusion {now}\n")
        f.write(f"**Node:** {node['id']}\n\n")
        f.write("## Patch Proposal:\n")
        f.write(patch + "\n")

    # Save updated graph
    save_graph(graph, GRAPH_PATH)
    print(f"Узел `{node['id']}` обновлён и заключение сохранено в `{conclusion_path}`.")


if __name__ == "__main__":
    main()
