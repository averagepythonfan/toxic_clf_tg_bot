import os

TOKEN: str = os.getenv('TOKEN')
FASTAPI_ADDRESS: str = os.getenv('FASTAPI_ADDRESS')
TOXICITY_LEVEL: float = float(os.getenv('TOXICITY_LEVEL'))