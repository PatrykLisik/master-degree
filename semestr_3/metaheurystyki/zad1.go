package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
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

func change_genome(genome Genome, dist float64, field_count_to_change int) Genome {
	new_gens := make([]float64, len(genome.gens))
	copy(new_gens, genome.gens)
	new_genome := Genome{new_gens}

	order := rand.Perm(len(genome.gens))

	for _, gen_position := range order[0:field_count_to_change] {
		new_val := new_genome.gens[gen_position]
		new_val += random_float(-dist, dist)
		new_val = math.Min(math.Pi, new_val)
		new_val = math.Max(0, new_val)
		new_genome.gens[gen_position] = new_val

	}

	return new_genome
}

type SimulationData struct {
	gens_to_change int
	iter_count     int
	final_value    float64
	prec           float64
}

func run_simualtion(gens_to_change int, size int, dist float64, prec float64) SimulationData {
	max_iteration_count := 10_000_000

	current_genome := make_genome(size)
	current_fitness := fitness(current_genome)
	//fmt.Println(fmt.Sprintf("start fit %f", current_fitness))

	for i := 0; i <= max_iteration_count; i++ {
		new_genome := change_genome(current_genome, dist, gens_to_change)
		new_fitness := fitness(new_genome)

		//fmt.Println(current_genome)
		//fmt.Println(fmt.Sprintf("%v| new fit %v", i, current_fitness))

		if new_fitness > current_fitness {
			current_genome = new_genome
			current_fitness = new_fitness

		}

		if current_fitness > prec {
			return SimulationData{gens_to_change, i, current_fitness, prec}
		}

	}

	return SimulationData{gens_to_change, max_iteration_count, current_fitness, prec}

}

func main() {
	rand.Seed(time.Now().Unix())
	gen_counts := []int{5, 10}
	dists := []float64{0.5, 0.25, 0.1, 0.05}
	repeat := 1000
	precisions := []float64{700.0, 800.0, 999.0, 999.9, 999.99, 999.999, 999.9999}

	fmt.Println("gen_count, change_count, dist, prec, iterations, end_fitness")
	for _, gen_count := range gen_counts {
		for _, dist := range dists {
			for gen_count_to_change := 1; gen_count_to_change < gen_count; gen_count_to_change++ {
				for _, prec := range precisions {
					for i := 0; i < repeat; i++ {
						result := run_simualtion(
							gen_count_to_change,
							gen_count,
							dist,
							prec,
						)
						fmt.Println(
							fmt.Sprintf("%v, %v, %v, %v, %v, %v",
								gen_count,
								gen_count_to_change,
								dist,
								prec,
								result.iter_count,
								result.final_value,
							),
						)

					}
				}

			}
		}
	}
	//fmt.Println(run_simualtion(1, 5, 0.5, 990.0))
	//fmt.Println(change_genome(start_genome,0.5,1))
}
