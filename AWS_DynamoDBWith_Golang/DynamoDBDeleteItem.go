package main

// snippet-start:[dynamodb.go.delete_item.imports]
import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"

	"fmt"
	"log"
)

// snippet-end:[dynamodb.go.delete_item.imports]

func main() {

	// and region from the shared configuration file ~/.aws/config.
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	// Create DynamoDB client
	svc := dynamodb.New(sess)

	// snippet-start:[dynamodb.go.delete_item.call]
	tableName := "Movies"
	movieName := "The Big New Movie"
	movieYear := "2015"

	input := &dynamodb.DeleteItemInput{
		Key: map[string]*dynamodb.AttributeValue{
			"Year": {
				N: aws.String(movieYear),
			},
			"Title": {
				S: aws.String(movieName),
			},
		},
		TableName: aws.String(tableName),
	}

	_, err := svc.DeleteItem(input)
	if err != nil {
		log.Fatalf("Got error calling DeleteItem: %s", err)
	}

	fmt.Println("Deleted '" + movieName + "' (" + movieYear + ") from table " + tableName)
	// snippet-end:[dynamodb.go.delete_item.call]
}
