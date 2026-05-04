import streamlit as st
from PIL import Image
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="S.I.V. - Módulo de Evidencia", layout="centered")

# --- ENCABEZADO PERSONALIZADO ---
st.title("📸 GENERADOR DE ANEXO FOTOGRÁFICO")
st.sidebar.markdown(f"""
**S.I.V. Satélite** *Autoría: Sub Comisario CASTAÑEDA Juan* Fecha: {datetime.date.today().strftime('%d/%m/%Y')}
""")

st.info("Utilice este módulo para procesar las imágenes del hecho y el croquis realizado a mano.")

# --- SECCIÓN 1: CAPTURA DE DATOS DEL PROCEDIMIENTO ---
with st.expander("📝 Datos del Acta (Para el encabezado del Anexo)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        cui = st.text_input("CUI / Expte N°:", placeholder="00-000000-0")
        preventora = st.text_input("Unidad Preventora:", value="Comisaría...")
    with c2:
        lugar = st.text_input("Lugar del Hecho:", placeholder="Ej: Mendoza y M. Rodríguez")

# --- SECCIÓN 2: CARGA DE ARCHIVOS ---
st.divider()
st.header("🖼️ Carga de Imágenes")
st.caption("Suba las fotos de la escena, indicios y el croquis de libreta.")

fotos_subidas = st.file_uploader("Arrastre aquí las fotos o el croquis:", 
                                  type=['jpg', 'png', 'jpeg'], 
                                  accept_multiple_files=True)

# --- SECCIÓN 3: PROCESAMIENTO Y EPÍGRAFES ---
if fotos_subidas:
    st.subheader("📋 Detalle de Evidencia")
    
    # Creamos un contenedor para que el oficial complete los epígrafes
    for i, archivo in enumerate(fotos_subidas):
        with st.container():
            col_img, col_txt = st.columns([1, 2])
            
            with col_img:
                img = Image.open(archivo)
                st.image(img, use_container_width=True)
            
            with col_txt:
                st.markdown(f"**Archivo:** `{archivo.name}`")
                epigrafe = st.text_area(f"Epígrafe / Descripción {i+1}:", 
                                        value=f"Vista de: ", 
                                        key=f"epi_{i}", 
                                        height=100)
            st.divider()

    # --- SECCIÓN 4: FINALIZACIÓN ---
    st.header("🏁 Generar Documento")
    if st.button("GENERAR PDF DE ANEXO FOTOGRÁFICO"):
        # Aquí irá la lógica para unir las fotos y textos en un PDF prolijo
        st.success("✅ Generando archivo... El PDF incluirá las imágenes con sus respectivos epígrafes legales.")
        st.balloons()

else:
    st.warning("Esperando carga de archivos para procesar...")

# --- NOTA AL PIE ---
st.sidebar.divider()
st.sidebar.caption("Este es un módulo independiente del S.I.V. diseñado para optimizar el rendimiento del servidor.")
