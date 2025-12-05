import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math

# ---------------- Container model -----------------

class Container:
    def __init__(self, initial=0.0):
        self.amount = float(initial)
        self._neighbors = set()

    def getAmount(self) -> float:
        return self.amount

    def connectTo(self, other: "Container") -> None:
        if other is self:
            return
        self._neighbors.add(other)
        other._neighbors.add(self)
        self._redistribute_in_component()

    def disconnectFrom(self, other: "Container") -> None:
        if other in self._neighbors:
            self._neighbors.remove(other)
            other._neighbors.remove(self)

    def addWater(self, amt: float) -> None:
        self.amount += amt
        self._redistribute_in_component()

    def _collect_component(self):
        stack = [self]
        visited = {self}
        while stack:
            cur = stack.pop()
            for n in cur._neighbors:
                if n not in visited:
                    visited.add(n)
                    stack.append(n)
        return visited

    def _redistribute_in_component(self) -> None:
        comp = self._collect_component()
        total = sum(c.amount for c in comp)
        each = total / len(comp)
        for c in comp:
            c.amount = each

# ------------- Visualization helpers --------------

def draw_states(states, connections, names=None):
    """
    states: list of dicts, e.g. {'a': 0, 'b': 0, 'c': 0, 'd': 8}
    connections: list of list-of-tuples, e.g. [('a','b'), ('b','c')]
                 for each state
    names: ordering of containers vertically (top to bottom)
    """
    if names is None:
        names = sorted(states[0].keys())

    num_states = len(states)
    max_amt = max(max(s[n] for n in names) for s in states) or 1.0

    fig, ax = plt.subplots(figsize=(3*num_states, 6))

    col_width = 1.5
    cont_width = 0.8
    cont_height = 1.4
    v_spacing = 0.5

    # Precompute y positions for containers (top to bottom)
    y_positions = {}
    for i, name in enumerate(names[::-1]):  # bottom to top for nicer layout
        y_positions[name] = i * (cont_height + v_spacing)

    for step, state in enumerate(states):
        x0 = step * col_width * 2  # spread steps horizontally

        # Draw containers and water
        for name in names:
            y = y_positions[name]
            # outline
            ax.add_patch(Rectangle((x0, y),
                                   cont_width, cont_height,
                                   fill=False))

            # water fill (height proportional to amount)
            frac = state[name] / max_amt
            if frac > 0:
                ax.add_patch(Rectangle((x0, y),
                                       cont_width, cont_height * frac))

            # label with amount
            ax.text(x0 + cont_width/2,
                    y + cont_height + 0.1,
                    f"{state[name]:.0f}",
                    ha="center", va="bottom", fontsize=10)

            # label container name to the left (only once for first column)
            if step == 0:
                ax.text(x0 - 0.4,
                        y + cont_height/2,
                        name,
                        ha="right", va="center", fontsize=12)

        # Draw connections for this state as "pipes" between containers
        for (a, b) in connections[step]:
            y1 = y_positions[a] + cont_height/2
            y2 = y_positions[b] + cont_height/2
            ax.plot([x0 + cont_width, x0 + cont_width + 0.3],
                    [y1, y1])
            ax.plot([x0 + cont_width + 0.3, x0 + cont_width + 0.3],
                    [y1, y2])
            ax.plot([x0 + cont_width + 0.3, x0 + cont_width],
                    [y2, y2])

        # Step title below
        ax.text(x0 + cont_width/2,
                -0.8,
                f"Step {step}",
                ha="center", va="top", fontsize=11)

    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.show()

# ------------- Example scenario (like the slide) -------------

# Four containers a,b,c,d; d starts with 8 units
a, b, c, d = Container(), Container(), Container(), Container(8)
containers = {"a": a, "b": b, "c": c, "d": d}

states = []
connections = []

def snapshot(conns):
    states.append({name: cont.getAmount() for name, cont in containers.items()})
    connections.append(conns)

# Step 0: initial
snapshot([])

# Step 1: put 12 units into a (total 20), d has 8
a.addWater(12)
snapshot([])

# Step 2: connect a-b → both become 6
a.connectTo(b)
snapshot([("a", "b")])

# Step 3: connect b-c → a,b,c become 4
b.connectTo(c)
snapshot([("a", "b"), ("b", "c")])

# Step 4: connect c-d → all 4 become 5
c.connectTo(d)
snapshot([("a", "b"), ("b", "c"), ("c", "d")])

draw_states(states, connections, names=["a", "b", "c", "d"])
