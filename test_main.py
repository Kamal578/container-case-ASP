import unittest

from main import Container


class ContainerTests(unittest.TestCase):
    def test_simple_equalization(self):
        a = Container(10)
        b = Container(0)

        a.connectTo(b)

        self.assertAlmostEqual(a.getAmount(), 5.0)
        self.assertAlmostEqual(b.getAmount(), 5.0)

    def test_chain_add_and_disconnect(self):
        a = Container(6)
        b = Container(0)
        c = Container(0)

        a.connectTo(b)  # both 3
        b.connectTo(c)  # all 2
        a.addWater(3)   # all 3
        b.disconnectFrom(c)
        a.addWater(3)   # a,b -> 4.5 ; c -> 3

        self.assertAlmostEqual(a.getAmount(), 4.5)
        self.assertAlmostEqual(b.getAmount(), 4.5)
        self.assertAlmostEqual(c.getAmount(), 3.0)

    def test_duplicate_direct_connection_is_noop(self):
        a = Container(8)
        b = Container(0)

        a.connectTo(b)
        initial_neighbors = len(a._neighbors)

        a.connectTo(b)  # duplicate; should be ignored

        self.assertEqual(len(a._neighbors), initial_neighbors)
        self.assertAlmostEqual(a.getAmount(), 4.0)
        self.assertAlmostEqual(b.getAmount(), 4.0)

    def test_cycle_connection_is_prevented(self):
        a = Container(9)
        b = Container(0)
        c = Container(0)

        a.connectTo(b)  # both 4.5
        b.connectTo(c)  # all 3
        a.connectTo(c)  # already connected via b; ignore

        self.assertNotIn(c, a._neighbors)
        self.assertAlmostEqual(a.getAmount(), 3.0)
        self.assertAlmostEqual(b.getAmount(), 3.0)
        self.assertAlmostEqual(c.getAmount(), 3.0)

    def test_negative_within_component_budget(self):
        a = Container(5)
        b = Container(5)
        a.connectTo(b)  # both 5

        a.addWater(-4)  # total 6 -> each 3

        self.assertAlmostEqual(a.getAmount(), 3.0)
        self.assertAlmostEqual(b.getAmount(), 3.0)

    def test_negative_overdraw_raises_and_preserves_state(self):
        a = Container(2)
        original = a.getAmount()

        with self.assertRaises(ValueError):
            a.addWater(-3)

        self.assertAlmostEqual(a.getAmount(), original)

    def test_negative_to_zero(self):
        a = Container(1.5)
        a.addWater(-1.5)
        self.assertAlmostEqual(a.getAmount(), 0.0)


if __name__ == "__main__":
    unittest.main()
