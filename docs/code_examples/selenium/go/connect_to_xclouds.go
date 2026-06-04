package main

import (
	"fmt"

	"github.com/tebeka/selenium"
)

func main() {
	caps := selenium.Capabilities{
		"browserName": "chrome",
	}

	driver, err := selenium.NewRemote(caps, "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY")
	if err != nil {
		panic(err)
	}
	defer driver.Quit()

	if err := driver.Get("https://google.com"); err != nil {
		panic(err)
	}

	source, err := driver.PageSource()
	if err != nil {
		panic(err)
	}

	fmt.Println(source)
}
