package main

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"

	"fmt"
)

func CreateBucket(client *s3.S3, bucketName string) error {
	_, err := client.CreateBucket(&s3.CreateBucketInput{
		Bucket: aws.String(bucketName),
	})

	return err
}

func main() {
	sess, err := session.NewSessionWithOptions(session.Options{
		Profile: "default",
		Config: aws.Config{
			Region: aws.String("us-west-2"),
		},
	})

	if err != nil {
		fmt.Printf("Failed to initialize new session: %v", err)
		return
	}

	s3Client := s3.New(sess)

	bucketName := "learnaws-go-sdk-tutorial-cloudquicklabs"
	err = CreateBucket(s3Client, bucketName)
	if err != nil {
		fmt.Printf("Couldn't create bucket: %v", err)
		return
	}

	fmt.Println("Successfully created bucket")
}
