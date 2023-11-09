from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path='.env')
load_dotenv()

class RecordSettings(BaseSettings):
    record_host: str
    record_user: str
    record_password: str
    record_name: str


def get_settings(i=None):
    return RecordSettings()

if __name__ == '__main__':
    print(get_settings('api'))
