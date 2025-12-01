import streamlit as st
import streamlit.components.v1 as components

# ===============================
# CONFIGURAÇÃO GLOBAL DO APP
# ===============================
st.markdown(""" 
    <style>
        /* FONTES */
        label, .stRadio, .stCheckbox, .stTextInput, .stSelectbox, .stTextArea {
            font-size: 12px !important;
        }
        .small-title {
            font-size: 12px !important;
            font-weight: 600;
            margin-bottom: 3px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Protocolo de Inclusão")

# Inicializa quantidade de formulários
if "form_count" not in st.session_state:
    st.session_state.form_count = 1

# ===============================
# FUNÇÃO PARA RENDERIZAR FORMULÁRIO
# ===============================
def render_form(form_id):
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        numero_req = st.text_input("Número de Requisição", key=f"numero_req_{form_id}")
    with col2:
        quantidade = st.text_input("Quantidade", key=f"quantidade_{form_id}")
    with col3:
        tipo = st.selectbox(
            "Tipo",
            ["CAP", "XAROPE", "COMP", "CREME", "SACHÊS", "LOÇÃO", "SHAMPOO", "FILME", "FLORAL", "GEL",
             "POMADA", "BISCOITO", "ÓVULO", "GOMA", "CHOCOLATE"],
            key=f"tipo_{form_id}"
        )

    # Se CAP, mostrar tipo de cápsula
    if tipo == "CAP":
        capsula_opcao = st.selectbox(
            "Tipo de Cápsula:",
            ["Gelatinosa", "Vegetal", "Enterica", "Sprinkle", "Vet", "Oleosa", "Tapioca", "Clorofila", "Duo", "Outra"],
            key=f"capsula_radio_{form_id}"
        )

    # Se SACHÊS, exibir efervescente
    if tipo == "SACHÊS":
        colEf1, colEf2, colEf3, colEf4 = st.columns([1.2, 2, 2, 3])
        with colEf1:
            st.write("<p class='small-title'>Efervescente</p>", unsafe_allow_html=True)
        with colEf2:
            ef1 = st.checkbox("EFERVESCENTE", key=f"ef1_{form_id}")
        with colEf3:
            ef2 = st.checkbox("NÃO EFERVESCENTE", key=f"ef2_{form_id}")
        with colEf4:
            ef3 = st.checkbox("BASE FRESH DRINK", key=f"ef3_{form_id}")

    # Aroma / Essência e Adoçante
    colA1, colA2, colD1, colD2 = st.columns([1.2, 2.5, 1.2, 2.5])
    with colA1:
        st.write("<p class='small-title'>Aroma / Essência</p>", unsafe_allow_html=True)
    with colA2:
        aroma_opcao = st.radio("", ["SIM", "NÃO"], horizontal=True, key=f"aroma_radio_{form_id}", index=1)

    tipos_sem_adocante = ["ÓVULO", "CREME", "LOÇÃO", "SHAMPOO", "FLORAL", "GEL", "POMADA"]
    if tipo not in tipos_sem_adocante:
        with colD1:
            st.write("<p class='small-title'>Adoçante</p>", unsafe_allow_html=True)
        ado_index = 0 if aroma_opcao == "SIM" else 1
        with colD2:
            adocante_opcao = st.radio("", ["SIM", "NÃO"], index=ado_index, horizontal=True, key=f"adocante_radio_{form_id}")
    else:
        adocante_opcao = "N/A"

    if aroma_opcao == "SIM":
        aroma_texto = st.text_input("Qual Aroma/Essência?", key=f"aroma_texto_{form_id}")

# ===============================
# RENDERIZA TODOS OS FORMULÁRIOS
# ===============================
for i in range(1, st.session_state.form_count + 1):
    render_form(i)

# ===============================
# OBSERVAÇÕES FINAIS
# ===============================
st.markdown("---")
observacoes_finais = st.text_area("Outras informações / Observações gerais:", key="observacoes_finais", height=50)

# ===============================
# BOTÃO PARA ADICIONAR MAIS FORMULÁRIOS
# ===============================
if st.button("+ Adicionar nova fórmula"):
    st.session_state.form_count += 1
    st.rerun()

# ===============================
# GERAÇÃO DO RESUMO COM BORDAS FORTES E CORES ALTERNADAS
# ===============================
form_summary = ""
for i in range(1, st.session_state.form_count + 1):
    numero_req = st.session_state.get(f"numero_req_{i}", "")
    quantidade = st.session_state.get(f"quantidade_{i}", "")
    tipo = st.session_state.get(f"tipo_{i}", "")

    ef1 = st.session_state.get(f"ef1_{i}", False)
    ef2 = st.session_state.get(f"ef2_{i}", False)
    ef3 = st.session_state.get(f"ef3_{i}", False)

    aroma_opcao = st.session_state.get(f"aroma_radio_{i}", "NÃO")
    aroma_texto = st.session_state.get(f"aroma_texto_{i}", "") if aroma_opcao == "SIM" else ""
    adocante_opcao = st.session_state.get(f"adocante_radio_{i}", "N/A")

    capsula_opcao = st.session_state.get(f"capsula_radio_{i}", "") if tipo == "CAP" else ""

    bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"

    line = f"""
    <div style="
        display:flex; gap:15px; flex-wrap: wrap; 
        margin-bottom:15px; padding:10px; border:3px solid #000; border-radius:6px;
        background-color:{bg_color};
    ">
        <div><strong>Form {i}</strong></div>
        {'<div><strong>Número Req:</strong> ' + numero_req + '</div>' if numero_req else ''}
        {'<div><strong>Quantidade:</strong> ' + quantidade + '</div>' if quantidade else ''}
        {'<div><strong>Tipo:</strong> ' + tipo + '</div>' if tipo else ''}
    """

    if tipo == "CAP" and capsula_opcao:
        line += f"<div><strong>Tipo de Cápsula:</strong> {capsula_opcao}</div>"

    if tipo == "SACHÊS":
        if ef1:
            line += "<div><strong>Efervescente:</strong> Sim</div>"
        if ef2:
            line += "<div><strong>Não Efervescente:</strong> Sim</div>"
        if ef3:
            line += "<div><strong>Base Fresh Drink:</strong> Sim</div>"

    if aroma_opcao == "SIM" and aroma_texto:
        line += f"<div><strong>Aroma/Essência:</strong> {aroma_texto}</div>"

    if adocante_opcao != "N/A":
        line += f"<div><strong>Adoçante:</strong> {adocante_opcao}</div>"

    line += "</div>"
    form_summary += line

if observacoes_finais:
    form_summary += f'<div style="margin-top:15px; padding:10px; border:3px solid #000; border-radius:6px; background-color:#e8f0fe;"><strong>Observações Finais:</strong> {observacoes_finais}</div>'

# ===============================
# BOTÃO DE IMPRESSÃO
# ===============================
print_html = f"""
<div id="printContent" style="font-family: Arial, sans-serif;">
{form_summary}
</div>

<div style="margin-top:16px;">
  <button id="printBtn" style="
        background-color:#4CAF50;
        color:white;
        padding:10px 20px;
        font-size:14px;
        border:none;
        border-radius:8px;
        cursor:pointer;
    ">🖨️ Imprimir Resumo</button>
</div>

<script>
const btn = document.getElementById("printBtn");
btn.addEventListener("click", function() {{
  const printContent = document.getElementById("printContent").innerHTML;
  const newWindow = window.open("", "_blank", "width=1000,height=600");
  newWindow.document.write("<html><head><title>Imprimir</title><style>body {{ font-family: Arial, sans-serif; font-size:14px; line-height:1.6; }}</style></head><body>");
  newWindow.document.write(printContent);
  newWindow.document.write("</body></html>");
  newWindow.document.close();
  newWindow.print();
}});
</script>
"""

components.html(print_html, height=450)


