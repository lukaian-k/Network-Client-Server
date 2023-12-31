import tkinter as tk
import socket
from tkinter.simpledialog import askstring

SERVER_ADDRESS = ("127.0.0.1", 8080)


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("rapENSINA")
        self.root.geometry("500x650")
        self.root.configure(bg="#fbfaff")
        self.create_gui()
        self.client = Client()

    def create_gui(self):
        self.create_header()
        self.create_buttons()
        self.create_response_display()

    def create_header(self):
        header_label = tk.Label(
            self.root,
            text="Comandos",
            font=("Helvetica", 20, "bold"),
            bg="#fbfaff",
            fg="#606060",
        )
        header_label.pack(pady=3)

    def create_buttons(self):
        buttons_frame = tk.Frame(self.root, bg="#fbfaff")
        buttons_frame.pack(pady=3)

        button_properties = {
            "bg": "#6d8d8c",
            "fg": "#fbfaff",
            "font": ("Helvetica", 14, "bold"),
            "width": 20,
        }

        buttons = [
            ("CONSULTA", 0, True),
            ("HORA", 1, False),
            ("ARQUIVO", 2, True),
            ("LISTAR", 3, False),
            ("SAIR", 4, False),
        ]

        for label, row, text_input in buttons:
            button = tk.Button(
                buttons_frame,
                text=label,
                command=self.send_command(label, text_input),
                **button_properties,
            )
            button.grid(row=row, column=0, pady=5, sticky="w")

    def create_response_display(self):
        response_label = tk.Label(
            self.root,
            text="Resposta do servidor:",
            font=("Helvetica", 14, "bold"),
            bg="#fbfaff",
            fg="#606060",
        )
        response_label.pack(pady=30)
        self.response_text = tk.Label(
            self.root, text="", wraplength=300, font=("Helvetica", 12), bg="#fbfaff"
        )
        self.response_text.pack()

    def send_command(self, command, text_input):
        def command_handler():
            if text_input:
                user_input = askstring("Pop-up", f"{command}:")

                if user_input:
                    response = self.client.send(f"{command}|{user_input}")
                else:
                    return

            else:
                response = self.client.send(command)

                if command == "SAIR":
                    self.root.destroy()

            self.update_response_text(response)

        return command_handler

    def update_response_text(self, text):
        self.response_text.config(text=text, fg="#6d8d8c")


class Client:
    def __init__(self):
        self.server_address = SERVER_ADDRESS
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect(self.server_address)
        except ConnectionError as error:
            print(f"Erro ao conectar ao servidor: {error}")
            self.root.destroy()

    def send(self, command):
        try:
            self.client_socket.send(command.encode())
            response = self.client_socket.recv(1024).decode()
            return response

        except ConnectionError as error:
            message = f"Erro de conexão: {error}"
            print(message)
            return message

        except Exception as error:
            message = f"Erro desconhecido: {error}"
            print(message)
            return message


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
