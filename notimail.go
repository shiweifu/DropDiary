package main

import (
	"./process"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/smtp"
	"path"
	"strings"
	"time"
)

type Message struct {
	subject string
	content string
}

var Config map[string]string

// func SendMail(subject, content string, tos []string) error {
func SendMail(msg Message) error {

	message := `From: ` + Config["from_email"] + `
To: ` + Config["to_email"] + `
Subject: ` + msg.subject + `
Content-Type: text/html;charset=UTF-8

` + msg.content

	tos := []string{Config["to_email"]}

	auth := smtp.PlainAuth("", Config["smtp_username"], Config["smtp_password"], Config["smtp_host"])
	err := smtp.SendMail(Config["smtp_addr"], auth, Config["from_email"], tos, []byte(message))
	if err != nil {
		fmt.Println("Send Mail to", strings.Join(tos, ","), "error:", err)
		return err
	}
	fmt.Println("Send Mail to", strings.Join(tos, ","), "Successfully")
	return nil
}

func setup() {
	binDir, err := process.ExecutableDir()
	if err != nil {
		panic(err)
	}
	var ROOT = path.Dir(binDir + "/")

	// Load配置文件
	configFile := ROOT + "/conf/config.json"
	content, err := ioutil.ReadFile(configFile)
	if err != nil {
		panic(err)
	}
	Config = make(map[string]string)
	err = json.Unmarshal(content, &Config)
	if err != nil {
		panic(err)
	}
}

func makeSubject() string {
	// It's Saturday, Sep 20 - How did your day go?
	t := time.Now()
	_, month, day := t.Date()
	return fmt.Sprintf("It's %s, %s %d - How did your day go?", t.Weekday().String(), month, day)
}

func main() {
	setup()
	msg := Message{makeSubject(), "Reply the email and leave something for yourself."}
	SendMail(msg)

}
