import json
import socket
import sys
import ssl


#
# $ ./client <-p port> <-s> <hostname> <Northeastern-username>


def main():
    port = 27993
    host = "proj1.3700.network"
    username = "kosowski.e"
    tls_bool = True

    sys.argv.pop(0)

    '''if sys.argv[0] == "-p":
        port = int(sys.argv[1])
        if sys.argv[2] == "-s":
            tls_bool = True
            host = sys.argv[3]
            username = sys.argv[4]
        else:
            host = sys.argv[2]
            username = sys.argv[3]
    elif sys.argv[0] == "-s":
        port = 27994
        tls_bool = True
        host = sys.argv[1]
        username = sys.argv[2]
    else:
        host = sys.argv[0]
        username = sys.argv[1]'''

    port = 27994
    host = "proj1.3700.network"
    username = "kosowski.e"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if tls_bool:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ss = context.wrap_socket(s, server_hostname=host)
        wordle(ss, host, port, username)
    else:
        wordle(s, host, port, username)


def wordle(s, host, port, username):
    s.connect((host, port))
    s.sendall((json.dumps({"type": "hello", "northeastern_username": username}) + "\n").encode())
    data = s.recv(1024).decode("utf-8")
    while not data.endswith("\n"):
        data += s.recv(1024).decode("utf-8")
    message = (json.loads(data))
    game_id = message["id"]
    with open("project1-words.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    while True:

        s.sendall((json.dumps({"type": "guess", "id": game_id, "word": lines[0]}) + "\n").encode())
        data = s.recv(1024).decode("utf-8")
        while not data.endswith("\n"):
            data += s.recv(1024).decode("utf-8")
        message = (json.loads(data))

        if message["type"] == "bye":
            print(message["flag"])
            break
        if message["type"] == "error":
            print(message["message"])
            break

        current_guess = message["guesses"][-1]
        print(current_guess)
        first_letter_value = current_guess["marks"][0]

        for value in range(5):

            letter_value = current_guess["marks"][value]

            new_lines = []
            if int(letter_value) == 0 or int(letter_value) == 1:
                for word in lines:
                    if word[value] != current_guess["word"][value]:
                        new_lines.append(word)
                lines = new_lines


main()
