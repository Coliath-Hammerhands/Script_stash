import subprocess
import argparse
import logging
from pathlib import Path
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
import json

# 1. Setup Rich Logging
logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(show_path=False, rich_tracebacks=True)])
log = logging.getLogger("rich")

DB_FILE = "converted_history.json"


def load_history():
    """Load the list of already converted files."""
    if Path(DB_FILE).exists():
        with open(DB_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_history(history):
    """Save the list of already converted files."""
    with open(DB_FILE, "w") as f:
        json.dump(list(history), f, indent=4)


def get_duration(file_path):
    """Get video duration using ffprobe."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout) if result.stdout.strip() else 0


def main():
    parser = argparse.ArgumentParser(description="x265 Encoder with Rich Progress")
    parser.add_argument("folder", type=str, nargs="?", default=".", help="Root folder to scan")
    args = parser.parse_args()

    root_dir = Path(args.folder).resolve()
    extensions = (".mp4", ".mkv", ".mov", ".avi", ".ts")
    files = [f for f in root_dir.rglob("*") if f.suffix.lower() in extensions and "_temp" not in f.name]

    if not files:
        log.error(f"No files found in {root_dir}")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),  # 'None' allows it to expand
        TaskProgressColumn(),
        TimeRemainingColumn(),
        expand=True,
    ) as progress:
        overall_task = progress.add_task("[bold green]Total Progress", total=len(files))

        for file_path in files:
            relative_path = str(file_path.relative_to(root_dir))
            duration = get_duration(file_path)
            temp_output = file_path.with_name(f"{file_path.stem}_temp_x265.mkv")

            file_task = progress.add_task(f"[cyan]Encoding:[/] {file_path.name}", total=100)

            # FFmpeg Command using CRF 22 for real compression
            command = [
                "ffmpeg",
                "-i",
                str(file_path),
                "-map",
                "0",
                "-c:v",
                "libx265",
                "-crf",
                "20",
                "-preset",
                "medium",
                "-c:a",
                "copy",
                "-c:s",
                "copy",
                "-progress",
                "pipe:1",
                "-nostats",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                str(temp_output),
            ]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in process.stdout:
                if "out_time_us=" in line:
                    try:
                        us = int(line.split("=")[1])
                        percentage = (us / 1_000_000 / duration) * 100
                        progress.update(file_task, completed=min(percentage, 100))
                    except (ValueError, ZeroDivisionError, IndexError):
                        pass

            process.wait()
            progress.remove_task(file_task)  # Remove the per-file bar when done

            if process.returncode == 0 and temp_output.exists():
                orig_size = file_path.stat().st_size
                new_size = temp_output.stat().st_size

                # Calculate compression ratio
                # If ratio is 40%, the new file is 40% of the original (60% saved)
                ratio = (new_size / orig_size) * 100
                savings = 100 - ratio

                if new_size < orig_size:
                    file_path.unlink()
                    temp_output.rename(file_path)
                    log.info(f"[bold green]✓ [white]{file_path.name} ([yellow] {ratio:.1f}% of original | [bold cyan]-{savings:.1f}% saved)")
                else:
                    temp_output.unlink()
                    log.warning(f"[bold yellow]× Skipped [white]{file_path.name} (Encode was larger)")
                history = load_history()
                history.add(relative_path)
                save_history(history)
            else:
                log.error(f"[bold red]!! Failed to encode [white]{file_path.name}")

            progress.advance(overall_task)
