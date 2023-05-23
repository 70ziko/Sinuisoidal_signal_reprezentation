import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def generate_sinusoidal_signal(amplitude, frequency, phase, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return t, signal

def generate_composite_signal(amplitude1, frequency1, phase1, amplitude2, frequency2, phase2, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude1 * np.sin(2 * np.pi * frequency1 * t + phase1)
    signal2 = amplitude2 * np.sin(2 * np.pi * frequency2 * t + phase2)
    composite_signal = signal1 + signal2
    return t, composite_signal

def generate_custom_signal(amplitude, frequency, phase, duration, sampling_rate, t1, t2, n):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * (((t/t1)**n)/(1+(t/t1)**n)) * np.exp(-(t/t2))* np.cos(2 * np.pi * frequency * t + phase)
    return t, signal

def generate_composite_custom_signal(amplitude1, frequency1, phase1, amplitude2, frequency2, phase2, duration, sampling_rate, t1, t2, n):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal1 = amplitude1 * (((t/t1)**n)/(1+(t/t1)**n)) * np.exp(-(t/t2)) * np.cos(2 * np.pi * frequency1 * t + phase1)
    signal2 = amplitude2 * (((t/t1)**n)/(1+(t/t1)**n)) * np.exp(-(t/t2)) * np.sin(2 * np.pi * frequency2 * t + phase2)
    composite_signal = signal1 + signal2
    return t, composite_signal

def perform_fourier_transform(signal, sampling_rate):
    n = len(signal)
    frequencies = np.fft.fftfreq(n, d=1/sampling_rate)
    spectrum = np.fft.fft(signal) / n
    return frequencies[:n//2], np.abs(spectrum[:n//2])

def plot_signal_and_spectrum(t, signal, frequencies, spectrum):
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    axs[0].plot(t, signal)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Signal')

    axs[1].plot(frequencies, spectrum)
    axs[1].set_xlabel('Frequency')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_title('Spectrum')

    plt.tight_layout()
    return fig

def generate_signal():
    global canvas

    amplitude = float(amp_entry.get())
    frequency = float(freq_entry.get())
    phase = float(phase_entry.get())
    duration = float(duration_entry.get())
    sampling_rate = float(sampling_rate_entry.get())

    signal_type = signal_type_var.get()

    if signal_type == "Single":
        t, signal = generate_sinusoidal_signal(amplitude, frequency, phase, duration, sampling_rate)
    else:
        amplitude2 = float(amp2_entry.get())
        frequency2 = float(freq2_entry.get())
        phase2 = float(phase2_entry.get())
        t, signal = generate_composite_signal(amplitude, frequency, phase, amplitude2, frequency2, phase2, duration, sampling_rate)

    frequencies, spectrum = perform_fourier_transform(signal, sampling_rate)

    if canvas is not None:
        # Jeśli istnieje istniejący wykres, usuń go
        canvas.get_tk_widget().pack_forget()

    fig = plot_signal_and_spectrum(t, signal, frequencies, spectrum)

    if canvas is None:
        # Jeśli nie istnieje istniejący wykres, stwórz nowy widżet Canvas
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    else:
        # Jeśli istnieje istniejący wykres, zaktualizuj go
        canvas.figure = fig
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Dodawanie paska narzędzi nawigacji (opcjonalne)
    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Aplikacja prezentująca sygnały i ich widma")

# Ramka dla wprowadzania parametrów sygnału
parameters_frame = tk.Frame(root)
parameters_frame.pack(pady=10)

canvas = None

amp_label = tk.Label(parameters_frame, text="Amplituda:")
amp_label.grid(row=0, column=0, padx=5, pady=5)
amp_entry = tk.Entry(parameters_frame)
amp_entry.insert(0, "1.0")
amp_entry.grid(row=0, column=1, padx=5, pady=5)

freq_label = tk.Label(parameters_frame, text="Częstotliwość:")
freq_label.grid(row=1, column=0, padx=5, pady=5)
freq_entry = tk.Entry(parameters_frame)
freq_entry.insert(0, "10.0")
freq_entry.grid(row=1, column=1, padx=5, pady=5)

phase_label = tk.Label(parameters_frame, text="Faza:")
phase_label.grid(row=2, column=0, padx=5, pady=5)
phase_entry = tk.Entry(parameters_frame)
phase_entry.insert(0, "0.0")
phase_entry.grid(row=2, column=1, padx=5, pady=5)

duration_label = tk.Label(parameters_frame, text="Czas trwania:")
duration_label.grid(row=3, column=0, padx=5, pady=5)
duration_entry = tk.Entry(parameters_frame)
duration_entry.insert(0, "1.0")
duration_entry.grid(row=3, column=1, padx=5, pady=5)

sampling_rate_label = tk.Label(parameters_frame, text="Częstotliwość próbkowania:")
sampling_rate_label.grid(row=4, column=0, padx=5, pady=5)
sampling_rate_entry = tk.Entry(parameters_frame)
sampling_rate_entry.insert(0, "1000.0")
sampling_rate_entry.grid(row=4, column=1, padx=5, pady=5)

amp2_label = tk.Label(parameters_frame, text="Amplituda 2:")
amp2_label.grid(row=0, column=2, padx=5, pady=5)
amp2_entry = tk.Entry(parameters_frame)
amp2_entry.insert(0, "1.0")
amp2_entry.grid(row=0, column=3, padx=5, pady=5)

freq2_label = tk.Label(parameters_frame, text="Częstotliwość 2:")
freq2_label.grid(row=1, column=2, padx=5, pady=5)
freq2_entry = tk.Entry(parameters_frame)
freq2_entry.insert(0, "20.0")
freq2_entry.grid(row=1, column=3, padx=5, pady=5)

phase2_label = tk.Label(parameters_frame, text="Faza 2:")
phase2_label.grid(row=2, column=2, padx=5, pady=5)
phase2_entry = tk.Entry(parameters_frame)
phase2_entry.insert(0, "0.0")
phase2_entry.grid(row=2, column=3, padx=5, pady=5)

signal_type_label = tk.Label(parameters_frame, text="Typ sygnału:")
signal_type_label.grid(row=5, column=0, padx=5, pady=5)

signal_type_var = tk.StringVar()
signal_type_var.set("Single")

single_signal_radio = tk.Radiobutton(parameters_frame, text="Jedno", variable=signal_type_var, value="Single")
single_signal_radio.grid(row=5, column=1, padx=5, pady=5)

composite_signal_radio = tk.Radiobutton(parameters_frame, text="Złożone", variable=signal_type_var, value="Composite")
composite_signal_radio.grid(row=5, column=2, padx=5, pady=5)

generate_button = tk.Button(root, text="Generuj sygnał", command=generate_signal)
generate_button.pack(pady=10)

# Ramka dla wykresu
plot_frame = tk.Frame(root)
plot_frame.pack()

root.mainloop()
