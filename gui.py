# gui.py

import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from datetime import datetime

import config
from OCR import ocr_transcribe
from llavaRunner import llava_transcribe

class TranscriberApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Pre-flight checks
        if not os.path.isfile(config.TESSERACT_PATH):
            messagebox.showerror("Missing Tesseract", config.TESSERACT_PATH)
            self.destroy(); return
        if not os.path.isfile(config.OLLAMA_PATH):
            messagebox.showerror("Missing Ollama", config.OLLAMA_PATH)
            self.destroy(); return

        # Window
        self.title("ImageTranscriber v1.0")
        self.minsize(900, 500)

        # State
        self.input_dir     = config.ROOT_IMAGE_DIR
        self.queue_folders = []
        self.method        = tk.StringVar(value="OCR")
        self.log_history   = []

        # Colors & fonts
        TB_BG  = "#222222"; ACCENT = "#f44336"
        BTN_BG = "#85cdca"; BTN_FG = "#ffffff"
        LOG_BG = "#1e1e1e"; LOG_FG = "#E0E0E0"
        FONTSZ = ("Consolas", 14)

        # Toolbar
        toolbar = tk.Frame(self, bg=TB_BG, padx=8, pady=8)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="📂 Add Folder", command=self.add_folder,
                  bg=BTN_BG, fg=BTN_FG, relief="flat",
                  font=("Helvetica",12)).pack(side="left", padx=4)
        tk.Button(toolbar, text="🔄 Refresh Queue", command=self.refresh_queue,
                  bg=BTN_BG, fg=BTN_FG, relief="flat",
                  font=("Helvetica",12)).pack(side="left", padx=4)

        engine_frame = tk.LabelFrame(toolbar, text="Engine",
                                     bg=TB_BG, fg="white",
                                     font=("Helvetica",12,"bold"),
                                     labelanchor="n", bd=0, padx=6, pady=4)
        engine_frame.pack(side="left", padx=16)
        for txt,val in [("OCR Only","OCR"), ("LLAVA","LLAVA")]:
            rb = tk.Radiobutton(engine_frame, text=txt, variable=self.method,
                                value=val, bg=TB_BG, fg="white",
                                selectcolor=ACCENT, activebackground=TB_BG,
                                font=("Helvetica",11))
            rb.pack(side="left", padx=4)

        sep = tk.Frame(toolbar, bg="#444444", width=2, height=28)
        sep.pack(side="left", padx=8)

        self.start_btn = tk.Button(toolbar, text="▶ Start Processing",
                                   command=self.start_processing,
                                   bg=BTN_BG, fg=BTN_FG, relief="flat",
                                   font=("Helvetica",14,"bold"))
        self.start_btn.pack(side="left", padx=4)

        tk.Button(toolbar, text="🗑 Clear Log", command=self.clear_log,
                  bg=TB_BG, fg=ACCENT, relief="flat",
                  font=("Helvetica",12)).pack(side="left", padx=4)
        tk.Button(toolbar, text="⏻ Quit", command=self.destroy,
                  bg=ACCENT, fg=BTN_FG, relief="flat",
                  font=("Helvetica",12)).pack(side="right", padx=4)

        # Main layout
        main_pane = tk.Frame(self)
        main_pane.pack(fill="both", expand=True)

        # Queue sidebar
        queue_frame = tk.Frame(main_pane, width=250, bg="#2a2a2a")
        queue_frame.pack(side="left", fill="y")
        tk.Label(queue_frame, text="Folder Queue",
                 bg="#2a2a2a", fg="white",
                 font=("Helvetica",12,"bold")).pack(pady=(8,4))
        self.queue_listbox = tk.Listbox(queue_frame,
                                        bg="#333333", fg="white",
                                        font=("Helvetica",11),
                                        selectbackground=ACCENT,
                                        relief="flat", bd=0)
        self.queue_listbox.pack(fill="both", expand=True, padx=8, pady=4)
        tk.Button(queue_frame, text="➖ Remove Selected",
                  command=self.remove_selected_folder,
                  bg=BTN_BG, fg=BTN_FG, relief="flat",
                  font=("Helvetica",11)).pack(padx=8, pady=(0,8))

        # Right pane: progress + log
        right_frame = tk.Frame(main_pane)
        right_frame.pack(side="right", fill="both", expand=True)

        prog_frame = tk.Frame(right_frame)
        prog_frame.pack(fill="x", padx=8, pady=(8,4))
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Red.Horizontal.TProgressbar",
                        troughcolor="#2a2a2a",
                        background=ACCENT, thickness=16)
        self.progress = tk.DoubleVar()
        self.pb = ttk.Progressbar(prog_frame, variable=self.progress,
                                  maximum=100,
                                  style="Red.Horizontal.TProgressbar")
        self.pb.pack(fill="x", padx=4)

        status_line = tk.Frame(prog_frame, bg="#2a2a2a")
        status_line.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.status_label = tk.Label(status_line, text="0/0 images",
                                     fg="white", bg="#2a2a2a",
                                     font=("Helvetica",10))
        self.status_label.pack(side="left", padx=8)
        self.eta_label = tk.Label(status_line, text="Est. 0s remaining",
                                  fg="white", bg="#2a2a2a",
                                  font=("Helvetica",10))
        self.eta_label.pack(side="right", padx=8)

        self.log = scrolledtext.ScrolledText(right_frame,
                                             bg=LOG_BG, fg=LOG_FG,
                                             font=FONTSZ, wrap="word",
                                             state="disabled",
                                             padx=8, pady=4)
        self.log.pack(fill="both", expand=True, padx=8, pady=(0,8))
        self.log_message("⟳ Add folders, select engine, then ▶ Start Processing", tag="placeholder")

        # Shortcuts
        self.bind_all("<Control-l>", lambda e: self.clear_log())
        self.bind_all("<Control-r>", lambda e: self.start_processing())

    # Queue management
    def add_folder(self):
        folder = filedialog.askdirectory(initialdir=self.input_dir)
        if folder and folder not in self.queue_folders:
            self.queue_folders.append(folder)
            self.queue_listbox.insert("end", folder)
            self.log_message(f"➕ Added folder: {folder}")

    def remove_selected_folder(self):
        sel = list(self.queue_listbox.curselection())
        for idx in reversed(sel):
            folder = self.queue_listbox.get(idx)
            self.queue_listbox.delete(idx)
            self.queue_folders.remove(folder)
            self.log_message(f"➖ Removed folder: {folder}")

    def refresh_queue(self):
        self.log_message(f"🔄 Queue refreshed: {len(self.queue_folders)} folder(s)")

    # Logging
    def log_message(self, msg, tag=None):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag or ())
        self.log.see("end")
        self.log.config(state="disabled")

    def clear_log(self):
        self.log.config(state="normal"); self.log.delete("1.0","end"); self.log.config(state="disabled")
        self.log_message("⟳ Add folders, select engine, then ▶ Start Processing", tag="placeholder")

    # Batch processing
    def start_processing(self):
        if not self.queue_folders:
            messagebox.showwarning("No folders", "Add at least one folder.")
            return
        self.clear_log()
        self.start_btn.config(state="disabled", text="⏳ Processing…")
        threading.Thread(target=self._process_queue, daemon=True).start()

    def _process_queue(self):
        img_list = []
        for folder in self.queue_folders:
            for root,_,files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(('.png','jpg','jpeg','tiff','bmp','gif')):
                        img_list.append(os.path.join(root,f))

        total = len(img_list)
        if total == 0:
            self.log_message("❌ No images found.", tag="error")
            self.start_btn.config(state="normal", text="▶ Start Processing")
            return

        start_time = time.time()
        for i, img in enumerate(img_list, start=1):
            pct = (i-1)/total*100
            self.progress.set(pct)
            self.status_label.config(text=f"{i}/{total} images")
            elapsed = time.time() - start_time
            avg = elapsed/(i-1) if i>1 else 0
            rem = int(avg*(total-i+1))
            m,s = divmod(rem,60)
            self.eta_label.config(text=f"Est. {m}m {s}s remaining")

            if self.method.get() == "OCR":
                out = ocr_transcribe(img)
            else:
                out = llava_transcribe(img)

            base = os.path.splitext(os.path.basename(img))[0]
            out_path = os.path.join(config.OUTPUT_DIR, f"{base}Transcribed.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(out)
            self.log_message(f"✔ Saved → {out_path}", tag="success")

        self.progress.set(100)
        self.eta_label.config(text="Est. 0s remaining")
        self.start_btn.config(state="normal", text="▶ Start Processing")
        messagebox.showinfo("Done", f"Processed {total} images.\nOutputs in:\n{config.OUTPUT_DIR}")

if __name__ == "__main__":
    TranscriberApp().mainloop()
