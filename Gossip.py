import random
import socket
from threading import Thread
import time


class GossipNode:
    infected_nodes = []

    def __init__(self, port, connected_nodes):
        self.node = socket.socket(type=socket.SOCK_DGRAM)

        self.hostname = socket.gethostname()
        self.port = port

        self.node.bind((self.hostname, self.port))

        self.susceptible_nodes = connected_nodes

        print("Node started on port {0}".format(self.port))
        print("Susceptible nodes =>", self.susceptible_nodes)

        self.start_threads()

    def input_message(self):
        while True:
            message_to_send = input("Enter a message to send:\n")

            self.transmit_message(message_to_send.encode('ascii'))

    def receive_message(self):
        while True:
            message_to_forward, address = self.node.recvfrom(1024)

            self.susceptible_nodes.remove(address[1])
            GossipNode.infected_nodes.append(address[1])

            time.sleep(2)

            print("\nMessage is: '{0}'.\nReceived at [{1}] from [{2}]\n"
                  .format(message_to_forward.decode('ascii'), time.ctime(time.time()), address[1]))

                      self.transmit_message(message_to_forward)

    def transmit_message(self, message):
        while self.susceptible_nodes:
            selected_port = random.choice(self.susceptible_nodes)

            print("\n")
            print("-"*50)
            print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)
            print("Port selected is [{0}]".format(selected_port))

     
            self.node.sendto(message, (self.hostname, selected_port))

            self.susceptible_nodes.remove(selected_port)
            GossipNode.infected_nodes.append(selected_port)

            print("Message: '{0}' sent to [{1}].".format(message.decode('ascii'), selected_port))
            print("Susceptible nodes =>", self.susceptible_nodes)
            print("Infected nodes =>", GossipNode.infected_nodes)
            print("-"*50)
            time.sleep(2)
            print("\n")

    def start_threads(self):
        Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()
