"""
You need to make a program that will control the window on another screen, for example,
a TV, the essence of the task is to make a strobe light that will be adjusted through the
first screen by pressing the 1-2-3-4-5 buttons and a space under each number of some color.
The space bar is white and flickering fast. it would be ideal to synchronize the program
with the microphone so that the microphone hears certain frequencies of the track and
selects the color, thus it will be automated.
"""

from tkinter import *
import pyaudio
import numpy as np
from scipy.fftpack import fft


CHUNK = 1024  # Размер буфера для захвата звука
RATE = 44100  # Частота дискретизации
CHANNELS = 1  # Количество каналов (моно)

# Цветовая палитра для разных частот
color_map = {
    (0, 250): 'red',  # Низкие частоты
    (251, 550): 'orange',  # Средние низкие частоты
    (551, 1000): 'yellow',  # Средние высокие частоты
    (1001, 1500): 'green',  # Высокие частоты
    (1501, 8000): 'blue'  # Очень высокие частоты
}

class Strab():
    def __init__(self):
        self.straboscope_window = Tk()
        self.straboscope_window.title("STRABOSCOPE")
        self.straboscope_window.geometry("450x450")
        self.straboscope_window.bind("<KeyPress>", self.bind_keys)
        self.start_stop = 1
        self.temporary_color = 'black'

    def flicker(self, color):
        while self.start_stop:
            if self.straboscope_window.cget('bg') == color:
                self.straboscope_window.configure(bg="black")
            else:
                self.straboscope_window.configure(bg = color)
            self.straboscope_window.update()
            self.straboscope_window.after(120)

    def check_start_stop(self, color):
        if self.start_stop and color == self.temporary_color:
            self.start_stop = 0
        else:
            self.start_stop = 1
        self.temporary_color = color

    def on_off_micro(self):
        global CHANNELS, RATE, CHUNK
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while self.start_stop:
            data = stream.read(CHUNK)
            data_int = np.frombuffer(data, dtype=np.int16)
            freq = self.get_dominant_frequency(data_int)
            color = self.choose_color(freq)
            #print(f"Доминантная частота: {freq:.2f} Гц | Цвет: {color}")
            self.straboscope_window.configure(bg=color)
            self.straboscope_window.update()
            self.straboscope_window.after(120)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def get_dominant_frequency(self, data):
        data = np.array(data, dtype=float)
        n = len(data)
        yf = fft(data)
        xf = np.linspace(0.0, RATE // 2, n // 2)
        spectrum = 2.0 / n * np.abs(yf[:n // 2])
        dominant_freq_index = np.argmax(spectrum)
        dominant_freq = xf[dominant_freq_index]
        return dominant_freq

    def choose_color(self, freq):
        global color_map
        for range_min, range_max in color_map.keys():
            if freq >= range_min and freq <= range_max:
                return color_map[(range_min, range_max)]
        return 'red'

    def bind_keys(self, event):
        match event.char:
            case '1':
                self.check_start_stop("white")
                self.flicker("white")
            case '2':
                self.check_start_stop("yellow")
                self.flicker("yellow")
            case '3':
                self.check_start_stop("blue")
                self.flicker("blue")
            case '4':
                self.check_start_stop("red")
                self.flicker("red")
            case '5':
                self.check_start_stop("pink")
                self.flicker("pink")
            case '6': #on/off micro
                self.check_start_stop("micro")
                self.on_off_micro()


    def start(self):
        self.straboscope_window.mainloop()

if __name__ == "__main__":
    Strab().start()
