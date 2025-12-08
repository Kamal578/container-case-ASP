class Container:
    def __init__(self, initial=0.0):
        self.amount = float(initial)
        self._neighbors = set()

    def getAmount(self) -> float:
        """Return the amount of water currently in this container."""
        return self.amount

    def connectTo(self, other: "Container") -> None:
        """Connect this container to `other` and equalize water in the union."""
        if other is self:
            return  # ignore self-connection
        if other in self._neighbors:
            return  # already directly connected; no work needed
        if other in self._collect_component():
            return  # already connected via some path; avoid cycles

        # undirected edge
        self._neighbors.add(other)
        other._neighbors.add(self)

        # after connection, water equalizes over the whole component
        self._redistribute_in_component()

    def disconnectFrom(self, other: "Container") -> None:
        """Break the connection with `other`."""
        # remove undirected edge if it exists
        if other in self._neighbors:
            self._neighbors.remove(other)
            other._neighbors.remove(self)
        # amounts stay as they are; they were equal in the old component

    def addWater(self, amt: float) -> None:
        """Add (or remove, if negative) water and redistribute; disallow overdraw."""
        component = self._collect_component()
        current_total = sum(c.amount for c in component)
        new_total = current_total + amt
        if new_total < 0:
            # Don't allow removing more water than is present in the component
            # Make a warning or instead of changing anything
            print("Warning: Cannot remove more water than available in component. No changes made.")
            return
        each = new_total / len(component)
        for c in component:
            c.amount = each

    # Internal helpers ----------------------------------------

    def _redistribute_in_component(self) -> None:
        """Equalize water among all containers in the same connected component."""
        component = self._collect_component()
        total = sum(c.amount for c in component)
        if not component:
            return
        each = total / len(component)
        for c in component:
            c.amount = each

    def _collect_component(self):
        """Return all containers reachable from self (including self)."""
        stack = [self]
        visited = {self}
        while stack:
            cur = stack.pop()
            for n in cur._neighbors:
                if n not in visited:
                    visited.add(n)
                    stack.append(n)
        return visited
    
if __name__ == "__main__":
    a = Container(10)
    b = Container(0)
    c = Container(0)

    # Round all to 2 decimal places for easier reading
    a.connectTo(b)
    print(f"a: {round(a.getAmount(), 2)}, b: {round(b.getAmount(), 2)}")  # Both should be 5.0

    b.connectTo(c)
    print(f"a: {round(a.getAmount(), 2)}, b: {round(b.getAmount(), 2)}, c: {round(c.getAmount(), 2)}")  # All should be ~3.33

    a.addWater(6)
    print(f"a: {round(a.getAmount(), 2)}, b: {round(b.getAmount(), 2)}, c: {round(c.getAmount(), 2)}")  # All should be 5.0

    b.disconnectFrom(c)
    a.addWater(3)
    print(f"a: {round(a.getAmount(), 2)}, b: {round(b.getAmount(), 2)}, c: {round(c.getAmount(), 2)}")  # a and b should be 6.5, c should be 5.0
