"""
# Copyright Nick Cheng, William Cheung 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

from salboard import SALboard
from salbnode import SALBnode

# Add your functions here.


def salb2salbLL(salb):
    '''(SALboard) -> SALBnode
    Takes a dictionary representation of a Snakes and Ladders and returns the
    head of a linked list representation of the Snakes and Ladders board.
    The function creates a linked list with numSqaueres nodes that acts as
    each square of the board. The function then
    REQ: salb must be a valid dictionary representaion of a Snakes and Ladders
    Board
    '''
    # Call createNodeBoard to create a linked list with numSquares nodes and
    # set head to the head of the linked list
    head = createNodeBoard(salb.numSquares)
    # iterate through the keys in the dictionary
    for snadder in salb.snadders:
        # set start_snadder to the node that represents the start snadder node
        start_snadder = findNode(head, snadder)
        # set end_snadder to the node that represents the destination node
        end_snadder = findNode(head, salb.snadders[snadder])
        # point the snadder field of start_snadder to the destination node
        start_snadder.snadder = end_snadder
    # return the head of the linked list
    return head


def willfinish(first, stepsize):
    ''' (SALBnode) -> bool
    Function takes in a linked list representation of a Snakes and Ladders
    board and an int stepsize and returns a boolean True or False.
    The function checks to see if we ever reach the end square of the board.
    Since there is a fixed step size, there are possibilites of a loop.
    We use a slow point and a fast pointer. The slow pointer moves at the pace
    of stepsize. The fast pointer moves at twice the pace of the step size.
    If at any time the two point to the same node, we know there is a cycle and
    return False. We return True if the next field of the node points to the
    head(first) as that is the last node.

    REQ: first must be the head of a linked list representation of a Snakes and
    Ladders board
    REQ: stepsize is an positive int > 0

    >>> x = SALboard(16, {4:11,13:5})
    >>> x = salb2salbLL(x)
    >>> willfinish(x,2)
    False
    >>> willfinish(x,5)
    True
    '''
    # create a boolean reached_end
    reached_end = False
    # point slowNode to the start node (stepsize square)
    slowNode = moveSnadder(findNode(first, stepsize))
    # point fastNode to the start node (stepsize square)
    fastNode = moveSnadder(findNode(first, stepsize))
    # create while loop where it iterates as we have not reached the end node
    while(reached_end is False):
        # move slowNode by stepsize, if the node has a Snadder we move to the
        # destination
        slowNode = moveSnadder(moveNode(slowNode, stepsize))
        # iterate 2 times, as the fastNode goes twice as fast
        for move in range(0, 2):
            # move fastNode by stepsize, if the node has a Snadder we move to
            # the destination
            fastNode = moveSnadder(moveNode(fastNode, stepsize))
        # check if slowNode points to the same node as fastNode
        if(slowNode == fastNode):
            # set reached_end to True
            reached_end = True
            # set result to False
            result = False
        # check if slowNode.next is the head (last square)
        if(slowNode.next == first):
            # set reached_end and result to True
            reached_end = True
            result = True
    # return the result
    return result


def whowins(first, step1, step2):
    ''' (SALBnode, int, int) -> int
    Function takes in a linked list representaion of a Snakes and Ladders board
    ints: step1, step2 and returns a int 1 or 2 which represent the player that
    won. Calls willfinish to check if there is a loop for either players.
    Determines winner depending on whether players loop, if both players
    reaches the end of the board, call winTurns to determine the turns in took
    to reach the end for each player. The player that took the least amount of
    turns wins. If there is a tie, player one wins.
    REQ: first must be the head of a linked list representation of a Snakes and
    Ladders board
    REQ: step1 must be a positive int > 0
    REQ: step2 must be a positive int > 0

    >>> x = SALboard(16, {4:11,13:5})
    >>> x = salb2salbLL(x)
    >>> whowins(x, 2, 3)
    2
    >>> whowins(x, 5, 2)
    1
    >>> whowins(x, 2, 5)
    2
    >>> whowins(x, 5, 8)
    2
    '''
    # call willfinish and set booleans for each player
    finishP1 = willfinish(first, step1)
    finishP2 = willfinish(first, step2)
    # if player 1 reaches the end but player 2 loops, player 1 wins
    if (finishP1 is True and finishP2 is False):
        result = 1
    # if player 1 loops and player 2 reaches the end, player 2 wins
    elif (finishP1 is False and finishP2 is True):
        result = 2
    # if both players loop, player 2 wins
    elif (finishP1 is False and finishP2 is False):
        result = 2
    # if both players reach the end, call winTurns
    elif (finishP1 is True and finishP2 is True):
        # call winTurns to set the amount of turns each player took
        P1Turns = winTurns(first, step1)
        P2Turns = winTurns(first, step2)
        # if player 1 took more turns than player 2, player 2 wins
        if (P1Turns > P2Turns):
            result = 2
        # if player 1 took less turns than player 2, player 1 wins
        elif(P1Turns < P2Turns):
            result = 1
        # if there is a tie in turn amounts, player 1 wins
        elif(P1Turns == P2Turns):
            result = 1
    # return the result
    return result


def dualboard(first):
    ''' (SALbnode) -> SALbnode
    Function takes a linked list representaion of a Snakes and Ladders board
    and returns the head of a linked list that is the dual of first. A dual
    of a board is where the destination and start of each snadder is reversed.
    REQ: first is a valid linked list representation of a Snakes and Ladders
    Board
    REQ: first is the head of the linked list
    >>> x = SALboard(10, {4:2,3:5})
    >>> x = salb2salbLL(x)
    >>> dual = dualboard(x)
    >>> two = dual.next
    >>> three = two.next
    >>> four = three.next
    >>> five = four.next
    >>> two.snadder == four
    True
    >>> five.snadder == three
    True
    >>> three.snadder == five
    False
    '''
    # set bool reachedEnd to False
    reachedEnd = False
    # call findSquares to find the number of squares in the board and set it
    # to numSquares
    numSqaures = findSquares(first, first)
    # call createNodeBoard to create a new board with numSqaures squares
    dualBoard = createNodeBoard(numSqaures)
    # set currNode to the head
    currNode = first
    # set currNodeNum to be 1, the start of the square
    currNodeNum = 1
    # iterate while reachedEnd = Flase
    while(reachedEnd is False):
        # check if currNode has a snadder
        if(currNode.snadder is not None):
            # call findSquares and set the number to be destinationNode
            destinationNode = findSquares(first, currNode.snadder)
            # call findNode to find the nodes of both the destination node and
            # start node, set the snadder of the destination node to the
            # current node
            findNode(dualBoard, destinationNode).snadder = findNode(
                dualBoard, currNodeNum)
        # check if we are at the last node
        if(currNode.next == first):
            # set reachedEnd to True
            reachedEnd = True
        # set currNode to the next Node
        currNode = currNode.next
        # add one the the node counter
        currNodeNum += 1
    # return the head of the dual board
    return dualBoard


def findNode(head, nodeNumber):
    ''' (SALBnode, int) -> SALBnode
    Takes the head of a linked list representaion of a Snakes and Ladders board
    and a int nodNumber. Finds the node that represents the nodeNumber and
    return it.
    REQ: head is a SALBnode that is the head of a linked list representaion
    of a Snakes and Ladders board
    REQ: nodeNumber is an int > 0
    >>> x = SALboard(10, {4:2,3:5})
    >>> x = salb2salbLL(x)
    >>> findNode(x, 1) == x
    True
    >>> two = x.next
    >>> findNode(x, 2) == two
    True
    >>> findNode(x, 3) == two
    False
    '''
    # set nodeNum to 1
    nodeNum = 1
    # set currNode to the head
    currNode = head
    # iterate through 1 to nodeNumber
    for x in range(1, nodeNumber):
        # set currNode to currNode.next
        currNode = currNode.next
    # return currNode
    return currNode


def createNodeBoard(numSquares):
    '''(int) -> SALBnode
    Creates a new linked list board with numSquares squares and returns the
    head of the list.
    REQ: numSquares is a positive int > 0
    >>> head = createNodeBoard(10)
    >>> findSquares(head,head)
    10
    '''
    # create the new
    head = SALBnode()
    # set currNode to the head
    currNode = head
    # set nodeNum to 1
    nodeNum = 1
    # iterate while nodNum is less than numSquares
    while(nodeNum < numSquares):
        # create a newNode
        newNode = SALBnode()
        # set currNode.next to point to newNode
        currNode.next = newNode
        # set currNode to point to newNode
        currNode = newNode
        # increase nodeNum counter by 1
        nodeNum += 1
    # at the end of the board, set the node's next field to point to the head
    # making it circular
    currNode.next = head
    # return the head
    return head


def moveSnadder(node):
    ''' (SALBnode) -> SALBnode
    Function takes a node and if the snadder field of the node is not none,
    return the node that is at the snadder.
    REQ: node is SALBnode object

    >>> y = SALBnode(None, None)
    >>> x = SALBnode(None, y)
    >>> q = moveSnadder(x)
    >>> q == y
    True
    >>> d = moveSnadder(y)
    >>> d == y
    True
    '''
    # check if node.snadder is not None
    if (node.snadder is not None):
        # set node to the destination node
        node = node.snadder
    # return the destination node
    return node


def findSquares(head, node):
    ''' (SALBnode, SALBnode) -> int
    Function takes in head of a linked list and a SALbnode and returns an int
    that represents its position on a Snakes and Ladders board.
    REQ: head is a SALBnode
    REQ: node is a SALBnode
    >>> x = SALboard(10, {4:2,3:5})
    >>> x = salb2salbLL(x)
    >>> findSquares(x, x)
    10
    >>> two = x.next
    >>> findSquares(x, two)
    2
    >>> three = two.next
    >>> findSquares(x, three)
    3
    '''
    # set curr to head
    curr = head
    # set numSquares to 1
    numSquares = 1
    # iterate while curr.next does not reach node
    while (curr.next != node):
        # raise numSquares counter by 1
        numSquares += 1
        # set curr to curr.next
        curr = curr.next
    # add one to numSquares if head is not node
    if(head is not node):
        numSquares += 1
    # if head.next is node then numSquares is 2
    if(head.next == node):
        numSquares = 2
    # return 2
    return numSquares


def moveNode(node, movement):
    ''' (SALBnode, int) -> SALBnode
    Takes a node and a integer. Returns the node that is movement away from the
    original node by using a loop and iterating through the loop's next field.
    REQ: node must be a SALBnode object
    REQ: movement must be an int > 0

    >>> a = SALBnode(None, None)
    >>> b = SALBnode(a, None)
    >>> c = SALBnode(b, None)
    >>> d = moveNode(c, 2)
    >>> d == a
    True
    >>> d == b
    False
    '''
    # iterate movement times
    for x in range(0, movement):
        # set node to the next field of node
        node = node.next
    # return node
    return node


def winTurns(head, stepsize):
    ''' (SALBnode, int) -> int
    Function takes in the head of a linked list representaion of a Snakes and
    Ladders and a int stepsize. The function starts at the stepsize node and
    moves stepsize each turn until it reaches the end of the board. Uses a
    counter to calculate the number of turns.
    REQ: head is a valid linked list representaion of a Snakes and Ladders
    board
    REQ: stepsize is an int > 0
    REQ: combination of head and stepsize must ensure at some point the end is
    reached

    >>> x = SALboard(15, {4:12})
    >>> x = salb2salbLL(x)
    >>> winTurns(x,2)
    10
    >>> winTurns(x,1)
    6
    >>> x = SALboard(15, {4:12, 14:3})
    >>> x = salb2salbLL(x)
    >>> winTurns(x,2)
    8
    '''
    # set currNode to the starting position
    currNode = moveSnadder(findNode(head, stepsize))
    # initialize turns counter
    turns = 0
    # iterate while currNode is not the end node
    while(currNode.next != head):
        # set currNode to the node that is stepsize away from currNode
        currNode = moveSnadder(moveNode(currNode, stepsize))
        # increase turns counter by 1
        turns += 1
    # return turns
    return turns
