from taipy import Gui
import taipy.gui.builder as tgb
import requests

def get_data():
    response = requests.get("http://localhost:8000/data")

    if response.status_code == 200:
        return response.json()
    
    raise Exception("Failed to get data")


with tgb.Page() as page:
    tgb.text("# Anthro Web App", mode="md")
    tgb.text("## Introdução", mode="md")
    tgb.text("Esse é um web app para antropometria pediátrica.", mode="md")

    tgb.input("{data_nascimento}", label="Data de Nascimento")
    tgb.input("{sexo}", label="Sexo")
    tgb.input("{peso}", label="Peso (kg)")
    tgb.input("{altura}", label="Altura (cm)")
    
    


data = get_data()

if __name__ == "__main__":
    Gui(page=page).run(title="Anthro Web App", port=5000, debug=True, use_reloader=True)
