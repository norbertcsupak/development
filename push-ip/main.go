package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/push"
)

var (
	externalIP = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "external_ip_addr: " + hName(),
	})
)

func init() {
	prometheus.MustRegister(externalIP)
}

func hName() string {
	hostname, err := os.Hostname()
	if err != nil {
		log.Fatal(err)
	}
	return hostname
}

func ExternalIP() (string, error) {
	resp, err := http.Get("http://checkip.amazonaws.com/")
	body, err := ioutil.ReadAll(resp.Body)
	bodyString := string(body)
	if err != nil {
		// Handle Error
	}
	defer resp.Body.Close()

	if err != nil {
		return resp.Status, err
	}
	return bodyString, err
}

func main() {
	ip, err := ExternalIP()
	if err := push.New("http://192.168.4.188:9091", ip).Gatherer(prometheus.DefaultGatherer).
		Push(); err != nil {
		fmt.Printf("Could not push to Pushgateway: %v\n", err)
	}

	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(ip, hName())
}
