# Como colocar o AgenorConect no ar (grátis)

Este guia usa o [Render](https://render.com) porque tem plano gratuito, suporta
Flask nativamente e é o mais simples para quem nunca fez deploy. Leva uns 10-15 minutos.

⚠️ **Importante sobre o banco de dados:** o Render (e a maioria dos serviços
gratuitos) apaga os arquivos do servidor de vez em quando. Isso significa que
o `agenorconect.db` (SQLite) **seria apagado periodicamente**, perdendo todos
os alunos/posts cadastrados. Por isso, o passo 2 abaixo cria um banco
PostgreSQL gratuito separado — os dados ficam seguros nele.

---

## Passo 1 — Colocar o código no GitHub

1. Crie uma conta em [github.com](https://github.com) (se ainda não tiver).
2. Crie um repositório novo (pode ser privado).
3. Suba os arquivos deste projeto para o repositório (pelo site do GitHub
   mesmo, arrastando a pasta, ou usando `git push` se souber usar).

## Passo 2 — Criar o banco de dados (PostgreSQL grátis)

1. Em [render.com](https://render.com), crie uma conta e clique em **New +** → **PostgreSQL**.
2. Dê um nome (ex: `agenorconect-db`) e clique em **Create Database**.
3. Espere ficar pronto, depois copie o valor de **Internal Database URL**
   (algo como `postgresql://usuario:senha@...`). Você vai usar no passo 4.

## Passo 3 — Criar o serviço web

1. Clique em **New +** → **Web Service**.
2. Conecte sua conta do GitHub e escolha o repositório que você criou.
3. Preencha:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
   - **Instance Type:** Free

## Passo 4 — Configurar as variáveis de ambiente

Ainda na tela de criação (ou em **Environment** depois), adicione:

| Nome | Valor |
|---|---|
| `SECRET_KEY` | uma frase longa e aleatória só sua (ex: gere uma em [randomkeygen.com](https://randomkeygen.com)) |
| `DATABASE_URL` | a Internal Database URL que você copiou no Passo 2 |
| `FLASK_ENV` | `production` |

Clique em **Create Web Service**. O Render vai instalar tudo e subir o site sozinho.

## Passo 5 — Popular o banco com os primeiros usuários

Depois que o deploy terminar, abra a aba **Shell** do seu serviço no Render e rode:

```bash
python seed.py
```

Isso cria os usuários de teste. Depois, você vai querer trocar esse script
(ou criar um painel de cadastro) para adicionar os alunos, responsáveis e
profissionais de verdade da sua escola — os dados de teste são só para
você conseguir testar o site funcionando.

## Pronto!

Seu site estará em algo como `https://agenorconect.onrender.com`.

---

### Alternativas ao Render
- **PythonAnywhere** — também tem plano grátis, é ainda mais simples para
  quem nunca usou deploy, mas o processo é um pouco diferente (não usa Procfile).
- **Railway** — parecido com o Render, também tem plano gratuito com limite de uso mensal.

### Sobre o plano gratuito do Render
O serviço "dorme" depois de 15 minutos sem uso e demora ~30 segundos para
"acordar" na próxima visita. Para uma escola pequena isso não costuma ser
problema, mas se quiser que fique sempre instantâneo, existem planos pagos
a partir de poucos dólares por mês.
