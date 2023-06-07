import threading
import socket
import time
import sys
import os

global relative_time
global id

relative_time = 1
messages_queue = [] #list of messages
ack_queue = []
global score
score = 1000

def receive_m():
    while True:
        data, addr = s.recvfrom(1024)
        global n_address

        global score
        n_address = addr
        if("negado"==data.decode('utf-8')):
            print("\nRequisção NEGADA\n")
        elif("aceito"==data.decode('utf-8')):
            print("\nRequisição ACEITA\nIniciando acesso.\n")
            use_rc()
        elif("new_process"==data.decode('utf-8').split()[0]):
            # print("\nNovo processo na rede", int(data.decode('utf-8').split()[1]))
            process_network.update({int(data.decode('utf-8').split()[1])})
        elif("ACKjur"==data.decode('utf-8').split('-')[0]):
            score *= 1.1
            print('SALDO COM JUROS:' + str(score))
            print('MSGS:' + str(messages_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
            print('ACKS:' + str(ack_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
        elif("ACKdep"==data.decode('utf-8').split('-')[0]):
            score += 100
            print('SALDO COM DEPOSITO:' + str(score))
            print('MSGS:' + str(messages_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
            print('ACKS:' + str(ack_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
        else:
            # print(n_adress[1])
            print("Onde estamos ", port, data.decode('utf-8').split('-')[2])
            messages_queue.append(data.decode('utf-8'))
            print('MSGS:' + str(messages_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo
            print('ACKS:' + str(ack_queue)) #print de mensagem recebida, recebe dele mesmo e do outro processo

def send_m():
    s.sendto("connect".encode('utf-8'), n_address)
    while True:
        s.sendto(input("").encode('utf-8'), n_address)

def use_rc():
    print("\nPROCESSANDO EM ANDAMENTO\n")
    time.sleep(5)
    print("\nProcesso Terminado, enviando liberação.\n")
    s.sendto(("liberar").encode('utf-8'), n_address)

def send_to_all_processes(message):
    global relative_time
    # print('TR:[' + message + '-' + str(relative_time) + '-' + str(port) + ']\n') #print dele mesmo de local time inicial
    relative_time += 1
    for process in process_network:
        print('Enviando mensagem para processo:', process)
        s.sendto((message + '-' + str(relative_time) + '-' + str(port)).encode('utf-8'), ('localhost', process))

def send_ack_to_all_processes():
    global relative_time
    for message in messages_queue:
        message_splitted = message.split('-')
        if (int(message_splitted[1]) <= relative_time):
            for process in process_network:
                if(process != port):
                    s.sendto(('ACK' + message_splitted[0] + '-'+ str(relative_time) + '-' + str(port)).encode('utf-8'), ('localhost', process))
                    print('@@@@@@@@@@', process)
                    print(('ACK' + message_splitted[0] + '-'+ str(relative_time) + '-' + str(port)).encode('utf-8'))
                    ack_queue.append(message)
            messages_queue.remove(message)

# def execute_messages_ack():
#     global relative_time
#     for message in messages_queue:
#         message_splitted = message.split('-')
#         if relative_time <= int(message_splitted[1]): #se o tempo relativo for menor que o tempo relativo da mensagem
#             #enviar ack daquela mensagem
#             # s.sendto("ack".encode('utf-8'), ('localhost', int(message_splitted[2])))
#             # print(messages_queue)
#             messages_queue.remove(message)

            # print(messages_queue)        
    relative_time += 1


host = 'localhost' 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, 0))

_, port = s.getsockname()

os.system('clear')

print('\nPorta deste processo inicializado em:', port)
process_network = {port}


n_address = ('localhost', 4000)

t1 = threading.Thread(target=send_m)
t2 = threading.Thread(target=receive_m)

t1.start()
t2.start()

time.sleep(2)

send_to_all_processes(sys.argv[1])


time.sleep(2)

#executa se estiver ack ou envia ack

send_ack_to_all_processes()
# execute_messages_ack()
send_ack_to_all_processes()

# print(len(messages_queue))

# _acks_to_process(sys.argv[1])