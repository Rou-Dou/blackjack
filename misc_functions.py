from time import sleep


def typeWriter(string) -> None:
    build_string: str = ''
    for count, char in enumerate(string):
        if count == len(string) - 1:
            build_string += char
            print(build_string, end="")
            print()
            sleep(0.05)
        else:
            build_string += char
            print(build_string, end="")
            print("\r", end="")
            sleep(0.05)
    sleep(0.5)