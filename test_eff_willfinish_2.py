def testing(__salb1__, size):
    
    # first node is the output of the salb2salbLL function
    __head__ = __salb1__
    # get the max width by rounding down the square root of numSquares
    __maxwidth__ = math.floor(math.sqrt(size))

    try:
        # copy the nodes into a list
        __squares__ = []
        # set node to be the head of the list
        __node__ = __head__
        # for every node
        for o in range(0, size):
            # append it to the list
            __squares__.append(__node__)
            # move one forward
            if __node__.next is not None:
                __node__ = __node__.next
            else:
                print("Null pointer at node.next\n One of your links is not",
                      "pointing to the right place :O")
        # empty start:end dict
        __snadders__ = {}
        # run through the list and copy the start:end pairs from the nodes
        for p in range(0, len(__squares__)):
            if __squares__[p].snadder is not None:
                __snadders__[p + 1] = __squares__.index(
                    __squares__[p].snadder) + 1
        # keep records of the start and end of each snadder from the dict
        __start__ = list(__snadders__.keys())
        #__start__.sort()
        __end__ = list(__snadders__.values())
        #__end__.sort()

    except (IndexError, TypeError) as ex:
        print(
            "Oh no! Something broke, double check your code!")
    else:
        if list(__snadders__.keys()) != __start__:
            print("Your linked list snadders and your dictionary snadders",
                  "don't match 0_0\n")

    # counter to reference the current square's number
    __counter__ = 1
    try:
        # for each row in the board
        for k in range(0, int(math.ceil(size / __maxwidth__))):
            # make a string to add the squares into
            row = ""
            # for each column in the board
            for j in range(int(k * __maxwidth__), int((k + 1) * __maxwidth__)):
                # if the square has a snadder
                if __counter__ in __start__:
                    # print a square with the number of the index in it
                    row += ("[_" + str(__start__.index(__counter__)) + "S_]")
                elif __counter__ in __end__:
                    # print a square with the number of the index in it
                    row += ("[_" + str(__end__.index(__counter__)) + "E_]")
                elif __counter__ <= size:
                    # print an empty square
                    row += ("[____]")
                # add one to the counter
                __counter__ += 1
                # move to the next node
                __node__ = __node__.next
            # print the row
            print(row, "\n\n")
    except IndexError:
        print("Graph failed :(\nDouble check your code!")

if __name__ == "__main__":
    import math
    import doctest
    
    print("NORMAL BOARD")
    board = salb2salbLL(SALboard(16, {3:2, 6:4, 5:14}))
    testing(board, 16)
    print("\n")
    print("DUAL BOARD")
    testing(dualboard(board), 16)