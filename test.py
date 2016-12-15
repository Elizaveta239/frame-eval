import frame

frame.main()



def bar():
    return "hey"


def foo():
    bar()
    a = 1
    b = 2
    return a + b


foo()

