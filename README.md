# MedInfo — Plataforma de Conteúdos Médicos

## Como executar?

```bash
nix develop
```

Isso cria o `.venv`, instala dependências e sobe o container MariaDB (`medic_db`) automaticamente.

Ative o venv (se não estiver em bash):

Fish:
```fish
source .venv/bin/activate.fish
```

Bash:
```bash
source .venv/bin/activate
```

Migrações (primeira vez):
```bash
python manage.py migrate
```

Criar superuser:
```bash
python manage.py createsuperuser
```

Subir o servidor:
```bash
python manage.py runserver
```

Parar / reiniciar MariaDB:
```bash
podman stop medic_db
podman start medic_db
```

---

## How to use

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Endpoints:

```
/admin/              --> server_medic/settings.py           --> Painel administrativo do Django (CRUD completo de todas as entidades via interface web)

/usuario/            --> server_medic/usuario/views.py      --> Lista usuários cadastrados (GET) ou cria novo (POST)
/usuario/criar/      --> server_medic/usuario/views.py      --> Formulário de cadastro de usuário
/usuario/<int:pk>/   --> server_medic/usuario/views.py      --> Detalhe, edição ou remoção de um usuário específico

/conteudo/           --> server_medic/conteudo/views.py    --> Lista conteúdos médicos (GET) ou cria novo (POST)
/conteudo/criar/     --> server_medic/conteudo/views.py    --> Formulário de criação de conteúdo
/conteudo/<int:pk>/  --> server_medic/conteudo/views.py    --> Detalhe, edição ou remoção de um conteúdo específico

/especialidade/      --> server_medic/especialidade/views.py --> Lista especialidades (GET) ou cria nova (POST)
/especialidade/<int:pk>/ --> server_medic/especialidade/views.py --> Detalhe, edição ou remoção de uma especialidade

/autor/              --> server_medic/autor/views.py        --> Lista autores/colaboradores (GET) ou cria novo (POST)
/autor/<int:pk>/     --> server_medic/autor/views.py        --> Detalhe, edição ou remoção de um autor específico

/avaliacao/          --> server_medic/avaliacao/views.py   --> Lista avaliações de conteúdos (GET) ou cria nova (POST)
/avaliacao/<int:pk>/ --> server_medic/avaliacao/views.py   --> Detalhe, edição ou remoção de uma avaliação

/comentario/         --> server_medic/comentario/views.py  --> Lista comentários em conteúdos (GET) ou cria novo (POST)
/comentario/<int:pk/ --> server_medic/comentario/views.py  --> Detalhe, edição ou remoção de um comentário

/categoria/          --> server_medic/categoria/views.py   --> Lista categorias por tipo e nível (GET) ou cria nova (POST)
/categoria/<int:pk>/ --> server_medic/categoria/views.py   --> Detalhe, edição ou remoção de uma categoria
```

---

## Documentation

Plataforma digital voltada à organização e distribuição de conteúdos médicos para estudantes e profissionais da saúde.

### Condições de existência

- Cadastro de usuário: e-mail, senha, data de nascimento, perfil de acesso (estudante ou profissional); se profissional, número do CRM e especialidade de atuação.
- Usuários autenticados acessam materiais organizados por especialidade médica (cardiologia, pediatria, neurologia), por tipo de conteúdo (artigos, vídeos, resumos, casos clínicos) e por nível de complexidade (básico, intermediário, avançado).
- Cada conteúdo é produzido por um autor/colaborador com nome na plataforma, CRM, área de atuação e instituição.
- Conteúdos recebem avaliações e comentários dos usuários.
- A plataforma registra o progresso de estudo de cada usuário: materiais acessados, marcados como favoritos ou concluídos.

### Entidades

Usuário · Conteúdo · Especialidade · Autor · Avaliação · Comentário · Categoria · Progresso · Favorito

### Minimundo

**Minimundo** (ou universo de discurso) é a descrição da parte do mundo real que será representada no banco de dados. Sua função é delimitar o escopo do sistema, identificando quais entidades, atributos e relacionamentos são relevantes, servindo como base para a modelagem conceitual (Modelo E-R). Sem o minimundo, o modelo ficaria ambíguo ou incompleto.

### Entidades, Atributos e Relacionamentos

| Entidade | Atributos | Relacionamentos |
|----------|-----------|-----------------|
| **Usuário** | nome, e-mail, senha, data_nascimento, perfil (estudante/profissional), crm, especialidade_atuacao | Acessa Conteúdo (Progresso), avalia (Avaliação), comenta (Comentário), favorita (Favorito) |
| **Conteúdo** | titulo, descricao, link, data_publicacao | Pertence a 1 Especialidade, 1 Autor, 1 Categoria; recebe Avaliação, Comentário, Progresso, Favorito |
| **Especialidade** | nome, descricao | Contém vários Conteúdos; profissionais se vinculam a ela |
| **Autor** | nome_plataforma, crm, atuacao, instituicao | Produz vários Conteúdos |
| **Avaliação** | nota, data_avaliacao | Usuário → avalia → Conteúdo (N:N) |
| **Comentário** | texto, data | Usuário → comenta → Conteúdo (N:N) |
| **Categoria** | tipo (artigo/vídeo/caso_clínico), nivel_complexidade (básico/intermediário/avançado) | Classifica vários Conteúdos |
| **Progresso** | concluido, data_ultimo_acesso | Usuário → estuda → Conteúdo (N:N) |
| **Favorito** | data | Usuário → favorita → Conteúdo (N:N) |

