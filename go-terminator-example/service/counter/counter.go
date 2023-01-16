package counter

import (
	"fmt"
	"time"
)

// Counting service
type ACountServer struct {
	stop   bool
	StopAt time.Time

	Count  int
	Period time.Duration
}

func (a *ACountServer) Init(period time.Duration) {
	if period <= time.Second*1 {
		period = time.Second
	}
	a.Period = time.Second
	a.Count = 0
}

func (a *ACountServer) Add() {
	a.Count += 1
	fmt.Println("Current Count: ", a.Count)
}

func (a *ACountServer) Terminated() {
	a.stop = true
	a.StopAt = time.Now()
	fmt.Println("ACountServer is stopping: ", a.StopAt.String())
}

func (a *ACountServer) Run() {
	tricker := time.NewTicker(a.Period)

	for {
		if a.stop {
			fmt.Println("ACountServer is stopped .")
			break
		}

		<-tricker.C
		a.Add()
	}
}
