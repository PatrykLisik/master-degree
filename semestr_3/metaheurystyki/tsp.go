package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

type Specimen struct{
    cities []int
    genome []int
}


func create_genome(size int) []int {
    bin := make([]int, size)
    genome := make([]int, size)

    for i:=0;i<size;i++{
            bin[i]=i
            genome[i] = rand.Intn(size-i) 
        }
    return genome
}

func remove_index(s []int, index int) []int {
    return append(s[:index], s[index+1:]...)
}

func cities_order(genome []int) []int {
    size := len(genome)
    bin := make([]int, size)
    for i:=0;i<size;i++{
            bin[i]=i
        }

    city_list := make([]int,size)
    for i, gen := range(genome){
        city_list[i] = bin[gen]
        bin = remove_index(bin, gen)
        
    }
    return city_list
}

func fitness(cities_data [][]int, city_order []int) int{
    distance := 0;

    for i:=0; i<len(city_order)-1; i++{
        start := city_order[i]
        end := city_order[i+1]
        dist := cities_data[start][end]
        fmt.Println(
        fmt.Sprintf("start %v | end %v | distance %v", start, end, dist),
    )
        distance+=dist
    }
    return distance;
}

func main(){
    dat, err := os.ReadFile("./miasta.txt")
    check(err)
    cities_lines := strings.Split(string(dat), "\n")
    cities_data := make([][]int,0)
    // fmt.Print(cities_lines[0])
    for _,dist_line := range(cities_lines){
        line := make([]int, 0)
        for _, dist := range(strings.Fields(dist_line)){
            value, err := strconv.Atoi(dist)
            check(err)
            line = append(line, value)
        }
        cities_data = append(cities_data, line)
    }
//    fmt.Println(cities_data)

    //fmt.Println(create_bin(16))
    genome := create_genome(16)
    fmt.Println(genome)
    city_order := cities_order(genome)
    fmt.Println(cities_data[1][0])
    
    fmt.Println(distance)

    current_fitness := fitness(cities_data, genome)
    for i:=0; i<10000; i++{
        new_genome := make([]int, len(genome))
        copy(new_genome, genome)
        gen_to_chnage := rand.Intn(len(genome))
        new_gen := rand.Intn(len(genome) - gen_to_chnage)
        new_genome[gen_to_chnage]=new_gen
        new_city_order := cities_order(new_genome)
        new_fitness := fitness(cities_data, new_city_order)
        if current_fitness > new_fitness{
            genome = new_genome
            current_fitness = new_fitness
            fmt.Println(fmt.Sprintf("%v %v", i, new_fitness))
        }

    }
    


}
