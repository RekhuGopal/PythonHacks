package main

import (
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sns"
)

func main() {
	err := SendSMS("Phone Number", "Hi, I am from AWS SNS")
	if err != nil {
		log.Fatal(err)
	}

}

/*
const (
	// Replace AccessKeyID with your AccessKeyID key.
	AccessKeyID = "Access Key"

	// Replace AccessKeyID with your AccessKeyID key.
	SecretAccessKey = "Access Secret"

	// Replace us-west-2 with the AWS Region you're using for Amazon SNS.
	AwsRegion = "us-west-2"
)
*/

func SendSMS(phoneNumber string, message string) error {
	// Create Session and assign AccessKeyID and SecretAccessKey
	/*
		sess, err := session.NewSession(&aws.Config{
			Region:      aws.String(AwsRegion),
			Credentials: credentials.NewStaticCredentials(AccessKeyID, SecretAccessKey, ""),
		},
		)
	*/

	//
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	// Create SNS service
	svc := sns.New(sess)

	// Pass the phone number and message.
	params := &sns.PublishInput{
		PhoneNumber: aws.String(phoneNumber),
		Message:     aws.String(message),
	}

	// sends a text message (SMS message) directly to a phone number.
	resp, err := svc.Publish(params)

	if err != nil {
		log.Println(err.Error())
	}

	fmt.Println(resp) // print the response data.

	return nil
}
