
import json
from pathlib import Path
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Simulação - Execução x Planejado", layout="wide")

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "executado_counts.csv")

st.title("Simulação - Execução x Planejado (rótulos MakeSense)")
st.caption("Protótipo acadêmico: usa os .txt rotulados como se fossem a saída da visão computacional.")

# Load classes for reference
classes = []
try:
    classes = json.loads((BASE / "classes.json").read_text(encoding="utf-8"))["classes"]
except Exception:
    pass

with st.expander("Classes detectáveis"):
    if classes:
        st.write(pd.DataFrame({"class_id": list(range(len(classes))), "class_name": classes}))
    else:
        st.info("classes.json não encontrado; nomes deduzidos como class_0, class_1, ...")

# Load planned
plan_path = BASE / "planejado.xlsx"
planejado = None
if plan_path.exists():
    try:
        planejado = pd.read_excel(plan_path)
        st.success("Planilha 'planejado.xlsx' carregada.")
    except Exception as e:
        st.warning(f"Não foi possível ler o Excel automaticamente: {e}")

# Filters
days = sorted([int(x) for x in df["day"].dropna().unique()]) if "day" in df.columns else []
col1, col2 = st.columns(2)
sel_day = col1.selectbox("Dia", [None] + days, index=0)

if sel_day is not None:
    dff = df[df["day"]==sel_day]
else:
    dff = df.copy()

# Show gallery
for _, row in dff.iterrows():
    img_path = BASE / "fotos" / Path(row["image_path"]).name
    ov_path = BASE / "overlays" / Path(row["overlay_path"]).name
    counts = json.loads(row["counts_json"])

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Imagem original")
            if img_path.exists():
                st.image(Image.open(img_path), use_column_width=True)
            else:
                st.warning(f"Imagem não encontrada: {img_path.name}")
        with c2:
            st.subheader("Detecções (simuladas)")
            if ov_path.exists():
                st.image(Image.open(ov_path), use_column_width=True)
            else:
                st.warning(f"Overlay não encontrado: {ov_path.name}")

        st.markdown("**Contagem detectada por classe**")
        if counts:
            st.table(pd.DataFrame([counts]).T.rename(columns={0:"Qtd"}))
        else:
            st.info("Sem labels para esta imagem.")

        if planejado is not None:
            dia_col = next((c for c in planejado.columns if str(c).lower() in ["dia","day"]), None)
            classe_col = next((c for c in planejado.columns if "classe" in str(c).lower()), None)
            qtd_col = next((c for c in planejado.columns if any(k in str(c).lower() for k in ["qtd","quant","quantidade"])), None)

            if dia_col and classe_col and qtd_col:
                df_plan = planejado[planejado[dia_col]==row["day"]]
                if not df_plan.empty:
                    comp_rows = []
                    for _, r2 in df_plan.iterrows():
                        cname = str(r2[classe_col]).strip()
                        prev = float(r2[qtd_col]) if pd.notna(r2[qtd_col]) else 0.0
                        det = float(counts.get(cname, 0))
                        progresso = (det/prev)*100 if prev>0 else (100.0 if det>0 else 0.0)
                        status = "🟢 OK" if det>=prev else ("🟡 Parcial" if 0<det<prev else "🔴 Não iniciado")
                        comp_rows.append({"Classe": cname, "Previsto": prev, "Detectado": det, "Progresso_%": round(progresso,1), "Status": status})
                    if comp_rows:
                        st.markdown("**Planejado x Executado**")
                        st.dataframe(pd.DataFrame(comp_rows))
                else:
                    st.info("Não encontrei linhas do dia correspondente no Excel.")
            else:
                st.info("Ajuste as colunas do Excel para conter Dia / Classe / Quantidade.")
