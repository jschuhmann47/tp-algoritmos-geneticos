from cromosoma import decodificar_cromosoma, generar_cromosoma
from fixture import calcular_aptitud
import pygad

def fitness_func(ga_instance, solution, solution_idx):
    return calcular_aptitud(decodificar_cromosoma(solution))

fitness_function = fitness_func

def on_start(ga_instance):
    print("on_start()")

def on_fitness(ga_instance, population_fitness):
    print("on_fitness()")

def on_parents(ga_instance, selected_parents):
    print("on_parents()")

def on_crossover(ga_instance, offspring_crossover):
    print("on_crossover()")

def on_mutation(ga_instance, offspring_mutation):
    print("on_mutation()")

def on_generation(ga_instance):
    print("on_generation()")

def on_stop(ga_instance, last_population_fitness):
    print("on_stop()")

poblacion_inicial_custom = []
for i in range(20):
    poblacion_inicial_custom.append(generar_cromosoma())

ga_instance = pygad.GA(num_generations=5,
                       num_parents_mating=5,
                       fitness_func=fitness_function,
                       #sol_per_pop=10,
                       #num_genes=len(function_inputs),
                       initial_population=poblacion_inicial_custom,
                       on_start=on_start,
                       on_fitness=on_fitness,
                       on_parents=on_parents,
                       on_crossover=on_crossover,
                       on_mutation=on_mutation,
                       on_generation=on_generation,
                       on_stop=on_stop)

# ga_instance.run()

# # ga_instance.plot_fitness()

# solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
# print(f"Parameters of the best solution : {solution}")
# print(f"Fitness value of the best solution = {solution_fitness}")
# print(f"Index of the best solution : {solution_idx}")


# if ga_instance.best_solution_generation != -1:
#     print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.")