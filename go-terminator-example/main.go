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

	globalTerminator.Register("clockServer.Terminated", 1, time.Second*2, clockServer.Terminated)
	go clockServer.Run()

	for {
		time.Sleep(time.Second)
	}
}

// Go to the root directory of the sample project and execute the packaging command: go build
// Run ./go-terminator-example
// Wait a few seconds
// Press Control + C
// output:
/*
Current Count:  1
Bang , Bang , Bang
Current Count:  2
Current Count:  3
Current Count:  4
Bang , Bang , Bang
Current Count:  5
^Cgo-terminator: Service interrupted by interrupt signal,and the service is exiting gracefully .
go-terminator: func globalTerminator.Terminated[0] start running
.ACountServer is stopping:  2023-01-16 17:00:44.610857 +0800 CST m=+5.340958792
go-terminator: func globalTerminator.Terminated[0] is done
.go-terminator: func clockServer.Terminated[1] start running
.Clock is stopping:  2023-01-16 17:00:44.711366 +0800 CST m=+5.441469334
go-terminator: func clockServer.Terminated[1] is done
*/
