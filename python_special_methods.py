"""
Python Special Methods (Dunder Methods) Cheat Sheet

Common Use Cases:
- __str__, __repr__: String representations
- __eq__, __lt__: Comparison operations  
- __len__, __getitem__: Container behavior
- __enter__, __exit__: Context managers
- __add__, __mul__: Mathematical operations
- __call__: Function-like objects

Remember:
- Return NotImplemented for unsupported operations
- Implement comparison methods as a set
- Keep __str__ readable and __repr__ unambiguous 
- Special methods are called implicitly by Python
"""

# INITIALIZATION AND CONSTRUCTION
class SpecialMethods:
    def __new__(cls, *args, **kwargs):  # Object creation
        return super().__new__(cls)
    
    def __init__(self):  # Initialization
        pass
    
    def __del__(self):  # Cleanup/destructor
        pass


# STRING REPRESENTATION
    def __str__(self):  # str(), print()
        return "Human readable"
    
    def __repr__(self):  # repr(), debugger display
        return "Unambiguous representation"
    
    def __format__(self, format_spec):  # format(), f-strings
        return f"Formatted {format_spec}"


# COMPARISON METHODS
    def __eq__(self, other): return True  # ==
    def __ne__(self, other): return False  # !=
    def __lt__(self, other): return False  # <
    def __le__(self, other): return False  # <=
    def __gt__(self, other): return False  # >
    def __ge__(self, other): return False  # >=
    def __hash__(self): return 0  # hash()


# NUMERIC OPERATIONS
    def __add__(self, other): return self  # +
    def __sub__(self, other): return self  # -
    def __mul__(self, other): return self  # *
    def __truediv__(self, other): return self  # /
    def __floordiv__(self, other): return self  # //
    def __mod__(self, other): return self  # %
    def __pow__(self, other): return self  # **
    
    # Reverse operations (when left operand doesn't support operation)
    def __radd__(self, other): return self  # other + self
    def __rsub__(self, other): return self  # other - self
    def __rmul__(self, other): return self  # other * self
    
    # In-place operations
    def __iadd__(self, other): return self  # +=
    def __isub__(self, other): return self  # -=
    def __imul__(self, other): return self  # *=


# CONTAINER METHODS
    def __len__(self): return 0  # len()
    def __getitem__(self, key): pass  # self[key]
    def __setitem__(self, key, value): pass  # self[key] = value
    def __delitem__(self, key): pass  # del self[key]
    def __iter__(self): return self  # iter()
    def __next__(self): raise StopIteration  # next()
    def __contains__(self, item): return False  # in


# ATTRIBUTE ACCESS
    def __getattr__(self, name): pass  # Fallback for missing attributes
    def __setattr__(self, name, value): pass  # Setting attributes
    def __delattr__(self, name): pass  # Deleting attributes
    def __getattribute__(self, name): pass  # All attribute access
    def __dir__(self): return []  # dir()


# CONTEXT MANAGEMENT
    def __enter__(self): return self  # with statement entry
    def __exit__(self, exc_type, exc_val, exc_tb): pass  # with statement exit


# CALLABLE OBJECTS
    def __call__(self, *args, **kwargs): pass  # Calling instances like functions


# TYPE CONVERSION
    def __int__(self): return 0  # int()
    def __float__(self): return 0.0  # float()
    def __complex__(self): return 0j  # complex()
    def __bool__(self): return False  # bool(), if statement
    def __bytes__(self): return b""  # bytes()


# COPY BEHAVIOR
    def __copy__(self): return type(self)()  # copy.copy()
    def __deepcopy__(self, memo): return type(self)()  # copy.deepcopy()


# PICKLE SUPPORT
    def __getstate__(self): return {}  # Pickling
    def __setstate__(self, state): pass  # Unpickling 