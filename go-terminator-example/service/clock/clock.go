package clock

import (
	"fmt"
	"time"
)

type Clock struct {
	stop   bool
	StopAt time.Time
}

func (c *Clock) RingBell() {
	fmt.Println("Bang , Bang , Bang")
}

func (c *Clock) Terminated() {
	c.stop = true
	c.StopAt = time.Now()
	fmt.Println("Clock is stopping: ", c.StopAt.String())
}

func (c *Clock) Run() {
	tricker := time.NewTicker(time.Second * 2)

	for {
		if c.stop {
			fmt.Println("Clock is stopped .")
			break
		}

		<-tricker.C
		c.RingBell()
	}
}

// Enter the root directory and execute the package command go build
// run ./go-terminator-example
// Wait a few seconds
// Press "Control + C"
// output:
/*
Current Count:  1
Current Count:  2
Bang , Bang , Bang
Current Count:  3
Bang , Bang , Bang
Current Count:  4
Current Count:  5
^Cgo-terminator: Service interrupted by interrupt signal,and the service is exiting gracefully .
go-terminator: func globalTerminator.Terminated[0] start running
.ACountServer is stopping:  2023-01-16 16:54:29.722497 +0800 CST m=+5.301817793
go-terminator: func globalTerminator.Terminated[0] is done
.go-terminator: func clockServer.Terminated[1] start running
.Clock is stopping:  2023-01-16 16:54:29.823712 +0800 CST m=+5.403033960
go-terminator: func clockServer.Terminated[1] is done
*/
