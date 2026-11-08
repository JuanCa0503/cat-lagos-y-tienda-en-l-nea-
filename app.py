import os
from flask import Flask, render_template, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Configuración correcta de Supabase con respaldo directo
url: str = os.environ.get("SUPABASE_URL", "https://cngsfkwkaodbopikrplm.supabase.co")
key: str = os.environ.get("SUPABASE_KEY", "sb_publishable_ZByXGOuhARBXw_0w_xbN3w_qld1NU2P")

supabase: Client = create_client(url, key)

@app.route("/")
def index():
    try:
        response = supabase.table("autopartes").select("*").execute()
        autopartes = response.data
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        autopartes = []
    
    return render_template("index.html", autopartes=autopartes)

@app.route("/api/autopartes")
def api_autopartes():
    try:
        response = supabase.table("autopartes").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
