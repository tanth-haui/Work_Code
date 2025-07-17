from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import base64
import binascii

class DecodeThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, input_folder, output_folder):
        super().__init__()
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def run(self):
        try:
            self.output_folder.mkdir(exist_ok=True)
            files = list(self.input_folder.glob("*.txt"))
            if not files:
                self.finished.emit("📁 INPUT không có file .txt!")
                return

            errors = []
            successes = []
            for file in files:
                parts = file.stem.split('-', 1)
                if len(parts) < 2:
                    continue
                suffix, name = parts
                out_name = name if '.' in name else f"{name}.{suffix}"
                out_path = self.output_folder / out_name

                with open(file, 'r') as f:
                    b64 = f.read().strip()

                try:
                    decoded_data = base64.b64decode(b64, validate=True)
                    with open(out_path, 'wb') as out:
                        out.write(decoded_data)
                    successes.append(file.name)
                except (binascii.Error, ValueError):
                    errors.append(f"{file.name}: Không phải base64 hợp lệ")

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
