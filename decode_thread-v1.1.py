from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import base64
import binascii
import re

class DecodeThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, input_folder, output_folder):
        super().__init__()
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def run(self):
        try:
            self.output_folder.mkdir(exist_ok=True)
            txt_files = list(self.input_folder.glob("*.txt"))
            if not txt_files:
                self.finished.emit("📁 INPUT không có file .txt!")
                return

            errors = []
            successes = []

            # Gom nhóm các file theo tên gốc (không tính .partN)
            file_groups = {}
            part_pattern = re.compile(r"^(.*?)-(.*?)(?:\.part(\d+))?$")
            for file in txt_files:
                m = part_pattern.match(file.stem)
                if not m:
                    continue
                suffix, stem, part = m.groups()
                key = f"{suffix}-{stem}"
                if key not in file_groups:
                    file_groups[key] = []
                file_groups[key].append((int(part) if part else 0, file))

            for key, parts in file_groups.items():
                # Sắp xếp theo thứ tự part
                parts.sort()
                suffix, stem = key.split("-", 1)
                out_name = stem if '.' in stem else f"{stem}.{suffix}"
                out_path = self.output_folder / out_name
                try:
                    b64_all = ""
                    for _, file in parts:
                        with open(file, "r") as f:
                            b64_all += f.read().strip()
                    decoded_data = base64.b64decode(b64_all, validate=True)
                    with open(out_path, "wb") as out:
                        out.write(decoded_data)
                    if len(parts) > 1:
                        successes.append(f"{', '.join([f.name for _, f in parts])}")
                    else:
                        successes.append(parts[0][1].name)
                except (binascii.Error, ValueError):
                    errors.append(f"{', '.join([f.name for _, f in parts])}: Không phải base64 hợp lệ")

            msg = ""
            if successes:
                msg += "✅ Đã biên dịch thành công:\n"
                for i, f in enumerate(successes, 1):
                    msg += f"{i}. {f}\n"
            if errors:
                msg += "❌ Một số file lỗi:\n"
                for i, e in enumerate(errors, 1):
                    msg += f"{i}. {e}\n"
            self.finished.emit(msg)
        except Exception as e:
            self.finished.emit(f"❌ Biên dịch lỗi: {str(e)}")
