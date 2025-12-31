import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

class SRTConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SRT 轉 TXT 終極轉換器 (自訂分割與時間軸)")
        self.root.geometry("650x580")
        
        # --- 變數設定 ---
        self.source_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.mode_var = tk.StringVar(value="file")
        
        # 功能變數
        self.split_files_var = tk.BooleanVar(value=False) # 是否啟用分割
        self.split_hours = tk.IntVar(value=2)             # 分割時數 (預設2小時)
        
        self.keep_timestamp_var = tk.BooleanVar(value=True) 
        self.merge_text_var = tk.BooleanVar(value=False) 
        self.merge_seconds = tk.IntVar(value=60) 
        
        self.create_widgets()

    def create_widgets(self):
        # 1. 來源模式
        frame_mode = tk.LabelFrame(self.root, text="1. 選擇來源模式", padx=10, pady=5)
        frame_mode.pack(fill="x", padx=10, pady=5)
        tk.Radiobutton(frame_mode, text="單一檔案 (.srt)", variable=self.mode_var, value="file", command=self.update_ui_state).pack(side="left", padx=10)
        tk.Radiobutton(frame_mode, text="指定資料夾 (批次處理)", variable=self.mode_var, value="folder", command=self.update_ui_state).pack(side="left", padx=10)

        # 2. 路徑設定
        frame_paths = tk.LabelFrame(self.root, text="2. 設定路徑", padx=10, pady=5)
        frame_paths.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_paths, text="來源位置:").grid(row=0, column=0, sticky="w")
        self.entry_source = tk.Entry(frame_paths, textvariable=self.source_path, width=55)
        self.entry_source.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_paths, text="瀏覽...", command=self.browse_source).grid(row=0, column=2, padx=5)
        
        tk.Label(frame_paths, text="存檔位置:").grid(row=1, column=0, sticky="w")
        self.entry_output = tk.Entry(frame_paths, textvariable=self.output_path, width=55)
        self.entry_output.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_paths, text="瀏覽...", command=self.browse_output).grid(row=1, column=2, padx=5)

        # 3. 檔案分割設定 (本次更新重點)
        frame_split = tk.LabelFrame(self.root, text="3. 檔案分割設定", padx=10, pady=5)
        frame_split.pack(fill="x", padx=10, pady=5)
        
        # 使用 Frame 來排列 Checkbox 和輸入框
        split_inner_frame = tk.Frame(frame_split)
        split_inner_frame.pack(anchor="w")
        
        tk.Checkbutton(split_inner_frame, text="啟用長檔案自動分割", variable=self.split_files_var, command=self.toggle_split_input).pack(side="left")
        
        tk.Label(split_inner_frame, text="   ( 每").pack(side="left")
        self.entry_split_hours = tk.Entry(split_inner_frame, textvariable=self.split_hours, width=3, state="disabled")
        self.entry_split_hours.pack(side="left", padx=2)
        tk.Label(split_inner_frame, text="小時 切分一個新檔案 )").pack(side="left")

        # 4. 格式設定
        frame_format = tk.LabelFrame(self.root, text="4. 內容格式設定", padx=10, pady=5)
        frame_format.pack(fill="x", padx=10, pady=5)
        
        tk.Checkbutton(frame_format, text="顯示時間軸 (格式: [00:00:00~00:01:00])", variable=self.keep_timestamp_var).grid(row=0, column=0, sticky="w", padx=5, columnspan=2)
        
        tk.Checkbutton(frame_format, text="啟用固定時間合併", variable=self.merge_text_var, command=self.toggle_merge_input).grid(row=1, column=0, sticky="w", padx=5)
        
        frame_merge_settings = tk.Frame(frame_format)
        frame_merge_settings.grid(row=1, column=1, sticky="w")
        tk.Label(frame_merge_settings, text="每").pack(side="left")
        self.entry_seconds = tk.Entry(frame_merge_settings, textvariable=self.merge_seconds, width=5, state="disabled")
        self.entry_seconds.pack(side="left", padx=2)
        tk.Label(frame_merge_settings, text="秒 合併一段文字").pack(side="left")

        # 5. 執行
        frame_action = tk.Frame(self.root, padx=10, pady=5)
        frame_action.pack(fill="both", expand=True, padx=10)
        self.btn_run = tk.Button(frame_action, text="開始轉換", command=self.start_conversion, bg="#28a745", fg="white", font=("Arial", 12, "bold"), height=2)
        self.btn_run.pack(fill="x", pady=5)
        
        self.log_text = tk.Text(frame_action, height=8, state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def update_ui_state(self):
        self.source_path.set("")

    def toggle_merge_input(self):
        state = "normal" if self.merge_text_var.get() else "disabled"
        self.entry_seconds.config(state=state)
        
    def toggle_split_input(self):
        state = "normal" if self.split_files_var.get() else "disabled"
        self.entry_split_hours.config(state=state)

    def browse_source(self):
        if self.mode_var.get() == "file":
            path = filedialog.askopenfilename(filetypes=[("SRT Subtitles", "*.srt")])
        else:
            path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
            if not self.output_path.get():
                self.output_path.set(os.path.dirname(path) if self.mode_var.get() == "file" else path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path: self.output_path.set(path)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update()

    def parse_time_to_seconds(self, time_str):
        try:
            parts = time_str.replace(',', ':').split(':')
            h, m, s, ms = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            return h * 3600 + m * 60 + s + ms / 1000.0
        except:
            return 0.0

    def format_seconds_to_hms(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))

    def process_single_file(self, file_path, output_dir):
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        self.log(f"處理中: {filename}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
        except:
            try:
                with open(file_path, 'r', encoding='cp950') as f: content = f.read()
            except:
                self.log(f"錯誤: 無法讀取 {filename}")
                return

        srt_items = []
        blocks = re.split(r'\n\n+', content.strip())
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                time_line_idx = -1
                for idx, line in enumerate(lines):
                    if "-->" in line:
                        time_line_idx = idx
                        break
                
                if time_line_idx != -1 and len(lines) > time_line_idx + 1:
                    time_part = lines[time_line_idx].split("-->")
                    start_str = time_part[0].strip()
                    end_str = time_part[1].strip()
                    text_lines = lines[time_line_idx+1:]
                    text_content = " ".join(text_lines)
                    
                    start_sec = self.parse_time_to_seconds(start_str)
                    end_sec = self.parse_time_to_seconds(end_str)
                    srt_items.append({'start': start_sec, 'end': end_sec, 'text': text_content})

        if not srt_items:
            self.log(f"警告: {filename} 解析不到內容")
            return

        # === 處理分割邏輯 ===
        file_chunks = []
        
        if self.split_files_var.get():
            hours_val = self.split_hours.get()
            split_threshold = hours_val * 3600 # 將輸入的小時轉換為秒
            
            for item in srt_items:
                target_idx = int(item['start'] // split_threshold)
                while len(file_chunks) <= target_idx:
                    file_chunks.append([])
                file_chunks[target_idx].append(item)
        else:
            file_chunks.append(srt_items)

        # 寫入檔案
        for idx, items in enumerate(file_chunks):
            if not items: continue
            
            save_name = f"{base_name}.txt"
            if self.split_files_var.get() and len(file_chunks) > 1:
                # 檔名格式： 原檔名-1.txt, 原檔名-2.txt
                save_name = f"{base_name}-{idx+1}.txt"
            
            output_content = self.format_content(items)
            save_full_path = os.path.join(output_dir, save_name)
            
            with open(save_full_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            self.log(f"-> 產生: {save_name}")

    def format_content(self, items):
        lines = []
        keep_time = self.keep_timestamp_var.get()
        do_merge = self.merge_text_var.get()
        merge_interval = self.merge_seconds.get()
        
        if do_merge and merge_interval > 0:
            grouped_data = {}
            for item in items:
                group_idx = int(item['start'] // merge_interval)
                if group_idx not in grouped_data: grouped_data[group_idx] = []
                grouped_data[group_idx].append(item['text'])
            
            sorted_indices = sorted(grouped_data.keys())
            for g_idx in sorted_indices:
                texts = grouped_data[g_idx]
                merged_text = " ".join(texts)
                
                if keep_time:
                    seg_start = g_idx * merge_interval
                    seg_end = seg_start + merge_interval
                    t_start = self.format_seconds_to_hms(seg_start)
                    t_end = self.format_seconds_to_hms(seg_end)
                    lines.append(f"[{t_start}~{t_end}]\n{merged_text}\n")
                else:
                    lines.append(f"{merged_text}\n")
        else:
            for item in items:
                text = item['text']
                if keep_time:
                    t_start = self.format_seconds_to_hms(item['start'])
                    t_end = self.format_seconds_to_hms(item['end'])
                    lines.append(f"[{t_start}~{t_end}] {text}")
                else:
                    lines.append(text)
                
        return "\n".join(lines)

    def start_conversion(self):
        source = self.source_path.get()
        output = self.output_path.get()
        
        if not source or not os.path.exists(source):
            messagebox.showerror("錯誤", "來源路徑無效")
            return
        if not output:
            messagebox.showerror("錯誤", "請設定存檔位置")
            return
            
        # 參數驗證
        if self.merge_text_var.get() and self.merge_seconds.get() <= 0:
            messagebox.showerror("錯誤", "合併秒數必須 > 0")
            return
        
        if self.split_files_var.get() and self.split_hours.get() <= 0:
            messagebox.showerror("錯誤", "分割時數必須 > 0")
            return

        if not os.path.exists(output): os.makedirs(output)
        
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        
        files = []
        if self.mode_var.get() == "file":
            if source.lower().endswith(".srt"): files.append(source)
        else:
            for root, dirs, filenames in os.walk(source):
                for f in filenames:
                    if f.lower().endswith(".srt"): files.append(os.path.join(root, f))
        
        if not files:
            self.log("找不到 SRT 檔案")
            return
            
        for f in files:
            self.process_single_file(f, output)
            
        messagebox.showinfo("完成", "轉換作業結束")

if __name__ == "__main__":
    root = tk.Tk()
    app = SRTConverterApp(root)
    root.mainloop()