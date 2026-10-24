import subprocess
import os

ps_code = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("voiceover_demo.wav")
$text = @"
Selamat pagi dan salam tangguh. Izin Komandan dan Dewan Juri Kartika Cyber Hackathon 2026. 
Berikut adalah demonstrasi simulasi operasional SENTINEL-AD, Sistem Intelijen Siber dan Pertahanan Kognitif Generasi Baru untuk TNI Angkatan Darat.
Modul pertama adalah Pusat Komando C2, yang memantau kesiapsiagaan DEFCON dan sentimen teritorial di dua puluh tujuh Kodam se-Indonesia.
Modul kedua adalah Ingesti dan Loncatan Narasi, yang melacak propagasi disinformasi dari kanal gelap Telegram hingga viral di platform TikTok dan Twitter.
Modul ketiga adalah CIB Screener dan Forensik Multimodal, yang mengaudit botnet terkoordinasi, rekaman kloning suara deepfake dengan Fourier Transform 16 kilohertz, serta pemalsuan surat perintah mutasi militer menggunakan Error Level Analysis.
Modul keempat adalah Cognitive Wargaming Sandbox, yang menyimulasikan naskah klarifikasi Dispenad terhadap sepuluh persona masyarakat guna meminimalkan risiko bumerang opini publik.
Modul kelima adalah Graf Jaringan Ancaman atau Social Network Analysis, yang memetakan simpul inisiator, botnet amplifikasi, dan kanal jembatan.
Dan modul keenam adalah Tactical SOAR, yang mengotomatisasi rantai komando pengesahan digital tanda tangan komandan serta ekspor berkas dossier hukum BSSN dan dokumen laporan situasi militer SITREP berformat PDF.
SENTINEL-AD siap menjaga kedaulatan kognitif Negara Kesatuan Republik Indonesia. Cakra!
"@
$synth.Speak($text)
$synth.Dispose()
Write-Host "Audio voiceover successfully generated!"
"""

with open("temp_generate_tts.ps1", "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "temp_generate_tts.ps1"], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
if os.path.exists("voiceover_demo.wav"):
    print("voiceover_demo.wav generated successfully! Size:", os.path.getsize("voiceover_demo.wav"))
