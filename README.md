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

Popular dados iniciais:
```bash
python manage.py seed_especialidades   # 55 especialidades médicas brasileiras
python manage.py seed_categorias       # 9 combinações tipo × nível
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

- Site: http://127.0.0.1:8000/conteudo/
- Admin: http://127.0.0.1:8000/admin/

### Endpoints

```
/login/                    --> Django Auth LoginView          --> Tela de login com link "Criar conta"
/logout/                   --> Django Auth LogoutView (POST) --> Encerra sessão, redireciona para /conteudo/

/usuario/                  --> usuario_list (login required) --> Lista todos os usuários
/usuario/criar/            --> usuario_create (público)      --> Formulário de registro: email, username, senha, data_nasc, perfil, CRM, especialidade (fuzzy search)
/usuario/<pk>/             --> usuario_detail (login req.)   --> Perfil do usuário: email, perfil, CRM, especialidade, data de entrada

/conteudo/                 --> conteudo_list (público)       --> Lista conteúdos + botão "Adicionar conteúdo" (requer login)
/conteudo/criar/           --> conteudo_create (login req.)  --> Formulário: título, descrição, corpo, link, arquivo, especialidade (fuzzy), categoria
/conteudo/<pk>/            --> conteudo_detail (público)     --> Detalhe + PDF inline via iframe + avaliar (1-5) + comentar + lista de comentários
/conteudo/<pk>/avaliar/    --> conteudo_avaliar (login req.) --> Envia ou atualiza nota do usuário (inline POST)
/conteudo/<pk>/comentar/   --> conteudo_comentar (login req.)--> Envia comentário do usuário (inline POST)
/conteudo/<pk>/arquivo/    --> conteudo_arquivo_view (públ.) --> Serve arquivo com Content-Disposition inline (PDF renderiza no navegador)

/especialidade/            --> especialidade_list (público)  --> Lista as 55 especialidades médicas
/especialidade/<pk>/       --> especialidade_detail (públ.)  --> Detalhe + lista de conteúdos da especialidade

/autor/                    --> autor_list (público)          --> Lista autores (criados automaticamente ao publicar conteúdo)
/autor/<pk>/               --> autor_detail (público)        --> Detalhe + lista de conteúdos do autor

/avaliacao/                --> avaliacao_list (login req.)   --> Lista todas as avaliações
/avaliacao/<pk>/           --> avaliacao_detail (login req.) --> Detalhe de uma avaliação

/comentario/               --> comentario_list (público)     --> Lista todos os comentários
/comentario/<pk>/          --> comentario_detail (público)   --> Detalhe de um comentário

/categoria/                --> categoria_list (público)      --> Lista as 9 categorias (tipo × nível)
/categoria/<pk>/           --> categoria_detail (público)    --> Detalhe + lista de conteúdos da categoria
```

### Matriz de acesso

| Recurso | Listar | Detalhe | Criar |
|---|---|---|---|
| Conteúdo | Público | Público | Login |
| Usuário | Login | Login | Público (registro) |
| Especialidade | Público | Público | Admin only |
| Autor | Público | Público | Automático |
| Categoria | Público | Público | Admin only |
| Avaliação | Login | Login | Login (inline) |
| Comentário | Público | Público | Login (inline) |

### Fluxo do usuário

1. Visitante acessa `/conteudo/` — vê lista de conteúdos públicos
2. Clica "Adicionar conteúdo" → redirecionado para `/login/?next=/conteudo/criar/`
3. Na tela de login, clica "Criar conta" → `/usuario/criar/`
4. Preenche registro (especialidade com barra de pesquisa fuzzy nas 55 opções)
5. Auto-login após registro → redirecionado para criar conteúdo
6. Conteúdo suporta: corpo de texto rico, link externo, upload de arquivo (PDF/vídeo)
7. PDFs são exibidos inline via `<iframe>` no detalhe do conteúdo
8. Usuários logados podem avaliar (1-5) e comentar em qualquer conteúdo
9. Logs de criação de conteúdo salvos em `logs/medinfo.log`

---

## Documentation

Plataforma digital voltada à organização e distribuição de conteúdos médicos para estudantes e profissionais da saúde.

### Condições de existência

- Cadastro de usuário: e-mail, senha, data de nascimento, perfil de acesso (estudante ou profissional); se profissional, número do CRM e especialidade de atuação.
- Usuários autenticados acessam materiais organizados por especialidade médica (cardiologia, pediatria, neurologia, etc.), por tipo de conteúdo (artigos, vídeos, casos clínicos) e por nível de complexidade (básico, intermediário, avançado).
- Cada conteúdo é produzido por um autor/colaborador (criado automaticamente a partir do usuário logado) com nome na plataforma, CRM, área de atuação e instituição.
- Conteúdos podem ter: corpo de texto rico, link externo, ou arquivo anexo (PDF, vídeo).
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
| **Conteúdo** | titulo, descricao, corpo, link, arquivo, data_publicacao | Pertence a 1 Especialidade, 1 Autor, 1 Categoria; recebe Avaliação, Comentário, Progresso, Favorito |
| **Especialidade** | nome, descricao | Contém vários Conteúdos; profissionais se vinculam a ela |
| **Autor** | nome_plataforma, crm, atuacao, instituicao | Produz vários Conteúdos; vinculado 1:1 a Usuário |
| **Avaliação** | nota, data_avaliacao | Usuário → avalia → Conteúdo (N:N, unique_together) |
| **Comentário** | texto, data | Usuário → comenta → Conteúdo (N:N) |
| **Categoria** | tipo (artigo/vídeo/caso_clínico), nivel_complexidade (básico/intermediário/avançado) | Classifica vários Conteúdos |
| **Progresso** | concluido, data_ultimo_acesso | Usuário → estuda → Conteúdo (N:N, unique_together) |
| **Favorito** | data | Usuário → favorita → Conteúdo (N:N, unique_together) |

### Pinpoint visual

```
┌────────────────────────────────────────────────────────────────────┐
│  Browser ──GET──> Django View ──ORM──> MariaDB 11                  │
│    │                    │                                          │
│    │ HTML + CSS         │ /conteudo/criar/ ──> cria Autor (1:1)    │
│    │ iframe PDF          │ /conteudo/<pk>/ ──> avalia + comenta    │
│    │ fuzzy search       │ /conteudo/<pk>/arquivo/ ──> serve inline│
│    │                    │ logs/medinfo.log ──> logging            │
│    ▼                    ▼                                          │
│  Usuário registra ──> Faz login ──> Cria conteúdo ──> Publica     │
│  Visitante vê conteúdo público (lista + detalhe + comentários)     │
└────────────────────────────────────────────────────────────────────┘
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
- **Conteúdo**: titulo, descricao, corpo, link, arquivo, data_publicacao
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
USUÁRIO ── 1:1 ── AUTOR                   (um usuário, um perfil de autor)
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
USUÁRIO (1) ── perfil ── (1) AUTOR
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
│ senha,perfil│  comenta  │ corpo,link,   │               └────────────┘
│ crm,esp_at │─────────────│ arquivo,     │
└────┬───────┘             │ data_pub      │
     │                     └──────┬────────┘
     │ 1:1                        │
     │ estuda                     │ produz (N:1)
     │ favorita                   │
     │                     ┌──────┴──────┐
     └─────────────────────│    AUTOR     │
                           │ nome_plat,  │
                           │ crm, atua,  │
                           │ instituicao │
                           └─────────────┘
