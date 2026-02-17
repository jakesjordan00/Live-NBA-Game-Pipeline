

import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent / 'Drivers' / '.env')


DATABASES = {
    'JJsNBA':{
        'server': os.getenv('ServerIP'),
        'database': os.getenv('Database'),
        'user': 'jjAdmin',
        'password': os.getenv('AdminPass')
    }
}