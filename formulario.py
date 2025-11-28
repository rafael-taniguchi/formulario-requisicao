import streamlit as st
import streamlit.components.v1 as components

# ===============================
# CONFIGURAÇÃO GLOBAL DO APP
# ===============================
st.markdown("""
    <style>

        /* ======== FONTES ======== */
        label, .stRadio, .stCheckbox, .stTextInput, .stSelectbox, .stTextArea {
            font-size: 12px !important;
        }
        .small-title {
            font-size: 12px !important;
            font-weight: 600;
            margin-bottom: 3px;
        }

        /* ================================
             APENAS NA IMPRESSÃO → fundo branco
           ================================ */
        @media print {
            body, html, .main, .stApp, .block-container {
                background: white !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            * {
                background-color: white !important;
                color: black !important;
            }
        }

        /* ================================
             NA TELA → mantém o tema normal
           ================================ */
        @media screen {
            .stApp, .main, .block-container {
                background: inherit !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("Formulário de Requisição")

# Inicializa quantidade de formulários
if "form_count" not in st.session_state:
    st.session_state.form_count = 1


# ===============================
# FUNÇÃO QUE RENDERIZA CADA FORMULÁRIO
# ===============================
def render_form(form_id):

    st.markdown("---")

    # --------------------------
    # LINHA 1 → Requisição / Quantidade / Tipo
    # --------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        numero_req = st.text_input("Número de Requisição", key=f"numero_req_{form_id}")

    with col2:
        quantidade = st.text_input("Quantidade", key=f"quantidade_{form_id}")

    with col3:
        tipo = st.selectbox(
            "Tipo",
            [
                "CAP", "XAROPE", "COMP", "CREME", "SACHÊS",
                "LOÇÃO", "SHAMPOO", "FILME", "FLORAL", "GEL",
                "POMADA", "BISCOITO", "ÓVULO", "GOMA", "CHOCOLATE"
            ],
            key=f"tipo_{form_id}"
        )

    # --------------------------
    # EFERVESCENTE — aparece somente se tipo = SACHÊS
    # --------------------------
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

    # --------------------------
    # Linha combinada → AROMA + ADOÇANTE
    # --------------------------
    colA1, colA2, colD1, colD2 = st.columns([1.2, 2.5, 1.2, 2.5])

    with colA1:
        st.write("<p class='small-title'>Aroma / Essência</p>", unsafe_allow_html=True)

    with colA2:
        aroma_opcao = st.radio(
            "",
            ["SIM", "NÃO"],
            horizontal=True,
            key=f"aroma_radio_{form_id}",
            index=1
        )

    with colD1:
        st.write("<p class='small-title'>Adoçante</p>", unsafe_allow_html=True)

    ado_index = 0 if aroma_opcao == "SIM" else 1

    with colD2:
        adocante_opcao = st.radio(
            "",
            ["SIM", "NÃO"],
            index=ado_index,
            horizontal=True,
            key=f"adocante_radio_{form_id}"
        )

    # CAMPO DO AROMA SE "SIM"
    if aroma_opcao == "SIM":
        aroma_texto = st.text_input("Qual Aroma/Essência?", key=f"aroma_texto_{form_id}")


# ===============================
# RENDERIZA TODOS OS FORMULÁRIOS
# ===============================
for i in range(1, st.session_state.form_count + 1):
    render_form(i)

# ===============================
# CAMPO ÚNICO — OBSERVAÇÕES FINAIS
# ===============================
st.markdown("---")

observacoes_finais = st.text_area(
    "Outras informações / Observações gerais:",
    key="observacoes_finais",
    height=50
)

# ===============================
# BOTÃO PARA ADICIONAR MAIS FORMULÁRIOS
# ===============================
if st.button("+ Adicionar nova fórmula"):
    st.session_state.form_count += 1
    st.rerun()


# ===============================
# BOTÃO IMPRIMIR (JS)
# ===============================
print_button_html = """
<div style="margin-top:16px;">
  <button id="printBtn" style="
        background-color:#4CAF50;
        color:white;
        padding:10px 20px;
        font-size:14px;
        border:none;
        border-radius:8px;
        cursor:pointer;
    ">🖨️ Imprimir</button>
</div>

<script>
const btn = document.getElementById("printBtn");
btn.addEventListener("click", function() {
  try {
    if (window.parent && window.parent !== window && typeof window.parent.print === "function") {
      window.parent.print();
    } else {
      window.print();
    }
  } catch (e) {
    window.print();
  }
});
</script>
"""

components.html(print_button_html, height=80)


