from time import sleep
from typing import Union, Iterator

def typeWriter(string: Union[str, Iterator], speed: str = 'slow') -> None:
    '''
    prints a given string with type writer effect at either slow (0.05) or fast speed (0.02)
    '''

    options: dict[str, float] = \
    {
        'slow' : 0.05,
        'fast' : 0.02
    }

    for char in string:
        print(char, end="", flush=True)
        sleep(options[speed])
    print(' ', end="\n\n", flush=True)
    sleep(0.75)