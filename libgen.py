# coding=utf-8
import os
from alimentador import Alimentador


if __name__ == '__main__':
    ali = Alimentador()
    res = ali.proceed()
    if res == -1:
        print('Libgen gave a non-valid page')
        print('Exited')
        os.system("pause")
