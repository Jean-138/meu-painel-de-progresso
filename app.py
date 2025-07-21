import streamlit as st  # Importo o Streamlit para criar a interface web interativa
import pandas as pd     # Importo o pandas para manipular dados em tabelas (DataFrames)
from datetime import date  # Importo a função date pra pegar a data atual
import os  # Importo o módulo os para verificar se um arquivo existe no computador

# Defino o nome do arquivo onde vou salvar os dados no formato CSV
progresso = "meus_estudos.csv"

# Verifico se o arquivo com os dados já existe na pasta do projeto
if os.path.exists(progresso):
    # Se existe, eu leio os dados do arquivo para dentro do DataFrame df
    df = pd.read_csv(progresso)
    # E pego as listas das colunas do DataFrame para colocar no st.session_state 
    st.session_state["lista_materias"] = df["Materia"].tolist() #.tolist() transforma a coluna em uma lista do Python.


    st.session_state["lista_minutos"] = df["Minutos"].tolist() 
    st.session_state["lista_datas"] = df["Data"].tolist()
else:
    # Se o arquivo não existe, crio listas vazias no session state para começar limpo
    st.session_state["lista_materias"] = []
    st.session_state["lista_minutos"] = []
    st.session_state["lista_datas"] = []

# título da página no app
st.title("Bem vindo!")
# mensagem de boas-vindas com markdown
st.markdown("Seja bem-vindo ao seu painel de progresso!")
# Insiro uma linha horizontal para separar 
st.markdown("---")

# Verifico novamente se as listas estão no estado da sessão,
# se não estiverem, inicializo elas para evitar erros
if "lista_materias" not in st.session_state:
    st.session_state["lista_materias"] = []

if "lista_minutos" not in st.session_state:
    st.session_state["lista_minutos"] = []

if "lista_datas" not in st.session_state:
    st.session_state["lista_datas"] = []

# Aqui peço para o usuário digitar o nome da matéria estudada
materia_estudada = st.text_input("O que você estudou hoje?")

# Aqui para o usuário informar o tempo que estudou em minutos
minutos_estudados = st.number_input("Quantos minutos você estudou", step=1) # step1 clicar nas setas o valor muda de 1 em 1 

# Crio um botão para o usuário clicar e salvar os dados que ele digitou
salvar_entrada = st.button("Salvar progresso")

# Se o usuário clicou no botão para salvar os dados
if salvar_entrada:
    # Verifico se o usuário realmente digitou a matéria e um tempo válido > 0 para nao salvar uma entrada inválida ou vazia.
    if materia_estudada != "" and minutos_estudados > 0:
        # Adiciono a matéria nova na lista de matérias na sessão
        st.session_state["lista_materias"].append(materia_estudada)
        # Adiciono os minutos estudados na lista de minutos na sessão
        st.session_state["lista_minutos"].append(minutos_estudados)
        # Adiciono a data de hoje na lista de datas na sessão
        st.session_state["lista_datas"].append(date.today())

        # um dicionário com as 3 listas atualizadas para formar o DataFrame
        lista = {
            "Materia": st.session_state["lista_materias"],
            "Minutos": st.session_state["lista_minutos"],
            "Data": st.session_state["lista_datas"]
        }
        # Crio um DataFrame com os dados atualizados
        df = pd.DataFrame(lista)

        # Salvo o DataFrame atualizado no arquivo CSV para guardar os dados permanentemente
        df.to_csv("meus_estudos.csv", index=False) # index=false esconde os números de índice (numeração das linhas
    else:
        # Se algum campo está errado ou vazio, uma mensagem de erro 
        st.write("Por favor, preencha os campos corretamente.")

# Crio o dicionário e DataFrame com os dados atuais para mostrar e manipular (mesmo que não tenha salvado agora)
lista = {
    "Materia": st.session_state["lista_materias"],
    "Minutos": st.session_state["lista_minutos"],
    "Data": st.session_state["lista_datas"]
}
df = pd.DataFrame(lista)  # Crio o DataFrame para mostrar na tela

# Se salvou com sucesso, mostra uma mensagem confirmando o que foi salvo
if salvar_entrada and materia_estudada != "" and minutos_estudados > 0:
    st.write(f"Você estudou {materia_estudada} por {minutos_estudados} minutos hoje.")

# Mostro a tabela completa com tudo que o usuário já salvou para acompanhar o progresso
st.dataframe(df)

