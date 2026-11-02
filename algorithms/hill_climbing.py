"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""
import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        # TODO: Implement Hill Climbing with sideways moves and restarts
        best_overall_state = None
        best_overall_cost = float('inf')
        
        for restart in range(self.max_restarts + 1):
            if restart == 0:
                current_state = self.problem.generate_initial_state()
            else:
                current_state = self.problem.generate_initial_state()
                for _ in range(random.randint(1, 5)):
                    neighbors = get_neighbors(current_state, self.problem)
                    if len(neighbors) > 0:
                        current_state = random.choice(neighbors)
                
            current_cost = self.problem.evaluate(current_state)
            sideways_count = 0
            
            while True:
                self.history.append(current_cost)
                
                if current_cost < best_overall_cost:
                    best_overall_cost = current_cost
                    best_overall_state = current_state
                
                neighbors = get_neighbors(current_state, self.problem)
                if len(neighbors) == 0:
                    break
                    
                best_neighbor = None
                best_neighbor_cost = float('inf')
                
                for neighbor in neighbors:
                    cost = self.problem.evaluate(neighbor)
                    if cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbor = neighbor
                
                if best_neighbor_cost < current_cost:
                    current_state = best_neighbor
                    current_cost = best_neighbor_cost
                    sideways_count = 0
                    
                elif best_neighbor_cost == current_cost:
                    if sideways_count < self.max_sideways:
                        current_state = best_neighbor
                        current_cost = best_neighbor_cost
                        sideways_count += 1
                    else:
                        break
                else:
                    break
                    
        return best_overall_state, best_overall_cost