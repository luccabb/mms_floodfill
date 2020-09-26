import API
import heapq
import sys


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    log("Running...")

    mazeSettings = [
        [14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14],
        [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
        [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
        [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
        [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
        [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
        [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
        [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
        [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
        [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
        [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
        [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
        [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
        [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
        [14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14]
    ]

    stack = []
    # 0 > up | 1 > right | 2 > down | 3 > left | 
    orientation = 0
    currPosition = [0, 0]
    nodesSinceLastDecision = []
    lastDecisionNode = []
    
    while mazeSettings[currPosition[0]][currPosition[1]] != 0:
        F = API.wallFront()
        R = API.wallRight()
        L = API.wallLeft()

        row, col = currPosition
        # Forward, Right, Left
        nodesAround = [(), (), ()]
        valuesAround = [float("inf"), float("inf"), float("inf")]

        if not F:
            # no wall in front
            if orientation == 0:
                frontVal = mazeSettings[row+1][col]
                nodesAround[0] = (row+1, col)
            elif orientation == 1:
                frontVal = mazeSettings[row][col+1]
                nodesAround[0] = (row, col+1)
            elif orientation == 2:
                frontVal = mazeSettings[row-1][col]
                nodesAround[0] = (row-1, col)
            elif orientation == 3:
                frontVal = mazeSettings[row][col-1]
                nodesAround[0] = (row, col-1)
            valuesAround[0] = frontVal
        
        if not R:
            # no wall in the right
            if orientation == 0:
                rightVal = mazeSettings[row][col+1]
                nodesAround[1] = (row, col+1)
            elif orientation == 1:
                rightVal = mazeSettings[row-1][col]
                nodesAround[1] = (row-1, col)
            elif orientation == 2:
                rightVal = mazeSettings[row][col-1]
                nodesAround[1] = (row, col-1)
            elif orientation == 3:
                rightVal = mazeSettings[row+1][col]
                nodesAround[1] = (row+1, col)
            valuesAround[1] = rightVal

        if not L:
            # no wall in the left
            if orientation == 0:
                leftVal = mazeSettings[row][col-1]
                nodesAround[2] = (row, col-1)
            if orientation == 1:
                leftVal = mazeSettings[row+1][col]
                nodesAround[2] = (row+1, col)
            if orientation == 2:
                leftVal = mazeSettings[row][col+1]
                nodesAround[2] = (row, col+1)
            if orientation == 3:
                leftVal = mazeSettings[row-1][col]
                nodesAround[2] = (row-1, col)
            valuesAround[2] = leftVal
        
        if lastDecisionNode and (row, col) in lastDecisionNode:
            prev = (row, col)
            for i, node in enumerate(nodesSinceLastDecision[-2]):

                mazeSettings[node[0]][node[1]] = mazeSettings[prev[0]][prev[1]] + 1
                prev = (node[0], node[1])

        if L and R and F:
            # Dead End, we need to turn 180 degrees
            API.turnRight()
            API.turnRight()
            API.moveForward()
            for nodesSince in nodesSinceLastDecision:
                nodesSince.append((row, col))
            prev = lastDecisionNode[-1]

            # log(lastDecisionNode)
            for i, node in enumerate(nodesSinceLastDecision[-1]):

                mazeSettings[node[0]][node[1]] = mazeSettings[prev[0]][prev[1]] + 1
                prev = (node[0], node[1])
                # log(node)
                # log(mazeSettings[node[0]][node[1]])
            
            if orientation == 0:
                currPosition[0] -= 1
                orientation = 2
            elif orientation == 1:
                currPosition[1] -= 1
                orientation = 3
            elif orientation == 2:
                currPosition[0] += 1
                orientation = 0
            elif orientation == 3:
                currPosition[1] += 1
                orientation = 1
            continue

        lowerNeighbor = min(valuesAround)

        if lowerNeighbor == valuesAround[0]:
            # lowerNeighbor is Front
            API.moveForward()
            for nodesSince in nodesSinceLastDecision:
                nodesSince.append((row, col))

            if valuesAround[1] != float("inf"):
                if (valuesAround[1], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[1], (row, col)))
            
            if valuesAround[2] != float("inf"):
                if (valuesAround[2], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[2], (row, col)))

            if orientation == 0:
                currPosition[0] += 1
            elif orientation == 1:
                currPosition[1] += 1
            elif orientation == 2:
                currPosition[0] -= 1
            elif orientation == 3:
                currPosition[1] -= 1

        elif lowerNeighbor == valuesAround[1]:
            # lowerNeighbor is Right side
            API.turnRight()
            API.moveForward()
            for nodesSince in nodesSinceLastDecision:
                nodesSince.append((row, col))

            if valuesAround[0] != float("inf"):
                if (valuesAround[0], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[0], (row, col)))
            if valuesAround[2] != float("inf"):
                if (valuesAround[2], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[2], (row, col)))

            if orientation == 0:
                currPosition[1] += 1
                orientation = 1
            
            elif orientation == 1:
                currPosition[0] -= 1
                orientation = 2
            
            elif orientation == 2:
                currPosition[1] -= 1
                orientation = 3
            
            elif orientation == 3:
                currPosition[0] += 1
                orientation = 0
        
        elif lowerNeighbor == valuesAround[2]:
            # lowerNeighbor is Left side
            API.turnLeft()
            API.moveForward()
            for nodesSince in nodesSinceLastDecision:
                nodesSince.append((row, col))

            if valuesAround[0] != float("inf"):
                if (valuesAround[0], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[0], (row, col)))
            if valuesAround[1] != float("inf"):
                if (valuesAround[1], (row, col)) not in stack:
                    heapq.heappush(stack, (valuesAround[1], (row, col)))

            if orientation == 0:
                currPosition[1] -= 1
                orientation = 3

            elif orientation == 1:
                currPosition[0] += 1
                orientation = 0

            elif orientation == 2:
                currPosition[1] += 1
                orientation = 1

            elif orientation == 3:
                currPosition[0] -= 1
                orientation = 2

        if (not L and not R) or (not L and not F) or (not F and not R):
            nodesSinceLastDecision.append([])
            if (row, col) not in lastDecisionNode:
                lastDecisionNode.append((row, col))

    log(mazeSettings)

if __name__ == "__main__":
    main()
