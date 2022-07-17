package main

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"

	"fmt"
)

func ListItems(client *s3.S3, bucketName string, prefix string) (*s3.ListObjectsV2Output, error) {
	res, err := client.ListObjectsV2(&s3.ListObjectsV2Input{
		Bucket: aws.String(bucketName),
		Prefix: aws.String(prefix),
	})

	if err != nil {
		return nil, err
	}

	return res, nil
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

	bucketName := "learnaws-go-sdk-tutorial-cloud23"
	prefixName := ""

	bucketObjects, err := ListItems(s3Client, bucketName, prefixName)
	if err != nil {
		fmt.Printf("Couldn't retrieve bucket items: %v", err)
		return
	}

	for _, item := range bucketObjects.Contents {
		fmt.Printf("Name: %s, Last Modified: %s\n", *item.Key, *item.LastModified)
	}
}
