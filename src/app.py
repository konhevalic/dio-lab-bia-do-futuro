import json
import pandas as pd
import streamlit as st
import requests

#   ==============CONFIGURACAO=======================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:120b-cloud"


#   ==============CARREGADR DADOS=====================
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

#   ==============MONTAR CONTEXTO=====================
contexto = f""""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMONIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSACOES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

## System Prompt

SYSTEM_PROMPT = """"
Voce é o Educador financeiro amigavel e didatico.

OBJETIVO:
Ensinar conceitos de financas pessoasi de forma simples, usando os dados do cliente como exemplos praticos.

REGRAS:
1. NUNCA recomende investimentos especificos - apenas explique como funciona
2. Use os dados fornecidos para dar exemplos personalizados
3. Linguagem simples, como se explicasse para uma crianca, fazendo analogias.
4. Se nao souber algo, admita que nao tem essa informacao, mas que pode explicar
5. Sempre pergunte se o cliente entendeu
6. Responda de forma sucinta e direta, em no maximo 3 paragrafos.
"""""

#   =============CHAMAR OLLAMA================
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    print(r.json())
    return r.json()['response']

#   ================INTERFACE================
st.title("Seu Agende Educador Financeiro")

if pergunta := st.chat_input("Sua duvida sobre financas..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))