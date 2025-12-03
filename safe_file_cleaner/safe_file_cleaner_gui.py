import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

def run_cleaner():
    folder_path = folder_path_var.get().strip()
    exts_input = ext_var.get().strip()

    if not folder_path:
        messagebox.showwarning("警告", "フォルダを選択してください。")
        return

    if not exts_input:
        messagebox.showwarning("警告", "削除する拡張子を入力してください。")
        return

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        messagebox.showerror("エラー", "正しいフォルダを選択してください。")
        return

    exts = [e.strip() for e in exts_input.split(",")]

    target_files = [f for f in folder.iterdir() if f.is_file() and f.suffix in exts]

    if not target_files:
        messagebox.showinfo("結果", "削除対象のファイルは見つかりませんでした。")
        log_message("✅ 削除対象ファイルなし")
        return

    file_list = "\n".join([f.name for f in target_files])
    confirm = messagebox.askyesno(
        "最終確認",
        f"以下のファイルを削除しますか？\n\n{file_list}"
    )

    if not confirm:
        log_message("✅ 削除はキャンセルされました")
        return

    deleted_count = 0
    for f in target_files:
        try:
            f.unlink()
            log_message(f"🗑 削除しました：{f.name}")
            deleted_count += 1
        except Exception as e:
            log_message(f"⚠ 削除失敗：{f.name} → {e}")

    messagebox.showinfo("完了", f"{deleted_count} 件のファイルを削除しました。")
    log_message(f"✅ 完了：{deleted_count} 件削除")

# =========================
# GUI 本体
# =========================

root = tk.Tk()
root.title("Safe File Cleaner（GUI版）")
root.geometry("600x500")

# フォルダ選択
frame_folder = tk.Frame(root)
frame_folder.pack(pady=10)

tk.Label(frame_folder, text="削除対象フォルダ：").pack(side=tk.LEFT)
folder_path_var = tk.StringVar()
tk.Entry(frame_folder, textvariable=folder_path_var, width=50).pack(side=tk.LEFT, padx=5)
tk.Button(frame_folder, text="参照", command=select_folder).pack(side=tk.LEFT)

# 拡張子入力
frame_ext = tk.Frame(root)
frame_ext.pack(pady=10)

tk.Label(frame_ext, text="削除する拡張子（例：.txt,.log,.tmp）：").pack(side=tk.LEFT)
ext_var = tk.StringVar()
tk.Entry(frame_ext, textvariable=ext_var, width=25).pack(side=tk.LEFT, padx=5)

# 実行ボタン
tk.Button(root, text="削除実行", command=run_cleaner, bg="red", fg="white", height=2, width=20).pack(pady=15)

# ログ表示
tk.Label(root, text="実行ログ：").pack()
log_box = scrolledtext.ScrolledText(root, width=70, height=15)
log_box.pack(pady=5)

root.mainloop()
