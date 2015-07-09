from tree import Node

testString = "abbcccdddd"
testMap = { 'a': 1, 'b': 2, 'c': 3, 'd': 4}
testTree = Node(
    v = "",
    l =  Node(
        v = "d",
        r = None,
        l = None
        ),
    r = Node(
        v = "",
        l =  Node(
            v = "c",
            l = None,
            r = None
            ),
        r  =  Node(
            v = "",
            l = Node(
                v = "a",
                l = None,
                r = None
                ),
            r = Node(
                v = "b",
                l = None,
                r = None
                )
            )
        )
    )
testTreeBinary = '0' +  \
('1' + '01100100') +    \
'0' +                   \
('1' + '01100011') +    \
'0' +                   \
('1' + '01100001') +    \
('1' + '01100010')      \
