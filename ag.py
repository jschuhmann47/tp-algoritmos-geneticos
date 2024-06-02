from cromosoma import decodificar_cromosoma, generar_cromosoma
from fixture import calcular_aptitud
import pygad

def fitness_func(ga_instance, solution, solution_idx):
    return -calcular_aptitud(decodificar_cromosoma(solution))

fitness_function = fitness_func

def on_fitness(ga_instance, population_fitness):
    print(ga_instance.generations_completed)

poblacion_inicial_custom = []
for i in range(50):
    poblacion_inicial_custom.append(generar_cromosoma())

ga_instance = pygad.GA(num_generations=1000,
                       num_parents_mating=25,
                       fitness_func=fitness_function,
                       gene_type=int,
                       initial_population=poblacion_inicial_custom,
                       gene_space=[{"low": 0, "high": 19}, {"low": 0, "high": 19}, {"low": 0, "high": 3}] * 190,
                       parent_selection_type="sss",
                       crossover_probability=0.4,
                       mutation_probability=0.1,
                    #    parallel_processing=["process", 4],
                    #    on_start=on_start,
                    #    on_fitness=on_fitness,
                    #    on_parents=on_parents,
                    #    on_crossover=on_crossover,
                    #    on_mutation=on_mutation,
                    #    on_generation=on_generation,
                    #    on_stop=on_stop,
                       keep_parents=5,
                       crossover_type="two_points",
                       save_best_solutions=True)

ga_instance.run()

ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
solution = decodificar_cromosoma(solution)
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")

soluciones_por_gen = ga_instance.best_solutions
print(soluciones_por_gen)

if ga_instance.best_solution_generation != -1:
    print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.")