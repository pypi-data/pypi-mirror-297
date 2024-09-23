# def sum(*args):
#     return sum(args)

def avg(*args):
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

# def max(*args):
#     if len(args) == 0:
#         return None
#     return max(args)

def min(*args):
    if len(args) == 0:
        return None
    return min(args)

def count(*args):
    return len([x for x in args if isinstance(x, (int, float))])

def sqrt(number):
    if number < 0:
        return "cannot calculate the sqrt because its a negative number"
    return number ** 0.5
