import time

def example(seconds):
    print ('Start task')
    for i in range(seconds):
        print (i)
        time.sleep(1)
    print ('task end')
    return i