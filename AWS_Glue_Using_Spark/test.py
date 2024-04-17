''''
There are multiple zip files in s3
                  1. Download all the zip files 
                  2. Loop through all the zip files and extract the zip files
                  3. Find a particular file e.g test.txt from the list of files
                  4. From that file read line by line
                  5. Read the content of the file and extract values of specific key
                  6. Store the value in an array of objects 
                  7. Save the json object file

          LoginId - 124556, org - abc , ip - 12.42.56.78, loginAttempt - 20, status - failed
          LoginId - 124556, org - abc , ip - 12.42.56.78, loginAttempt - 20, status - failed
'''
import boto

s3_client =  boto.client("S3")

s3_client.downloadAll("C:/temp/")

for eachzip in "C:/temp/":
    #unzip and stored folder C:/temp/unzip/

store = []
for eachfolder in "C:/temp/unzip/":
     for file in eachfolder:
        if file.name() == "test.txt":
            file = read("test.txt")
            for eachlin in file:
                if "loginAttempt"  in eachlin and "LoginId" in eachlin:
                    splitList =  eachlin.split(",")
                    neaded = splitList[2]
                    Ip = 


