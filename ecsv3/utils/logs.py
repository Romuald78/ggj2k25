import inspect
import sys


class ECSv3:

    @staticmethod
    def __display_msg(msg: str, typ: str, caller: int):
        stack = inspect.stack()
        data = stack[2 + caller]
        fun = data[3]
        lin = data[2]
        fil = data[1]
        typ = typ.replace(' ', '')
        if len(typ) < 7:
            n = 7 - len(typ)
            m = n//2
            n -= m
            typ = ' '*m + typ + ' '*n
        typ = typ.upper()
        brdr = '━' * len(typ)
        print(f"┏━━━━━┳{brdr}┓", file=sys.stderr)
        print(f"┃ECSv3┃{typ}┃", file=sys.stderr)
        print(f"┗━┳━━━┻{brdr}┛", file=sys.stderr)
        print(f"  ┣━ in function  : '{fun}'", file=sys.stderr)
        print(f"  ┣━ with message : \"{msg}\"", file=sys.stderr)
        print(f"  ┗━┳━ File \"{fil}\", line {lin}", file=sys.stderr)
        # upper layer call stack
        for i in range(3 + caller, len(stack) - 1):
            lin = stack[i][2]
            fil = stack[i][1]
            print(f"    ┣━ File \"{fil}\", line {lin}", file=sys.stderr)
        # first call
        lin = stack[len(stack)-1][2]
        fil = stack[len(stack)-1][1]
        print(f"    ┗━ File \"{fil}\", line {lin}", file=sys.stderr)

    @staticmethod
    def error(msg: str, error_code: int = 255, caller: int = 0):
        ECSv3.__display_msg(msg, 'error', caller)
        exit(error_code)

    @staticmethod
    def warning(msg: str, caller: int = 0):
        ECSv3.__display_msg(msg, 'warning', caller)

    @staticmethod
    def info(msg: str):
        stack = inspect.stack()
        data = stack[2]
        fun = data[3]
        lin = data[2]
        fil = data[1]
        print(f"┃ECSv3┃ INFO  ┃", file=sys.stderr)
        print(f"  ┣━ in function  : '{fun}'", file=sys.stderr)
        print(f"  ┣━ with message : \"{msg}\"", file=sys.stderr)
        print(f"  ┗━━━ File \"{fil}\", line {lin}", file=sys.stderr)
