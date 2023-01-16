package main

import (
	"os"
	"syscall"
	"time"

	"go-terminator-example/service/clock"
	"go-terminator-example/service/counter"

	terminator "github.com/biandoucheng/go-terminator"
)

var (
	globalTerminator = terminator.TerminatedHandler{}
	counterServer    = counter.ACountServer{}
	clockServer      = clock.Clock{}
)

func main() {
	globalTerminator.Init([]os.Signal{syscall.SIGINT})
	globalTerminator.Run()

	counterServer.Init(time.Second * 1)
	globalTerminator.Register("globalTerminator.Terminated", 0, time.Second*5, counterServer.Terminated)
	go counterServer.Run()

	globalTerminator.Register("clockServer.Terminated", 0, time.Second*2, clockServer.Terminated)
	go clockServer.Run()

	for {
		time.Sleep(time.Second)
	}
}
