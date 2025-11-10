
<h1 align="center">🧠 Rótus — Dashboard Nutricional- 2025 | DSM</h1>
<p align="center">

  ![]()
  
</p>

<p align="center">
Projeto avaliativo da disciplina Banco de dados não relacional, 3° semestre, do curso <a href="https://fatecararas.cps.sp.gov.br/tecnologia-em-desenvolvimento-de-softwares-multiplataforma/">DSM- Desenvolvimento de software multiplataforma.</a>

# 📃 Sumário:
<p align="center">
 <a href="#-status-do-projeto">Status</a> • 
 <a href="#-layout-da-página-inicial">Layout</a> • 
 <a href="#-tecnologias-utilizadas">Tecnologias</a> • 
 <a href="#-estrutura-do-projeto">Estrutura</a> • 
 <a href="#️-instalação-e-configuração">Instalação</a> • 
 <a href="#-executar-testes-com-coverage">Testes</a> • 
 <a href="#️-executar-o-servidor-para-desenvolvimento">Execução</a> • 
 <a href="#-funcionalidades">Funcionalidades</a> • 
 <a href="#-indicadores-do-dashboard">Indicadores</a> • 
 <a href="#-endpoints-da-api">API</a> • 
 <a href="#-autores">Autores</a> • 
 <a href="#memo-licença">Licença</a>
</p>

 

**Rótus** é um dashboard interativo desenvolvido em **Django 5 + MongoDB (Atlas)** para **análise e gerenciamento de receitas e ingredientes**.  
A aplicação permite **CRUD completo** de receitas, cálculo de indicadores, e exibe **insights visuais** com gráficos dinâmicos via **Chart.js**.

---


