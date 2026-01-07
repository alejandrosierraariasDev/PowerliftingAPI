import requests
import os

# En una API real, llamarías a la base de datos.
# En este ejemplo gratuito, pediremos a Render que reinicie el servicio para volver al estado inicial.
RENDER_DEPLOY_HOOK = os.getenv("RENDER_DEPLOY_HOOK")

def reset():
    if RENDER_DEPLOY_HOOK:
        requests.get(RENDER_DEPLOY_HOOK)
        print("Reset solicitado a Render.")
    else:
        print("No hay URL de reset configurada.")

if __name__ == "__main__":
    reset()