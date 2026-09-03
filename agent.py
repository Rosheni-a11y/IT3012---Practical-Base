import random
from collections import deque
import heapq
import math

# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    def bfs_search(self, start, goal, grid_size, walls):
        queue = deque([(start, [])])
        reached = {start}

        width, height = grid_size

        moves = [
          
            ((0, 1), 'Up'),
            ((0, -1), 'Down'),
            ((-1, 0), 'Left'),
            ((1, 0), 'Right')

        ]

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            for (dx, dy), action in moves:
                next_state = (current[0] + dx, current[1] + dy)

                x, y = next_state

                if (
                    0 <= x < width
                    and 0 <= y < height
                    and next_state not in walls
                    and next_state not in reached
                ):
                    reached.add(next_state)
                    queue.append((next_state, path + [action]))

        return []

    def dfs_search(self, start, goal, grid_size, walls):
        stack = [(start, [])]
        reached = {start}

        width, height = grid_size

        moves = [
             ((0, 1), 'Up'),
             ((0, -1), 'Down'),
             ((-1, 0), 'Left'),
             ((1, 0), 'Right')
        ]

        while stack:
            current, path = stack.pop()

            if current == goal:
                return path

            for (dx, dy), action in moves:
                next_state = (current[0] + dx, current[1] + dy)

                x, y = next_state

                if (
                    0 <= x < width
                    and 0 <= y < height
                    and next_state not in walls
                    and next_state not in reached
                ):
                    reached.add(next_state)
                    stack.append((next_state, path + [action]))

        return []

    def ucs_search(self, start, goal, grid_size, walls):
        frontier = [(0, start, [])]
        reached = set()

        width, height = grid_size

        moves = [
            ((0, 1), 'Up'),
            ((0, -1), 'Down'),
            ((-1, 0), 'Left'),
            ((1, 0), 'Right')
        ]

        while frontier:
            cost, current, path = heapq.heappop(frontier)

            if current in reached:
                continue

            reached.add(current)

            if current == goal:
                return path

            for (dx, dy), action in moves:
                next_state = (current[0] + dx, current[1] + dy)

                x, y = next_state

                if (
                    0 <= x < width
                    and 0 <= y < height
                    and next_state not in walls
                    and next_state not in reached
                ):
                    new_cost = cost + 1

                    heapq.heappush(
                        frontier,
                        (new_cost, next_state, path + [action])
                    )

        return []

    def sense_and_act(self, percept):
        # If there is no current plan, create a new one
        if not self.plan:
            start = percept['agent_pos']
            foods = percept['all_food']
            grid_size = percept['grid_size']
            walls = percept['walls']

            # If there is no food left, return no action
            if not foods:
                return None

            # Find the closest food using Manhattan distance
            goal = min(
                foods,
                key=lambda food: abs(food[0] - start[0]) + abs(food[1] - start[1])
            )

            # Create a plan using the selected algorithm
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(
                    start,
                    goal,
                    walls,
                    grid_size,
                    heuristic_type='manhattan'
                )

        # Execute the first action in the plan
        if self.plan:
            return self.plan.pop(0)

        return None


    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        frontier = []
        reached_states = set()

        width, height = grid_size

        # Calculate heuristic for the starting position
        if heuristic_type == 'euclidean':
            h_start = self.euclidean_distance(start_pos, goal_pos)
        else:
            h_start = self.manhattan_distance(start_pos, goal_pos)

        # (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(frontier, (h_start, 0, start_pos, []))

        moves = [
            ((0, 1), 'Up'),
            ((0, -1), 'Down'),
            ((-1, 0), 'Left'),
            ((1, 0), 'Right')
        ]

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            for (dx, dy), action in moves:
                next_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                x, y = next_pos

                if (
                    0 <= x < width
                    and 0 <= y < height
                    and next_pos not in walls
                    and next_pos not in reached_states
                ):
                    # Cost from start to this neighbor
                    g_new = g_cost + 1

                    # Estimated cost from neighbor to goal
                    if heuristic_type == 'euclidean':
                        h_new = self.euclidean_distance(next_pos, goal_pos)
                    else:
                        h_new = self.manhattan_distance(next_pos, goal_pos)

                    # A*: f(n) = g(n) + h(n)
                    f_new = g_new + h_new

                    heapq.heappush(
                        frontier,
                        (f_new, g_new, next_pos, path_taken + [action])
                    )

        return []





if __name__ == "__main__":
    test_agent = SearchAgent()

    print("Manhattan Distance:",
          test_agent.manhattan_distance((0, 0), (3, 4)))

    print("Euclidean Distance:",
          test_agent.euclidean_distance((0, 0), (3, 4)))
   

    