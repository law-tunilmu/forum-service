import os
from dotenv import load_dotenv
from supabase.client import create_client

load_dotenv()

PRODUCTION = os.environ.get('PRODUCTION', False)
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

def create_supabase_client():
    load_dotenv()
    supa_client = create_client(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    # if not os.environ.get('PRODUCTION', False):
    #     supa_client.rest_url = os.environ['SUPABASE_URL']

    return supa_client
