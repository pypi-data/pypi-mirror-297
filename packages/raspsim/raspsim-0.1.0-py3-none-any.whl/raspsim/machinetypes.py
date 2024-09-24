def iNty(n: int):
    def wrapper(cls):
        class iNty(cls):
            def __init__(self, value: int | None = None):
                if value is None:
                    value = 0
                
                self.value = value % (2 ** n)

            def __repr__(self):
                negrep = ""
                if self.value >> (n - 1):
                    negrep = ", -" + str(2 ** n - self.value)
                    
                return f"i{n}({self.value}, {self.value:#x}{negrep})"

            def __add__(self, other: cls):
                return i64(self.value + other.value)

            def __sub__(self, other: cls):
                return i64(self.value - other.value)

            def __mul__(self, other: cls):
                return iNty(self.value * other.value)

            def __truediv__(self, other: cls):
                return iNty(self.value // other.value)

            def __floordiv__(self, other: cls):
                return iNty(self.value // other.value)

            def __mod__(self, other: cls):
                return iNty(self.value % other.value)

            def __pow__(self, other: cls):
                return iNty(self.value ** other.value)

            def __lshift__(self, other: cls):
                return iNty(self.value << other.value)

            def __rshift__(self, other: cls):
                return iNty(self.value >> other.value)

            def __and__(self, other: cls):
                return iNty(self.value & other.value)

            def __or__(self, other: cls):
                return iNty(self.value | other.value)

            def __xor__(self, other: cls):
                return iNty(self.value ^ other.value)

            def __neg__(self):
                return iNty(-self.value)

            def __pos__(self):
                return iNty(+self.value)

            def __invert__(self):
                return iNty(~self.value)

            def __eq__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value == other
                return self.value == other.value
            
            def __ne__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value != other
                return self.value != other.value
            
            def __lt__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value <  other
                return self.value < other.value
            
            def __le__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value <= other
                return self.value <= other.value
            
            def __gt__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value >  other
                return self.value > other.value
            
            def __ge__(self, other: int | cls):
                if isinstance(other, int):
                    return self.value >= other
                return self.value >= other.value
            
            def __bool__(self):
                return bool(self.value)

            def __int__(self):
                return self.value
        
        iNty.__name__ = cls.__name__
        return iNty
    return wrapper
    

@iNty(8)
class i8:
    """
    A class representing an 8-bit integer.
    """

@iNty(16)
class i16:
    """
    A class representing a 16-bit integer.
    """

@iNty(32)
class i32:
    """
    A class representing a 32-bit integer.
    """

@iNty(64)
class i64:
    """
    A class representing a 64-bit integer.
    """
