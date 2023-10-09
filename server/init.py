import socket
import threading
import os
import json
from datetime import datetime


SERVER_HOST = ""
SERVER_PORT = 8080
DATABASE_DIR = "server/database"
BDA_BIRTHDAYS_DIR = f"{DATABASE_DIR}/BDA_birthdays"


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on port {self.port}")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection received from {addr}")

                client_handler = ClientHandlerThread(client_socket)
                client_handler.start()

        except KeyboardInterrupt:
            print("Server terminated.")
        finally:
            server_socket.close()


class ClientHandlerThread(threading.Thread):
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
            print(f"Connection error: {error}")
        finally:
            self.client_socket.close()

    def process_command(self, command):
        command = command.upper()

        if command == "HORA":
            time_now = datetime.now()
            formatted_time = time_now.strftime("%H:%M:%S")
            return f"HORA_ATUAL: {formatted_time}"

        elif command == "LISTAR":
            files = os.listdir(BDA_BIRTHDAYS_DIR)
            return "LISTA_ARQUIVOS:\n\n" + "\n".join(files)

        elif command == "SAIR":
            print(f"Goodbye: {self.client_socket}")
            self.client_socket.close()
            return

        command, user_input = command.split("|")

        if command == "CONSULTA":
            with open(
                os.path.join(DATABASE_DIR, "battle_rap_dictionary.json"), "r"
            ) as file:
                info_battle_rap = json.load(file)
                info_battle_rap = {
                    key.upper(): value for key, value in info_battle_rap.items()
                }

                if user_input in info_battle_rap:
                    return f"CONSULTA:\n\n{user_input}: {info_battle_rap[user_input]}"

        elif command == "ARQUIVO":
            files = os.listdir(BDA_BIRTHDAYS_DIR)

            for file in files:
                if user_input in file:
                    with open(os.path.join(BDA_BIRTHDAYS_DIR, file), "r") as value:
                        value = value.read()
                        return f"{file}:\n\n{value}"

            return "ARQUIVO_NAO_ENCONTRADO"

        return "COMANDO_DESCONHECIDO"


def main():
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()


if __name__ == "__main__":
    main()
