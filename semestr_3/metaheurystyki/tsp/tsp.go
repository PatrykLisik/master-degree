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

func fitness(cities_data [][]int, s Specimen) int {
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
	return distance
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

func main() {
	rand.Seed(time.Now().Unix())
	cities_data := get_cities_data("./miasta.txt")
	fmt.Println(cities_data[1][0])
    
	specimen := create_specimen(16)
	current_fitness := fitness(cities_data, specimen)
	for i := 0; i < 1_000_000; i++ {
		new_specimen := evolve(specimen)
		new_fitness := fitness(cities_data, new_specimen)
		if current_fitness > new_fitness {
			specimen = new_specimen
			current_fitness = new_fitness
			fmt.Println(fmt.Sprintf("%v %v", i, new_fitness))
		}
		if i%10_000 == 0 {
			fmt.Println(fmt.Sprintf("%v %v", i, current_fitness))
		}

	}

}
