import speech_recognition as sr
import time,os
from datetime import datetime


# Fungsi untuk mengonversi string waktu menjadi objek waktu
def convert_to_time(time_str):
    # Mengonversi string waktu (format 'HH:MM') menjadi objek waktu
    return datetime.strptime(time_str, '%H:%M').time()

# Fungsi untuk mengecek apakah waktu sekarang berada dalam jam yang diizinkan
def is_allowed_time():
    current_time = datetime.now().time()
    start_morning = convert_to_time("08:00")  # Jam mulai pagi
    end_morning = convert_to_time("12:00")  # Jam berakhir pagi
    start_afternoon = datetime.strptime('2:00', '%H:%M').time()  # Jam mulai sore
    end_afternoon = datetime.strptime('21:00', '%H:%M').time()  # Jam berakhir sore

    # Cek apakah waktu saat ini dalam rentang jam yang diizinkan
    if start_morning <= current_time <= end_morning or start_afternoon <= current_time <= end_afternoon:
        return True
    return False

# Fungsi untuk mendengarkan suara dan memprosesnya
def listen_for_commands():
    # Membuat objek recognizer
    recognizer = sr.Recognizer()

    # Menggunakan microphone sebagai sumber input audio
    with sr.Microphone() as source:
        print("Menunggu suara...")

        # Mengatur ambang batas untuk menyesuaikan dengan kebisingan latar belakang
        recognizer.adjust_for_ambient_noise(source)

        # start_time = time.time()

        while True:
            try:
                print("Mendengarkan...")
                audio = recognizer.listen(source, timeout=5)  # Tunggu selama 5 detik untuk mendeteksi suara

                print("Mengenali...")
                text = recognizer.recognize_google(audio, language="id-ID")
                print(f"Anda berkata: {text}")

                # Jika mendeteksi perintah 'stop', berhenti
                if "stop" in text.lower():
                    print("Perintah 'stop' diterima. Program berhenti.")
                    os.system('exit')
                elif any(keyword in text.lower() for keyword in ["jadwal salat", "daftar salat"]):		
                    os.system('/data/data/com.termux/files/home/jamBira/jamBira sol')
                elif "waktu salat" in text.lower():					
                    os.system('/data/data/com.termux/files/home/jamBira/jamBira 4')
                elif "jb 12" in text.lower():					
                    os.system('/data/data/com.termux/files/home/jamBira/jamBira 12')                                          
                # Jika lebih dari 10 detik tanpa suara, keluar
                # if time.time() - start_time > 10:
                    # print("Tidak ada suara dalam 10 detik, program berhenti.")
                    # return False  # Program berhenti
                # Setelah mendeteksi suara, berhenti mendengarkan selama 10 detik
                menitnya=3
                print("Mendengarkan dihentikan selama "+str(menitnya)+" detik...")
                time.sleep(int(menitnya))  # Menunggu 10 detik sebelum melanjutkan mendengarkan
            except sr.WaitTimeoutError:
                print("Tidak ada suara terdeteksi, menunggu lagi...")
            except sr.UnknownValueError:
                pass  # Tidak ada suara yang dikenali, tunggu lagi
            except sr.RequestError as e:
                print(f"Gagal menghubungi Google Speech Recognition service; {e}")
                break
    return True  # Jika loop selesai dengan normal, kembali True

# Fungsi utama untuk menjalankan program sesuai dengan jam yang diizinkan
def main():
    while True:
        if not is_allowed_time():
            # Jika waktu tidak sesuai, program akan berhenti sementara
            current_time = datetime.now().strftime('%H:%M')
            print(f"Program tidak dapat dijalankan pada jam {current_time}. Menunggu waktu yang sesuai...")
            time.sleep(60)  # Cek setiap menit apakah waktu sudah sesuai
        else:
            # Jika waktu sesuai, jalankan program
            print("Program dijalankan pada jam yang sesuai.")
            if not listen_for_commands():
                print("Program dihentikan. Memulai ulang...")
                time.sleep(2)  # Tunggu sebentar sebelum memulai ulang
            else:
                print("Program berjalan kembali.")

if __name__ == "__main__":
    main()
