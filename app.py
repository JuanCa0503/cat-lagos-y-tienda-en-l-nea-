import os
from supabase import create_client, Client

# Lectura segura desde el entorno de Render
url: str = os.getenv("https://cngsfkwkaodbopikrplm.supabase.co")
key: str = os.getenv("sb_publishable_ZByXGOuhARBXw_0w_xbN3w_qld1NU2P")

if not url or not key:
    raise ValueError("Las credenciales de Supabase no están configuradas en el entorno.")

supabase: Client = create_client(url, key)

# Ejemplo de prueba de conexión
response = supabase.table("tu_tabla").select("*").limit(1).execute()
print("Conexión exitosa:", response.data)
