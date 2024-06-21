from time import sleep

def typeWriter(string) -> None:
    for char in string:
        print(char, end="", flush=True)
        sleep(0.05)
    print(' ', end="\n\n", flush=True)
    sleep(0.75)