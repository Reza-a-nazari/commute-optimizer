"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""
import random
import math
from typing import Tuple , List
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        # TODO: Implement Genetic Algorithm
        population = self._initialize_population()
        
        best_state = min(population, key=lambda s: self.problem.evaluate(s))
        best_cost = self.problem.evaluate(best_state)
        
        for generation in range(self.generations):
            self.history.append(best_cost)
            
            new_population = []
            
            sorted_population = sorted(population, key=lambda s: self.problem.evaluate(s))
            for i in range(self.elitism):
                new_population.append(sorted_population[i])
                
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(population)
                parent2 = self._tournament_selection(population)
                
                if random.random() < self.crossover_rate:
                    child = crossover(parent1, parent2, self.problem)
                else:
                    child = random.choice([parent1, parent2])
                    
                if random.random() < self.mutation_rate:
                    neighbors = get_neighbors(child, self.problem)
                    if len(neighbors) > 0:
                        child = random.choice(neighbors)
                        
                if self.problem.is_valid_state(child):
                    new_population.append(child)
                    
            population = new_population
            
            current_best = min(population, key=lambda s: self.problem.evaluate(s))
            current_best_cost = self.problem.evaluate(current_best)
            
            if current_best_cost < best_cost:
                best_cost = current_best_cost
                best_state = current_best
                
        return best_state, best_cost

    def _initialize_population(self) -> List[State]:
        base_state = self.problem.generate_initial_state()
        population = [base_state]
        
        while len(population) < self.population_size:
            neighbors = get_neighbors(base_state, self.problem)
            if len(neighbors) > 0:
                population.append(random.choice(neighbors))
            else:
                population.append(base_state)
                
        return population

    def _tournament_selection(self, population: List[State], k: int = 3) -> State:
        selected = random.sample(population, min(k, len(population)))
        best_in_tournament = min(selected, key=lambda s: self.problem.evaluate(s))
        return best_in_tournament