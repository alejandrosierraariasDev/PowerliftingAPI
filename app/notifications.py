import os
import httpx
from dotenv import load_dotenv

# Esto asegura que si main.py no cargó el .env, lo haga este módulo
load_dotenv()


async def send_slack_notification(message: str):
    # Buscamos la URL justo antes de enviar
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        # Esto saldrá en tu consola de uvicorn si falla
        print("❌ DEBUG NOTIFICATIONS: No se encontró SLACK_WEBHOOK_URL")
        return

    payload = {"text": message}

    try:
        async with httpx.AsyncClient() as client:
            # Enviamos y capturamos la respuesta
            response = await client.post(webhook_url, json=payload, timeout=10.0)
            if response.status_code == 200:
                print("✅ Sent to Slack")
            else:
                print(f"⚠️ Slack error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"🔥 Slack connection failed: {str(e)}")