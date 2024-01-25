package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
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

func select_parents_rulette(population []Specimen, cities_data [][]int) []Specimen {
	fitness_cache := make([]int, len(population))
	for i, speci := range population {
		fitness_cache[i] = fitness(cities_data, speci)
	}

	cumulative_population_finess := 0
	for i := range population {
		cumulative_population_finess += fitness_cache[i]
	}
	fmt.Println(fmt.Sprintf("Cumulative fitness: %v", cumulative_population_finess))

	cirlce_parts := make([]float64, len(population))
    current_fitness_sum := 0

	for i := range cirlce_parts {
        relative_fitness := float64(current_fitness_sum) / float64(cumulative_population_finess)
        cirlce_parts[i] =relative_fitness
        current_fitness_sum+=fitness_cache[i]
	}
    cirlce_parts = append(cirlce_parts, 1.0)

    fmt.Println(fmt.Sprintf("Circle parts: %v", cirlce_parts))
	new_population := make([]Specimen, len(population))
	for new_pop_idx := range new_population {
		rng := rand.Float64()
        fmt.Println(fmt.Sprintf("RNG %v ", rng))

		for i := range cirlce_parts {
            if rng > cirlce_parts[i] && rng <= cirlce_parts[i+1] {
                new_population[new_pop_idx] = Specimen(population[i])
                fmt.Println(fmt.Sprintf("Range start %v end: %v", cirlce_parts[i], cirlce_parts[i+1]))
                break
            }
		}
	}

	return new_population
}
func main() {
	rand.Seed(time.Now().Unix())

	//	MAX_ROAD_LEN := 8000 // just to make this minimization problem
	//	P_MUTATION := 0.1    // mutation probability
	POPULATION_SIZE := 25
	CITY_COUNT := 16

	cities_data := get_cities_data("./miasta.txt")
	for _, city_line := range cities_data {
		fmt.Println(city_line)
	}

	best_specimen := create_specimen(CITY_COUNT)
	population := make([]Specimen, POPULATION_SIZE)
	for i := range population {
		population[i] = create_specimen(CITY_COUNT)
		fmt.Println(population[i])

	}
	current_fitness := road_len(cities_data, best_specimen)

	for _, s := range population {
		new_fitness := fitness(cities_data, s)
		if current_fitness > new_fitness {
			best_specimen = s
			current_fitness = new_fitness
		}
	}

	fmt.Println(fmt.Sprintf("Genome %v \nCity order %v", best_specimen.genome, best_specimen.cities))
	fmt.Println(fmt.Sprintf("Fitness %v", current_fitness))
	for i := 0; i < 1; i++ {
        new_parents := select_parents_rulette(population, cities_data)
        fmt.Println(fmt.Sprintf("New parents %v ", new_parents))
    
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
