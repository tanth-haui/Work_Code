from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import base64
import math

class EncodeThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, input_folder, output_folder):
        super().__init__()
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def run(self):
        try:
            self.output_folder.mkdir(exist_ok=True)
            files = [f for f in self.input_folder.iterdir() if f.is_file()]
            if not files:
                self.finished.emit("📁 INPUT trống hoặc không hợp lệ!")
                return

            errors = []
            successes = []
            MAX_SIZE = 35 * 1024 * 1024  # 35MB

            for file in files:
                suffix = file.suffix[1:] if file.suffix else "unknown"
                stem = file.stem

                try:
                    with open(file, 'rb') as f:
                        data = f.read()
                    if not data:
                        raise Exception("File trống")

                    # Mã hóa base64 toàn bộ trước (vì base64 tăng kích thước ~1.34 lần)
                    encoded = base64.b64encode(data).decode('utf-8')
                    encoded_bytes = encoded.encode('utf-8')
                    total_size = len(encoded_bytes)
                    if total_size > MAX_SIZE:
                        # Cắt thành nhiều phần
                        part_count = math.ceil(total_size / MAX_SIZE)
                        for idx in range(part_count):
                            start = idx * MAX_SIZE
                            end = start + MAX_SIZE
                            part_data = encoded_bytes[start:end]
                            part_str = part_data.decode('utf-8')
                            out_name = f"{suffix}-{stem}.part{idx+1}.txt"
                            out_path = self.output_folder / out_name
                            with open(out_path, 'w') as out:
                                out.write(part_str)
                        successes.append(f"{file.name} (đã tách thành {part_count} phần)")
                    else:
                        out_name = f"{suffix}-{stem}.txt"
                        out_path = self.output_folder / out_name
                        with open(out_path, 'w') as out:
                            out.write(encoded)
                        successes.append(file.name)
                except Exception as e:
                    errors.append(f"{file.name}: {e}")

            msg = ""
            if successes:
                msg += "✅ Đã mã hóa thành công:\n"
                for i, f in enumerate(successes, 1):
                    msg += f"{i}. {f}\n"
            if errors:
                msg += "❌ Một số file lỗi:\n"
                for i, e in enumerate(errors, 1):
                    msg += f"{i}. {e}\n"
            self.finished.emit(msg)
        except Exception as e:
            self.finished.emit(f"❌ Mã hóa lỗi: {str(e)}")
