import socket, threading, os
import json

from datetime import datetime


class NetworkServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor ouvindo na porta {self.port}")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Conexão recebida de {addr}")

                client_handler = ClientHandler(client_socket)
                client_handler.start()

        except KeyboardInterrupt:
            print("Servidor encerrado.")
        finally:
            server_socket.close()


class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        try:
            while True:
                command = self.client_socket.recv(1024).decode()

                if not command:
                    break

                response = self.process_command(command)
                self.client_socket.send(response.encode())

        except Exception as error:
            print(f"Erro na conexão: {error}")
        finally:
            self.client_socket.close()

    def process_command(self, command):
        command = command.upper()

        if command == "HORA":
            time_now = datetime.now()
            formatted_time = time_now.strftime("%H:%M:%S")
            return f'HORA_ATUAL: {formatted_time}'

        elif command == "LISTAR":
            dir = "server/database"
            files = os.listdir(dir)
            return "LISTA_ARQUIVOS:\n\n"+"\n".join(files)
        
        elif command == "SAIR":
            print(f"ADEUS: {self.client_socket}")
            self.client_socket.close()
            return
        

        command, user_input = command.split('|')

        if command == 'CONSULTA':
            with open('server/database/battle_rap_dictionary.json', 'r') as file:
                info_battle_rap = json.load(file)

                info_battle_rap = {
                    key.upper(): value
                    for key, value in info_battle_rap.items()
                }

                if user_input in info_battle_rap:
                    return f'CONSULTA:\n\n{user_input}: {info_battle_rap[user_input]}'
                
        elif command == 'ARQUIVO':
            dir = "server/database"
            files = os.listdir(dir)

            for file in files:
                if user_input in file:
                    with open(f'{dir}/{file}', 'r') as value:
                        value = value.read()
                        return f'{file}:\n\n{value}'
                    
            return 'ARQUIVO_NAO_ENCONTRADO'
            
        return "COMANDO_DESCONHECIDO"


def main():
    server = NetworkServer('', 8080)
    server.start()



if __name__ == "__main__":
    main()
