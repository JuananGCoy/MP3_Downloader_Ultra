# MP3 Downloader Ultra 🎵

A clean, modern, and high-quality YouTube to MP3 downloader built in Python. Designed for speed and compatibility with high-end audio devices like **Shokz OpenSwim Pro**.

## ✨ Features
*   **High Fidelity Audio**: Support for VBR 0 (Variable Bitrate, Highest Quality) and 320kbps.
*   **Automated Naming**: Intelligent folder-based naming for YouTube playlists (e.g., `01 - Title.mp3`).
*   **Portable Build**: Fully standalone `.exe` generator with FFmpeg bundled inside.
*   **Modern UI**: Beautiful Dark Mode interface utilizing `CustomTkinter`.
*   **No Overhead**: Lightweight downloads without loose image files or bloated metadata.

## 🚀 How to Run Locally

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/JuananGCoy/MP3_Downloader_Ultra.git
    cd MP3_Downloader_Ultra
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python main.py
    ```

## 🔨 How to Build the Portable Executable

1.  Make sure `ffmpeg.exe` and `ffprobe.exe` are in the project root.
2.  Run the build script:
    ```bash
    python build_app.py
    ```
3.  Your `MP3_Downloader_Ultra.exe` will appear in the `dist` folder.

## 📜 Dependencies
*   [yt-dlp](https://github.com/yt-dlp/yt-dlp): Powerful YouTube download engine.
*   [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter): Modern UI framework.
*   [Mutagen](https://github.com/quodlibet/mutagen): Robust MP3 metadata management.

---
*Developed with ❤️ for high-quality audio lovers.*
