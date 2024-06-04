import os
import datetime

import dotenv

from supabase.client import AsyncClient, Client
from supabase.lib.client_options import ClientOptions

async def supa_async() -> AsyncClient:
    dotenv.load_dotenv()
    supa_client = AsyncClient(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    if not os.environ.get('PRODUCTION', False):
        supa_client.rest_url = os.environ['SUPABASE_URL']
        
        schema = os.environ.get("SUPABSE_SCHEMA", "public")
        supa_client.options = ClientOptions(schema=schema)

    return supa_client

def supa() -> Client:
    dotenv.load_dotenv()
    supa_client = Client(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    if not os.environ.get('PRODUCTION', False):
        supa_client.rest_url = os.environ['SUPABASE_URL']
        
        schema = os.environ.get("SUPABSE_SCHEMA", "public")
        supa_client.options = ClientOptions(schema=schema)

    return supa_client

def get_current_utc() -> str:
    utc_now = datetime.datetime.now(datetime.UTC)
    utc_now_str = str(utc_now).split(".")[0] # strip away miliseconds precision
    return utc_now_str