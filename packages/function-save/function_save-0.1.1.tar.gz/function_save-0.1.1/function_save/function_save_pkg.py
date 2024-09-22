class FunctionSaver:
    def __init__(self) -> None:
        self.__save_output = {} # function : return value
        self.__f_counter = {} # function : number of output
        pass
    
    def add(self, func, return_value, *args):
        if self.__save_output.get(func):
            self.__save_output[func].append([return_value, *args])
        else:
            self.__save_output[func] = [[return_value, *args]]
        if self.__f_counter.get(func):
            self.__f_counter[func] += 1
        else:
            self.__f_counter[func] = 1
        pass
    
    def counter(self):
        print('Function Counts: ')
        for key, value in self.__f_counter.items():
            print(f'{key} : {value}')
        print()
    
    def __str__(self):
        data = self.__save_output
        for key, value in data.items():
            print(key)
            for ans in value:
                print(' - ',end='')
                print(f'{ans[0]} Parameter {ans[1:]}')
            print()
        return ''

fr = FunctionSaver()

def function_results():
    print(fr)

def function_counter():
    fr.counter()

def save(func):
    recursive_depth = 0
    def wrapper(*args, **kwargs):
        nonlocal recursive_depth
        recursive_depth += 1
        result = func(*args, **kwargs)
        recursive_depth -= 1
        if recursive_depth == 0:
            fr.add(func.__name__, result, *args)
        return result
    return wrapper