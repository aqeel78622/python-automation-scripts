"""
File Organizer - Automatically sorts files in a folder by type
Author: Your Name
Description: Organizes messy folders by moving files into categorized subfolders
Usage: python file_organizer.py --folder "C:/Users/You/Downloads"
"""

import os
import shutil
import argparse
from datetime import datetime

# File categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
    "Executables": [".exe", ".apk", ".dmg", ".deb", ".msi"],
}


def get_category(extension):
    """Return the category name for a given file extension."""
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_folder(folder_path, dry_run=False):
    """
    Organize all files in the given folder into subfolders by type.
    
    Args:
        folder_path: Path to the folder to organize
        dry_run: If True, only show what would happen without moving files
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' does not exist.")
        return

    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        print("📂 No files found in the folder.")
        return

    print(f"\n{'[DRY RUN] ' if dry_run else ''}📁 Organizing: {folder_path}")
    print(f"📄 Found {len(files)} file(s)\n")

    moved = {}

    for filename in files:
        _, ext = os.path.splitext(filename)
        category = get_category(ext)

        dest_folder = os.path.join(folder_path, category)
        src = os.path.join(folder_path, filename)
        dst = os.path.join(dest_folder, filename)

        if dry_run:
            print(f"  Would move: {filename} → {category}/")
        else:
            os.makedirs(dest_folder, exist_ok=True)
            # Avoid overwriting files with same name
            if os.path.exists(dst):
                name, extension = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dst = os.path.join(dest_folder, f"{name}_{timestamp}{extension}")
            shutil.move(src, dst)
            print(f"  ✅ Moved: {filename} → {category}/")

        moved[category] = moved.get(category, 0) + 1

    print(f"\n{'📊 Summary (Dry Run):' if dry_run else '📊 Summary:'}")
    for category, count in sorted(moved.items()):
        print(f"  {category}: {count} file(s)")
    print(f"\n{'✅ Done! All files organized.' if not dry_run else '✅ Dry run complete. Run without --dry-run to apply.'}")


def main():
    parser = argparse.ArgumentParser(
        description="📁 File Organizer - Sort your files automatically by type"
    )
    parser.add_argument(
        "--folder",
        type=str,
        default=os.path.expanduser("~/Downloads"),
        help="Path to the folder you want to organize (default: Downloads)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually moving files"
    )

    args = parser.parse_args()
    organize_folder(args.folder, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
