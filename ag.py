from cromosoma import decodificar_cromosoma, generar_cromosoma
from fixture import calcular_aptitud
import pygad

def fitness_func(ga_instance, solution, solution_idx):
    return -calcular_aptitud(decodificar_cromosoma(solution))

fitness_function = fitness_func

poblacion_inicial_custom = []
for i in range(50):
    poblacion_inicial_custom.append(generar_cromosoma())

corrida = "5"
ga_instance = pygad.GA(num_generations=1000,
                       num_parents_mating=40,
                       parent_selection_type="rws",
                       crossover_probability=0.85,
                       mutation_probability=0.15,
                       fitness_func=fitness_function,
                       gene_type=int,
                       initial_population=poblacion_inicial_custom,
                       gene_space=[{"low": 0, "high": 19}, {"low": 0, "high": 19}, {"low": 0, "high": 3}] * 190,
                       save_best_solutions=True)

ga_instance.run()

ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
solution = decodificar_cromosoma(solution)

soluciones_por_gen = ga_instance.best_solutions
joined = '\n'.join(', '.join(map(str, row)) for row in soluciones_por_gen)
file1 = open("output" + corrida + ".csv", "w")
file1.write(joined)
file1.write('\nEND\n')
file1.write(f"Parameters of the best solution : {solution}\n")
file1.write(f"Fitness value of the best solution = {solution_fitness}\n")
if ga_instance.best_solution_generation != -1:
    file1.write(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.\n")
file1.close()
