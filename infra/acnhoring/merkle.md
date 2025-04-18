---
id: project404.infra_anchoring
ver: 0.1
parent: project404.foundation
hash: null
---

# Инфраструктура Anchoring (Merkle)

Документ описывает, как мы фиксируем корневые хэши и Merkle‑proof в блокчейн.

## 1. Структура Merkle‑дерева
- Листовые узлы: `hash = sha256(content)`
- Внутренние узлы: `hash = sha256(concat(child1, child2, ...))`

## 2. Смарт‑контракт
- Хранит единственный `rootHash` и проверяет Merkle‑proof.
- API‑методы: `updateRoot(bytes32 newRoot, bytes32[] proof, bytes32[] proofPath)`

## 3. Обновление цепочки
1. Генерация нового `rootHash` off‑chain.
2. Формирование Merkle‑proof для изменённого узла.
3. Транзакция `updateRoot` с proof.

## 4. Пример скрипта обновления
```bash
# perl‑style pseudocode
node merkle_update.js \
  --graph project404.graph.yaml \
  --node capture/0001-boat-wreck \
  --contract 0xABC... \
  --key ~/.keys/priv.key