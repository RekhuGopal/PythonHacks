package main

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"

	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
)

// Create struct to hold info about new item
type Item struct {
	Year   int
	Title  string
	Plot   string
	Rating float64
}

// Get table items from JSON file
func getItems() []Item {
	raw, err := ioutil.ReadFile("./movie_data.json")
	if err != nil {
		log.Fatalf("Got error reading file: %s", err)
	}

	var items []Item
	json.Unmarshal(raw, &items)
	return items
}

// snippet-end:[dynamodb.go.load_items.func]

func main() {

	// and region from the shared configuration file ~/.aws/config.
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	// Create DynamoDB client
	svc := dynamodb.New(sess)

	// Get table items from .movie_data.json
	items := getItems()

	// Add each item to Movies table:
	tableName := "Movies"

	for _, item := range items {
		av, err := dynamodbattribute.MarshalMap(item)
		if err != nil {
			log.Fatalf("Got error marshalling map: %s", err)
		}

		// Create item in table Movies
		input := &dynamodb.PutItemInput{
			Item:      av,
			TableName: aws.String(tableName),
		}

		_, err = svc.PutItem(input)
		if err != nil {
			log.Fatalf("Got error calling PutItem: %s", err)
		}

		year := strconv.Itoa(item.Year)

		fmt.Println("Successfully added '" + item.Title + "' (" + year + ") to table " + tableName)
		// snippet-end:[dynamodb.go.load_items.call]
	}
}

// snippet-end:[dynamodb.go.load_items]
