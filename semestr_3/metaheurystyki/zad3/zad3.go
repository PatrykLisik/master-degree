package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Specimen struct {
	cities []int
	genome []int
}

func create_genome(size int) []int {
	genome := make([]int, size)
	for i := 0; i < size; i++ {
		genome[i] = rand.Intn(size - i)
	}
	return genome
}

func remove_index(s []int, index int) []int {
	return append(s[:index], s[index+1:]...)
}

func cities_order(genome []int) []int {
	size := len(genome)
	bin := make([]int, size)
	for i := 0; i < size; i++ {
		bin[i] = i
	}

	city_list := make([]int, size)
	for i, gen := range genome {
		city_list[i] = bin[gen]
		bin = remove_index(bin, gen)

	}
	return city_list
}

func create_specimen(size int) Specimen {
	genome := create_genome(size)
	city_order := cities_order(genome)

	return Specimen{city_order, genome}
}

func road_len(cities_data [][]int, s Specimen) int {
	distance := 0
	city_order := s.cities

	for i := 0; i < len(city_order)-1; i++ {
		start := city_order[i]
		end := city_order[i+1]
		dist := cities_data[start][end]
		//	fmt.Println(
		//		fmt.Sprintf("start %v | end %v | distance %v", start, end, dist),
		//	)
		distance += dist
	}
	distance += cities_data[len(city_order)-1][0]
	return distance
}

func fitness(cities_data [][]int, s Specimen) int {
	return 8000 - road_len(cities_data, s)
}

func get_cities_data(path string) [][]int {
	dat, err := os.ReadFile(path)
	check(err)
	cities_lines := strings.Split(string(dat), "\n")
	cities_data := make([][]int, 0)
	// fmt.Print(cities_lines[0])
	for _, dist_line := range cities_lines {
		line := make([]int, 0)
		for _, dist := range strings.Fields(dist_line) {
			value, err := strconv.Atoi(dist)
			check(err)
			line = append(line, value)
		}
		cities_data = append(cities_data, line)
	}
	return cities_data
}

func evolve(s Specimen) Specimen {
	genome := s.genome
	new_genome := make([]int, len(genome))
	copy(new_genome, genome)
	gen_to_chnage := rand.Intn(len(genome))
	new_gen := rand.Intn(len(genome) - gen_to_chnage)
	new_genome[gen_to_chnage] = new_gen
	new_city_order := cities_order(new_genome)

	return Specimen{new_city_order, new_genome}
}

func select_parents_tournament(population []Specimen, cities_data [][]int, group_size int) []Specimen {
	fitness_cache := make([]int, len(population))
	for i, speci := range population {
		fitness_cache[i] = fitness(cities_data, speci)
	}
	new_population := make([]Specimen, len(population))
	for new_pop_idx := range population {
		// find parents idx
		idxs := make([]int, 0)
		for len(idxs) < group_size {

			// println("Population size ", len(population))
			new_idx := rand.Intn(len(population))
			if !slices.Contains(idxs, new_idx) {
				idxs = append(idxs, new_idx)
			}
		}
		// find index of winner
		current_best_fit := 0
		best_index := 0
		for _, idx := range idxs {
			if fitness_cache[idx] > current_best_fit {
				current_best_fit = fitness_cache[idx]
				best_index = idx
			}
		}
		new_population[new_pop_idx] = population[best_index]
	}

	return new_population

}

func select_parents_rulette(population []Specimen, cities_data [][]int) []Specimen {
	fitness_cache := make([]int, len(population))
	for i, speci := range population {
		fitness_cache[i] = fitness(cities_data, speci)
	}

	cumulative_population_finess := 0
	for i := range population {
		cumulative_population_finess += fitness_cache[i]
	}
	// fmt.Println(fmt.Sprintf("Cumulative fitness: %v", cumulative_population_finess))

	cirlce_parts := make([]float64, len(population))
	current_fitness_sum := 0

	for i := range cirlce_parts {
		relative_fitness := float64(current_fitness_sum) / float64(cumulative_population_finess)
		cirlce_parts[i] = relative_fitness
		current_fitness_sum += fitness_cache[i]
	}
	cirlce_parts = append(cirlce_parts, 1.0)

	// fmt.Println(fmt.Sprintf("Circle parts: %v", cirlce_parts))
	new_population := make([]Specimen, len(population))
	for new_pop_idx := range new_population {
		rng := rand.Float64()
		// fmt.Println(fmt.Sprintf("RNG %v ", rng))

		for i := range cirlce_parts {
			if rng > cirlce_parts[i] && rng <= cirlce_parts[i+1] {
				new_population[new_pop_idx] = Specimen(population[i])
				// fmt.Println(fmt.Sprintf("Range start %v end: %v", cirlce_parts[i], cirlce_parts[i+1]))
				break
			}
		}
	}

	return new_population
}

