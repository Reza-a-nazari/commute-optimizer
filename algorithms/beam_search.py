"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""
import math
import random
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """
        # TODO: Implement Local Beam Search
        initial_state = self.problem.generate_initial_state()
        initial_cost = self.problem.evaluate(initial_state)
        
        beam = [(initial_cost, initial_state)]
        best_state = initial_state
        best_cost = initial_cost
        
        for _ in range(self.max_iterations):
            self.history.append(best_cost)
            
            all_candidates = []
            
            for cost, state in beam:
                neighbors = get_neighbors(state, self.problem)
                for neighbor in neighbors:
                    neighbor_cost = self.problem.evaluate(neighbor)
                    all_candidates.append((neighbor_cost, neighbor))
                    
            if len(all_candidates) == 0:
                break
                
            all_candidates.sort(key=lambda x: x[0])
            
            new_beam = []
            seen_paths = set()
            
            for cost, state in all_candidates:
                if state.path not in seen_paths:
                    new_beam.append((cost, state))
                    seen_paths.add(state.path)
                    
                if len(new_beam) == self.beam_width:
                    break
                    
            beam = new_beam
            
            current_best_cost = beam[0][0]
            current_best_state = beam[0][1]
            
            if current_best_cost < best_cost:
                best_cost = current_best_cost
                best_state = current_best_state
                
        return best_state, best_cost