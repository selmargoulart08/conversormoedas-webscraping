# app.py
from flask import Flask, render_template, jsonify, request
from scraper import RemessaOnlineScraper # Importa a classe do scraper

app = Flask(__name__) # Inicializa a aplicação Flask

# Instancia o scraper uma única vez para ser reutilizado
scraper = RemessaOnlineScraper()

@app.route('/')
def index():
    """
    Renderiza a página HTML principal do conversor.
    """
    return render_template('index.html')

@app.route('/api/cotacao-dolar', methods=['GET'])
def get_dolar_cotacao():
    """
    Endpoint da API para buscar a cotação atual do dólar.
    Retorna a cotação em formato JSON.
    """
    try:
        dolar_cotacao = scraper.buscar_cotacao_dolar()
        if dolar_cotacao:
            # Retorna a cotação como JSON
            return jsonify({'success': True, 'cotacao_dolar': dolar_cotacao})
        else:
            # Retorna erro se o scraper falhar
            return jsonify({'success': False, 'message': 'Não foi possível obter a cotação do dólar.'}), 500
    except Exception as e:
        # Captura e retorna erros gerais do servidor
        return jsonify({'success': False, 'message': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/converter', methods=['POST'])
def converter_moeda():
    """
    Endpoint da API para realizar a conversão de moedas.
    Espera JSON com 'valor' e 'moeda_destino' (apenas para dólar por enquanto).
    """
    data = request.get_json()
    valor = data.get('valor')
    moeda_destino = data.get('moeda_destino') # Para futuras expansões, se tivermos mais moedas

    if not valor or not isinstance(valor, (int, float)):
        return jsonify({'success': False, 'message': 'Valor inválido fornecido.'}), 400

    try:
        cotacao_dolar = scraper.buscar_cotacao_dolar()
        if cotacao_dolar:
            valor_convertido = valor * cotacao_dolar # Converte do Real para o Dólar (R$X = Y USD)
            # ou valor / cotacao_dolar se for converter de USD para BRL, dependendo da sua interface
            return jsonify({
                'success': True,
                'valor_original': valor,
                'moeda_origem': 'BRL',
                'moeda_destino': 'USD',
                'cotacao': cotacao_dolar,
                'valor_convertido': round(valor_convertido, 2) # Arredonda para 2 casas decimais
            })
        else:
            return jsonify({'success': False, 'message': 'Não foi possível obter a cotação para conversão.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro na conversão: {str(e)}'}), 500

if __name__ == '__main__':
    # Para rodar o Flask em modo de desenvolvimento
    # Em produção, você usaria um servidor WSGI como Gunicorn ou uWSGI
    app.run(debug=True) # debug=True ativa o modo de depuração e auto-reload