# Гиперинструкция (ежедневный цикл Project 404)

1. **Seed (Docs)**  
   – `make seed`  
   – Генерируете или вручную добавляете новую «точку боли» в `project404.graph.yaml`.

2. **Structure (Basics)**  
   – Открываете `project404.graph.yaml`, находите новый узел `capture/...`.  
   – Добавляете поля:
   ```yaml
   stage: basics
   data:
     reporter: ...
     title: ...
     description: ...
     severity: ...
   fields:
     photos: []
     witness_statements: []
