#----------------
# Equality validation
#----------------

def gt_zero(*args):
    '''
    Check that passed in arguments are strictly greater than zero
    '''
    if len(args) != 0:
        for arg in args:
            if arg <= 0: raise ValueError(f'Value {arg} must be strictly greater than zero!') from None           

#----------------
# Type Validation
#----------------

def type_check(dtype, *args):
    '''
    Check the type of passed in values
    '''
    if len(args) != 0:
        for arg in args:
            if type(arg) != dtype: raise TypeError(f'Value {arg} must be of type {dtype}!') from None
