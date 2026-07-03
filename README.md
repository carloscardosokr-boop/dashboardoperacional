# Dashboard Logístico - Servidor Local (Python)

Este projeto consiste em um dashboard logístico com servidor local Python para sincronização de dados com o GitHub.

## 📋 Pré-requisitos

- Python 3.x (já instalado no seu sistema: 3.14.6)
- Git
- Conta no GitHub
- Token de acesso pessoal do GitHub

## 🚀 Instalação

### 1. Configurar Credenciais do GitHub

1. **Criar um Token de Acesso Pessoal:**
   - Acesse: https://github.com/settings/tokens
   - Clique em "Generate new token" → "Generate new token (classic)"
   - Dê um nome ao token (ex: "Dashboard Logístico")
   - Selecione as permissões:
     - ✅ repo (full control of private repositories)
   - Clique em "Generate token"
   - **Copie o token gerado** (você não poderá ver novamente!)

2. **Configurar o arquivo .env:**
   - Renomeie o arquivo `.env.example` para `.env`
   - Abra o arquivo `.env` e preencha com suas informações:
     ```env
     GITHUB_TOKEN=seu_token_aqui
     GITHUB_OWNER=seu_usuario_github
     GITHUB_REPO=nome_do_repositorio
     ```

### 2. Instalar Dependências Python

No diretório do projeto, execute:
```bash
pip install -r requirements.txt
```

Isso instalará as dependências necessárias:
- flask (servidor web)
- flask-cors (para permitir requisições de outros domínios)
- requests (para fazer requisições HTTP)
- python-dotenv (para gerenciar variáveis de ambiente)

## ▶️ Como Usar

### Iniciar o Servidor Local

No diretório do projeto, execute:
```bash
python server.py
```

O servidor iniciará em `http://localhost:3000`

Você verá a mensagem:
```
Servidor rodando em http://localhost:3000
Pressione Ctrl+C para parar
```

### Endpoints da API

**Obter dados:**
```bash
GET http://localhost:3000/api/data
```

**Adicionar dados:**
```bash
POST http://localhost:3000/api/data
Content-Type: application/json

{
  "mes": "JUNHO",
  "filial": "ATM",
  "cte": 10,
  "peso": 5000,
  "mercadoria": 50000,
  "frete": 10000
}
```

**Sincronizar manualmente com GitHub:**
```bash
POST http://localhost:3000/api/sync
```

## 📁 Estrutura do Projeto

```
Projeto/
├── index.html              # Dashboard principal
├── server.py               # Servidor local Python
├── requirements.txt         # Dependências Python
├── .env                    # Credenciais (não commitar no Git)
├── .env.example            # Exemplo de configuração
├── data/
│   └── dashboard-data.json # Dados locais (gerado automaticamente)
└── README.md               # Este arquivo
```

## 🔧 Como Funciona

1. **Servidor Local:** Roda no seu computador na porta 3000 usando Flask
2. **Armazenamento Local:** Dados são salvos em `data/dashboard-data.json`
3. **Sincronização GitHub:** Quando você adiciona dados, o servidor:
   - Salva localmente
   - Envia para o GitHub via API
   - Atualiza o arquivo no repositório

4. **Dashboard no GitHub Pages:** O dashboard no GitHub Pages pode ler os dados do arquivo JSON atualizado

## 🌐 Integrar com o Dashboard

Para que o dashboard no GitHub Pages use os dados do servidor local, você precisará:

1. Modificar o `index.html` para carregar dados do servidor local quando disponível
2. Fallback para dados hardcoded quando o servidor não estiver rodando

## 🔒 Segurança

- **Nunca** commitar o arquivo `.env` no Git
- O arquivo `.env` já está no `.gitignore`
- Mantenha seu GitHub Token seguro
- Revogue tokens que não estão mais em uso

## 🛠️ Solução de Problemas

**Python não reconhecido:**
- Verifique se o Python está instalado corretamente
- Use `python --version` para verificar
- Em alguns sistemas, use `python3` em vez de `python`

**Erro de permissão no GitHub:**
- Verifique se o token tem as permissões corretas (repo)
- Verifique se as credenciais no `.env` estão corretas
- Gere um novo token se necessário

**Servidor não inicia:**
- Verifique se a porta 3000 não está em uso
- Verifique se todas as dependências foram instaladas
- Verifique o arquivo `.env` está configurado corretamente

**Erro ao instalar dependências:**
- Use `pip install --upgrade pip` para atualizar o pip
- Tente instalar cada dependência separadamente

## 📝 Notas

- O servidor precisa estar rodando para sincronizar dados com o GitHub
- Dados são salvos localmente mesmo sem conexão com GitHub
- O dashboard no GitHub Pages mostrará os dados do último commit
- Para atualizar o dashboard no GitHub Pages, o servidor local precisa fazer push dos dados

## 🖥️ Gerenciador de Dados por CLI

Alternativamente ao servidor web, você pode usar o gerenciador de dados por linha de comando para gerenciar os dados diretamente:

### Usar o Gerenciador de Dados

No diretório do projeto, execute:
```bash
python data_manager.py
```

### Funcionalidades do Gerenciador

1. **Listar dados:** Visualize todos os dados ou filtre por mês/filial
2. **Adicionar valor:** Adicione valores a uma filial específica em um mês
3. **Alterar valor:** Altere o valor existente de uma filial em um mês
4. **Deletar valor:** Zere o valor de uma filial em um mês
5. **Commit e Push:** Faça automaticamente `git add`, `git commit` e `git push` para o GitHub

### Exemplo de Uso

```
1. Listar dados
   - Mês: JUNHO
   - Filial: ATM

2. Adicionar valor
   - Mês: JUNHO
   - Filial: ATM
   - Tipo: frete
   - Valor: 10000

5. Fazer commit e push para o GitHub
```

### Filiais Disponíveis

- ATM - Altamira
- APL - Anápolis
- GYL - Goiânia
- PPY - Pouso Alegre
- APS - Anápolis
- BSB - Brasília
- VIX - Serra
- DCX - Rio de Janeiro
- SPO - Guarulhos
- GYN - Goiânia

### Tipos de Dados

- frete (em R$)
- peso (em kg)
- mercadoria (em R$)
- cte (quantidade)

## 🤝 Suporte

Para problemas ou dúvidas, verifique a documentação do:
- [Python](https://docs.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [GitHub API](https://docs.github.com/en/rest)
