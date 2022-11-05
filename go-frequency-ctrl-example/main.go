package main

import (
	"net/http"

	frq "github.com/biandoucheng/go-frequency-ctrl"
	"github.com/gin-gonic/gin"
)

var (
	frequency = frq.Frequency{}
)

func init() {
	frequency.Init(256)
	go frequency.Tricker()
}

func fTest(c *gin.Context) {
	allow := frequency.Access()

	c.JSON(http.StatusOK, gin.H{
		"allow": allow,
		// "desc":  desc.ToString(),
	})

	// desc := frequency.Describe()
	// fmt.Println(desc.ToString())
}

func main() {

	router := gin.New()
	//添加路由
	router.Any("/", func(c *gin.Context) {
		c.String(http.StatusOK, "ok")
	})

	router.Any("/fTest", fTest)
	router.Run(":8000")
}
