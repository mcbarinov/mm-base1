version := `python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])'`


default: dev

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info

pip-compile:
    rm -f requirements.txt requirements-dev.txt
    uv pip compile -o requirements.txt pyproject.toml
    uv pip compile -o requirements-dev.txt --extra=dev pyproject.toml

pip-sync:
    uv pip sync requirements-dev.txt
    uv pip install -e .

pip-upgrade: pip-compile pip-sync
    echo done

build: clean lint audit test
    python -m build

format:
    ruff check --select I --fix src app tests
    ruff format src app tests

lint: format
    ruff check src app tests
    mypy src app

audit:
    pip-audit
    bandit -r -c "pyproject.toml" src

test:
    pytest tests

publish: build cookiecutter
    twine upload dist/**
    git tag -a 'v{{version}}' -m 'v{{version}}'
    git push origin v{{version}}

cookiecutter:
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}
    cp -R demo cookiecutter/{{{{cookiecutter.project_slug}}
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.idea
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.mypy_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.pytest_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.ruff_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.venv
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/app.egg-info
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/build
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/dist
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/tmp
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.env

    cp cookiecutter/templates/.env cookiecutter/{{{{cookiecutter.project_slug}}
    cp cookiecutter/templates/README.md cookiecutter/{{{{cookiecutter.project_slug}}
    cp cookiecutter/templates/hosts.yml cookiecutter/{{{{cookiecutter.project_slug}}/ansible/hosts.yml

    mkdir cookiecutter/{{{{cookiecutter.project_slug}}/tmp
    touch cookiecutter/{{{{cookiecutter.project_slug}}/tmp/todo.txt
    touch cookiecutter/{{{{cookiecutter.project_slug}}/tmp/tmp.py


dev:
    uvicorn --reload --port 3000 --log-level warning app.main:server
