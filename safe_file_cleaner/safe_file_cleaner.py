from pathlib import Path

def main():
    print("=== Safe File Cleaner ===")
    print("指定したフォルダ内のファイルを拡張子で安全に削除します。\n")

    # 対象フォルダ
    folder_path = input("削除対象のフォルダパスを入力してください：").strip()
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("❌ フォルダが存在しません。正しいパスを入力してください。")
        return

    # 削除する拡張子（複数OK）
    exts_input = input("削除したい拡張子をカンマ区切りで入力（例：.txt,.log,.tmp）：")
    exts = [e.strip() for e in exts_input.split(",")]

    # 対象ファイルの取得
    target_files = [f for f in folder.iterdir() if f.is_file() and f.suffix in exts]

    if not target_files:
        print("✅ 削除対象のファイルは見つかりませんでした。")
        return

    print("\n以下のファイルが削除対象です：")
    for f in target_files:
        print(f" - {f.name}")

    confirm = input("\n本当に削除しますか？（yes/no）：").strip().lower()
    if confirm != "yes":
        print("✅ 削除はキャンセルされました。")
        return

    # 削除実行
    deleted_count = 0
    for f in target_files:
        try:
            f.unlink()
            print(f"🗑 削除しました：{f.name}")
            deleted_count += 1
        except Exception as e:
            print(f"⚠ 削除失敗：{f.name} → {e}")

    print(f"\n✅ 完了：{deleted_count} 件のファイルを削除しました。")

if __name__ == "__main__":
    main()