func print_population_fitnes(population []Specimen, cities_data [][]int){

    for _, s := range population {
        fit := fitness(cities_data, s)
        fmt.Println(fmt.Sprintf("%-2v  %-2v | fitness %v", s.genome, s.cities, fit))
    }
}

func sekect_parents_rank(population []Specimen, cities_data [][]int, a float64, b float64, k float64)[]Specimen{
    println("Select parent rank")
	new_population := make([]Specimen, len(population))

    ranks := make([]float64, len(population))
    fitness_cache := make([]int, len(population))
    max_fit := 0
    for i,s := range population{
        fit := fitness(cities_data, s)
        fitness_cache[i] = fit
        if fit > max_fit{
            max_fit = fit
        }
    }
    
    ranks_sum := 0.0
    for i := range population {
        rank := + k* math.Pow((float64(max_fit)-float64(fitness_cache[i])), b)
        ranks_sum += rank
        ranks[i] = rank
    }
    
	cirlce_parts := make([]float64, len(ranks))
	for i := range cirlce_parts {
		relative_rank :=  ranks[i] / ranks_sum
		cirlce_parts[i] = relative_rank
	}
	cirlce_parts = append(cirlce_parts, 1.0)

	// fmt.Println(fmt.Sprintf("Circle parts: %v", cirlce_parts))
	for new_pop_idx := range new_population {
		rng := rand.Float64()
		// fmt.Println(fmt.Sprintf("RNG %v ", rng))

		for i := range cirlce_parts {
			if rng > cirlce_parts[i] && rng <= cirlce_parts[i+1] {
				new_population[new_pop_idx] = Specimen(population[i])
				// fmt.Println(fmt.Sprintf("Range start %v end: %v", cirlce_parts[i], cirlce_parts[i+1]))
				break
			}
		}
	}



 return new_population
}

// selekcja progowa
func select_parents_threshold(population []Specimen, cities_data [][]int, ro float64) []Specimen {
    println("Select parent threshold")
	new_population := make([]Specimen, len(population))

	sort.Slice(population, func(i, j int) bool {
		return fitness(cities_data, population[i]) > fitness(cities_data, population[j])
	})

	threshold := int32(float64(len(population)) * ro)
	for i := range population {
		new_parent_idx := rand.Intn(int(threshold))
		new_population[i] = population[new_parent_idx]
	}

	return new_population
}

func crossover(s1 Specimen, s2 Specimen) Specimen {
	new_genome := make([]int, len(s1.genome))
	point := rand.Intn(len(s1.cities))
	if point == 0 {
		return s2
	}
	if point == len(s1.cities)-1 {
		return s1
	}
	copy(new_genome[0:point], s1.genome[0:point])
	copy(new_genome[point:len(s1.genome)], s2.genome[point:len(s1.genome)])

	return Specimen{cities_order(new_genome), new_genome}
}

func crossover_population(population []Specimen, p_cross float64) []Specimen {
	pop_size := len(population)
	new_population := make([]Specimen, pop_size)
	for i := 0; i < len(population); i++ {
		rng := rand.Float64()
		if rng < p_cross {
			new_population[i] = crossover(population[i], population[(i+1)%pop_size]) // modulo to crossover last with first
			//     fmt.Println(fmt.Sprintf("Crossover \ns1: %-2v \ns2: %-2v \ns3: %-2v",
			//     population[i].genome,
			//     population[(i+1)%pop_size].genome,
			//     new_population[i].genome),
			// )

		} else {
			new_population[i] = population[i]
		}
	}
	return new_population
}

func mutate_population(population []Specimen, p_mutation float64) []Specimen {
	for _, specimen := range population {
		for gen_idx := range specimen.genome {
			rng := rand.Float64()
			if rng > p_mutation {
				specimen.genome[gen_idx] = rand.Intn(len(specimen.cities) - gen_idx)
			}
		}
	}
	for _, s := range population {
		s.cities = cities_order(s.genome)
	}
	return population
}

