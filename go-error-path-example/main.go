package main

import (
	"fmt"
	"go-error-path-example/pkgb"
)

// go build
// ./go-error-path-exalpme
// pkgb.FuncB Error: Wrong B : pkga.FuncA Error: Wrong A : faild run func A

func main() {
	err := pkgb.FuncB()
	if err != nil {
		fmt.Println(err)
	}
}