### 📊 Status do Projeto
<!-- ![Status](https://img.shields.io/badge/status-em%20andamento-yellow)   -->
<!-- <h3 align="center">✅ Concluído ✅</h3> -->
<h3 align="center">🚧🚧 Em construção!  👷 🧱🚧</h3>

---
## Layout da página inicial
![Dashboard Screenshot](/img/index.JPG)

<br>
<br>

## Layout do Dashboard

![Dashboard Screenshot](/img/dash.JPG)

---

## 🚀 Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|--------------|
| **Backend** | Django 5.x, MongoEngine (ODM), Python 3.12+ |
| **Banco de Dados** | MongoDB Atlas (ou local) |
| **Frontend** | Bootstrap 5, Chart.js, JavaScript Vanilla |
| **Outros** | Faker (para gerar dados fictícios), SweetAlert2, Fetch API |
| **Ambiente** | Virtualenv ou Docker (opcional) |

---

## 📂 Estrutura do Projeto

```
📦 R-TUS-DASHBOARD/
├─ 📂 core/
│  ├─ 📄 __init__.py
│  ├─ 📄 asgi.py
│  ├─ 📄 mongo.py
│  ├─ 📄 settings.py
│  ├─ 📄 urls.py
│  └─ 📄 wsgi.py
│
├─ 📂 dashboard/
| ├─ 📂 management/
│  ├─ 📂 commands/
|  │   └─  📄 popular_receitas.py
│  ├─ 📂 migrations/
│  ├─ 📂 models/
│  │   ├─ 📄 __init__.py
│  │   ├─ 📄 ingrediente.py
│  │   ├─ 📄 models.py
│  │   └─ 📄 Receita.py
│  ├─ 📂 templates/
│  │   ├─ 📄 index.html
│  │   ├─ 📄 dash.html
│  ├─ 📂 tests/
│  │   ├─ 📄 __init__.py
│  │   ├─ 📄 conftest.py
│  │   ├─ 📄 test_api_integrations.py
│  │   ├─ 📄 test_ingrediente_models.py
│  │   ├─ 📄 test_receita_models.py
│  │   └─ 📄 test_urls.py
│  ├─ 📄 admin.py
│  ├─ 📄 apis.py
│  ├─ 📄 api_utils.py
│  └─ 📄 views.py
│
├─ 📂 htmlcov/ # Resultado de tests
│
├─ 📂 static/
│  └─ 📂 css/
│  |   ├─ 📄 dash.css
│  |   └─ 📄 style.css
|  └─ 📂 js/
│     ├─ 📄 dash.js
│     └─ 📄 index.js
│     
│
├─ 📄 .coverage
├─ 📄 .gitignore
├─ 📄 compose-connections.json
├─ 📄 databases.txt
├─ 📄 LICENSE
├─ 📄 manage.py
├─ 📄 pytest.ini
├─ 📄 README.md
└─ 📄 requirements.txt

```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone git@github.com:Lucas-Ed/R-tus-Dashboard.git
cd R-tus-Dashboard
```

### 2️⃣ Criar e ativar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # (Linux/macOS)
# ou .venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
```

### 3️⃣ Configurar o MongoDB

O projeto suporta **MongoDB local** ou **Atlas**.  
No arquivo `core/settings.py`, edite ativando a configuração desejada.: 

```python
MONGO_HOST = "mongodb://localhost:27017/rotus_db"
```

Para o Atlas, substitua pela sua URI:

```python
MONGO_HOST = "cluster0.wmistgg.mongodb.net"
MONGO_DB = "seu_db"
MONGO_USER = 'seu_usuario'
MONGO_PASS = 'sua_senha'
```

---

## 🧪 Executar Testes com Coverage

Em settings.py, certifique-se de que o banco de dados está configurado   e ativao para SQLite em memória para os testes:

```python 
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
```
Observação: Isso é necessário para isolar os testes do MongoDB, os testes são
Efetuados no Atlas real.

Então, execute os testes com coverage:

```bash
python -m coverage run -m pytest
python -m coverage report
python -m coverage html
start htmlcov/index.html
```
 
## 🧪 Popular Banco com Dados Fictícios

```bash
python manage.py popular_receitas
```

Saída esperada:
```
  Banco populado com 100 receitas!
``` 

---

## 🖥️ Executar o Servidor para desenvolvimento

```bash
# Sobe a aplicação no servidor local para o navegador.
python manage.py runserver
```

Acesse:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📊 Funcionalidades

| Função | Descrição |
|--------|------------|
| 🍲 **CRUD de Receitas** | Criar, listar, editar e excluir receitas |
| 🧂 **Ingredientes** | Associar ingredientes a receitas com pesos e alimentos |
| 📈 **Dashboard Analítico** | Indicadores automáticos e gráficos dinâmicos |
| 💾 **Integração MongoDB Atlas** | Armazena e consulta dados de forma não relacional |
| 💬 **Interface Dinâmica** | Feita com Bootstrap + JavaScript + Fetch API |
| 🔍 **Visualização Interativa** | Gráficos com Chart.js (pizza, barras e doughnut) |

---

## 📈 Indicadores do Dashboard

O dashboard analítico exibe dados calculados em tempo real via endpoint `/dashboard/dashboard-stats/`:

| Indicador | Descrição |
|------------|------------|
| **Total de Receitas** | Contagem total de receitas cadastradas |
| **Total de Ingredientes** | Quantidade total de ingredientes no sistema |
| **Receitas por Tipo** | Distribuição por categoria (Doce, Salgada, Fit, etc.) |
| **Top 5 Ingredientes Mais Usados** | Ingredientes mais frequentes nas receitas |
| **Energia Média por Receita** | Calculada a partir dos alimentos da TACO (kcal/100g) ou indicador alternativo |

Gráficos utilizados:
- 🥧 **Pie Chart** — Receitas por Tipo  
- 🍩 **Doughnut Chart** — Ingredientes Mais Usados  
- 📊 **Bar Chart** — Energia Média ou Indicador Alternativo  

---

## 🧰 Endpoints da API

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
| `GET` | `/dashboard/receitas/` | Lista todas as receitas |
| `POST` | `/dashboard/receitas/` | Cria nova receita |
| `GET` | `/dashboard/receitas/<id>/` | Retorna detalhes da receita |
| `PUT` | `/dashboard/receitas/<id>/` | Atualiza receita existente |
| `DELETE` | `/dashboard/receitas/<id>/` | Remove uma receita |
| `POST` | `/dashboard/receitas/<id>/ingredientes/` | Adiciona ingredientes à receita |
| `GET` | `/dashboard/ingredientes/` | Lista todos os ingredientes |
| `GET` | `/dashboard/dashboard-stats/` | Retorna os indicadores do dashboard |

---

## 📊 Exemplo de Resposta do Endpoint `/dashboard/dashboard-stats/`

```json
{
  "total_receitas": 12,
  "total_ingredientes": 84,
  "receitas_por_tipo": {
    "Doce": 5,
    "Salgada": 4,
    "Vegana": 3
  },
  "top_ingredientes": {
    "Farinha": 10,
    "Açúcar": 8,
    "Ovos": 7,
    "Leite": 6,
    "Manteiga": 5
  },
  "media_energia": 254.8
}
```

---

## 👨‍💻 Autores

<table>
  <tr>
    <td align="center"><a href="https://github.com/Lucas-Ed"><img src="https://avatars.githubusercontent.com/u/30055762?v=4" width="100px;" alt="Lucas"/><br /><sub><b>Lucas Eduardo</b></sub></a><br /><a href="https://www.instagram.com/lucas.eduardo007/">@lucas.eduardo007</a></td>
    <td align="center"><a href="https://github.com/Marques894"><img src="https://avatars.githubusercontent.com/u/136036690?v=4" width="100px;" alt="Renan"/><br /><sub><b>Renan Augusto</b></sub></a><br /><a href="https://www.instagram.com/augustti_m/">@augustti_m</a></td>
    <td align="center"><a href="https://github.com/willsf2021"><img src="https://avatars.githubusercontent.com/u/178531137?v=4" width="100px;" alt="Wilson"/><br /><sub><b>Wilson Pereira</b></sub></a><br /><a href="https://www.instagram.com/w.pereira1307">@w.pereira1307</a></td>
    <td align="center"><a href="https://github.com/KaSantos0100"><img src="https://avatars.githubusercontent.com/u/179961593?v=4" width="100px;" alt="Karina"/><br /><sub><b>Karina Santos</b></sub></a></td>
    <td align="center"><a href="https://github.com/RafaelRRita"><img src="https://avatars.githubusercontent.com/u/175157548?v=4" width="100px;" alt="Rafael"/><br /><sub><b>Rafael Rita</b></sub></a></td>
    <td align="center"><a href="https://github.com/TiagoBertoline"><img src="https://avatars.githubusercontent.com/u/183771495?v=4" width="100px;" alt="Tiago"/><br /><sub><b>Tiago Bertoline</b></sub></a></td>
  </tr>
</table>

---

## :memo: Licença

Distribuído sob a licença **MIT**.  
Este projeto é de uso acadêmico e pode ser utilizado livremente para fins educacionais.
Sinta-se livre para usar, modificar e compartilhar o projeto.

---

### 💚 Feito com dedicação, café ☕ e Django.
