# scraper.py
import requests
from bs4 import BeautifulSoup
import re

class RemessaOnlineScraper:
    def __init__(self):
        self.url_dolar = "https://www.remessaonline.com.br/cotacao/dolar-comercial"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _fazer_requisicao(self):
        try:
            response = requests.get(self.url_dolar, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            raise Exception(f"Tempo limite excedido ao conectar a {self.url_dolar}.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição para {self.url_dolar}: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado na requisição: {e}")

    def buscar_cotacao_dolar(self):
        try:
            html_content = self._fazer_requisicao()
            soup = BeautifulSoup(html_content, 'html.parser')

            # --- ATENÇÃO: VERIFIQUE E AJUSTE A LINHA ABAIXO SE NECESSÁRIO ---
            # Confirme a TAG HTML correta para a classe 'style__QuotationCurrency-sc-1a6mtr6-6 lkSDNm'.
            # Ex: 'p', 'span', 'h2'. O exemplo abaixo usa 'p'.
            cotacao_element = soup.find('p', class_='style__QuotationCurrency-sc-1a6mtr6-6 lkSDNm') # <--- LINHA PARA VERIFICAR/AJUSTAR A TAG

            if cotacao_element:
                full_text = cotacao_element.get_text(strip=True)
                match = re.search(r'\d+[.,]\d+', full_text)

                if match:
                    cotacao_text = match.group(0).replace(',', '.')
                    try:
                        cotacao_dolar = float(cotacao_text)
                        return cotacao_dolar
                    except ValueError:
                        print(f"Erro no scraper: Não foi possível converter o valor numérico '{cotacao_text}' para float.")
                        return None
                else:
                    print(f"Erro no scraper: Não foi possível encontrar um padrão numérico no texto '{full_text}'.")
                    return None
            else:
                print("Erro no scraper: Não foi possível encontrar o elemento da cotação do dólar na página. "
                      "A estrutura HTML pode ter mudado ou os seletores estão incorretos.")
                return None

        except Exception as e:
            print(f"Ocorreu um erro inesperado no scraper: {e}")
            return None

if __name__ == "__main__":
    # Teste rápido do scraper
    scraper = RemessaOnlineScraper()
    dolar_hoje = scraper.buscar_cotacao_dolar()
    if dolar_hoje:
        print(f"Dólar via scraper: R$ {dolar_hoje:.2f}")
    else:
        print("Falha ao obter cotação via scraper.")