# AgenorConect

Portal da Escola Estadual Agenor Couto de Magalhães — construído em
Flask (Python) + SQL, com login separado para estudantes, responsáveis e
profissionais da educação, mural de posts com permissões por perfil,
chamada escolar com propagação instantânea de faltas, boletim e
observações.

## Rodar localmente

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # depois edite a SECRET_KEY
python seed.py                    # cria o banco com usuários de teste
python run.py
```

Acesse `http://127.0.0.1:5000`. Usuários de teste ficam impressos no
terminal depois do `python seed.py`.

## Publicar de verdade (grátis)

Veja o passo a passo completo em **[DEPLOY.md](DEPLOY.md)**.

## Estrutura

```
app/
├── models.py              Tabelas do banco (Estudante, Responsavel,
│                           ProfissionalEducacao, Post, Comentario, Curtida,
│                           Falta, Nota, Observacao)
├── filtro_palavras.py      Filtro de linguagem imprópria
├── forms.py                Formulários de login com validação
├── routes/
│   ├── auth.py              Login / logout (3 perfis)
│   ├── main.py              Redireciona para o painel certo
│   ├── estudante.py          Faltas / boletim / observações (visão do aluno)
│   ├── responsavel.py        Mesmas páginas, visão do responsável
│   ├── profissional.py       Chamada, salvar notas, fazer observações
│   ├── posts.py               Mural: criar, curtir, comentar
│   ├── escola.py               Página institucional + "esqueci o RA"
│   └── api.py                   Endpoint usado pela atualização automática
├── static/css/              Todo o visual (fiel ao design do Canva)
├── static/js/site.js         Atualização automática de faltas + curtir sem reload
└── templates/                 Todas as páginas (Jinja2)
```

## Quem pode fazer o quê

| Perfil | Publicar posts | Comentar / curtir / compartilhar | Ver posts | Chamada / notas / observações |
|---|---|---|---|---|
| Estudante do grêmio | ✅ | ✅ | ✅ | — |
| Estudante comum | ❌ | ✅ | ✅ | — |
| Responsável | ❌ | ❌ (só visualiza) | ✅ | — |
| Profissional da educação | ✅ | ✅ | ✅ | ✅ |

## Sobre o visual

O CSS foi construído para reproduzir fielmente o design feito no Canva
(cores, tipografia, layout, ícones). Elementos puramente ilustrativos do
Canva (o grafite "AGENOR", a árvore, o fogo de artifício, a gravata, o
logo "AC") são aproximações em CSS/SVG. Para 100% de identidade visual
nesses itens específicos, exporte-os do Canva como PNG transparente e
troque pelos placeholders indicados nos comentários dos templates
(`_logo_ac.html`, `posts.html`, `escola_info.html`).
