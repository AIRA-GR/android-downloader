from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import yt_dlp
import threading

class DownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.layout.add_widget(Label(text="Media Downloader", font_size=24, size_hint=(1, 0.2)))
        
        self.url_input = TextInput(hint_text='Paste Link Here...', multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.url_input)
        
        self.format_spinner = Spinner(text='Select Format', values=('Video (MP4)', 'Audio (MP3)'), size_hint=(1, 0.2))
        self.layout.add_widget(self.format_spinner)
        
        self.quality_spinner = Spinner(text='Select Quality', values=('High', 'Medium', 'Low'), size_hint=(1, 0.2))
        self.layout.add_widget(self.quality_spinner)
        
        self.start_btn = Button(text='Start Download', background_color=(0, 0.7, 1, 1), size_hint=(1, 0.2))
        self.start_btn.bind(on_press=self.start_download)
        self.layout.add_widget(self.start_btn)
        
        self.status_label = Label(text="Status: Ready", size_hint=(1, 0.2))
        self.layout.add_widget(self.status_label)
        return self.layout

    def start_download(self, instance):
        self.status_label.text = "Status: Downloading..."
        threading.Thread(target=self.process_download).start()

    def process_download(self):
        url = self.url_input.text
        fmt = self.format_spinner.text
        qual = self.quality_spinner.text

        if not url or fmt == 'Select Format' or qual == 'Select Quality':
            self.status_label.text = "Error: Fill all fields"
            return

        ydl_opts = {'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s', 'quiet': True}

        if fmt == 'Video (MP4)':
            if qual == 'High': ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif qual == 'Medium': ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best'
            else: ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best'
        else:
            ydl_opts['format'] = 'bestaudio/best'
            kbps = '320' if qual == 'High' else ('192' if qual == 'Medium' else '128')
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': kbps}]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
            self.status_label.text = "Success! Check Downloads."
        except Exception:
            self.status_label.text = "Download Failed."

if __name__ == '__main__':
    DownloaderApp().run()
