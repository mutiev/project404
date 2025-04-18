# Makefile для Project404

# Путь к граф‑файлу
GRAPH := project404.graph.yaml
# Директория для выводов AI
CONCLUSIONS := action/conclusions

# Подхватываем .env автоматически (bash/zsh)
ifneq (,$(wildcard ./.env))
	include .env
	export OPENAI_API_KEY
endif

.PHONY: help init seed hash ai commit all deps lint fmt test coverage migrate backup-db restore-db serve watch docs clean

help:
	@echo "Использование:"
	@echo "  make init      — инициализация git"
	@echo "  make seed      — генерация тестовых точек боли"
	@echo "  make hash      — пересчитать и вставить hash в $(GRAPH)"
	@echo "  make ai        — запустить churn.py (Echo‑агент)"
	@echo "  make commit    — добавить и закоммитить изменения"
	@echo "  make all       — seed → hash → ai → commit"
	@echo "  make deps      — установить / обновить зависимости"
	@echo "  make lint      — запустить линтер по YAML и Python"
	@echo "  make fmt       — авто‑формат YAML и Python"
	@echo "  make test      — запустить юнит‑тесты"
	@echo "  make coverage  — собрать отчёт по покрытию"
	@echo "  make migrate   — пример DB‑миграции"
	@echo "  make backup-db — создать дамп БД"
	@echo "  make restore-db<file> — восстановить БД из дампа"
	@echo "  make serve     — локальный HTTP‑сервер"
	@echo "  make watch     — следить за изменениями и перезапускать ai"
	@echo "  make docs      — собрать / превью Markdown-документацию"
	@echo "  make clean     — удалить временные артефакты"

init:
	git init
	@echo "Git репозиторий инициализирован"

seed:
	@echo "Генерируем 3 тестовые точки боли…"
	python scripts/seed_nodes.py --count 3
	@echo "Seed completed"

hash:
	@echo "Пересчет hash для $(GRAPH)…"
	@bash -c '\
	NEW=$$(sha256sum $(GRAPH) | cut -d" " -f1) && \
	sed -i "s|hash: \".*\"|hash: \"$$NEW\"|" $(GRAPH) && \
	echo "Новый hash: $$NEW"'

ai:
	@echo "Запуск Echo‑агента (churn.py)…"
	python churn.py

commit:
	@echo "Коммитим изменения…"
	git add $(GRAPH) $(CONCLUSIONS)/*
	git commit -m "chore: auto-patch via Echo-agent & hash update"

all: seed hash ai commit
	@echo "Готово! Один цикл DBQA пройден."

# Дополнительные Lazy‑пилюли для Project404

deps:
	pip install -r requirements.txt

lint:
	yamllint project404.graph.yaml
	flake8 .

fmt:
	yq eval --inplace . project404.graph.yaml
	black .

test:
	pytest --maxfail=1 --disable-warnings -q

coverage:
	pytest --cov=src --cov-report=html

migrate:
	@echo "Выполняем миграции баз данных (псевдокоманда)"
	# ./manage.py migrate

backup-db:
	mkdir -p backups && pg_dump mydb > backups/db-$(date +%F).sql

restore-db:
	psql mydb < $(filter-out $@,$(MAKECMDGOALS))

serve:
	python -m http.server 8080

watch:
	while inotifywait -e modify project404.graph.yaml; do make ai; done

docs:
	mkdocs build --clean && mkdocs serve

clean:
	rm -rf __pycache__ .pytest_cache backups/*.sql action/conclusions/*.md
