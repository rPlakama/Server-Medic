# AGENTS.md

Guide for AI agents working on this project.

## What is this

MedInfo — Plataforma de conteúdos médicos para estudantes e profissionais da saúde. Academic project for Uninassau Caxangá, Projeto de Banco de Dados, 1º Semestre, Grupo 1.

## Tech stack

- Python 3.13 + Django 5.x
- MariaDB 11 (via Podman container `medic_db`)
- Nix flake devshell (flake.nix)
- mysqlclient for DB driver
- python-decouple for env vars
- Custom user model: `usuario.Usuario` (AUTH_USER_MODEL)

## How to enter and run

```bash
nix develop                  # enters devshell, creates .venv, starts MariaDB
source .venv/bin/activate.fish  # or .venv/bin/activate for bash
python manage.py migrate     # first time only
python manage.py runserver    # http://127.0.0.1:8000/
```

If container stopped: `podman start medic_db`

## Project structure

```
Server_medic/
├── flake.nix                # Nix devshell (podman + MariaDB auto-start)
├── requirements.txt          # Django, mysqlclient, python-decouple
├── manage.py
└── server_medic/
    ├── settings.py           # DB config via env vars (python-decouple)
    ├── urls.py                # Root URL routing per domain app
    ├── wsgi.py / asgi.py
    ├── usuario/               # Custom user model + Progresso + Favorito
    ├── conteudo/               # Content model
    ├── especialidade/          # Medical specialties
    ├── autor/                  # Content authors
    ├── avaliacao/             # User ratings
    ├── comentario/            # User comments
    └── categoria/              # Content type + complexity level
```

Every domain app follows the same layout:

```
app_name/
├── __init__.py
├── apps.py
├── models.py       # Django ORM models
├── admin.py        # Admin site registration
├── urls.py          # URL patterns (app_name namespace)
├── views.py         # Stub views (placeholder responses)
├── tests.py
└── migrations/
    └── __init__.py
```

## Conventions

- Language for models, fields, verbose_name, and verbose_name_plural: **Portuguese (PT-BR)**
- App labels use Portuguese: `usuario`, `conteudo`, `especialidade`, `avaliacao`, `comentario`
- AUTH_USER_MODEL is `usuario.Usuario` — never use `auth.User` directly; reference via `settings.AUTH_USER_MODEL`
- FK references across apps use string format: `"autor.Autor"`, `"conteudo.Conteudo"`, etc.
- All env vars have sane defaults in settings.py (no .env file required for dev)
- DB credentials: user=medic, password=medicpass, db=server_medic, host=127.0.0.1:3306

## Models at a glance

```
Usuario (AbstractUser)
  ├── email (unique, USERNAME_FIELD)
  ├── data_nascimento
  ├── perfil: estudante | profissional
  ├── crm (blank, for professionals)
  ├── especialidade_atuacao → FK Especialidade (nullable)
  └── related: progressos, favoritos

Autor
  ├── user → 1:1 Usuario
  ├── nome_plataforma
  ├── crm
  ├── atuacao
  ├── instituicao
  └── related: conteudos

Especialidade
  ├── nome (unique)
  ├── descricao
  └── related: conteudos, profissionais

Categoria
  ├── tipo: artigo | video | caso_clinico
  └── nivel_complexidade: basico | intermediario | avancado

Conteudo
  ├── titulo, descricao, link
  ├── autor → FK Autor
  ├── especialidade → FK Especialidade
  ├── categoria → FK Categoria
  ├── data_publicacao (auto)
  └── related: avaliacoes, comentarios, progressos, favoritos

Avaliacao (N:N Usuario↔Conteudo, unique_together)
  ├── nota (PositiveSmallIntegerField)
  └── data_avaliacao (auto)

Comentario (N:N Usuario↔Conteudo)
  ├── texto
  └── data (auto)

Progresso (N:N Usuario↔Conteudo, unique_together)
  ├── concluido (bool)
  └── data_ultimo_acesso (auto_now)

Favorito (N:N Usuario↔Conteudo, unique_together)
  └── data (auto)
```

## Key gotchas

- `makemigrations` for `usuario` must run first (custom user model) before dependent apps
- Use `--no-input` flag when running makemigrations non-interactively (e.g. field renames)
- Podman requires `~/.config/containers/policy.json` and `registries.conf` on non-NixOS — the flake.nix shellHook handles this
- Fish shell users must use `.venv/bin/activate.fish` not `.venv/bin/activate`
- The .venv is created inside the project root by the flake.nix shellHook

## Before committing changes

After modifying models, always:

```bash
python manage.py makemigrations
python manage.py migrate
```

After modifying any Python files, check for syntax errors:

```bash
python -m py_compile server_medic/settings.py
```