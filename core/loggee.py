from datetime import datetime

from core.config import ROOT


LOG_PATH = ROOT / "Log"


class Loggee:
    def __init__(self, text):
        LOG_PATH.mkdir(exist_ok=True)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        logfile = LOG_PATH / f"log.{now.strftime('%Y-%m-%d')}.log"

        line = f"[{timestamp}]> {text}"
        with logfile.open("a", encoding="utf8") as log:
            print(line, file=log)
        print(line)
