class Scaevola:
    def __ge__(self, other, /):
        """Return other<=self."""
        return type(self)(other) <= self

    def __gt__(self, other, /):
        """Return other<self."""
        return type(self)(other) < self

    def __radd__(self, other, /):
        """Return other+self."""
        return type(self)(other) + self

    def __rand__(self, other, /):
        """Return other&self."""
        return type(self)(other) & self

    def __rdivmod__(self, other, /):
        """Return divmod(other, self)."""
        return divmod(type(self)(other), self)

    def __rfloordiv__(self, other, /):
        """Return other//self."""
        return type(self)(other) // self

    def __rlshift__(self, other, /):
        """Return other<<self."""
        return type(self)(other) << self

    def __rmatmul__(self, other, /):
        """Return other@self."""
        return type(self)(other) @ self

    def __rmod__(self, other, /):
        """Return other%self."""
        return type(self)(other) % self

    def __rmul__(self, other, /):
        """Return other*self."""
        return type(self)(other) * self

    def __ror__(self, other, /):
        """Return other|self."""
        return type(self)(other) | self

    def __rpow__(self, other, /):
        """Return other**self."""
        return type(self)(other) ** self

    def __rrshift__(self, other, /):
        """Return other>>self."""
        return type(self)(other) >> self

    def __rsub__(self, other, /):
        """Return other-self."""
        return type(self)(other) - self

    def __rtruediv__(self, other, /):
        """Return other/self."""
        return type(self)(other) / self

    def __rxor__(self, other, /):
        """Return other^self."""
        return type(self)(other) ^ self
