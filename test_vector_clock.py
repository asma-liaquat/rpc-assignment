from server.vector_clock import VectorClock as ServerVC
from client.vector_clock import VectorClock as ClientVC


def test_compare():
    # A increments, then B increments -> concurrent if they don't see each other
    a = ClientVC()
    b = ClientVC()

    a.increment('A')
    b.increment('B')

    print('a:', a.to_dict())
    print('b:', b.to_dict())
    print('a vs b:', a.compare(b))  # expect 'concurrent'

    # Now a sees b -> a updated with b
    a.update(b)
    print('a after merge b:', a.to_dict())
    print('a vs b after merge:', a.compare(b))  # expect 'happens-after' or equal

    # Separate scenario: A increments, then B updates from A and increments
    a2 = ClientVC()
    b2 = ClientVC()
    a2.increment('A')
    # B sees A
    b2.update(a2)
    b2.increment('B')
    print('\na2:', a2.to_dict())
    print('b2:', b2.to_dict())
    print('a2 vs b2:', a2.compare(b2))  # expect 'happens-before'


if __name__ == '__main__':
    test_compare()
