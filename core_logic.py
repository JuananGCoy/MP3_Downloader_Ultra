import os
import yt_dlp
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, APIC, TALB
import urllib.request

class ShokzDownloader:
    def __init__(self, callback_progress=None, callback_status=None, resource_path=None):
        self.callback_progress = callback_progress
        self.callback_status = callback_status
        self.resource_path = resource_path or (lambda p: p)
        self.is_cancelled = False
        
        # Get paths for bundled ffmpeg
        self.ffmpeg_exe = self.resource_path("ffmpeg.exe")
        self.ffprobe_exe = self.resource_path("ffprobe.exe")

    def check_ffmpeg(self):
        """Check if FFmpeg is available (either bundled or on PATH)."""
        if os.path.exists(self.ffmpeg_exe):
            return True
        return shutil.which("ffmpeg") is not None

    def progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("Download cancelled by user")
        
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                percent = float(p)
                if self.callback_progress:
                    self.callback_progress(percent / 100)
            except ValueError:
                pass
            
            if self.callback_status:
                filename = d.get('filename', 'Unknown')
                self.callback_status(f"Downloading: {os.path.basename(filename)}")
        
        elif d['status'] == 'finished':
            if self.callback_status:
                self.callback_status("Download finished, converting...")

    def post_process_metadata(self, filepath, info):
        """Embed basic metadata (Title, Artist, Album) into the MP3 file."""
        try:
            audio = MP3(filepath, ID3=ID3)
            try:
                audio.add_tags()
            except:
                pass

            # Basic tags
            audio.tags.add(TIT2(encoding=3, text=info.get('title', 'Unknown')))
            audio.tags.add(TPE1(encoding=3, text=info.get('uploader', 'Unknown Artist')))
            
            # Album name (playlist name if applicable)
            playlist_title = info.get('playlist_title')
            if playlist_title:
                audio.tags.add(TALB(encoding=3, text=playlist_title))

            audio.save()
        except Exception as e:
            print(f"Error embedding metadata: {e}")

    def download(self, url, output_dir, bitrate='192'):
        if not self.check_ffmpeg():
            raise Exception("FFmpeg not found. Please install FFmpeg and add it to your PATH.")

        # Determine if it's a playlist
        ydl_opts_info = {'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            is_playlist = 'entries' in info

        # Base options
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': os.path.dirname(self.ffmpeg_exe) if os.path.exists(self.ffmpeg_exe) else None,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                # If bitrate is '320', use VBR 0 for maximum quality. Otherwise use CBR.
                'preferredquality': '0' if bitrate == '320' else bitrate,
            }, {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'progress_hooks': [self.progress_hook],
            'writethumbnail': False,
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            # Force high quality resampling if needed
            'postprocessor_args': [
                '-ar', '44100',
                '-ac', '2'
            ]
        }

        if is_playlist:
            playlist_name = info.get('title', 'Playlist').replace('/', '_').replace('\\', '_')
            final_dir = os.path.join(output_dir, playlist_name)
            if not os.path.exists(final_dir):
                os.makedirs(final_dir)
            ydl_opts['outtmpl'] = os.path.join(final_dir, '%(playlist_index)02d - %(title)s.%(ext)s')
        else:
            ydl_opts['outtmpl'] = os.path.join(output_dir, '%(title)s.%(ext)s')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We need the full info for post-processing metadata
            result = ydl.extract_info(url, download=True)
            
            if is_playlist:
                for entry in result.get('entries', []):
                    if entry:
                        # Improved logic to find the resulting MP3 file
                        base_path = ydl.prepare_filename(entry)
                        filepath = os.path.splitext(base_path)[0] + '.mp3'
                        if os.path.exists(filepath):
                            entry['playlist_title'] = playlist_name
                            self.post_process_metadata(filepath, entry)
            else:
                base_path = ydl.prepare_filename(result)
                filepath = os.path.splitext(base_path)[0] + '.mp3'
                if os.path.exists(filepath):
                    self.post_process_metadata(filepath, result)

        if self.callback_status:
            self.callback_status("All tasks completed!")
        if self.callback_progress:
            self.callback_progress(1.0)
