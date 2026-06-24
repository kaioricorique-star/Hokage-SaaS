# Hokage PDV (Sistema de Gestão SaaS)
Criei este projeto no intuito de aprender a limguagem python.

Este é um projeto de Ponto de Venda (PDV) que está sendo desenvolvido como uma solução SaaS (Software as a Service), focado em performance, escalabilidade e facilidade de uso para pequenos e médios negócios.

## 🚀 Tecnologias Utilizadas
- **Backend:** Python (FastAPI)
- **Frontend:** React.js
- **Banco de Dados:** SQLite (Portátil) / MongoDB (Suporte)
- **DevOps:** Docker (Opcional)

## 🏗️ Arquitetura do Sistema
Segue o modelo Client-Server (Cliente-Servidor) com Multi-tenancy (isolamento de dados por cliente/loja):

Front-end (A Interface): O que o usuário vê (React + Tailwind CSS).

Back-end (O Cérebro): A API que processa a lógica e protege os dados (Python + FastAPI).

Database (O Armazém): Onde as informações são guardadas (MongoDB ou SQLite).

## 📋 Funcionalidades
-**Gestão de Atendimento:** Funcionando para realizar venda
- **Gestão de Logística:** CRUD, Entregadores. A entrega, contém o código para criar-se o botão de Pânico caso houver imprevisto na rota da entrega.
- **Gestão de Produtos:** Cadastro, edição e controle de estoque.
- **Controle de Pedidos:** Registro de vendas em tempo real.
- **Controle de estoque**
- **Blindado Multi-tenanticy** atualmente penso em usá-lo em B2b.
- **Interface Intuitiva:** Foco na experiência do usuário para agilizar o atendimento.

## 🛠️ Como rodar o projeto localmente

### Pré-requisitos
- Node.js instalado
- Python 3.8+ instalado

### Passos
1. Clone o repositório:
   `git clone https://github.com/kaioricorique-estrela/hokage-pdv.git`

2. Instale as dependências do Backend:
   `cd backend && pip install -r requirements.txt`

3. Instale as dependências do Frontend:
   `cd ../frontend && npm install`

4. Inicie o sistema:
   `npm start`

---
*Desenvolvido por Guilherme de Oliveira Souza.*