// jezeli najlepszy osobnik z nowej populacji jest lepszy niz
// najlepszy osobnik z poprzednich populacji, to skopiuj
// najlepszego z nowej populacji, jezeli nie, to zastap
// najgorszego osobnika z biezacej populacji przez najlepszego
// z poprzednich pokolen
func elitist(population []Specimen, best_specimen Specimen, cities_data [][]int) ([]Specimen, Specimen) {
	population_best_specimen := population[0]
	population_best_fitness := fitness(cities_data, population_best_specimen)

	for _, s := range population {
		fit := fitness(cities_data, s)
		if population_best_fitness < fit {
			population_best_fitness = fit
			population_best_specimen = s
		}
	}

	if population_best_fitness > fitness(cities_data, best_specimen) {
		best_specimen = population_best_specimen
		println(fmt.Sprintf("Population has new best at %v", population_best_fitness))
	} else {
		// println(fmt.Sprint("Population is not better at %v", population_best_specimen))
		worst_index := 0
		worst_fitness := math.MaxInt32

		for i, specimen := range population {
			fit := fitness(cities_data, specimen)
			if fit < worst_fitness {
				worst_fitness = fit
				worst_index = i
			}
		}
		// best_fitness := fitness(cities_data, best_specimen)
		// println(fmt.Sprint("Replacing the worst at %v with fitness %v ", worst_index, worst_fitness))
		// println(fmt.Sprint("Replacing the worst with old best with fitness %v ", best_fitness))

		population[worst_index] = best_specimen
	}

	return population, best_specimen
}

func print_population(population []Specimen) {
	println()
	for _, s := range population {
		fmt.Println(fmt.Sprintf("New parent genome %-2v city order %-2v", s.genome, s.cities))
	}
}

func main() {
	//	MAX_ROAD_LEN := 8000 // just to make this minimization problem
	//	P_MUTATION := 0.1    // mutation probability
	POPULATION_SIZE := 25
	CITY_COUNT := 16
	P_CROSSOVER := 0.8 // crossover probability
	P_MUTATION := 0.1
	cities_data := get_cities_data("./miasta.txt")
	println("Cities data")
	for _, city_line := range cities_data {
		fmt.Println(fmt.Sprintf("%-3v", city_line))
	}

	var best_specimen Specimen
	best_fit := 0
	population := make([]Specimen, POPULATION_SIZE)

	fmt.Println(fmt.Sprintf("%-50v city order %-2v", "genome", "cities"))
	for i := range population {
		s := create_specimen(CITY_COUNT)
		population[i] = s
		fit := fitness(cities_data, s)
		if fit > best_fit {
			println("New best @", fit)
			best_fit = fit
			best_specimen = s
		}
		fmt.Println(fmt.Sprintf("%-2v  %-2v | fitness %v", s.genome, s.cities, fit))
	}

	current_fitness := road_len(cities_data, best_specimen)

	for _, s := range population {
		new_fitness := fitness(cities_data, s)
		if current_fitness > new_fitness {
			best_specimen = s
			current_fitness = new_fitness
		}
	}

	for i := 0; i < 1_000_000; i++ {
		// new_parents := select_parents_rulette(population, cities_data)
		// new_parents := select_parents_tournament(population, cities_data, len(population)/7 )
		new_parents := select_parents_threshold(population, cities_data, 0.4)
		// print_population(new_parents)
		new_parents = crossover_population(new_parents, P_CROSSOVER)
		// print_population(new_parents)

		new_parents = mutate_population(new_parents, P_MUTATION)
		// print_population(new_parents)

		population, best_specimen = elitist(new_parents, best_specimen, cities_data)

		// println(fmt.Sprintf("best fitness %v", fitness(cities_data, best_specimen)))
		// TODO
		// Wybieramy osobiniki które będą rodziami na zasadzie ruletki
		// Krzyżujemy geny w połowie
		// Robimy losową mutację genów z prawdopodobieństwem 0.1
		// Strategia elitanra
		// wyszykujmy osobnika najlepszego i najgorszego
		//
		//  new_population := make([]Specimen, POPULATION_SIZE)
		//  for _,s:= range population{
		//      rfitness:=float64((cities_data, s))/float64(cumulative_population_finess)

		//      if rfitness>rand.Float64(){
		//

		//      }
		//  }

	}

}