### Pinpoint visual

```
Site --> Empurra conteúdo (Content) -- fetch/pull 'local-link' WebDAV
<-- Site recebe (DB) site empurra --> DB via Django ORM
--> Acesso do site (criar user // cadastro user \\ login user)
```

---

## Tasks (Atividades)

**Uninassau Caxangá · Análise e Desenvolvimento de Sistemas · 1º Semestre · 08/05/2026**

**MedInfo — Plataforma de Conteúdos Médicos · Grupo 1 · Líder: Joaquim**

| # | Atividade | Status |
|---|-----------|--------|
| 1 | O que é um Minimundo? Qual sua função no processo de modelagem de BD? | [x] Resposta na seção Documentation → Minimundo |
| 2 | Identificar e listar entidades, atributos e relacionamentos do minimundo | [x] Definido nos models Django e tabela acima |
| 3 | Escolher ferramenta para desenhar o Modelo E-R | [ ] Pendente — sugestão: draw.io ou BRModelo Web |
| 4 | Esboço inicial do Modelo E-R à mão | [ ] Pendente — guia abaixo |

### Guia para Esboço do Modelo E-R (Atividade 4)

**1. Desenhe as entidades principais como retângulos:**

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   USUÁRIO    │   │  ESPECIALIDADE│   │    AUTOR     │   │  CATEGORIA   │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   CONTEÚDO   │   │  AVALIAÇÃO   │   │  COMENTÁRIO  │
└──────────────┘   └──────────────┘   └──────────────┘
```

**2. Adicione os atributos como elipses ligados a cada entidade:**

- **Usuário**: nome, e-mail, senha, data_nascimento, perfil, crm, especialidade_atuacao
- **Conteúdo**: titulo, descricao, link, data_publicacao
- **Especialidade**: nome, descricao
- **Autor**: nome_plataforma, crm, atuacao, instituicao
- **Avaliação**: nota, data_avaliacao
- **Comentário**: texto, data
- **Categoria**: tipo, nivel_complexidade

> Atributos sublinhados = chave primária (ex: id em cada entidade, e-mail em Usuário)

**3. Desenhe os relacionamentos como losangos:**

```
USUÁRIO ────< avalia >──── CONTEÚDO        (N:N, entidade associativa: Avaliação)
USUÁRIO ────< comenta >─── CONTEÚDO        (N:N, entidade associativa: Comentário)
USUÁRIO ────< estuda >──── CONTEÚDO        (N:N, entidade associativa: Progresso)
USUÁRIO ────< favorita >─── CONTEÚDO       (N:N, entidade associativa: Favorito)
AUTOR ───────< produz >─── CONTEÚDO        (1:N — um autor, vários conteúdos)
ESPECIALIDADE< contém >─── CONTEÚDO        (1:N — uma especialidade, vários conteúdos)
CATEGORIA ───< classifica > CONTEÚDO       (1:N — uma categoria, vários conteúdos)
```

**4. Marque as cardinalidades:**

```
USUÁRIO (N) ── avalia ── (N) CONTEÚDO
USUÁRIO (N) ── comenta ── (N) CONTEÚDO
USUÁRIO (N) ── estuda ── (N) CONTEÚDO
USUÁRIO (N) ── favorita ── (N) CONTEÚDO
AUTOR (1) ── produz ── (N) CONTEÚDO
ESPECIALIDADE (1) ── contém ── (N) CONTEÚDO
CATEGORIA (1) ── classifica ── (N) CONTEÚDO
USUÁRIO (1) ── é profissional ── (1) ESPECIALIDADE  (opcional, só se perfil=profissional)
```

**5. Diagrama textual de referência para copiar à mão:**

```
                        ┌─────────────┐
                        │ ESPECIALIDADE│
                        │  nome, descr │
                        └──────┬──────┘
                               │ 1
                               │ contém
                               │ N
┌──────────┐    avalia    ┌────┴─────────┐   classifica   ┌────────────┐
│ USUÁRIO   │─────────────│   CONTEÚDO    │───────────────│ CATEGORIA  │
│ nome,email│             │ titulo,descr  │               │tipo, nível │
│ senha,perfil│  comenta  │ link, data_pub│               └────────────┘
│ crm,esp_at │─────────────│               │
└──────┬─────┘             └──────┬────────┘
       │                          │
       │ estuda                   │ produz (N:1)
       │ favorita                 │
       │                          │
       │                   ┌──────┴──────┐
       └───────────────────│    AUTOR     │
                           │ nome_plat,  │
                           │ crm, atua,  │
                           │ instituicao │
                           └─────────────┘
```

> Dica: use retângulos para entidades, losangos para relacionamentos, elipses para atributos, e sublinhe as chaves primárias.

---

## Technologies currently used

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.13 | Linguagem principal |
| Django | 5.x | ORM + framework web |
| MariaDB | 11 | Banco de dados relacional |
| Podman | latest | Container do MariaDB |
| Nix | flake.nix | Devshell reprodutível |
| mysqlclient | 2.2+ | Driver MySQL/MariaDB para Python |
| python-decouple | 3.8+ | Variáveis de ambiente (.env) |
