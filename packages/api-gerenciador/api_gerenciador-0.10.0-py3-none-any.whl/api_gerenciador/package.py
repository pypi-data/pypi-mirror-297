import requests
from utils import DOMAIN, APLICATIVO, PROJECT, TOKEN_SECRET, TOKEN_PUBLIC


class GerenciadorApi:

    def __init__(self) -> None:
        pass

    def __get_headers(self) -> dict:
        try:

            response = requests.get(f"https://{PROJECT}.supabase.co/rest/v1/rpc/get_last_token", headers={
                'apikey': TOKEN_PUBLIC,
                'Authorization': f'Bearer {TOKEN_SECRET}'
            })

            if response.status_code == 200 and len(response.json()) > 0:

                token = response.json()[0].get('token', None)

                if token is not None:
                    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

        except Exception as e:
            return {}

    def __response(self, url: str, method: str, data: str | None = None) -> dict:
        try:
            if data is None:
                data = {}

            if method == 'GET':
                response = requests.get(url, headers=self.__get_headers())

            elif method == 'POST':
                response = requests.post(url, headers=self.__get_headers(), data=data)

            elif method == 'PUT':
                response = requests.put(url, headers=self.__get_headers(), data=data)

            else:
                return {}

            if response.status_code == 200 or response.status_code == 201:
                return response.json()['data']
            else:
                return {}

        except requests.exceptions.RequestException as e:
            return {}
        except Exception as e:
            return {}

    def find_filas_by_application(self, ip_server: str, server_process: str) -> dict:
        __url = f'{DOMAIN}/fila/{APLICATIVO}/{ip_server}?server_process={server_process}'
        return self.__response(__url, 'GET')

    def update_fila(self, payload: str) -> dict:
        __url = f'{DOMAIN}/fila/{APLICATIVO}'
        return self.__response(__url, 'PUT', payload)

    def create_process(self, payload: str) -> dict:
        __url = f'{DOMAIN}/ativador'
        return self.__response(__url, 'POST', payload)

    def find_all_applications_by_application_name(self) -> dict:
        __url = f'{DOMAIN}/aplicativos/system/{APLICATIVO}'
        return self.__response(__url, 'GET')

    def create_session_by_user(self, payload: str) -> dict:
        __url = f'{DOMAIN}/sessoes/{APLICATIVO}'
        return self.__response(__url, 'POST', payload)

    def find_all_fila_playlist_by_application(self, application: str, server_process: str) -> dict:
        __url = f'{DOMAIN}/fila/playlist/no-processed?application={application}&server_process={server_process}'
        return self.__response(__url, 'GET')

    def update_fila_playlist(self, payload: str) -> dict:
        __url = f'{DOMAIN}/fila/playlist'
        return self.__response(__url, 'PUT', payload)
