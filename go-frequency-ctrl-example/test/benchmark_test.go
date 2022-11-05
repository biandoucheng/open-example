package test

import (
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"testing"
	"time"
)

// qps limit 256/s, request 500/s for 10 s .
func TestFrequency(t *testing.T) {
	ul := "http://127.0.0.1:8000/fTest"
	trans := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true,
		},
		DisableKeepAlives: false,
		Proxy:             http.ProxyFromEnvironment,
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 10 * time.Second,
		}).DialContext,
		MaxIdleConns:        200,
		MaxIdleConnsPerHost: 10,
		IdleConnTimeout:     30 * time.Second,
		TLSHandshakeTimeout: 2 * time.Second,
	}
	client := &http.Client{
		Timeout:   time.Millisecond * 30,
		Transport: trans,
	}

	success := 0
	access := 5000
	for i := 0; i < access; i++ {
		request, _ := http.NewRequest("GET", ul, nil)
		resp, err := client.Do(request)
		if err != nil {
			fmt.Println("http error:", err)
			return
		}

		defer resp.Body.Close()
		res := map[string]bool{
			"allow": false,
		}

		defer resp.Body.Close()
		byts, _ := ioutil.ReadAll(resp.Body)
		json.Unmarshal(byts, &res)

		if res["allow"] == true {
			success += 1
		}

		time.Sleep(time.Millisecond * 2)
	}

	fmt.Printf("access %d, success: %d, success rate:%.2f", access, success, float32(success)/float32(access)*100)
}
