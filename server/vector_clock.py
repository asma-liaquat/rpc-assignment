class VectorClock:
    """Simple vector clock implementation.

    Stores a mapping node_id -> counter (int).
    """
    def __init__(self, clock=None):
        self.clock = dict(clock) if clock else {}

    def increment(self, node_id):
        """Increment the counter for node_id."""
        self.clock[node_id] = self.clock.get(node_id, 0) + 1

    def update(self, other):
        """Merge another vector clock (dict or VectorClock) into this one by taking element-wise maxima."""
        if other is None:
            return
        other_clock = other.clock if hasattr(other, 'clock') else dict(other)
        for k, v in other_clock.items():
            self.clock[k] = max(self.clock.get(k, 0), v)

    def compare(self, other):
        """Compare this clock to another (dict or VectorClock).

        Returns one of: 'happens-before', 'happens-after', 'concurrent', 'equal'
        """
        other_clock = other.clock if hasattr(other, 'clock') else dict(other)
        keys = set(self.clock.keys()) | set(other_clock.keys())
        less = False
        greater = False
        for k in keys:
            a = self.clock.get(k, 0)
            b = other_clock.get(k, 0)
            if a < b:
                less = True
            elif a > b:
                greater = True
        if not less and not greater:
            return 'equal'
        if less and not greater:
            return 'happens-before'
        if greater and not less:
            return 'happens-after'
        return 'concurrent'

    def to_dict(self):
        return dict(self.clock)

    @staticmethod
    def from_dict(d):
        return VectorClock(dict(d))
