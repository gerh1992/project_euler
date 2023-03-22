from collections import (
    Counter,
    deque,
    Hashable
)
import functools
import math

import multiprocessing as mp


def worker(fn, end):
    """End is used to send the result back to the worker so it can later be used"""
    result = fn()
    end.send(result)


def run_cpu_tasks_in_parallel(tasks):
    running_tasks = []
    pipe_list = []

    for task in tasks:
        recv_end, send_end = mp.Pipe(False)
        p = mp.Process(target=worker, args=(task, send_end))
        running_tasks.append(p)
        pipe_list.append(recv_end)
        p.start()

    for task in running_tasks:
        task.join()

    result_list = [x.recv() for x in pipe_list]
    return result_list


def is_palindrome_number(n):
    str_n = str(n)
    return is_palindrome(str_n)


def is_palindrome(string):
    len_str = len(string)
    for i in range(len_str // 2):
        if string[i] != string[len_str - i - 1]:
            return False
    return True


def p(n):
    tmp = n
    cmp = 0
    while True:
        cmp += tmp % 10
        tmp = tmp // 10
        if tmp == 0:
            break
        cmp *= 10

    return cmp == n


def lowest_common_multiple(a, b):
    """
    La idea es calcular los factores primos que componen ambos numeros.
    Despues multiplicar cada factor la cantidad de veces que sea mas grande entre los dos nums.
    Por ej 30 y 45:
         30 => 2, 3, 5
         45 => 3, 3, 5
            Entonces: 2 * ( 3 * 3 ) * 5 ==> 90
    """
    factores_a = get_factors(a)
    factores_b = get_factors(b)

    keys = set(factores_a + factores_b)
    c_a = Counter(factores_a)
    c_b = Counter(factores_b)

    total = 1

    for k in keys:
        power = max(c_a[k], c_b[k])
        total *= k ** power

    return total


def get_factors(n):
    """
    Returns a list with all factors of a number
    """
    factor = 2
    factores = []
    while n > 1:
        while n % factor != 0:
            if factor == 2:
                factor += 1
            else:
                factor += 2
        factores.append(factor)
        n /= factor
    return factores


def from_list_to_num(lista):
    """
    Input a list or tuple of digits
    Output a number
    """
    total = 0
    for digit in lista:
        total += digit
        total *= 10
    return total // 10


def is_prime_2(n, primes_so_far):
    stop = int(math.ceil(math.sqrt(n)))
    for prime in primes_so_far:
        if n % prime == 0:
            return False
        elif prime >= stop:
            break
    primes_so_far.append(n)
    return True


def get_total_factors(n):
    total = 2
    if math.sqrt(n) == int(math.sqrt(n)):
        total += 1
    for i in range(2, int(math.ceil(math.sqrt(n)))):
        if n % i == 0:
            total += 2
    return total


def sum_factors(n, already_computed):
    if n in already_computed:
        return already_computed[n]
    total = 1
    if math.sqrt(n) == int(math.sqrt(n)):
        total += int(math.sqrt(n))
    for i in range(2, int(math.ceil(math.sqrt(n)))):
        if n % i == 0:
            total += i + n // i
    already_computed[n] = total
    return total


def find_cyclic_length(n):
    """
    The idea is that if a prime is a `long prime`, defined by:
    In number theory long prime in base b is an odd prime number p such that the Fermat quotient:
    fermat_quotient = (b ^ p-1 - 1) / p
    Outputs a cyclic number and the no of digits of the cyclic number will be equal to the p - 1
    """
    r = 1
    for i in range(1, n):
        r = (10 * r) % n
    rr = r
    period = 0
    while True:
        r = (10 * r) % n
        period += 1
        if r == rr:
            break
    return period


def is_fermat(n):
    pass


def get_digits(num):
    """
    Pass a number and returns its digits in a list format
    """
    digits = list()
    while num > 0:
        digit = num % 10
        num //= 10
        digits.append(digit)

    digits.reverse()
    return digits


def check_all_digits(result, i, j):
    res = str(result)
    str_i = str(i)
    str_j = str(j)

    if "0" in str_i or "0" in str_j or "0" in res:
        return False
    if len(res) + len(str_i) + len(str_j) == 9:
        ss = set()
        for x in res: ss.add(x)
        for x in str_i: ss.add(x)
        for x in str_j: ss.add(x)
        if len(ss) == 9:
            return True
    return False


def get_loop_range(no_of_digits):
    upper_bound = 9

    for x in range(1, no_of_digits):
        upper_bound *= 10
        upper_bound += 9

    upper_bound = (upper_bound // 6) + 1
    return range(1, upper_bound)


def get_digits_dict(number):
    """
    Gets a number and spits all its digits in a dict format, for ex 1123
    returns {1: 2, 2: 1, 3: 1}
    """
    result = dict()
    digits = get_digits(number)
    for digit in digits:
        if digit not in result:
            result[digit] = 1
        else:
            result[digit] = result[digit] + 1
    return result


def check_if_all_digits_are_the_same(number):
    digits_dict = get_digits_dict(number)
    for i in range(2, 7):
        if get_digits_dict(number * i) != digits_dict:
            return False
    return True


def _get_divisors(num):
    factors = list()
    for i in range(1, int(math.ceil(math.sqrt(num)))):
        if num % i == 0:
            factors.append(i)
            factors.append(num / i)
    return factors


def get_highest_common_factor(a, b):
    factors_a = _get_divisors(a)
    factors_b = _get_divisors(b)

    for factor in reversed(sorted(factors_a)):
        if factor in factors_b:
            return factor    


def get_lowest_common_term(num, den):
    factor = get_highest_common_factor(num, den)
    return (num / factor, den / factor)


def generate_rotation_nums(digits):
    """
    Receives a list of digits and genertate all possible ROTATIONS of the number,
    for ex for number 179, the rotations are: 179, 791 and 917
    """
    rotations = len(digits)
    combinations = list()
    for _ in range(rotations):
        digits.append(digits.pop(0))
        combinations.append(from_list_to_num(digits))
    
    return combinations


class memoized(object):
    '''
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
    

@memoized
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.ceil(math.sqrt(n))) + 1, 2):
        if n % i == 0:
            return False
    return True