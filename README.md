# Dashboard de Estações Meteorológicas

Dashboard para visualização de dados das estações meteorológicas conectadas ao AWS Timestream.

## Estrutura do Projeto

```
dashboard/
├── src/
│   ├── config/         # Configurações do projeto
│   ├── data/           # Funções de acesso aos dados
│   ├── utils/          # Funções auxiliares
│   ├── visualization/  # Componentes de visualização
│   └── main.py         # Aplicação principal
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## Requisitos

- Python 3.8+
- Credenciais AWS configuradas
- Acesso ao AWS Timestream

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para executar o dashboard:

```bash
streamlit run src/main.py
```

## Funcionalidades

- Visualização de dados de múltiplas estações
- Seleção de período de dados (1 hora até 1 mês)
- Gráficos de temperatura, umidade e pressão
- Indicadores de qualidade do ar
- Mapa com localização das estações

## Desenvolvimento

O projeto está organizado em módulos:

- `config/`: Configurações e constantes
- `data/`: Funções de acesso ao AWS Timestream
- `utils/`: Funções auxiliares
- `visualization/`: Componentes de visualização (cards, gauges, gráficos)
- `main.py`: Aplicação principal

## Autores

- Vitor
- Jerônimo

## Licença

Este projeto é parte do curso de IoT do Insper. 