```

> Dica: use retângulos para entidades, losangos para relacionamentos, elipses para atributos, e sublinhe as chaves primárias.

---

## Finished task list — O que a plataforma faz atualmente

| # | Funcionalidade | Status |
|---|---|---|
| 1 | Registro de usuário com email, username, senha, data_nasc, perfil, CRM, especialidade (fuzzy search) | [x] |
| 2 | Login / Logout via Django Auth (sessão) | [x] |
| 3 | Controle de acesso: rotas públicas vs rotas protegidas (`@login_required`) | [x] |
| 4 | CRUD de conteúdo: título, descrição, corpo de texto, link externo, upload de arquivo | [x] |
| 5 | Criação automática de perfil Autor (1:1 com Usuário) ao publicar primeiro conteúdo | [x] |
| 6 | PDF renderizado inline via `<iframe>` com `Content-Disposition: inline` + link de download | [x] |
| 7 | Barra de pesquisa fuzzy (`<datalist>`) para selecionar especialidade (55 opções) | [x] |
| 8 | Avaliação de conteúdo (nota 1-5) inline no detalhe, create/update via `unique_together` | [x] |
| 9 | Comentários em conteúdo inline no detalhe, lista pública de comentários | [x] |
| 10 | Navegação pública: especialidades, categorias, autores, conteúdos | [x] |
| 11 | Listagem de usuários e perfil detalhado (requer login) | [x] |
| 12 | Validação de formulários com erros por campo e feedback visual (CSS `.error`) | [x] |
| 13 | Logging: criação de conteúdo registrada em `logs/medinfo.log` + console | [x] |
| 14 | Seed commands: 55 especialidades médicas + 9 categorias (tipo × nível) | [x] |
| 15 | Django Admin com todas as entidades registradas para CRUD administrativo | [x] |
| 16 | Media files servidos via Django (`media/conteudos/<id>/`) em modo DEBUG | [x] |
| 17 | Migrations aplicadas: usuário customizado + todos os modelos relacionais | [x] |
| 18 | Template base com navegação responsiva, links condicionais por autenticação | [x] |
| 19 | MariaDB 11.8 rodando em container via flake.nix, driver mysqlclient | [x] |
| 20 | Progresso e Favorito modelados (N:N unique_together) — views pendentes | [ ] |

### Pendências conhecidas

- Progresso e Favorito: modelos existem e admin está registrado, mas endpoints de view (marcar como concluído, favoritar) ainda são stubs
- Edição e exclusão de conteúdo pelo próprio autor
- Recuperação de senha (password reset)
- Estilização visual completa (CSS atual é funcional mas mínimo)

---

## Technologies currently used

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.13 | Linguagem principal |
| Django | 5.x | ORM + framework web |
| MariaDB | 11.8 | Banco de dados relacional |
| Podman | latest | Container do MariaDB |
| Nix | flake.nix | Devshell reprodutível |
| mysqlclient | 2.2+ | Driver MySQL/MariaDB para Python |
| python-decouple | 3.8+ | Variáveis de ambiente (.env) |
