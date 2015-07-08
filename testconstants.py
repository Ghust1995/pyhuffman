from tree import Node

testString = "abbcccdddd"
testMap = { 'a': 1, 'b': 2, 'c': 3, 'd': 4}
testTree = Node(
    v = "",
    r =  Node(
        v = "d",
        r = None,
        l = None
        ),
    l = Node(
        v = "",
        r =  Node(
            v = "c",
            r = None,
            l = None
            ),
        l  =  Node(
            v = "",
            r = Node(
                v = "a",
                r = None,
                l = None
                ),
            l = Node(
                v = "b",
                r = None,
                l = None
                )
            )
        )
    )
