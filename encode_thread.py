from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
import base64

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
            for file in files:
                suffix = file.suffix[1:] if file.suffix else "unknown"
                out_name = f"{suffix}-{file.stem}.txt"
                out_path = self.output_folder / out_name

                try:
                    with open(file, 'rb') as f:
                        data = f.read()
                    if not data:
                        raise Exception("File trống")
                    encoded = base64.b64encode(data).decode('utf-8')
                    with open(out_path, 'w') as out:
                        out.write(encoded)
                    successes.append(file.name)
                except Exception as e:
                    errors.append(f"{file.name}: {e}")

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
            self.finished.emit(f"❌ Mã hóa lỗi: {str(e)}")
