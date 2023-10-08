# NEWS TRADE
Trading based on sentiment analysis. The system fetches news for analysis, retrieves data from provided links (web pages only), extracts annotations for the news (for more focused analysis). It enables Web3 subscription signals for monetization and self-sustainability of the service (addressing liquidity concerns).

## Install
Installation and Setup: Provide detailed instructions for installing and running the frontend, agents, describe the structure, and the web3 smart contract.

## Frontend
The frontend is located in the news-trade folder. It consists of a React application connected to the database via REST and provides real-time mechanisms (from the database to the frontend). It is recommended to use Node.js version > 15.

1. Installation: 
```
yarn
```
2. Running:
```
yarn run dev
```

## Backend
1) Database
We utilize a cloud-based service for providing database fulfillment. The database management system is Postgresql. Interaction with the database is facilitated through PostgREST. It serves as the primary data repository and a cloud-based vector database.

Additional Notes:
- TimeScaleDb (for storing time series) - currently disabled.
- Vector storages are disabled (with plans for future development).

## Agents
Агенты предоставлены в папке agents и представляют собой маленькие python-программы автономно выполняемые и несущие за собой небольшую пользу.

### Functional-agents:
- agents.news - парсинг новостей и актуализация списка новостей в базе данных
- agents.prices - цены на используемые в новостях криптовалюты (а если быть точнее то все вероятные пары)
- agents.sentiment - разбор новостей на позитивную, негативную, нейтральную - актуализацю в БД (в разработке)
- agents.trade - прокси-агент по созданию сделок на криптоборже (в разработке)

## Technolics & Services
### Coding
1. Python3.9+, Multiprocessing
2. Node.js 15+, JavaScript, React
### Infra
3. Supabase
4. Docker (plan)
5. Cubernates (plan)
### Blockchain
4. Web3 Etherium
### AI
5. OpenAI ChatGPT
6. YandexGPT2.0 (preview)
7. FinGPT, FinRL
### DS
7. Cryptopanic
8. ⚙️ Langchain 🦜

Current versions as of today. If you have any questions or uncertainties, please write them in the Issues section.

Project Structure: Describe the structure of your project, including the location of main files and folders.
## Project files:
The files are located in a single subfolder, with the remaining parts grouped inside.

```bash
.
├── agents
│   ├── langchain <-- linc to repository
│   ├── news <-- news_functions
│   │   ├── ... .py
│   ├── prices
│   │   └── agent.py
│   ├── requirements.txt
│   ├── sentiment
│   │   └── agent.py
│   └── trade
│       └── agent.py
├── contracts
│   └── contract.sol
├── docs
│   ├── imgs
│   │   └── schema.svg
│   └── schema.drawio
├── news-trade
│   ├── src
│   ├── ...
└── readme.md
```

### ...
Usage Examples: Provide code samples or requests to demonstrate the functionality of your project.

Configuration: If your project requires configuration, describe the necessary steps.

Contributing to the Project: If you have a team or want other developers to contribute, describe the collaboration process and contribution guidelines.

License: Specify information about your project's license.

Contact Information: Provide contact details for reaching you or your team for questions and feedback.