

def make_fun(x):
    y = 5
    def yo():
        #y += 1
        return x+5+y
    return yo

f = make_fun(4)

print(f())





