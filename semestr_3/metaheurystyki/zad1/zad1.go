package main

import (
	"fmt"
	"math"
	"math/rand"
	"slices"
	"sort"
)

type Genome struct {
	gens []float64
}

func random_float(min float64, max float64) float64 {
	return min + rand.Float64()*(max-min)

}

func make_genome(size int) Genome {
	gens := make([]float64, size)
	for i := range gens {
		gens[i] = random_float(0.0, math.Pi)

	}

	return Genome{gens}
}

func fitness(g Genome) float64 {
	val := 1.0
	for _, gen := range g.gens {
		val *= math.Sin(gen)
	}
	return val * 1000.0
}

func change_genome(genome Genome, change_lower_bound float64, change_upper_bound float64, field_count_to_change int) Genome {
	new_gens := make([]float64, len(genome.gens))
	copy(new_gens, genome.gens)
	new_genome := Genome{new_gens}

	order := rand.Perm(len(genome.gens))

	for _, gen_position := range order[0:field_count_to_change] {
		new_val := new_genome.gens[gen_position]
		new_val += random_float(change_lower_bound, change_upper_bound)
		new_val = math.Min(math.Pi, new_val)
		new_val = math.Max(0, new_val)
		new_genome.gens[gen_position] = new_val
	}

	return new_genome
}

func select_parents_tournament(population []Genome, group_size int, winner_size int) []Genome {
	new_population := make([]Genome, len(population))
	for i := 0; i < len(population); {
		// find parents idx
		idxs := make([]int, 0)
		for len(idxs) < group_size {

			// println("Population size ", len(population))
			new_idx := rand.Intn(len(population))
			if !slices.Contains(idxs, new_idx) {
				idxs = append(idxs, new_idx)
			}
		}
		genome_group := make([]Genome, group_size)
		for j, parent_idx := range idxs {
			genome_group[j] = population[parent_idx]
		}
		sort.Slice(genome_group, func(i, j int) bool {
			return fitness(genome_group[i]) > fitness(genome_group[j])
		})

		// println("After sort")
		// for k := range genome_group{
		//     println(k, " Fit: ", fitness(genome_group[k]), "selected? ", k<winner_size)
		// }

		// population has constant size
		for k := 0; k < winner_size && i < len(new_population); k++ {
			new_population[i] = genome_group[k]
			i++

		}

	}

	return new_population

}

func elitist(population []Genome, best_specimen Genome) ([]Genome, Genome) {
	population_best_specimen := population[0]
	population_best_fitness := fitness(population_best_specimen)

	for _, s := range population {
		fit := fitness(s)
		if population_best_fitness < fit {
			population_best_fitness = fit
			population_best_specimen = s
		}
	}

	if population_best_fitness > fitness(best_specimen) {
		best_specimen = population_best_specimen
		println(fmt.Sprintf("Population has new best. Genome %v  Fitness %v", best_specimen.gens, population_best_fitness))
	} else {
		// println(fmt.Sprint("Population is not better at %v", population_best_specimen))
		worst_index := 0
		worst_fitness := math.MaxFloat64

		for i, specimen := range population {
			fit := fitness(specimen)
			if fit < worst_fitness {
				worst_fitness = fit
				worst_index = i
			}
		}
		// best_fitness := fitness(best_specimen)
		// println(fmt.Sprintf("Replacing the worst at %v with fitness %v ", worst_index, worst_fitness))
		// println(fmt.Sprintf("Replacing the worst with old best with fitness %v ", best_fitness))

		population[worst_index] = best_specimen
	}

	return population, best_specimen
}

type SimulationData struct {
	gens_to_change int
	iter_count     int
	final_value    float64
	prec           float64
}

//Zadanie
// sinusy 5 sinsów
// selekcja turniejowa
// 2 reprezentów z 3 do puli rozdicieskiej
// mutacja dodanie do genu wartości wybiernaje losowo (-0.1; 0.2)

func run_simualtion(gens_to_change int, size int, dist float64, prec float64) SimulationData {
	max_iteration_count := 1_000_000
	// current_genome := make_genome(size)
	// current_fitness := fitness(current_genome)

	best_fitness := 0.0
	var best_genome Genome

	population := make([]Genome, 25)
	for i := range population {
		population[i] = make_genome(size)
		fit := fitness(population[i])
		if fit > best_fitness {
			fit = best_fitness
			best_genome = population[i]

		}
	}

	group_size := 3
	winner_size := 2
	//fmt.Println(fmt.Sprintf("start fit %f", current_fitness))

	for i := 0; i <= max_iteration_count; i++ {
		new_parents := select_parents_tournament(population, group_size, winner_size)

		for j, parent := range new_parents {
			new_parents[j] = change_genome(parent, -0.1, 0.2, gens_to_change)
		}

		new_parents, best_genome = elitist(new_parents, best_genome)
		population = new_parents
	}

	result := SimulationData{gens_to_change, max_iteration_count, fitness(best_genome), prec}
	return result

}

func main() {
	// gen_counts := []int{5, 10}
	// dists := []float64{0.5, 0.25, 0.1, 0.05}
	// repeat := 1000
	// precisions := []float64{700.0, 800.0, 999.0, 999.9, 999.99, 999.999, 999.9999}
	//precisions := []float64{999.0}
	run_simualtion(
		1,
		5,
		0.25,
		999.99,
	)

	//fmt.Println(run_simualtion(1, 5, 0.5, 990.0))
	//fmt.Println(change_genome(start_genome,0.5,1))
}
