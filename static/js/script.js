// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const cotacaoDolarSpan = document.getElementById('cotacao-dolar');
    const ultimaAtualizacaoSpan = document.getElementById('ultima-atualizacao');
    const valorInput = document.getElementById('valor');
    const moedaDestinoSelect = document.getElementById('moeda-destino');
    const btnConverter = document.getElementById('btn-converter');
    const resultadoConversaoSpan = document.getElementById('resultado-conversao');
    const mensagemErroParagrafo = document.getElementById('mensagem-erro');

    // Função para buscar e exibir a cotação do dólar
    async function buscarCotacaoDolar() {
        try {
            const response = await fetch('/api/cotacao-dolar'); // Chama o endpoint do Flask
            const data = await response.json();

            if (data.success) {
                cotacaoDolarSpan.textContent = `R$ ${data.cotacao_dolar.toFixed(2)}`;
                ultimaAtualizacaoSpan.textContent = new Date().toLocaleTimeString();
                mensagemErroParagrafo.textContent = ''; // Limpa qualquer erro anterior
            } else {
                cotacaoDolarSpan.textContent = 'Erro ao carregar';
                mensagemErroParagrafo.textContent = `Erro: ${data.message}`;
            }
        } catch (error) {
            console.error('Erro ao buscar cotação do dólar:', error);
            cotacaoDolarSpan.textContent = 'Erro de conexão';
            mensagemErroParagrafo.textContent = 'Erro ao conectar com o servidor para buscar cotação.';
        }
    }

    // Função para realizar a conversão
    async function realizarConversao() {
        const valor = parseFloat(valorInput.value);
        const moedaDestino = moedaDestinoSelect.value; // USD por enquanto

        if (isNaN(valor) || valor <= 0) {
            mensagemErroParagrafo.textContent = 'Por favor, insira um valor numérico válido e positivo.';
            resultadoConversaoSpan.textContent = '-';
            return;
        }

        mensagemErroParagrafo.textContent = ''; // Limpa erros anteriores
        resultadoConversaoSpan.textContent = 'Calculando...';

        try {
            const response = await fetch('/api/converter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ valor: valor, moeda_destino: moedaDestino })
            });
            const data = await response.json();

            if (data.success) {
                resultadoConversaoSpan.textContent = `${data.valor_convertido.toFixed(2)} ${data.moeda_destino}`;
            } else {
                resultadoConversaoSpan.textContent = 'Erro!';
                mensagemErroParagrafo.textContent = `Erro na conversão: ${data.message}`;
            }
        } catch (error) {
            console.error('Erro ao converter moeda:', error);
            resultadoConversaoSpan.textContent = 'Erro de conexão!';
            mensagemErroParagrafo.textContent = 'Erro ao conectar com o servidor para converter.';
        }
    }

    // Carregar a cotação do dólar ao carregar a página
    buscarCotacaoDolar();
    // Opcional: Atualizar a cotação a cada 5 minutos (300000 ms)
    setInterval(buscarCotacaoDolar, 300000);

    // Adicionar evento ao botão de converter
    btnConverter.addEventListener('click', realizarConversao);
});