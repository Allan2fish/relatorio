import streamlit as st
from PIL import Image

class RelatorioFinanceiro:
    def __init__(self):
        self.entradas_semana = {
            "Segunda": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Terça": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Quarta": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Quinta": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Sexta": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Sábado": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Secretaria": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0}
        }

        self.entradas_domingo = {
            "Domingo Manhã": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Domingo Tarde": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0},
            "Domingo Noite": {"dizimo": 0.0, "coleta": 0.0, "cpm": 0.0, "fundo": 0.0, "construcao": 0.0}
        }

    def inserir_valores(self, dia, dizimo, coleta, cpm, fundo, construcao):
        if dia in self.entradas_semana:
            self.entradas_semana[dia] = {
                "dizimo": dizimo,
                "coleta": coleta,
                "cpm": cpm,
                "fundo": fundo,
                "construcao": construcao,
            }
        elif dia in self.entradas_domingo:
            self.entradas_domingo[dia] = {
                "dizimo": dizimo,
                "coleta": coleta,
                "cpm": cpm,
                "fundo": fundo,
                "construcao": construcao,
            }

    def calcular_totais(self, dias):
        total_dizimo = sum(dias[dia]["dizimo"] for dia in dias)
        total_coleta = sum(dias[dia]["coleta"] for dia in dias)
        total_cpm = sum(dias[dia]["cpm"] for dia in dias)
        total_fundo = sum(dias[dia]["fundo"] for dia in dias)
        total_construcao = sum(dias[dia]["construcao"] for dia in dias)
        return total_dizimo, total_coleta, total_cpm, total_fundo, total_construcao

    def gerar_relatorio(self, dias):
        total_dizimo, total_coleta, total_cpm, total_fundo, total_construcao = self.calcular_totais(dias)

        dizimo_porcentagens = self.calcular_porcentagens(total_dizimo, 75, 25)
        coleta_porcentagens = self.calcular_porcentagens(total_coleta, 80, 20)

        return {
            "totais": {
                "total_dizimo": total_dizimo,
                "total_coleta": total_coleta,
                "total_cpm": total_cpm,
                "total_fundo": total_fundo,
                "total_construcao": total_construcao,
            },
            "distribuicao_dizimo": dizimo_porcentagens,
            "distribuicao_coleta": coleta_porcentagens
        }

    def calcular_porcentagens(self, total, porcentagem_fundo, porcentagem_matriz):
        fundo = total * porcentagem_fundo / 100
        matriz = total * porcentagem_matriz / 100
        return {"fundo": fundo, "matriz": matriz}


def main():
    st.title("Relatório Financeiro")

    # Exibe a imagem do brasão
    brasao = Image.open("brasao.jpeg")
    st.image(brasao, caption='Paróquia N.S. Aparecida', use_column_width=True)

    # Inicializa a classe do relatório
    relatorio = RelatorioFinanceiro()

    # Seleção entre semana e domingo
    escolha = st.radio("Escolha o período:", ("Semana", "Domingo"))

    if escolha == "Semana":
        dias = relatorio.entradas_semana
    else:
        dias = relatorio.entradas_domingo

    # Criar uma tabela para as entradas de dados
    st.subheader("Preencha os valores:")
    st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
    
    # Header da Tabela
    header_cols = st.columns([1.5, 1, 1, 1, 1, 1])  # Criação das colunas
    header_cols[0].markdown("**Data/Dia**")
    header_cols[1].markdown("**Dízimo**")
    header_cols[2].markdown("**Coleta**")
    header_cols[3].markdown("**CPM**")
    header_cols[4].markdown("**Fundo**")
    header_cols[5].markdown("**Construção**")

    # Gerar as linhas da tabela para cada dia
    for dia in dias.keys():
        cols = st.columns([1.5, 1, 1, 1, 1, 1])  # Criação de uma nova linha para cada dia
        cols[0].markdown(f"**{dia}**")
        dizimo = cols[1].number_input("", value=0.0, step=0.01, key=f'dizimo_{dia}')
        coleta = cols[2].number_input("", value=0.0, step=0.01, key=f'coleta_{dia}')
        cpm = cols[3].number_input("", value=0.0, step=0.01, key=f'cpm_{dia}')
        fundo = cols[4].number_input("", value=0.0, step=0.01, key=f'fundo_{dia}')
        construcao = cols[5].number_input("", value=0.0, step=0.01, key=f'construcao_{dia}')
        relatorio.inserir_valores(dia, dizimo, coleta, cpm, fundo, construcao)

    # Gerar relatório
    if st.button("Gerar Relatório"):
        relatorio_final = relatorio.gerar_relatorio(dias)
        st.subheader("Totais:")
        st.write(f"Total Dízimo: {relatorio_final['totais']['total_dizimo']}")
        st.write(f"Total Coleta: {relatorio_final['totais']['total_coleta']}")
        st.write(f"Total CPM: {relatorio_final['totais']['total_cpm']}")
        st.write(f"Total Fundo: {relatorio_final['totais']['total_fundo']}")
        st.write(f"Total Construção: {relatorio_final['totais']['total_construcao']}")

        st.subheader("Distribuição do Dízimo:")
        st.write(f"Fundo: {relatorio_final['distribuicao_dizimo']['fundo']}")
        st.write(f"Matriz: {relatorio_final['distribuicao_dizimo']['matriz']}")

        st.subheader("Distribuição da Coleta:")
        st.write(f"Fundo: {relatorio_final['distribuicao_coleta']['fundo']}")
        st.write(f"Matriz: {relatorio_final['distribuicao_coleta']['matriz']}")

if __name__ == "__main__":
    main()
