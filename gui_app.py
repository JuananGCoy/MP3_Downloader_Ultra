import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from core_logic import ShokzDownloader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ShokzFlowApp(ctk.CTk):
    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path

        self.title("ShokzFlow - MP3 Downloader")
        self.geometry("700x550")

        self.output_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Music"))
        self.downloader = None

        # UI Components
        self.header_label = ctk.CTkLabel(self, text="ShokzFlow", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=20)

        # URL Input
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.pack(fill="x", padx=40, pady=10)
        
        self.url_label = ctk.CTkLabel(self.url_frame, text="YouTube URL:")
        self.url_label.pack(side="left", padx=10)
        
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="https://www.youtube.com/watch?v=...", width=400)
        self.url_entry.pack(side="left", padx=10, fill="x", expand=True)

        # Folder Selection
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.pack(fill="x", padx=40, pady=10)
        
        self.folder_label = ctk.CTkLabel(self.folder_frame, text="Destination Folder:")
        self.folder_label.pack(side="left", padx=10)
        
        self.folder_entry = ctk.CTkEntry(self.folder_frame, textvariable=self.output_path, state="readonly", width=300)
        self.folder_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        self.browse_button = ctk.CTkButton(self.folder_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="right", padx=10)

        # Format and Quality Selection
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(fill="x", padx=40, pady=10)
        
        # Format Selector (MP3/MP4)
        self.format_label = ctk.CTkLabel(self.options_frame, text="Format:")
        self.format_label.pack(side="left", padx=10)
        
        self.format_var = ctk.StringVar(value="MP3")
        self.format_switch = ctk.CTkSegmentedButton(self.options_frame, values=["MP3", "MP4"], 
                                                     variable=self.format_var, command=self.toggle_format_options)
        self.format_switch.pack(side="left", padx=10)

        # Container for dynamic options (Bitrate or Resolution)
        self.quality_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.quality_frame.pack(side="left", padx=20, fill="x", expand=True)

        # Action Buttons Frame (Static)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.download_button = ctk.CTkButton(self.button_frame, text="DOWNLOAD", command=self.start_download, 
                                             font=ctk.CTkFont(size=16, weight="bold"), height=40, width=200)
        self.download_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(self.button_frame, text="STOP", command=self.stop_download, 
                                         font=ctk.CTkFont(size=16, weight="bold"), height=40, width=100,
                                         fg_color="crimson", hover_color="#8B0000", state="disabled")
        self.stop_button.pack(side="left", padx=10)

        # Progress Bar (Static)
        self.progress_bar = ctk.CTkProgressBar(self, width=600)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        # Status Console (Static)
        self.status_label = ctk.CTkLabel(self, text="Ready", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=5)
        
        self.console = ctk.CTkTextbox(self, height=120, width=600, font=ctk.CTkFont(size=11))
        self.console.pack(pady=10)
        self.console.configure(state="disabled")
        
        # Initialize format options
        self.toggle_format_options("MP3")

    def toggle_format_options(self, selected_format):
        # Clear existing quality options
        for widget in self.quality_frame.winfo_children():
            widget.destroy()

        if selected_format == "MP3":
            ctk.CTkLabel(self.quality_frame, text="Bitrate:").pack(side="left", padx=5)
            self.quality_var = ctk.StringVar(value="320")
            for br in ["192", "256", "320"]:
                lbl = f"{br} (MAX)" if br == "320" else br
                ctk.CTkRadioButton(self.quality_frame, text=lbl, variable=self.quality_var, value=br).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(self.quality_frame, text="Resolution:").pack(side="left", padx=5)
            self.quality_var = ctk.StringVar(value="best")
            for res in ["360p", "720p", "1080p", "best"]:
                ctk.CTkRadioButton(self.quality_frame, text=res, variable=self.quality_var, value=res).pack(side="left", padx=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def log_status(self, message):
        self.console.configure(state="normal")
        self.console.insert("end", f"{message}\n")
        self.console.see("end")
        self.console.configure(state="disabled")
        self.status_label.configure(text=message)

    def update_progress(self, percent):
        self.progress_bar.set(percent)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        
        destination = self.output_path.get()
        if not os.path.exists(destination):
            messagebox.showerror("Error", "Selected folder does not exist.")
            return

        self.download_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)
        self.log_status("Starting background thread...")
        
        format_type = self.format_var.get().lower()
        quality = self.quality_var.get()
        
        # Run in a separate thread
        thread = threading.Thread(target=self.download_wrapper, args=(url, destination, format_type, quality))
        thread.daemon = True
        thread.start()

    def stop_download(self):
        if self.downloader:
            self.downloader.is_cancelled = True
            self.log_status("Stopping process... Please wait.")
            self.stop_button.configure(state="disabled")

    def download_wrapper(self, url, destination, format_type, quality):
        try:
            self.downloader = ShokzDownloader(
                callback_progress=self.update_progress,
                callback_status=self.log_status,
                resource_path=self.resource_path
            )
            self.downloader.download(url, destination, format_type=format_type, quality=quality)
            if not self.downloader.is_cancelled:
                messagebox.showinfo("Success", f"Download finished ({format_type.upper()})!")
            else:
                self.log_status("Download stopped by user.")
        except Exception as e:
            if "cancelled" in str(e).lower():
                self.log_status("Process stopped.")
            else:
                self.log_status(f"Error: {e}")
                messagebox.showerror("Download Error", str(e))
        finally:
            self.downloader = None
            self.download_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

if __name__ == "__main__":
    def dummy_resource_path(p): return p
    app = ShokzFlowApp(dummy_resource_path)
    app.mainloop()