# remover_materia
st.markdown("## Remover uma matéria")

# Verifica se há matérias para remover
if st.session_state["lista_materias"]:
    remover_materia = st.selectbox("Escolha uma matéria para remover", st.session_state["lista_materias"])
    remover_botao = st.button("Remover matéria")

    # se o botao remover for clicado
    if remover_botao:
        indice = st.session_state["lista_materias"].index(remover_materia) #índice exato da matéria que o usuário escolheu no selectbox.
        st.session_state["lista_minutos"].pop(indice) #Remove o tempo de estudo relacionado àquela matéria
        st.session_state["lista_datas"].pop(indice) #remoce a data
        st.session_state["lista_materias"].pop(indice) #remove a materia

        # Atualiza o CSV com os dados restantes
        df_atualizado = pd.DataFrame({
            "Materia": st.session_state["lista_materias"],
            "Minutos": st.session_state["lista_minutos"],
            "Data": st.session_state["lista_datas"]
        })
        df_atualizado.to_csv(progresso, index=False)

        # salva mensagem de sucesso na sessão (para aparecer após recarregar)
        st.session_state["mensagem_sucesso"] = "A matéria foi removida com sucesso"
        st.rerun()
else:
    st.info("Não há matérias para remover.")

# se a mensagem de sucesso existir, exibe e depois remove
if "mensagem_sucesso" in st.session_state:
    st.success(st.session_state["mensagem_sucesso"])
    del st.session_state["mensagem_sucesso"]

df_grouped = df.groupby("Materia")["Minutos"].sum() #Agrupar os dados por matéria e somo o total de minutos estudados em cada uma
media_minutos = df.groupby("Materia")["Minutos"].mean()    

# Crio uma versão do DataFrame em CSV para o usuário poder baixar seus dados
baixar_arquivo = df.to_csv(index=False)

# Crio o botão para download da planilha no formato CSV
st.download_button(label="Baixar planilha", data=baixar_arquivo,
                file_name="estudos.csv", mime="text/csv")

# Calculo o total de minutos estudados somando todos os valores da coluna "Minutos"
total_minutos = df["Minutos"].sum()

st.markdown("---")
# subtitulo antes de mostrar a media de minutos estudados para deixar mais organizado
st.markdown("## Média de minutos estudados por matéria")

# mostrar a media de minutos estudados na tela
# loop for para passar por cada item da media_minutos
for materia, media in media_minutos.items():
    st.write(f"Você estudou em média {round(media)} minutos em {materia}.") #round aparecer casas decimais

# Mostro na tela o total de minutos estudados até agora
st.write(f"Você estudou um total de {total_minutos} minutos até agora.")

# Crio um botão para limpar todos os dados salvos na sessão
deletar_csv = st.button("Limpar lista de matérias")

# mais uma linha horizontal para separar 
st.markdown("---")

# Se o usuário clicar no botão limpar
def limpar_tudo():
    # Limpa a lista de matérias da sessão, memória temporária do Streamlit
    st.session_state["lista_materias"].clear()
    
    # Limpa a lista de minutos de estudo
    st.session_state["lista_minutos"].clear()
    
    # Limpa a lista de datas dos estudos
    st.session_state["lista_datas"].clear()
    
    # se o arquivo CSV existe no diretório atual
    if os.path.exists("meus_estudos.csv"):
        # Remove o arquivo CSV para apagar os dados salvos
        os.remove("meus_estudos.csv")
    
    # Recarrega o app Streamlit para aplicar as alterações
    st.rerun()

# Se o botão ou a condição deletar_csv for ativada, chama a função limpar_tudo
if deletar_csv:
    limpar_tudo()

if not df_grouped.empty:
    # Identifico qual matéria tem o menor total de minutos para sugerir estudo
    sugestao_estudo = df_grouped.idxmin()
else:
    # Não tem dados, nada para sugerir
    sugestao_estudo = None

# Mostro uma mensagem destacando em vermelho a matéria que você menos estudou e sugiro estudar ela
if sugestao_estudo is not None:
    st.markdown(f'A matéria que você menos estudou foi <span style="color:red">{sugestao_estudo}</span>, vamos estudar um pouco dela hoje?',
                unsafe_allow_html=True)

# Outra linha separar
st.markdown("---")

# mostrar um gráfico de barras com o total de minutos por matéria para visualizar o progresso
st.bar_chart(df_grouped)
