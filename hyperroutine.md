# Гиперинструкция (ежедневный цикл Project 404) — версия 2.0

1. **Seed (Docs Stage)**
   - Запустить генерацию:
     ```bash
     make seed
     ```
   - Открыть `project404.graph.yaml` и найти все новые узлы вида  
     `capture/seed‑XX`.
   - Для каждого такого узла заполнить минимальный набор полей:
     ```yaml
     - id: capture/seed‑01
       ver: 0.0.1
       parent: project404.root
       hash: ""             # будет пересчитан
       updated: 2025‑MM‑DD   # сегодняшняя дата
       stage: basics        # сразу переводим в следующий этап
       data:
         reporter: "Arsen"                  # или кто посеял боль
         title: "Описание боли"            # краткий заголовок
         description: "Детальное описание" # что произошло, при каких условиях
         severity: "low|medium|high"        # уровень срочности
         # при необходимости:
         location:
           lat: <число>
           lon: <число>
     ```
   - Пересчитать и вставить хэш всего файла:
     ```bash
     make hash
     ```
   - Закоммитить:
     ```bash
     git add project404.graph.yaml
     git commit -m "basic: structure capture/seed‑XX nodes"
     ```

2. **Structure (Basics → Questions)**
   - Если вы сразу хотите два шага за раз, после заполнения полей `stage: basics` добавьте:
     ```yaml
     stage: questions
     processed: false
     checks:
       - фотография
       - координаты
       - подтверждение свидетелей
     ```
   - И снова:
     ```bash
     make hash
     git commit -m "chore: mark seed nodes for questions stage"
     ```

3. **AI‑Patch (Action)**
   - Запустить Echo‑агента:
     ```bash
     make ai
     ```
   - Убедиться, что в `project404.graph.yaml` у одного из `stage: questions` появился блок `patches` и `processed: true`.
   - Логи рассуждений и предложений будут в `action/conclusions/YYYYMMDD‑HHMM.md`.

4. **Commit & Push**
   - Собрать изменения:
     ```bash
     make commit
     git push
     ```

5. **Review & Iterate**
   - Рассмотреть PR: проверить предложенный AI‑патч, доработать вручную, смерджить.
   - Начать новый цикл с **Seed** или перейти к тестированию/Loop‑стадии.

> **Важно:**  
> – После каждого изменения в узле (seed, basics, questions) обязательно выполнять `make hash` и фиксировать коммит.  
> – Не оставляйте узлы без `stage` или `processed` — агент их просто пропустит.  
> – Цикл должен идти строго по одному узлу за итерацию, чтобы сохранить историю последовательной эволюции.  
