# 🧠 Rótus — Dashboard 

**Rótus** é um dashboard interativo desenvolvido em **Django 5 + MongoDB** para análise e gerenciamento de **informações nutricionais**.  
A aplicação exibe indicadores nutricionais (energia média, top 10 receitas, etc.) e permite **CRUD completo (Create, Read, Update, Delete)** de rótulos diretamente no navegador.

---
### Status do Projeto
<!-- ![Status](https://img.shields.io/badge/status-em%20andamento-yellow)   -->
<!-- <h3 align="center">✅ Concluído ✅</h3> -->
<h3 align="center">🚧🚧 Em construção!  👷 🧱🚧</h3>


## 🚀 Tecnologias Utilizadas

| Camada | Tecnologias |
|--------|--------------|
| Backend | Django 5.x, MongoEngine (ODM), Python 3.10+ |
| Banco de Dados | MongoDB (local ou Atlas) |
| Frontend | Bootstrap 5, Chart.js, JavaScript Vanilla |
| Dados Fictícios | Faker |
| Ambiente | Docker (opcional), Virtualenv |

---

## 📂 Estrutura do Projeto

```
 
📂rotus-project/
├─ 📂 core/                 # Projeto principal Django
│  ├─ 📄 settings.py
│  ├─ 📄 urls.py
│  └─ 📄 mongo.py           # Conexão com MongoDB
├─ 📂 dashboard/            # App principal
│  ├─ 📄 models.py
│  ├─ 📄 views.py
│  ├─ 📄 urls.py
│  └─ 📄 templates/dashboard/index.html
├─ 📂 static/
│  ├─ 📄 css/style.css
│  └─ 📄 js/script.js
├─ 📂 scripts/
│  └─ 📄 populate_mongo.py  # Gera 100 registros fictícios
├─ 📄 requirements.txt
├─ 📄 manage.py
└─ 📄 README.md
```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o repositório
```bash
git clone git@github.com:Lucas-Ed/R-tus-Dashboard.git
cd R-tus-Dashboard
```

### 2️⃣ Criar ambiente virtual e instalar dependências
```bash
python -m venv .venv
source .venv/bin/activate        # (Linux/macOS)
# ou .venv\Scripts\activate      # (Windows)

pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Instalar e iniciar o MongoDB local
- **Windows/macOS/Linux:**  
  Siga as instruções oficiais: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
- Verifique se está rodando:
  ```bash
  mongosh
  ```

### 4️⃣ Configurar a conexão no Django
O arquivo `core/settings.py` já aponta para o Mongo local:
```python
MONGO_HOST = "mongodb://localhost:27017/rotus_db"
```

Se usar o **MongoDB Atlas**, substitua por sua string de conexão completa.

---

## 🧪 Gerar dados fictícios

Crie e popular 100 rótulos nutricionais com o script Faker:

```bash
python scripts/populate_mongo.py
```

Saída esperada:
```
Populando 100 registros...
Concluído.
```

---

## 🖥️ Executar o servidor Django

```bash
python manage.py runserver
```

Acesse no navegador:

👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📊 Funcionalidades do Dashboard

| Função | Descrição |
|--------|------------|
| ➕ Criar Rótulo | Adiciona novos rótulos com informações nutricionais |
| 📋 Listar Rótulos | Mostra todos os rótulos cadastrados |
| ✏️ Editar | Atualiza dados de energia, proteínas, sódio, etc. |
| ❌ Excluir | Remove registros do banco de dados |
| 📈 Indicadores | Mostra total de rótulos, média de energia e Top 10 receitas mais calóricas |

---

## 🧰 Endpoints de API

| Método | Endpoint | Descrição |
|--------|-----------|-----------|
| `GET` | `/api/rotulos/` | Lista todos os rótulos |
| `POST` | `/api/rotulos/` | Cria novo rótulo |
| `GET` | `/api/rotulos/<id>/` | Detalha um rótulo |
| `PUT` | `/api/rotulos/<id>/` | Atualiza dados de um rótulo |
| `DELETE` | `/api/rotulos/<id>/` | Exclui rótulo |
| `GET` | `/api/indicadores/` | Retorna dados de indicadores e top 10 |

---

## 📦 Requisitos (requirements.txt)

```text
asgiref==3.10.0
Django==5.2.7
dnspython==2.8.0
Faker==37.12.0
mongoengine==0.29.1
pymongo==4.15.3
sqlparse==0.5.3
tzdata==2025.2
```

---

## 🧩 Exemplo de Uso do Script Faker

```python
python scripts/populate_mongo.py
```

Depois, verifique no MongoDB:
```bash
mongosh
use rotus_db
db.rotulo_nutricional.countDocuments()
```

---

## 👨🏼‍🎓 Autores
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Lucas-Ed">
        <img src="https://avatars.githubusercontent.com/u/30055762?v=4" width="100px;" alt="Lucas"/>
        <br />
        <sub>
          <b>Lucas Eduardo</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com/lucas.eduardo007/" title="Instagram">@lucas.eduardo007</a> 
       <br />
    </td> 
    <td align="center">
      <a href="https://github.com/Marques894">
        <img src="https://avatars.githubusercontent.com/u/136036690?v=4" width="100px;" alt="Renan"/>
        <br />
        <sub>
          <b>Renan Augusto</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com/augustti_m/" title="Instagram">@augustti_m</a>
       <br />
    </td>
     <td align="center">
      <a href="https://github.com/willsf2021">
        <img src="https://avatars.githubusercontent.com/u/178531137?v=4" width="100px;" alt="Wilson"/>
        <br />
        <sub>
          <b>wilson</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com/w.pereira1307" title="instagram">@w.pereira1307</a>
       <br />
    </td>
     <td align="center">
      <a href="https://github.com/KaSantos0100">
        <img src="https://avatars.githubusercontent.com/u/179961593?v=4" width="100px;" alt="Karina"/>
        <br />
        <sub>
          <b>Karina Santos</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com/" title="instagram"></a>
       <br />
    </td>
    <td align="center">
      <a href="https://github.com/RafaelRRita ">
        <img src="https://avatars.githubusercontent.com/u/175157548?v=4" width="100px;" alt="Rafael"/>
        <br />
        <sub>
          <b>Rafael Rita</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com" title="instagram"></a>
       <br />
    </td>
    <td align="center">
      <a href="https://github.com/TiagoBertoline ">
        <img src="https://avatars.githubusercontent.com/u/183771495?v=4" width="100px;" alt="Tiago"/>
        <br />
        <sub>
          <b>Tiago Bertoline</b>
        </sub>
       </a>
       <br />
       <a href="https://www.instagram.com" title="instagram"></a>
       <br />
    </td>
  </tr>
  </table>
  <br>




## :memo: Licença

Distribuído sob a licença **MIT**.  
Sinta-se livre para usar, modificar e compartilhar o projeto.

---

### 💚 Feito com dedicação, café ☕ e Django.
