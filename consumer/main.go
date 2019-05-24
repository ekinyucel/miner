package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

var (
	// web server configurations
	serverPort = ":9090" // pass this as an environment variable from docker compose file
	// kafka configurations
	kafkaBrokerURL = []string{"10.65.135.159:29092"}
	kafkaClientID  = "web-server-consumer"
	kafkaTopic     = "tweet"
)

var logger = log.New(os.Stdout, "main: ", log.LstdFlags)

func main() {
	ConsumeKafkaTopic()

	router := mux.NewRouter()
	// router.HandleFunc("/ws", SocketHandler)

	server := NewServer(router, serverPort)

	logger.Printf("The server is listening on port %v", serverPort)
	if err := server.ListenAndServe(); err != http.ErrServerClosed {
		logger.Fatalf("Could not listen on %q: %s\n", serverPort, err)
	}
}
