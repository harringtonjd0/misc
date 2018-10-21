''' Header file to define color output options for scripts using ANSI escape sequences.'''
''' TODO: Maybe move functions into class'''

class colors:
    '''Defines ANSI escape sequences as colors
    Idea taken from https://stackoverflow.com/questions/287871/print-in-terminal-with-colors'''
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BOLDBLUE = BOLD + BLUE
    BOLDRED = BOLD + RED
    BOLDYELLOW = BOLD + YELLOW
    BOLDGREEN = BOLD + GREEN

def list_colors(self):
        '''Demo colored output'''
        c = colors() 
        options = [attr for attr in dir(c) if not attr.startswith('__')]
        for opt in options:
            if opt != 'END':
                print(eval("c.{}".format(opt)) + str(opt), end=c.END+'\n')

def cprint(string, *args, end='\n'):
    ''' Print string with given color(s)'''
    for color in args:
        assert(color.isalpha())
    c = colors()
    color_expr = '+'.join(["c.{}".format(color) for color in args])
    print(eval(color_expr) + string, end = c.END + end)


