import threading

def del_whitespace(x_):
    x_ = str(x_)
    x_ = int(''.join(tuple(x_.split())))
    return x_