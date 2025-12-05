Water Container Balancer
========================

Small Python exercise that models interconnected water containers. When two containers are connected, the water levels across the whole connected component are equalized. Two example scripts are included:

- `main.py` shows the core `Container` class and a few console demonstrations.
- `visual.py` adds a simple matplotlib visualization of a four-container scenario.

## Requirements
- Python 3.8+
- `matplotlib` (only needed for `visual.py`): `pip install matplotlib`

## Running the examples
- Console demo:
  ```bash
  python main.py
  ```
- Visualization (opens a matplotlib window):
  ```bash
  python visual.py
  ```

## Tests
- Run the unit tests:
  ```bash
  python -m unittest test_main.py
  ```

## How it works
- Each `Container` tracks its `amount` of water and its neighbors.
- Connecting two containers merges their components and redistributes water evenly across every container in that component; duplicate edges and cycle-forming connections are ignored to avoid extra work.
- Adding water to any container also redistributes within its component; disconnecting stops future sharing but keeps current levels.

## Usage patterns
- Instantiate a container with an optional starting amount: `a = Container(5)`.
- Connect containers with `connectTo`: `a.connectTo(b)` merges the components of `a` and `b` and equalizes water across the union.
- Add water anywhere in a component with `addWater`: the new amount spreads evenly across all nodes in that component.
- Use `disconnectFrom` to break a link; afterward each component evolves independently.
- Read the current water level with `getAmount`.

## Algorithm notes
- Connectivity is tracked as an undirected graph via neighbor sets.
- When water needs to be redistributed (after connect or add), the algorithm depth-first traverses the connected component to collect nodes, sums their amounts, and writes back the average to each node.
- Time complexity for redistribution is O(N + E) in the component; space is O(N) for the traversal set/stack. For small teaching examples this is fine; for large graphs a union-find–based approach with stored totals would avoid repeated traversals.
- Disconnect simply removes the edge; because levels are already equalized, no extra work is needed. Reconnecting nodes already in the same component is treated as a no-op to avoid redundant traversals.

## Example sequence (console)
The bottom of `main.py` runs a short scenario. Expected outputs:
```
connect a-b      -> a: 5.0, b: 5.0
connect b-c      -> a: 3.33, b: 3.33, c: 3.33
a.addWater(6)    -> a: 5.0, b: 5.0, c: 5.0
disconnect b-c
a.addWater(3)    -> a: 6.5, b: 6.5, c: 5.0
```

## Limitations and extensions
- No persistence or I/O; state lives in memory.
- No cycle or duplicate-connection guards beyond ignoring self-connections; reconnecting already-connected nodes is idempotent but still triggers a redistribution.
- Possible extensions: weighted pipes, leak/evaporation over time, larger simulations with a more efficient disjoint-set structure, or a CLI/REST wrapper for scripted experiments.
