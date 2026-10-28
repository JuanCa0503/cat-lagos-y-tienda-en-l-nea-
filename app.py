import os
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = "https://cngsfkwkaodbopikrplm.supabase.co"
SUPABASE_KEY ="sb_publishable_ZByXGOuhARBXw_0w_xbN3w_qld1NU2P"

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de la página web
st.set_page_config(page_title="Taller Mecánico - Autopartes", layout="wide")

st.title("🚗 Sistema de Gestión - Taller Mecánico y Autopartes")
st.markdown("Administra, busca y controla el inventario de tu taller en tiempo real.")

# Menú lateral
menu = st.sidebar.selectbox("Menú de Navegación", ["Registrar Autoparte", "Ver y Buscar Catálogo"])

if menu == "Registrar Autoparte":
    st.subheader("📝 Registrar Nueva Autoparte")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sku = st.text_input("Código SKU")
        nombre = st.text_input("Nombre de la Pieza")
        categoria = st.text_input("Categoría (Ej. Motor, Suspensión, Frenos)")
        ubicacion = st.text_input("Ubicación en Estante (Ej. Estante A-3)")
        
    with col2:
        precio = st.number_input("Precio ($)", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock Inicial", min_value=0, step=1)
        descripcion = st.text_area("Descripción de la pieza", height=106)
    
    if st.button("Guardar en Supabase", type="primary"):
        if sku and nombre:
            try:
                datos = {
                    "codigo_sku": sku,
                    "nombre": nombre,
                    "categoria": categoria,
                    "descripcion": descripcion,
                    "precio": float(precio),
                    "stock": int(stock),
                    "ubicacion_estante": ubicacion
                }
                supabase.table("autopartes").insert(datos).execute()
                st.success(f"¡Pieza '{nombre}' registrada con éxito en Supabase!")
            except Exception as e:
                st.error(f"Error al registrar la autoparte: {e}")
        else:
            st.warning("Por favor, completa al menos el Código SKU y el Nombre de la pieza.")

elif menu == "Ver y Buscar Catálogo":
    st.subheader("📦 Catálogo Actual de Inventario")
    
    # Barra de búsqueda
    busqueda = st.text_input("🔍 Buscar pieza por nombre o SKU:")
    
    if st.button("🔄 Actualizar Datos"):
        st.rerun()
        
    try:
        respuesta = supabase.table("autopartes").select("*").execute()
        catalogo = respuesta.data
        
        if catalogo:
            # Filtrar si el usuario escribió algo en la búsqueda
            if busqueda:
                catalogo = [
                    item for item in catalogo 
                    if busqueda.lower() in item.get("nombre", "").lower() 
                    or busqueda.lower() in item.get("codigo_sku", "").lower()
                ]
            
            if catalogo:
                st.dataframe(catalogo, use_container_width=True)
                
                # Sección para eliminar pieza por ID
                st.markdown("---")
                st.subheader("🗑️ Eliminar Pieza del Inventario")
                id_a_borrar = st.number_input("Ingresa el ID de la pieza que deseas eliminar:", min_value=1, step=1)
                
                if st.button("Eliminar Pieza", type="secondary"):
                    try:
                        supabase.table("autopartes").delete().eq("id", id_a_borrar).execute()
                        st.success(f"Pieza con ID {id_a_borrar} eliminada correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo eliminar la pieza: {e}")
            else:
                st.info("No se encontraron piezas que coincidan con la búsqueda.")
        else:
            st.info("No hay autopartes registradas en este momento.")
            
    except Exception as e:
        st.error(f"Error al consultar el catálogo: {e}")
