# ✅ Checklist - GitHub Pages Setup

## Status Atual

- [x] `index.html` criado na raiz (172 KB)
- [x] `.gitignore` configurado
- [x] `_config.yml` criado
- [x] Scripts de deploy preparados

## Próximos Passos

### 1️⃣ Push para GitHub

```bash
cd d:\MapaCustoRegiaoSP

# Se for a primeira vez:
git init
git add .
git commit -m "Dashboard Operacional SP - v1"
git branch -M main
git remote add origin https://github.com/carloscardosokr-boop/dashboardoperacional.git
git push -u origin main

# Próximas vezes:
git add .
git commit -m "Atualizacao: descrição da mudança"
git push
```

### 2️⃣ Ativar GitHub Pages no Repositório

1. Abra https://github.com/carloscardosokr-boop/dashboardoperacional
2. Vá para **Settings** (engrenagem)
3. Esquerda → **Pages**
4. **Source**: selecione `main` (branch)
5. **Folder**: deixe `/ (root)` (padrão)
6. Clique **Save**

### 3️⃣ Aguardar Publicação

- Pode levar 1-2 minutos
- Página ativa em: `https://carloscardosokr-boop.github.io/dashboardoperacional/`

## 🔄 Para Atualizar o Mapa

Depois de fazer mudanças no Python e regenerar o mapa:

**Opção A - Usar Script (Recomendado)**
```bash
cd d:\MapaCustoRegiaoSP
.\deploy_github.bat
```

**Opção B - Manual**
```bash
# 1. Copiar novo mapa
Copy-Item output\cybermap_sao_paulo.html index.html

# 2. Fazer commit
git add index.html
git commit -m "Atualizar mapa"
git push
```

## ⚙️ Estrutura no GitHub Pages

```
https://carloscardosokr-boop.github.io/dashboardoperacional/
│
├── index.html ........................ ← Página principal
├── data/
│   ├── cybermap_project.json
│   ├── sp_districts.geojson
│   └── ...
├── output/
│   └── cybermap_sao_paulo.html ........ (cópia em index.html)
└── mods/
    └── ... (temas)
```

## 🐛 Se não funcionar

**Verificações rápidas:**

1. **index.html existe?**
   - Verifique em Settings > Pages se está vendo a página

2. **Erro no console (F12)?**
   - Abra DevTools (F12)
   - Vá para **Console**
   - Procure por erros de rede ou CORS

3. **Folium/dados faltando?**
   - O HTML já deve ter tudo embutido
   - Se usar dados externos, precisam estar em `data/`

4. **GitHub Pages ainda não publicou?**
   - Espere 2-5 minutos
   - Atualize o navegador (Ctrl+F5)

## 📞 Referência Rápida

| Arquivo | Propósito |
|---------|-----------|
| `index.html` | Página principal - REQUER NA RAIZ |
| `.gitignore` | Excluir arquivos desnecessários |
| `_config.yml` | Configuração GitHub Pages |
| `deploy_github.bat` | Script automatizado de push |
| `GITHUB_PAGES_SETUP.md` | Instruções detalhadas |

## 🎯 Resumo em 3 linhas

1. Todos os arquivos já estão configurados
2. Faça `git push` para enviar ao GitHub
3. Ative Pages nas Settings do repositório
