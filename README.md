# Como executar o SalaConforto localmente

Este guia explica como executar o projeto utilizando apenas o simulador, sem a necessidade de conectar o ESP32 ou qualquer sensor físico.

## 1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd SalaConforto
```

## 2. Criar o ambiente virtual

Dentro da pasta do projeto, execute:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Instalar as bibliotecas

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

## 4. Executar o backend (API)

Abra um terminal, entre na pasta do projeto e ative o ambiente virtual novamente.

Acesse a pasta do backend:

```bash
cd backend
```

Inicie a API:

```bash
python app.py
```

**Importante:** mantenha esse terminal aberto enquanto estiver utilizando o projeto.

## 5. Executar o simulador

Abra um segundo terminal, entre na pasta do projeto e ative o ambiente virtual.

Acesse a pasta do simulador:

```bash
cd dispositivo_simulador
```

Execute:

```bash
python simulador.py
```

O simulador enviará medições fictícias para a API.

## 6. Executar a dashboard

Abra um terceiro terminal, entre na pasta do projeto e ative o ambiente virtual.

Na pasta principal do projeto, execute:

```bash
streamlit run frontend/dashboard.py
```

A dashboard será aberta no navegador.

## Ordem de execução

Execute os componentes nesta ordem:

1. **Backend:** recebe e armazena as medições.
2. **Simulador:** envia medições fictícias para a API.
3. **Dashboard:** apresenta as medições recebidas.

**Atenção:** mantenha os três terminais abertos durante a execução do projeto.

Não é necessário conectar o ESP32. O simulador fará o papel do dispositivo físico.
