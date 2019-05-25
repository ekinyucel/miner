package main

import (
	"log"
	"net/http"

	socketio "github.com/googollee/go-socket.io"
)

// ServeSocket is used for handling web socket server
func ServeSocket(w http.ResponseWriter, r *http.Request) {
	server, err := socketio.NewServer(nil)
	if err != nil {
		log.Println(err)
	}

	server.OnConnect("/", func(s socketio.Conn) error {
		s.SetContext("")
		return nil
	})

	server.OnEvent("/", "tweet", func(s socketio.Conn, msg string) {
		s.Emit("reply", "have "+msg)
	})

	server.OnError("/", func(e error) {
		logger.Println("error:", e)
	})
	go server.Serve() // accepting web socket connection
	defer server.Close()

	go ConsumeKafkaTopic(server)
}
