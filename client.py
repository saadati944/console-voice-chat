import socket
import threading
import pyaudio

class Client:
    def __init__(self):
        pass

    def start(self, ip: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.target_ip = ip
            self.target_port = port

            self.s.connect((self.target_ip, self.target_port))
        except:
            return False

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 16000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        # start threads
        threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()
    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

client = Client()
