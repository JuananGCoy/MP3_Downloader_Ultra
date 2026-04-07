<p align="center">
  <img src="assets/logo.png" alt="MP3 Downloader Ultra Logo" width="200" />
</p>

# MP3 Downloader Ultra 🎵
**La solución definitiva para descargar música en alta calidad, sin anuncios y optimizada para tus Shokz OpenSwim Pro.**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Downloads](https://img.shields.io/github/downloads/JuananGCoy/MP3_Downloader_Ultra/total)](https://github.com/JuananGCoy/MP3_Downloader_Ultra/releases)

---

## 🌊 El Problema y la Solución
¿Cansado de descargar música para tus **Shokz OpenSwim Pro** y que las pistas se desordenen, el audio suene "roto" o la interfaz esté llena de anuncios engañosos?

**MP3 Downloader Ultra** ha sido diseñado específicamente para nadadores y amantes de la música que buscan la perfección:
*   **Problema**: Audio de baja calidad (bitrate pobre).
*   **Solución**: Soporte para **VBR 0 / 320kbps (MAX Quality)** con re-muestreo a 44.1kHz.
*   **Problema**: Listas de reproducción desordenadas.
*   **Solución**: Modo "Shokz" que antepone `01 - `, `02 - ` automáticamente según el orden de la lista.
*   **Problema**: Complejidad y virus.
*   **Solución**: Un único ejecutable portable, **100% código abierto** y sin instalaciones externas.

---

## 📸 Captura de Pantalla
<p align="center">
  <img src="assets/screenshot.png" alt="MP3 Downloader Ultra Interface" width="600" />
</p>

---

## 🚀 Instalación y Uso

### 👤 Para Usuarios (Uso RÁPIDO)
Si solo quieres descargar música y nadar:
1.  Ve a la sección de [Releases](https://github.com/JuananGCoy/MP3_Downloader_Ultra/releases).
2.  Descarga el archivo `MP3_Downloader_Ultra.exe`.
3.  Ábrelo y ¡listo! No necesitas instalar nada más.

### 💻 Para Desarrolladores (Contribución)
Si quieres jugar con el código o mejorarlo:
1.  Clona el repositorio:
    ```bash
    git clone https://github.com/JuananGCoy/MP3_Downloader_Ultra.git
    cd MP3_Downloader_Ultra
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Asegúrate de tener `ffmpeg.exe` y `ffprobe.exe` en la carpeta raíz (necesarios para la conversión de audio).
4.  Ejecuta la app:
    ```bash
    python main.py
    ```

---

## 🔨 Cómo compilar tu propio .exe
Si has hecho cambios y quieres generar tu propio ejecutable portable:
1.  Asegúrate de que `ffmpeg.exe` esté en la raíz.
2.  Ejecuta el script de construcción:
    ```bash
    python build_app.py
    ```
3.  Recoge tu archivo en la carpeta `dist`.

---

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. ¡Siéntete libre de usarlo, mejorarlo y distribuirlo!

---
<p align="center">
  Hecho con ❤️ para la comunidad de natación por <b>Juanan el mejor</b>.
</p>
