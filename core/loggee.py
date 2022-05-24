import datetime
import os
import core.globals

Log_path = "Log"

class Loggee():
    def __init__(self, text):
        def DO_IT():
            now = str(datetime.datetime.now())
            loc = now.rfind('.')
            nnow = now[:loc]
            core.globals.now()
            with open(F'Log/log.{core.globals.timee}.log', 'a', encoding='utf8') as log:
                print(F'[{nnow}]> {text}', file=log)
            print(F'[{nnow}]> {text}')

        try:
            os.makedirs(Log_path)
            DO_IT()
        except FileExistsError:
            DO_IT()