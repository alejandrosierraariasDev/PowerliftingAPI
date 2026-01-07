import requests
import os

# In a real API, you would call the database.
# In this free example, we will ask Render to restart the service to return to the initial state.
RENDER_DEPLOY_HOOK = os.getenv("RENDER_DEPLOY_HOOK")

def reset():
    if RENDER_DEPLOY_HOOK:
        requests.get(RENDER_DEPLOY_HOOK)
        print("Reset requested to Render.")
    else:
        print("There is no reset URL configured.")

if __name__ == "__main__":
    reset()