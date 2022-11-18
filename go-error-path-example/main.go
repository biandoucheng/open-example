package main

import (
	"fmt"
	"go-error-path-example/pkgb"
)

// go build
// ./go-error-path-exalpme
// 对象 B 执行失败
// 内部错误 00B
// 对象 B 执行失败 : 对象A执行失败 : faild run func A
// pkgb.FuncB : 对象 B 执行失败 : pkga.FuncA : 对象A执行失败

func main() {
	err := pkgb.FuncB()
	if err != nil {
		fmt.Println(err.BaseError())
		fmt.Println(err.ShortError())
		fmt.Println(err.DetailError())
		fmt.Println(err.PathError())
	}
}
