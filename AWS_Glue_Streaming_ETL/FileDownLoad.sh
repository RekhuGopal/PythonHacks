cd ~/environment/

echo "==================> DOWNLOADING & EXECUTING THE ONE-STEP-SETUP SCRIPT <====================
$(curl -s 'https://static.us-east-1.prod.workshops.aws/public/c9b4eabe-d66f-466f-836c-2d81c13c2558/static/download/howtostart/awseevnt/s3-and-local-file/one-step-setup.sh' --output ~/environment/glue-workshop/library/one-step-setup.sh --create-dirs)
==========================================================================================="

. ./glue-workshop/library/one-step-setup.sh  'https://static.us-east-1.prod.workshops.aws/public/c9b4eabe-d66f-466f-836c-2d81c13c2558/static/0/'
