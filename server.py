from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações
PORT = 3000
DATA_FILE = 'data/dashboard-data.json'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_OWNER = os.getenv('GITHUB_OWNER')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_FILE_PATH = 'data/dashboard-data.json'

# Dados iniciais
initial_data = {
    'TODOS': {
        'filiais': {
            'ATM': {'cte': 2239, 'frete': 714149.61, 'peso': 335814, 'mercadoria': 11017168.51},
            'APL': {'cte': 2, 'frete': 192078.76, 'peso': 0, 'mercadoria': 0.02},
            'GYL': {'cte': 50, 'frete': 69058.99, 'peso': 58702, 'mercadoria': 2629352.55},
            'PPY': {'cte': 75, 'frete': 631939.24, 'peso': 562006, 'mercadoria': 53164824.17},
            'APS': {'cte': 176, 'frete': 254332.15, 'peso': 182763, 'mercadoria': 7657533.84},
            'BSB': {'cte': 316, 'frete': 230795.92, 'peso': 91996, 'mercadoria': 2502745.32},
            'VIX': {'cte': 1237, 'frete': 1643392.23, 'peso': 1873169, 'mercadoria': 77431147.14},
            'DCX': {'cte': 2908, 'frete': 3093363.71, 'peso': 2161723, 'mercadoria': 74805077.75},
            'SPO': {'cte': 7513, 'frete': 10179018.98, 'peso': 12041754, 'mercadoria': 303796315.95},
            'GYN': {'cte': 1861, 'frete': 4431407.94, 'peso': 14306179, 'mercadoria': 178341337.24}
        }
    },
    'JUNHO': {
        'filiais': {
            'ATM': {'cte': 1059, 'frete': 321611.15, 'peso': 151391, 'mercadoria': 4812272.45},
            'APL': {'cte': 1, 'frete': 106532.25, 'peso': 0, 'mercadoria': 0.01},
            'GYL': {'cte': 22, 'frete': 24762.89, 'peso': 19367, 'mercadoria': 915683.55},
            'PPY': {'cte': 13, 'frete': 110500.00, 'peso': 64659, 'mercadoria': 8763020.63},
            'APS': {'cte': 70, 'frete': 100200.64, 'peso': 79394, 'mercadoria': 2993657.14},
            'BSB': {'cte': 191, 'frete': 124880.87, 'peso': 51784, 'mercadoria': 1367527.57},
            'VIX': {'cte': 835, 'frete': 1035916.14, 'peso': 1078921, 'mercadoria': 39904912.81},
            'DCX': {'cte': 1403, 'frete': 1591608.42, 'peso': 1127661, 'mercadoria': 37124257.72},
            'SPO': {'cte': 3618, 'frete': 4685074.10, 'peso': 5700156, 'mercadoria': 141832354.89},
            'GYN': {'cte': 1022, 'frete': 2684764.97, 'peso': 3448035, 'mercadoria': 104188589.07}
        }
    },
    'MAIO': {
        'filiais': {
            'ATM': {'cte': 1180, 'frete': 392538.46, 'peso': 184423, 'mercadoria': 6204896.06},
            'APL': {'cte': 1, 'frete': 85546.51, 'peso': 0, 'mercadoria': 0.01},
            'GYL': {'cte': 28, 'frete': 44296.10, 'peso': 39335, 'mercadoria': 1713669.00},
            'PPY': {'cte': 62, 'frete': 521439.24, 'peso': 497347, 'mercadoria': 44401803.54},
            'APS': {'cte': 106, 'frete': 154131.51, 'peso': 103369, 'mercadoria': 4663876.70},
            'BSB': {'cte': 125, 'frete': 105915.05, 'peso': 40212, 'mercadoria': 1135217.75},
            'VIX': {'cte': 402, 'frete': 607476.09, 'peso': 794248, 'mercadoria': 37526234.33},
            'DCX': {'cte': 1505, 'frete': 1501755.29, 'peso': 1034062, 'mercadoria': 37680820.03},
            'SPO': {'cte': 3895, 'frete': 5493944.88, 'peso': 6341598, 'mercadoria': 161963961.06},
            'GYN': {'cte': 839, 'frete': 1746642.97, 'peso': 10828144, 'mercadoria': 74152748.17}
        }
    }
}

# Garantir que o diretório data existe
os.makedirs('data', exist_ok=True)

# Ler dados do arquivo local
def read_local_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
            return initial_data
    except Exception as e:
        print(f'Erro ao ler dados: {e}')
        return initial_data

# Salvar dados no arquivo local
def save_local_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f'Erro ao salvar dados: {e}')
        return False

# Sincronizar dados com GitHub
def sync_to_github(data):
    try:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Obter SHA do arquivo atual
        url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
        response = requests.get(url, headers=headers)
        sha = None
        
        if response.status_code == 200:
            file_data = response.json()
            sha = file_data['sha']
        elif response.status_code == 404:
            print('Arquivo não existe no GitHub, será criado')
        else:
            print(f'Erro ao verificar arquivo: {response.status_code}')
            return False
        
        # Converter dados para base64
        content = base64.b64encode(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')).decode('utf-8')
        
        # Preparar payload
        payload = {
            'message': 'Atualizar dados do dashboard',
            'content': content
        }
        
        if sha:
            payload['sha'] = sha
        
        # Atualizar ou criar arquivo no GitHub
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print('Dados sincronizados com GitHub!')
            return True
        else:
            print(f'Erro ao sincronizar: {response.status_code} - {response.text}')
            return False
            
    except Exception as e:
        print(f'Erro ao sincronizar com GitHub: {e}')
        return False

# Endpoint para obter dados
@app.route('/api/data', methods=['GET'])
def get_data():
    data = read_local_data()
    return jsonify(data)

# Endpoint para adicionar dados
@app.route('/api/data', methods=['POST'])
def add_data():
    try:
        data = request.json
        mes = data.get('mes')
        filial = data.get('filial')
        cte = data.get('cte', 0)
        peso = data.get('peso', 0)
        mercadoria = data.get('mercadoria', 0)
        frete = data.get('frete', 0)
        
        current_data = read_local_data()
        
        # Atualizar dados do mês selecionado
        if mes in current_data and filial in current_data[mes]['filiais']:
            current_data[mes]['filiais'][filial]['cte'] += cte
            current_data[mes]['filiais'][filial]['frete'] += frete
            current_data[mes]['filiais'][filial]['peso'] += peso
            current_data[mes]['filiais'][filial]['mercadoria'] += mercadoria
        
        # Atualizar dados de TODOS também
        if 'TODOS' in current_data and filial in current_data['TODOS']['filiais']:
            current_data['TODOS']['filiais'][filial]['cte'] += cte
            current_data['TODOS']['filiais'][filial]['frete'] += frete
            current_data['TODOS']['filiais'][filial]['peso'] += peso
            current_data['TODOS']['filiais'][filial]['mercadoria'] += mercadoria
        
        # Salvar localmente
        save_local_data(current_data)
        
        # Sincronizar com GitHub
        sync_to_github(current_data)
        
        return jsonify({'success': True, 'data': current_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Endpoint para sincronização manual
@app.route('/api/sync', methods=['POST'])
def manual_sync():
    data = read_local_data()
    success = sync_to_github(data)
    return jsonify({'success': success})

if __name__ == '__main__':
    print(f'Servidor rodando em http://localhost:{PORT}')
    print('Pressione Ctrl+C para parar')
    app.run(host='0.0.0.0', port=PORT, debug=True)
