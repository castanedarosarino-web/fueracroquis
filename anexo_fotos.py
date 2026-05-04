import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# --- CLASE PARA EL FORMATO POLICIAL DEL PDF ---
class PDF_Policial(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'POLICÍA DE LA PROVINCIA DE SANTA FE', ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'ANEXO DE RELEVAMIENTO FOTOGRÁFICO Y PLANIMÉTRICO', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="S.I.V. - Generador de Anexos", layout="centered")
st.title("📸 Módulo de Relevamiento")

# --- ENTRADA DE DATOS ---
with st.expander("Datos del Procedimiento", expanded=True):
    cui = st.text_input("CUI / Expediente:", value="00-000000-0")
    inspeccion_texto = st.text_area("Redacción de la Inspección Ocular (Bloque 6):", 
                                    help="Pegue aquí lo redactado para que figure como marco del anexo.")

fotos = st.file_uploader("Subir Croquis y Fotos:", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

epigrafes = {}
if fotos:
    for i, foto in enumerate(fotos):
        st.image(foto, width=300)
        epigrafes[i] = st.text_input(f"Epígrafe para Foto {i+1}:", value=f"Vista de: ", key=f"epi_{i}")

# --- BOTÓN DE TRANSFORMACIÓN ---
if st.button("🚀 GENERAR PDF FINAL"):
    if not fotos:
        st.error("Debe subir al menos una imagen.")
    else:
        pdf = PDF_Policial()
        pdf.add_page()
        
        # 1. Ponemos el texto de la inspección primero
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'I. RELATO DE LA INSPECCIÓN OCULAR:', ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, inspeccion_texto)
        pdf.ln(10)
        
        # 2. Ponemos las fotos con sus epígrafes
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'II. REGISTRO VISUAL (FOTOS Y CROQUIS):', ln=True)
        
        for i, foto in enumerate(fotos):
            # Guardar foto temporalmente para meterla al PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                img = Image.open(foto)
                img = img.convert("RGB")
                img.save(tmp.name)
                
                # Si la foto es la primera, asumimos que puede ser el croquis
                pdf.image(tmp.name, x=10, w=180)
                pdf.set_font('Arial', 'I', 10)
                pdf.multi_cell(0, 10, f"Referencia {i+1}: {epigrafes[i]}", align='C')
                pdf.ln(5)
                os.unlink(tmp.name) # Borrar temporal

        # --- DESCARGA ---
        pdf_output = pdf.output(dest='S').encode('latin-1', errors='replace')
        st.download_button(label="📥 Descargar Anexo PDF", 
                           data=pdf_output, 
                           file_name=f"Anexo_{cui}.pdf", 
                           mime="application/pdf")
        st.success("¡Documento transformado con éxito!")
