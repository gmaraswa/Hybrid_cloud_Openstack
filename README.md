# Cloud_project_2 - Hybrid Cloud
This project is a part of course work CSE 546: Cloud Computing.
Professor - Yuli Deng.


## Team Members
- Sai Vikhyath Kudhroli - 1225432689
- Gautham Maraswami - 1225222063
- Abhilash Subhash Sanap - 1225222362



## Project Requirements


### Software Requirements
    Python3
    Boto3 - AWS SDK for python
    face-recoginiton
    ffmpeg
    awslambdaric
    AWS SQS
    Openstack
    Linux


    
### AWS CLI
    Install aws-cli from 
    https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### AWS Configuration.
    Use command: aws configure
    ACCESS_KEY_ID = ####
    SECRET_ACCESS_KEY_ID = ####
    REGION = us-east-1
    OUTPUT = JSON

    PEM key file for SSH Access: cc.pem

### AWS components
    S3 buckets:
    himaliainputbucket
    himaliaoutputbucket
    Dynamo DB:
    student_data
    SQS Queues: 
    s3_input_notification 
    s3_output_notification 

### Installing requirements

Download Openstack from ``https://git.openstack.org/openstack-dev/devstack``

Download Python from ``https://www.python.org/downloads/``

#### Installing packages:
    boto3         : pip install boto3


### Running the application
    Make sure to install all the requirements before running the application.

    1. Launch an EC2 Instance
        a. Create an instance with configurations at least 4 VCPU 8GB Ram 50 GB Disk space.
        b. Enable hibernation for the instance by allowing disk encryption and choosing the hibernation option.
    2. Download devstack openstack from github
        a. Run command git clone https://git.openstack.org/openstack-dev/devstack
        b. Update the configuration file local.conf to accommodate minimal configuration.
    3. Update Security config of the host VM to enable HTTP traffic both inbund and outbound.
    4. Run the command ./stock.sh to start the installation.
    5. The installation will take 20 mins to complete.
    6. Now access the openstack-dashboard horizon using the web address https://<publicIP of the host OS>/dashboard.
    7. Now to create an ubuntu instance download OS- image from the ubuntu webpage link https://cloud-images.ubuntu.com/bionic/current/
    8. Create an image by uploading the image file to Horizon dashboard.
    9. Using the os uploaded image launch an instance inside openstack from horizon.
        a. Select the ssh key to login into the instance.
        b. Select a 10 GB disk 2 GB Ram as the flavor for the instance.
        c.Choose a private network as the network for instance.
        d. For the security group allow TCP/ ICMP/SSH and HTTP Traffic both inbound and outbound.
    10. Create a floating IP and assign it to the created instance
    11. Setup DNS Server inside the cloud image to google server 8.8.8.8
    12. Login into the created instance and install python dependencies.
    13. Run the controller.py code inside the created instance.
    14. Create S3 Bucket for input and output using AWS Console
    15. Create input and output SQS to enable notification from the S3 Buckets
    16. Add triggers in the bucket to push notifications to the queues
    17. Set Bucket permissions to public
    18. Use the handler file provide and create a docker image using the file.
    19. Create a Docker image and push it to AWS ECR
        a.Use the following commands:
        b. Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:
            i. aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 630075306220.dkr.ecr.us-east-1.amazonaws.com
        c. Build your Docker image using the following command:
            i. docker build -t face_recoginition_sample .
        d. After the build completes, tag your image so you can push the image to this repository:
            i. docker tag face_recoginition_sample:latest 630075306220.dkr.ecr.us-east-1.amazonaws.com/face_recoginition_sample:latest
        e. Run the following command to push this image to your  newly created AWS repository:
            i. docker push 630075306220.dkr.ecr.us-east-1.amazonaws.com/face_recoginition_sample:latest
    20. Create a Lambda function from the AWS Console and define a trigger so that it is invoked when a new object is added to S3.
    21. Create role for which has the following permissions
        a. AmazonS3FullAccess
        b. AmazonDynamoDBFullAccess
        c. AWSXRayDaemonWriteAccess
        d. AWSLambdaBasicExecutionRole
    22. Assign the role to the AWS Lambda function
    23. Update input bucket name in  Workload generator and run the to input bucket.
    24. The controller code in the openstack VM will be monitoring the SQS Queues, whenever a new message is received in the input queue, lambda function will be triggered from the openstack VM.
    25. The console of the openstack VM will be printing the input file names.
    26. Whenever the output is available in the output bucket, SQS Queues will be notified, The controller code in openstack VM will download the csv file from the Bucket and print its content in the console.


### Member tasks
#### Sai Vikhyath Kudhroli
- Launched an EC2 instance with the hibernation option used to install openstack.
- Configured AWS CLI and git in the EC2 instance.
Cloned the devstack git repository which is then used to install openstack.
- Create the local.conf in the devstack directory which specifies the configurations for installing openstack and run stack.sh to install openstack.
- Download a lightweight Ubuntu cloud image to launch an instance in openstack.
- Upload the Ubuntu image to openstack using glance.
- Create a security group to allow TCP traffic and ICMP traffic across the instance from all the devices.
- Create a key pair for the instance which is used to SSH into the instance.
- Setup a private network by creating a virtual router and virtual network to which the instance is attached.



#### Gautham Maraswami (1225222063)
- Create a nova instance inside openstack using the image and flavor.
-Set resource utilization ratio to allow higher resources for openstack from host os.
- Setup the network configuration for the created openstack instance.
- Setup volume for the created instance using the horizon dashboard.
- Enable Icmp, ssh  and tcp traffic for the created openstack instance.
- Enable DNS resolution for the created instance by updating the ip address in /etc/resolve
- Install all the necessary libraries including python3, pip, boto3, json etc. 
- Resolve version compatibility issues related to python/ boto3 
- Run the controller code on the created instance.



#### Abhilash Subhash Sanap (1225222362)
- Built the docker image from the given Docker File.
- Created an AWS Elastic Container Registry (ECR) repository, configured the programmatic access to the ECR and pushed the image to it.
- Configured an AWS Lambda function through the console using the “latest” image.
- Modified the AWS lambda function so it receives the key for downloading the image from S3 from the code running in the private cloud running on an Openstack. 
- Authored the controller.py file running on the private cloud.
- Set up the queues s3_input_notification and s3_output_notification. 
- Defined a trigger from s3_input_bucket to s3_input_notification queue and s3_output_bucket to s3_output_notification queue. 
- Wrote the code to invoke lambda from the controller running on a private cloud.



