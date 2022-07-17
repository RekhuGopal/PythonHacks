package main

import (
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"

	"fmt"
)

func DownloadFile(downloader *s3manager.Downloader, bucketName string, key string) error {
	file, err := os.Create(key)
	if err != nil {
		return err
	}

	defer file.Close()

	_, err = downloader.Download(
		file,
		&s3.GetObjectInput{
			Bucket: aws.String(bucketName),
			Key:    aws.String(key),
		},
	)

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

	bucketName := "learnaws-go-sdk-tutorial-cloudquicklabs"
	downloader := s3manager.NewDownloader(sess)
	key := "1.jpg"
	err = DownloadFile(downloader, bucketName, key)

	if err != nil {
		fmt.Printf("Couldn't download file: %v", err)
		return
	}

	fmt.Println("Successfully downloaded file")

}
