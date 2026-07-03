# Guia de Deploy no GitHub Pages

## 📋 Estrutura Atual
- `index.html` - Página principal do mapa (raiz do repositório)
- `data/` - Dados em GeoJSON e JSON
- `output/` - Saída HTML alternativa
- `mods/` - Temas CSS

## 🚀 Para Publicar no GitHub Pages

### Passo 1: Certificar que o repositório está no GitHub
```bash
# Se ainda não tiver git inicializado
git init
git add .
git commit -m "Initial commit: Dashboard Operacional SP"
git branch -M main
git remote add origin https://github.com/carloscardosokr-boop/dashboardoperacional.git
git push -u origin main
```

### Passo 2: Ativar GitHub Pages no repositório
1. Vá para **Settings** do repositório
2. Encontre a seção **Pages** (sidebar esquerda)
3. Em "Source", selecione **main branch**
4. A página será publicada em: `https://carloscardosokr-boop.github.io/dashboardoperacional/`

### Passo 3: Esperar alguns minutos para publicação
GitHub Pages leva alguns minutos para processar.

## 📝 Notas Importantes

- O arquivo `index.html` é a raiz do site
- Todos os dados referenciados devem estar no repositório
- CDN externas (Leaflet, Bootstrap, FontAwesome) funcionam normalmente
- Para atualizar o mapa, regenere `output/cybermap_sao_paulo.html` e copie para `index.html`

## 🔄 Atualizar o Mapa após Mudanças

Após fazer alterações e regenerar o mapa no Python:

```bash
# 1. Copiar novo mapa
Copy-Item output/cybermap_sao_paulo.html index.html

# 2. Commit das mudanças
git add .
git commit -m "Update: Mapa atualizado com novas regiões"
git push
```

## ✅ Verificar se está online
- Acesse: https://carloscardosokr-boop.github.io/dashboardoperacional/
- Se ver uma página em branco ou erro, verifique:
  - Se o `index.html` existe na raiz
  - Se GitHub Pages está ativado nas Settings
  - Verifique o console do navegador (F12) para erros
