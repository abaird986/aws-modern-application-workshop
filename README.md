# Build a Modern Application on AWS (Python)

**AWS Experience: Beginner**

**Time to Complete: 3-4 hours**

**Cost to Complete: Many of the services used are included in the AWS Free Tier. For those that are not, the sample application will cost, in total, less than $1/day.**

**Tutorial Prereqs:**

* **An AWS Account and Administrator-level access to it**

Please be sure to terminate all of the resources created during this workshop to ensure that you are no longer charged.

**Note:**  Estimated workshop costs assume little to no traffic will be served by your demo website created as part of this workshop.

### **Overview**

AWS provides all the services and features required for a developer to create a modern application, and the tools to build it using modern development methodologies.  This tutorial will walk you through the steps to create a sample web application that leverages concepts and approaches such as containers, infrastructure as code, CI/CD, and serverless.  You will build, from the ground up, a sample website called **Mythical Mysfits** that enables visitors to adopt a fantasy creature as a pet.  You can see a working sample of this website available at: www.mythicalmysfits.com

The site will present *mysfits* available for adoption with some different characteristics about each. Users will be able to vote on which mysfits are their favorites, and then choose to adopt the mysfit they'd like to reserve for adoption.  The Mythical Mysfits website you create will also allow you to gather insights about user behavior for future analyses.

This sample application will use many different AWS services and features that modern applications leverage on AWS. But, learning about *what* those individual services and their features are is not the primary objective of this workshop.  Instead, this workshop is meant to give you an experience of *how* developers are able to build modern applications by interacting with those features and services through the development tools that AWS provides.

### Application Architecture

The Mythical Mysfits website serves it's static content directly from Amazon S3, provides a microservice API backend deployed as a container through AWS Fargate on Amazon ECS, stores data in a managed NoSQL database provided by Amazon DynamoDB, with authentication and authorization for the application enabled through AWS API Gateway and it's integration with Amazon Cognito.  The user website clicks will be sent as records to an Amazon Kinesis Firehose Delivery stream where those records will be processed by serverless AWS Lambda functions and then stored in Amazon S3.

You will be creating and deploying changes to this application completely programmatically. You will use the AWS Command Line Interface to execute commands that create the required infrastructure components, which includes a fully managed CI/CD stack utilizing AWS CodeCommit, CodeBuild, and CodePipeline.  Finally, you will complete the development tasks required all within your own browser by leveraging the cloud-based IDE, AWS Cloud9.

# Module 1: IDE Setup and Static Website Hosting

**Time to complete:** 20 minutes

**Services used:**
* AWS Cloud9
* Amazon Simple Storage Service (S3)

In this module, follow the instructions to create your cloud-based IDE on AWS Cloud9 and deploy the first version of the static Mythical Mysfits website.  Amazon S3 is a highly durable, highly available, and inexpensive object storage service that can serve stored objects directly via HTTP. This makes it wonderfully useful for serving static web content (html, js, css, media content, etc.) directly to web browsers for sites on the Internet.  We will utilize S3 to host the content for our Mythical Mysfits website.

### Select a Region

Log in to the AWS Console.

This web application can be deployed in any AWS region that supports all the services used in this application. The supported regions include:

* us-east-1 (N. Virginia)
* us-east-2 (Ohio)
* us-west-2 (Oregon)
* eu-west-1 (Ireland)

Select a region from the dropdown in the upper right corner of the AWS Management Console.

### Create a new AWS Cloud9 Environment

 On the AWS Console home page, type **Cloud9** into the service search bar and select it:
 ![aws-console-home](/images/module-1/cloud9-service.png)


Click **Create Environment** on the Cloud9 home page:
![cloud9-home](/images/module-1/cloud9-home.png)


Name your environment **MythicalMysfitsIDE** with any description you'd like, and click **Next Step**:
![cloud9-name](/images/module-1/cloud9-name-ide.png)


Leave the Environment settings as their defaults and click **Next Step**:
![cloud9-configure](/images/module-1/cloud9-configure-env.png)


Click **Create Environment**:
![cloud9-review](/images/module-1/cloud9-review.png)


When the IDE has finished being created for you, you'll be presented with a welcome screen that looks like this:
![cloud9-welcome](/images/module-1/cloud9-welcome.png)

In the bottom panel, you will see a terminal command line open and read to use.  Run the following git command in the terminal to clone the necessary code to complete this tutorial:

```
git clone https://github.com/aws-samples/aws-modern-application-workshop.git
```

After cloning the repository, you'll see that your project explorer now includes the files cloned:
![cloud9-explorer](/images/module-1/cloud9-explorer.png)


In the terminal, change directory to the newly cloned repository directory:

```
cd aws-modern-application-workshop
```

Next, we will create the infrastructure components needed for hosting a static website in Amazon S3 via the AWS CLI.  

First, create an S3 bucket, replace the name below (mythical-mysfits-bucket-name) with your own unique bucket name.  Copy the name you choose and save it for later, as you will use it in several other places during this workshop:

```
aws s3 mb s3://mythical-mysfits-bucket-name
```

Now that we have created a bucket, we need to set some configuration options that enable the bucket to be used for static website hosting.  This configuration enables the objects in the bucket to be requested using a registered public DNS name for the bucket, as well as direct site requests to the base path of the DNS name to a selected website homepage (index.html in most cases):

```
aws s3 website s3://YOUR_BUCKET_NAME --index-document index.html
```

All buckets created in Amazon S3 are fully private by default.  In order to be used as a public website, we need to create an S3 **Bucket Policy** that indicates objects stored within this new bucket may be publicly accessed by anyone. Bucket policies are represented as JSON documents that define the S3 *Actions* (S3 API calls) that are allowed (or not not allowed) to be performed by different *Principals* (in our case the public, or anyone). The JSON document for the necessary bucket policy is located at: `/~/environment/aws-modern-application-workshop/module-1/aws-cli/bucket-policy.json`.  This file includes several places that you need to change to use the new bucket name you've created (indicated with `REPLACE_ME`).

Execute the following CLI command to add a public bucket policy to your website:

```
aws s3api put-bucket-policy --bucket mythical-mysfits-bucket-name --policy file://~/environment/aws-modern-application-workshop/module-1/aws-cli/website-bucket-policy.json
```

Now that our new website bucket is configured appropriately, let's add the first iteration of the Mythical Mysfits homepage to the bucket.  Use the following S3 CLI command that mimics the linux command for copying files (**cp**) to copy the provided index.html page locally from your IDE up to the new S3 bucket (replacing the bucket name appropriately).

```
aws s3 cp ~/environment/aws-modern-application-workshop/module-1/web/index.html s3://YOUR_BUCKET_NAME/index.html
```

Now, open up your favorite web browser and enter the below into the address bar. The string to replace YOUR_REGION should match whichever region you created, the possible region strings are listed above at the beginning of this modules instructions (eg: us-east-1):

http://YOUR_BUCKET_NAME.s3-website-YOUR_REGION.amazonaws.com

![mysfits-welcome](/images/module-1/mysfits-welcome.png)

Congratulations, you have created the basic static Mythical Mysfits Website!

That concludes Module 1.

# Module 2: Creating a Service with AWS Fargate

**Time to complete:** 60 minutes

**Services used:**
* AWS CloudFormation
* AWS Identity and Access Management (IAM)
* Amazon Virtual Private Cloud (VPC)
* Amazon Elastic Load Balancing
* Amazon Elastic Container Service (ECS)
* AWS Fargate
* AWS Elastic Container Registry (ECR)
* AWS CodeCommit
* AWS CodePipeline
* AWS CodeDeploy
* AWS CodeBuild


### Overview

In Module 2, you will create a new microservice hosted with AWS Fargate on Amazon Elastic Container Service so that your Mythical Mysfits website can have a application backend to integrate with. AWS Fargate is a deployment option in Amazon ECS that allows you to deploy containers without having to manage any clusters or servers. For our Mythical Mysfits backend, we will use Python and create a Flask app in a Docker container behind a Network Load Balancer. These will form the microservice backend for the frontend website to integrate with.

### Creating the Core Infrastructure

Before we can create our service, we need to create the core infrastructure environment that the service will use, including the networking infrastructure in Amazon VPC, and the AWS Identity and Access Management Roles that will define the permissions that ECS and our containers will have on top of AWS.  We will use AWS CloudFormation to accomplish this. AWS CloudFormation is a service that can programmatically provision AWS resources that you declare within JSON or YAML files called *CloudFormation Templates*, enabling the common best practice of *Infrastructure as Code*.  We have provided a CloudFormation template to create all of the necessary Network and Security resources in /module-2/cfn/core.yml.  This template will create the following resources:

* **An Amazon VPC** - a network environment that contains four subnets (two public and two private) in the 10.0.0.0/16 private IP space, as well as all the needed Route Table configurations.
* **Two NAT Gateways** (one for each public subnet) - allows the containers we will eventually deploy into our private subnets to communicate out to the Internet to download necessary packages, etc.
* **A DynamoDB Endpoint** - our microservice backend will eventually integrate with Amazon DynamoDB for persistence (as part of module 3).
* **A Security Group** - Allows your docker containers to receive traffic on port 8080 from the Internet through the Network Load Balancer.
* **IAM Roles** - Identity and Access Management Roles are created. These will be used throughout the workshop to give AWS services or resources you create access to other AWS services like DynamoDB, S3, and more.

To create these resources, run the following command in the Cloud9 terminal (will take ~10 minutes for stack to be created):

```
aws cloudformation create-stack --stack-name MythicalMysfitsCoreStack --capabilities CAPABILITY_IAM --template-body file://~/environment/aws-modern-application-workshop/module-2/cfn/core.yml   
```

You can check on the status of your stack creation either via the AWS Console or by running the command:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsCoreStack
```
When in the `describe-stacks` response, you see a status of `CREATE_COMPLETE`, CloudFormation has finished provisioning all of the core networking and security resources described above.

Once you see `CREATE_COMPLETE` in the `describe-stacks` response command above, copy the full response and save it for future reference in a text editor. Or, create a temporary folder and file to save it to within your IDE. This JSON response contains the unique identifiers for several of the created resources, which we will use later in this workshop.  

### Creating your First Docker Image

Next, you will create a docker container image that contains all of the code and configuration required to run the Mythical Mysfits backend as a microservice API created with Flask.  We will build the docker container image within Cloud9 and then push it to the Amazon Elastic Container Registry, where it will be available to pull when we create our service using Fargate.

All of the code required to run our service backend is stored within the `/module-2/app/` directory of the repository you've cloned into your Cloud9 IDE.  If you would like to review the Python code that uses Flask to create the service API, view the `/module-2/app/service/mythicalMysfitsService.py` file.

Docker comes already installed on the Cloud9 IDE that you've created, so in order to build the docker image locally, all we need to do is run the following commands in the Cloud9 terminal:

* First change directory to `~/environment/module-2/app`

```
cd ~/environment/aws-modern-application-workshop/module-2/app
```

* Then build the docker image, this will use the file in the current directory called Dockerfile that tells Docker all of the instructions that should take place when the build command is executed. Replace the contents in and the {braces} below with the appropriate information from the account/region you're working in:

```
docker build . -t {aws_account_id}.dkr.ecr.{us-east-1}.amazonaws.com/mythicalmysfits/service:latest
```

You will see docker download and install all of the necessary dependency packages that our application needs, and output the tag for the built image.  Copy the image tag for later reference.

```
Successfully built 8bxxxxxxxxab
Successfully tagged 111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest
```

Let's test our image locally within Cloud9 to make sure everything is operating as expected. Copy the image tag that resulted from the previous camm and run the following command to deploy the container “locally” (which is actually within your Cloud9 IDE inside AWS!):

```
docker run -p 8080:8080 111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest
```

As a result you will see docker reporting that your container is up and running locally:

```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

To test our service with a local request, we're going to open up the build-in web browser within the Cloud9 IDE that can be used to preview applications that are running on the IDE instance.  To open the preview web browser, select **Preview > Preview Running Application** in the Cloud9 menu bar:

![preview-menu](/images/module-2/preview-menu.png)

This will open another panel in the IDE where the web browser will be available.  Append /mysfits to the end of the URI in the address bar of the preview browser and hit enter:

![preview-menu](/images/module-2/address-bar.png)

If successful you will see a response from the service that returns the JSON document stored at `/aws-modern-application-workshop/module-2/app/service/mysfits-response.json`

With a successful test of our service locally, we're ready to create a container image repository in Amazon Elastic Container Registry (Amazon ECR) and push our image into it.  In order to create the registry, run the following command, this creates a new repository in the default AWS ECR registry created for your account.

```
aws ecr create-repository --repository-name mythicalmysfits/service
```

The response to this command will contain additional metadata about the created repository.
In order to push container images into our new repository, we will need to obtain authentication credentials for our Docker client to the repository.  Run the following command, which will return a login command to retrieve credentials for our Docker client and then automatically execute it (include the full command including the $ below). 'Login Succeeded' will be reported if the command is successful.

```
$(aws ecr get-login --no-include-email)
```

Next, push the image you created to the ECR repository using the copied tag from above. Using this command, docker will push your image and all the images it depends on to Amazon ECR:

```
docker push 111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest
```

Run the following command to see your newly pushed docker image stored inside the ECR repository:

```
aws ecr describe-images --repository-name mythicalmysfits/service
```

### Creating your first Fargate Service

Now,  we have an image available in ECR that we can deploy to a service hosted on Amazon ECS using AWS Fargate.  The same service you tested locally via the terminal in Cloud9 as part of the last module will now be deployed in the cloud and publicly available behind a Network Load Balancer.  

First, we will create a **Cluster** in the **Amazon Elastic Container Service (ECS)**. This represents the cluster of “servers” that your service containers will be deployed to.  Servers is in "quotations" because you will be using **AWS Fargate**. Fargate allows you to specify that your containers be deployed to a cluster without having to actually provision or manage any servers yourself.

To create a new cluster in ECS, run the following command:

```
aws ecs create-cluster --cluster-name MythicalMysfits-Cluster
```

Next, we will create a new log group in **AWS CloudWatch Logs**.  AWS CloudWatch Logs is a service for log collection and analysis. The logs that your container generates will automatically be pushed to AWS CloudWatch logs as part of this specific group. This is especially important when using AWS Fargate since you will not have access to the server infrastructure where your containers are running.

To create the new log group in CloudWatch logs, run the following command:

```
aws logs create-log-group --log-group-name mythicalmysfits-logs
```

Now that we have a cluster created and a log group defined for where our container logs will be pushed to, we're ready to register an ECS **task definition**.  A task in ECS is a set of container images that should be scheduled together. A task definition declares that set of containers and the resources and configuration those containers require.  You will use the AWS CLI to create a new task definition for how your new container image should be scheduled to the ECS cluster we just created.  

A JSON file has been provided that will serve as the input to the CLI command, stored at `~/environment/aws-modern-application-workshop/module-2/aws-cli/task-definition.json`. Open this file in the IDE and replace the indicated values with the appropriate ones from your created resources.  These values with be pulled from the CloudFormation response you copied earlier as well as the docker image tag that you pushed earlier to ECR, eg: `111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest`

Once you have replaced the values in `task-defintion.json` and saved it. Execute the following command to register a new task definition in ECS:

```
aws ecs register-task-definition --cli-input-json file://~/environment/aws-modern-application-workshop/module-2/aws-cli/task-definition.json
```

With a new task definition registered, we're ready to provision the infrastructure needed in our service stack. Rather than directly expose our service to the Internet, we will provision a **Network Load Balancer (NLB)** to sit in front of our service tier.  This would enable our frontend website code to communicate with a single DNS name while our backend service would be free to elastically scale in-and-out based on demand or if failures occur and new containers need to be provisioned.

To provision a new NLB, execute the following CLI command in the Cloud9 terminal:

```
aws elbv2 create-load-balancer --name mysfits-nlb --scheme internet-facing --type network --subnets subnet-0c7ca350 subnet-1f895078
```

Copy the response provided by this command, which contains the DNS name of the provisioned NLB as well as its ARN.  You will use this DNS name to test the service once it has been deployed.  And the ARN will be used in a future step.

Next, use the CLI to create an NLB **target group**. A target group allows AWS resources to register themselves as targets for requests that the load balancer receives to forward.  Our service containers will automatically register to this target so that they can receive traffic from the NLB when they are provisioned. This command includes one value that will need to be replaced, your `vpc-id` which can be found as a value within the earlier saved `MythicalMysfitsCoreStack` output returned by CloudFormation.

```
aws elbv2 create-target-group --name MythicalMysfits-TargetGroup --port 8080 --protocol TCP --target-type ip --vpc-id REPLACE_ME --health-check-interval-seconds 10 --health-check-path / --health-check-protocol HTTP --healthy-threshold-count 3 --unhealthy-threshold-count 3
```

Copy and save the response from the above command as well, which contains the Target Group ARN to be used in the next step.

Next, use the CLI to create a load balancing **listener** for the NLB.  This informs that load balancer that for requests received on a specific port, they should be forwarded to targets that have registered to the above target group. Be sure to replace the two indicated values with the appropriate ARN from the TargetGroup and the NLB that you saved from the previous steps:

```
aws elbv2 create-listener --default-actions TargetGroupArn=REPLACE_ME,Type=forward --load-balancer-arn REPLACE_ME --port 80 --protocol TCP
```

With the NLB created and configured, we're ready to create the actual ECS **service** where our containers will run and register themselves to the load balancer to receive traffic.  We have included a JSON file for the CLI input that is located at: `~/environment/aws-modern-application-workshop/module-2/aws-cli/service-definition.json`.  This file includes all of the configuration details for the service to be created, including indicating that this service should be launched with **AWS Fargate** - which means that you do not have to provision any servers within the targeted cluster.  The containers that are scheduled as part of the task used in this service will run on top of a cluster that is fully managed by AWS.

Open this file and replace the indicated values of `REPLACE_ME` and save it, then run the following command to create the service:

```
aws ecs create-service --cli-input-json file://~/environment/aws-modern-application-workshop/module-2/aws-cli/service-definition.json
```

After your service is created, ECS will provision a new task that's running the container you've pushed to ECR, and register it to the created NLB.  Copy that URL and send a request to it using the preview browser (or by simply any web browser, since this time our service is available on the Internet with the retrieved DNS name). Try sending a request to the mysfits resource:

```
http://mysfits-nlb-123456789-abc123456.elb.us-east-1.amazonaws.com/mysfits
```

A response showing the same JSON response we received earlier when testing the docker container locally in Cloud9 means your Flask API is up and running on AWS Fargate.

Next, we need to integrate our website with your new API backend instead of using the hard coded data that we previously uploaded to S3.  You'll need to update the following file to use the same NLB URL for API calls (do not inlcude the /mysfits path): `/module-2/web/index.html`

Open the file in Cloud9 and replace the highlighted area below between the quotes with the NLB URL:

![before replace](/images/module-2/before-replace.png)

After pasting, the line should look similar to below:

![after replace](/images/module-2/after-replace.png)

To upload this file to your S3 hosted website, use the bucket name again that was created during Module 1, and run the following command:

```
aws s3 cp ~/environment/aws-modern-application-workshop/module-2/web/index.html s3://INSERT-YOUR-BUCKET-NAME/index.html
```

 Open your website using the same URL used at the end of Module 1 in order to see your new Mythical Mysfits website, which is retrieving JSON data from your Flask API running within a docker container deployed to AWS Fargate!

### Automating Deployments using AWS Code Services

Now that you have a service up and running, you may think of code changes that you'd like to make to your Flask service.  It would be a bottleneck for your development speed if you had to go through all of the same steps above every time you wanted to deploy a new feature to your service. That's where Continuous Integration and Continuous Delivery or CI/CD come in!

In this module, you will create a fully managed CI/CD stack that will automatically deliver all of the code changes that you make to your code base to the service you created during the last module.  

First, you'll need a place to push and store your code in. Create an **AWS CodeCommit Repository** using the CLI for this purpose:

```
aws codecommit create-repository --repository-name MythicalMysfitsService-Repository
```

Next, we need to create another S3 bucket that will be used to store the temporary artifacts that are created in the middle of our CI/CD pipeline executions.  Choose a new bucket name for these artifacts and create one using the following CLI command:

```
aws s3 mb s3://mythical-mysfits-artifacts-bucket-name
```

Next, this bucket needs a bucket policy to define permissions for the data stored within it. But unlike our website bucket that allowed access to anyone, only our CI/CD pipeline should have access to this bucket.  We have provided the JSON file needed for this policy at `~/environment/aws-modern-application-workshop/module-2/aws-cli/artifacts-bucket-policy.json`.  Open this file, and inside you will need to replace several strings to include the ARNs that were created as part of the MythicalMysfitsCoreStack earlier, as well as your newly chosen bucket name for your CI/CD artifacts.

Once you've modified and saved this file, execute the following command to grant access to this bucket to your CI/CD pipeline:

```
aws s3api put-bucket-policy --bucket mythical-mysfits-artifacts-bucket-name --policy file://~/environment/aws-modern-application-workshop/module-2/aws-cli/artifacts-bucket-policy.json
```

With a repository to store our code in, and an S3 bucket that will be used for our CI/CD artifacts, lets add to the CI/CD stack with a way for a service build to occur.  This will be accomplished by creating an **AWS CodeBuild Project**.  Any time a build execution is triggered, AWS CodeBuild will automatically provision a build server to our configuration and execute the steps required to build our docker image and push a new version of it to the ECR repository we created (and then spin the server down when the build is completed).  The steps for our build (which package our Python code and build/push the Docker container) are included in the `~/environment/aws-modern-application-workshop/module-2/app/buildspec.yml` file.  The **buildspec.yml** file is what you create to instruct CodeBuild what steps are required for a build execution within a CodeBuild project.

To create the CodeBuild project, another CLI input file is required to be updated with parameters specific to your resources. It is located at `~/environment/aws-modern-application-workshop/module-2/aws-cli/code-build-project.json`.  Similarly replace the values within this file as you have done before from the MythicalMysfitsCoreStackOutput. Once saved, execute the following with the CLI to create the project:

```
aws codebuild create-project --cli-input-json file://~/environment/aws-modern-application-workshop/module-2/aws-cli/code-build-project.json
```

Finally, we need a way to *continuously integrate* our CodeCommit repository with our CodeBuild project so that builds will automatically occur whenever a code change is pushed to the repository.  Then, we need a way to *continuously deliver* those newly built artifacts to our service in ECS.  **AWS CodePipeline** is the service that glues these actions together in a **pipeline** you will create next.  

Your pipeline in CodePipeline will do just what I described above.  Anytime a code change is pushed into your CodeCommit repository, CodePipeline will deliver the latest code to your AWS CodeBuild project so that a build will occur. When successfully built by CodeBuild, CodePipeline will perform a deployment to ECS using the latest container image that the CodeBuild execution pushed into ECR.

All of these steps are defined in a JSON file provided that you will use as the input into the AWS CLI to create the pipeline. This file is located at `~/environment/aws-modern-application-workshop/module-2/aws-cli/code-pipeline.json`, open it and replace the required attributes within, and save the file.

Once saved, create a pipeline in CodePipeline with the following command:

```
aws codepipeline create-pipeline --cli-input-json file://~/environment/aws-modern-application-workshop/module-2/aws-cli/code-pipeline.json
```

We have one final step before our CI/CD pipeline can execute end-to-end successfully. With a CI/CD pipeline in place, you won't be manually pushing container images into ECR anymore.  CodeBuild will be pushing new images now. We need to give CodeBuild permission to perform actions on your image repository with an **ECR repository policy***.  The policy document needs to be updated with the specific ARN for the CodeBuild role created by the MythicalMysfitsCoreStack, and the policy document is located at `~/environment/aws-modern-application-workshop/module-2/aws-cli/ecr-policy.json`.  Update and save this file and then run the following command to create the policy:

```
aws ecr set-repository-policy --repository-name mythicalmysfits/service --policy-text file://~/environment/aws-modern-application-workshop/module-2/aws-cli/ecr-policy.json
```

When that has been created successfully, you have a working end-to-end CI/CD pipeline to deliver code changes automatically to your service in ECS.

To test out the new pipeline, we need to configure git within your Cloud9 IDE and integrate it with your CodeCommit repository.

AWS CodeCommit provides a credential helper for git that we will use to make integration easy.  Run the following commands in sequence the terminal to configure git to be used with AWS CodeCommit (neither will report any response if successful):

```
git config --global user.name "YOUR_NAME"
```

```
git config --global user.email your.name@example.com
```

```
git config --global credential.helper '!aws codecommit credential-helper $@'
```

```
git config --global credential.UseHttpPath true
```

Next change directories in your IDE to the environment directory using the terminal:

```
cd ~/environment/
```

Now, we are ready to clone our repository using the following terminal command:

```
git clone https://git-codecommit.REPLACE_REGION.amazonaws.com/v1/repos/MythicalMysfitsService-Repository
```

This will tell us that our repository is empty!  Let's fix that by copying the application files into our repository directory using the following command:

```
cp -r ~/environment/aws-modern-application-workshop/module-2/app/* ~/environment/MythicalMysfitsService-Repository/
```

Now the completed service code that we used to create our Fargate service in Module 2 is stored in the local repository that we just cloned from AWS CodeCommit.  Let's make a change to the Flask service before committing our changes, to demonstrate that the CI/CD pipeline we've created is working. In Cloud9, open the file stored at `~/environment/MythicalMysfitsService-Repository/service/mysfits-response.json` and change the age of one of the mysfits to another value and save the file.

After saving the file, change directories to the new repository directory:

```
cd ~/environment/MythicalMysfitsService-Repository/
```

Then, run the following git commands to push in your code changes.  

```
git add .
git commit -m "I changed the age of one of the mysfits."
git push
```

After they are pushed in to the repository, you can open the CodePipeline service in the AWS Console to view your changes as they progress through the CI/CD pipeline. After committing your code change, it will take about 5 to 10 minutes for the changes to be deployed to your live service running in Fargate. Refresh your Mythical Mysfits website in the browser to see that the changes have taken effect.

This concludes Module 2.

# Module 3 - Adding a Data Tier with Amazon DynamoDB

**Time to complete:** 20 minutes

**Services used:**
* Amazon DynamoDB

### Overview

Now that you have a service deployed and a working CI/CD pipeline to deliver changes to that service automatically whenever you update your code repository, you can quickly move new application features from conception to available for your Mythical Mysfits customers.  With this increased agility, let's add another foundational piece of functionality to the Mythical Mysfits website architecture, a data tier.  In this module you will create a table in Amazon DynamoDB, a managed and scalable NoSQL database service on AWS with super fast performance.  Rather than have all of the Mysfits be stored in a static JSON file, we will store them in a database to make the websites future more extensible and scalable.

### Creating A DynamoDB Table using CloudFormation

To add a DynamoDB table to the architecture, we have included another JSON CLI input file that defines a table called **MysfitsTable**. This table will have a primary index defined by a hash key attribute called **MysfitId**, and two more secondary indexes.  The first secondary index will have the hash key of **Species** and a range key of **MysfitId**, and the second secondary index will have the hash key of **Alignment** and a range key of **MysfitId**.  These two secondary indexes will allow us to execute queries against the table to retrieve all of the mysfits that match a given Species or Alignment to enable the filter functionality you may have noticed isn't yet working on the website.  You can view this file at `~/environment/aws-modern-application-workshop/module-3/aws-cli/dynamodb-table.json`. No changes need to be made to this file and it is ready to execute.

To create the table using the AWS CLI, execute the following command in the Cloud9 terminal:

```
aws dynamodb create-table --cli-input-json file://~/environment/aws-modern-application-workshop/module-3/aws-cli/dynamodb-table.json
```

After the command runs, you can view the details of your newly created table by executing the following AWS CLI command in the terminal:

```
aws dynamodb describe-table --table-name MysfitsTable
```

If we execute the following command to retrieve all of the items stored in the table, you'll see that the table is empty:

```
aws dynamodb scan --table-name MysfitsTable
```

```
{
    "Count": 0,
    "Items": [],
    "ScannedCount": 0,
    "ConsumedCapacity": null
}
```

Also provided is a JSON file that can be used to batch insert a number of Mysfit items into this table.  This will be accomplished through the DynamoDB API **BatchWriteItem.** To call this API using the provided JSON file, execute the following terminal command (the response from the service should report that there are no items that went unprocessed):

```
aws dynamodb batch-write-item --request-items file://~/environment/aws-modern-application-workshop/module-3/aws-cli/populate-dynamodb.json
```

Now, if you run the same command to scan all of the table contents, you'll find the items have been loaded into the table:

```
aws dynamodb scan --table-name MysfitsTable
```

### Committing your first *real* Code change

Now that we have our data included in the table, let's modify our application code to read from this table instead of returning the static JSON file that was used in Module 2.  We have included a new set of Python files for your Flask microservice, but now instead of reading the static JSON file will make a request to DynamoDB.

The request is formed using the AWS Python SDK called **boto3**. This SDK is a powerful yet simple way to interact with AWS services via Python code. It enables you to use service client definitions and functions that have great symmetry with the AWS APIs and CLI commands you've already been executing as part of this workshop.  Translating those commands to working Python code is simple when using **boto3**.  To copy the new files into your CodeCommit repository directory, execute the following command in the terminal:

```
cp ~/environment/aws-modern-application-workshop/module-3/app/service/* ~/environment/MythicalMysfitsService-Repository/service/
```

Now, we need to check in these code changes to CodeCommit using the git command line client.  Run the following commands to check in the new code changes and kick of your CI/CD pipeline:

```
cd ~/environment/MythicalMysfitsService-Repository
```

```
git add .
```

```
git commit -m "Add new integration to DynamoDB."
```

```
git push
```

Now, in just 5-10 minutes you'll see your code changes make it through your full CI/CD pipeline in CodePipeline and out to your deployed Flask service to AWS Fargate on Amazon ECS.  Feel free to explore the AWS CodePipeline console to see the changes progress through your pipeline.

### Update The Website Content in S3

Finally, we need to publish a new index.html page to our S3 bucket so that the new API functionality using query strings to filter responses will be used.  The new index.html file is located at `~/environment/aws-modern-application-workshop/module-3/web/index.html`.  Open this file in your Cloud9 IDE and replace the string indicating “REPLACE_ME” just as you did in Module 1, with the appropriate NLB endpoint.  Refer to the file you already edited in the /module-1/ directory if you need to.  After replacing the endpoint to point at your NLB, upload the new index.html file by running the following command (replacing with the name of the bucket you created in Module 1:

```
aws s3 cp --recursive ~/environment/aws-modern-application-workshop/module-3/web/ s3://your_bucket_name_here/
```

Re-visit your Mythical Mysfits website to see the new population of Mysfits loading from your DynamoDB table and how the Filter functionality is working!

That concludes module 3.

# Module 4: Adding User and API features with Amazon API Gateway and AWS Cognito

**Time to complete:** 40 minutes

**Services used:**
* Amazon Cognito
* Amazon API Gateway
* Amazon Simple Storage Service (S3)

### Overview

### Creating the API and User pool

In order to add some more critical aspects to the Mythical Mysfits website, like allowing users to vote for their favorite mysfit and adopt a mysfit, we need to first have users register on the website.  To enable registration and authentication of website users, we will create a **User Pool** in **AWS Cognito** - a fully managed user identity management service.  Then, to make sure that only registered users are authorized to like or adopt mysfits on the website, we will deploy an REST API with **Amazon API Gateway** to sit in front of our NLB. Amazon API Gateway is also a managed service, and provides commonly required REST API capabilities out of the box like SSL termination, request authorization, throttling, API stages and versioning, and much more.

You will again use the AWS CLI to deploy the needed resources to AWS.

To create the **Cognito User Pool** where all of the Mythical Mysfits visitors will be stored, execute the following CLI command to create a user pool named *MysfitsUserPool* and indicate that all users who are registered with this pool should automatically have their email address verified via confirmation email before they become confirmed users.
```
aws cognito-idp create-user-pool --pool-name MysfitsUserPool --auto-verified-attributes email
```
Copy the response from the above command, which includes the unique ID for your user pool that you will need to use in later steps. Eg: `Id: us-east-1_ab12345YZ)`

Next, in order to integrate our frontend website with Cognito, we must create a new **User Pool Client** for this user pool. This generates a unique client identifier that will allow our website to be authorized to call the unauthenticated APIs in cognito where website users can sign-in and register against the Mythical Mysfits user pool.  To create a new client using the AWS CLI for the above user pool, run the following command (replacing the `--user-pool-id` value with the one you copied above):

```
aws cognito-idp create-user-pool-client --user-pool-id REPLACE_ME --client-name MysfitsUserPoolClient
```

Next, let's turn our attention to creating a new RESTful API in front of our existing Flask service, so that we can perform request authorization before our NLB receives any requests.  We will do this with **Amazon API Gateway**, as described in the module overview.  In order for API Gateway to privately integrate with our NLB, we will configure an **API Gateway VPC Link** that enables API Gateway APIs to directly integrate with backend web services that are privately hosted inside a VPC. **Note:** For the purposes of this workshop, we created the NLB to be *internet-facing* so that it could be called directly in earlier modules. Because of this, even though we will be requiring Authorization tokens in our API after this module, our NLB will still actually be open to the public behind the API Gateway API.  In a real-world scenario, you should create your NLB to be *internal* from the beginning (or create a new internal load balancer to replace the existing one), knowing that API Gateway would be your strategy for Internet-facing API authorization.  But for the sake of time, we'll use the NLB that we've already created that will stay publicly accessible.

Create the VPC Link for our upcoming REST API using the following CLI command (you will need to replace the indicated value with the ARN you saved when the NLB was created in module 2):

```
aws apigateway create-vpc-link --name MysfitsApiVpcLink --target-arns REPLACE_ME
```

The response to the above will indicate that a new VPC link is being provisioned and is in `PENDING` state. Copy the indicated `id` for future use when we create our REST API in the next step.

```
{
    "status": "PENDING",
    "targetArns": [
        "YOUR_ARN_HERE"
    ],
    "id": "abcdef1",
    "name": "MysfitsApiVpcLink"
}
```

With the VPC link creating, we can move on to create the actual REST API using Amazon API Gateway.  Your MythicalMysfits REST API is defined using **Swagger**, a popular open-source framework for describing APIs via JSON.  This Swagger definition of the API is located at `~/environment/aws-modern-applicaiton-workshop/module-4/aws-cli/api-swagger.json`.  Open this file and you'll see the REST API and all of its resources, methods, and configuration defined within.  

There are several places within this JSON file that need to be updated to include parameters specific to your Cognito User Pool, as well as your Network Load Balancer.  

The `securityDefinitions` object within the API definition indicates that we have setup an apiKey authorization mechanism using the Authorization header.  You will notice that AWS has provided custom extensions to Swagger using the prefix `x-amazon-api-gateway-`, these extensions are where API Gateway specific functionality can be added to typical swagger files to take advantage of API Gateway-specific capabilities.

CTRL-F through the file to search for the various places `REPLACE_ME` is located and awaiting your specific parameters.  Once the edits have been made, save the file and execute the following AWS CLI command:

```
aws apigateway import-rest-api --parameters endpointConfigurationTypes=REGIONAL --body file://~/environment/aws-modern-application-workshop/module-4/aws-cli/api-swagger.json --fail-on-warnings
```

Copy the response this command returns and save the `id` value for the next step:

```
{
    "name": "MysfitsApi",
    "endpointConfiguration": {
        "types": [
            "REGIONAL"
        ]
    },
    "id": "abcde12345",
    "createdDate": 1529613528
}
```

Now, our API has been created, but it's yet to be deployed anywhere. To deploy our API, we must first create a deployment and indicate which **stage** the deployment is fore.  A stage is a named reference to a deployment, which is a snapshot of the API. You use a Stage to manage and optimize a particular deployment. For example, you can set up stage settings to enable caching, customize request throttling, configure logging, define stage variables or attach a canary release for testing.  We will call our stage `prod`. To create a deployment for the prod stage, execute the following CLI command:

```
aws apigateway create-deployment --rest-api-id wmxn9hti3e --stage-name prod
```

With that, our REST API that's capable of user Authorization is deployed and available on the Internet... but where?!  Your API is available at the following location:

```
https://REPLACE_ME_WITH_API_ID.execute-api.REPLACE_ME_WITH_REGION.amazonaws.com/prod
```

Copy the above, replacing the appropriate values, and add `/mysfits` to the end of the URI.  Entered into a browser address bar, you should once again see your Mysfits JSON response.  But, we've added several capabilities like adopting and liking mysfits that our Flask service backend doesn't have implemented yet.

Let's take care of that next.


### Updating Your Service Backend

To accommodate the new functionality to view Mysfit Profiles, like, and adopt them, we have included updated Python code for your backend Flask web service.  Let's overwrite your existing codebase with these files and push them into the repository:

```
cd ~/environment/MythicalMysfitsService-Repository/
```

```
cp -r ~/environment/aws-modern-application-workshop/module-4/app/* .
```

```
git add .
```

```
git commit -m "Update service code backend to enable additional website features."
```

```
git push
```

While those service updates are being automatically pushed through your CI/CD pipeline, continue on to the next step.

### Editing and Publishing the Website

Open the new version of the Mythical Mysfits index.html file we will push to S3 shortly, it is located at: `~/environment/aws-modern-application-workshop/module-4/app/web/index.html`
In this new index.html file, you'll notice additional HTML and JavaScript code that is being used to add a user registration and login experience.  This code is interacting with the AWS Cognito JavaScript SDK to help manage registration, authentication, and authorization to all of the API calls that require it.

In this file, replace the strings **REPLACE_ME** inside the single quotes with the OutputValues you copied from above and save the file:

![before-replace](/images/module-4/before-replace.png)

Also, for the user registration process, you have an additional two HTML files to insert these values into.  `register.html` and `confirm.html`.  Insert the copied values into the **REPLACE_ME** strings in these files as well.

Now, lets copy these HTML files, as well as the Cognito JavaScript SDK to the S3 bucket hosting our Mythical Mysfits website content so that the new features will be published online.

```
aws s3 cp --recursive ~/environment/aws-modern-application-workshop/module-4/web/ s3://YOUR-S3-BUCKET/
```

Refresh the Mythical Mysfits website in your browser to see the new functionality in action!

This concludes Module 4.

# Module 5: Capturing User Behavior

**Time to complete:** 30 minutes

**Services used:**
* AWS CloudFormation
* AWS Kinesis Firehose
* Amazon S3
* Amazon API Gateway
* AWS Lambda
* AWS CodeCommit
* AWS Serverless Appliation Model (AWS SAM)
* AWS SAM Command Line Interface (SAM CLI)

### Overview
Now that your Mythical Mysfits site is up and running, let's create a way to better understand how users are interacting with the website and its Mysfits.  It would be very easy for us to analyze user actions taken on the website that lead to data changes in our backend - when mysfits are adopted or liked.  But understanding the actions your users are taking on the website *before* a decision to like or adopt a mysfit could help you design a better user experience in the future that leads to mysfits getting adopted even faster.  To help us gather these insights, we will implement the ability for the website frontend to submit a tiny request, each time a mysfit profile is clicked by a user, to a new microservice API we'll create. Those records will be processed in real-time by a serverless code function, aggregated, and stored for any future analysis that you may want to perform.

Modern application design principles prefer focused, decoupled, and modular services.  So rather than add additional methods and capabilities within the existing Mysfits service that you have been working with so far, we will create a new and decoupled service for the purpose of receiving user click events from the Mysfits website. This approach to modular and decoupled microservices should not only apply to the services themselves, but also to infrastructure as code templates.  Infrastructure as code templates and application code repositories that are shared among many different service components can become just as unwieldy and complex as monolithic applications.  Rather than updating the existing service stack that you've been working with in the past few modules, you will create a CloudFormation stack - this will allow all of the components that relate to the streaming stack to exist fully decoupled from the rest of the architecture you've created thus far.

The serverless real-time processing service stack you are creating includes the following AWS resources:
* An **AWS Kinesis Firehose delivery stream**: Kinesis Firehose is a managed real-time streaming service that accepts data records and automatically ingests them into several possible storage destinations within AWS, examples including an Amazon S3 bucket, or an Amazon Redshift data warehouse cluster. Kinesis Firehose also enables all of the records received by the stream to be automatically delivered to a serverless function created with **AWS Lambda** This means that code you've written can perform any additional processing or transformations of the records before they are aggregated and stored in the configured destination.
* An **Amazon S3 bucket**: A new bucket will be created in S3 where all of the processed click event records are aggregated into files and stored as objects.
* An **AWS Lambda function**: AWS Lambda enables developers to write code functions that only contain what their logic requires and have their code be deployed, invoked, and scaled without having to manage infrastructure whatsoever. Here, a Serverless code function is defined using AWS SAM. It will be deployed to AWS Lambda, written in Python, and then process and enrich the click records that are received by the delivery stream.  The code we've written is very simple and the enriching it does could have been accomplished on the website frontend without any subsequent processing  at all.  The function retrieves additional attributes about the clicked on Mysfit to make the click record more meaningful (data that was already retrieved by the website frontend).  But, for the purpose of this workshop, the code is meant to demonstrate the architectural possibilities of including a serverless code function to perform any additional processing or transformation required, in real-time, before records are stored.  Once the Lambda function is created and the Kinesis Firehose delivery stream is configured as an event source for the function, the delivery stream will automatically deliver click records as events to code function we've created, receive the responses that our code returns, and deliver the updated records to the configured Amazon S3 bucket.
* An **Amazon API Gateway REST API**: AWS Kinesis Firehose provides a service API just like other AWS services, and in this case we are using its PutRecord operation to put user click event records into the delivery stream. But, we don't want our website frontend to have to directly integrate with the Kinesis Firehose PutRecord API.  Doing so would require us to manage AWS credentials within on frontend code to authorize those API requests to the PutRecord API, and it would expose to users the direct AWS API that is being depended on (which may encourage malicious site visitors to attempt to add records to the delivery stream that are malformed, or harmful to our goal of understanding real user behavior).  So instead, we will use Amazon API Gateway to create an **AWS Service Proxy** to the PutRecord API of Kinesis Firehose.  This allows us to craft our own public RESTful endpoint that does not require AWS credential management on the frontend for requests. Also, we will use a request **mapping template** in API Gateway as well, which will let us define our own request payload structure that will restrict requests to our expected structure and then transform those well-formed requests into the structure that the Kinesis Firehose PutRecord API requires.
* **IAM Roles**: Kinesis Firehose requires a service role that allows it to deliver received records as events to the created Lambda function as well as the processed records to the destination S3 bucket. The Amazon API Gateway API also requires a new role that permits the API to invoke the PutRecord API within Kinesis Firehose for each received API request.

### Creating the Streaming Service Codebase
This new stack you will deploy using CloudFormation will not only contain the infrastructure environment resources, but the application code itself that AWS Lambda will execute to process streaming events.  To bundle the creation of our infrastructure and code together in one deployment, we are going to use another AWS tool that comes pre-installed in the AWS Cloud9 IDE - the **AWS SAM CLI**.  Code for AWS Lambda functions is delivered to the service by uploading the function code in a .zip package to an Amazon S3 bucket.  The SAM CLI automates that process for us.  Using it, we can create a CloudFormation template that references locally in the filesystem where all of the code for our Lambda function is stored.  Then, the SAM CLI will package it into a .zip file, upload it to a configured Amazon S3 bucket, and create a new CloudFormation template that indicates the location in S3 where the created .zip package has been uploaded for deployment to AWS Lambda.  We can then deploy that SAM CLI-generated CloudFormation template to AWS and watch the environment be created along with the Lambda function that uses the SAM CLI-uploaded code package.  

First, let's create a new CodeCommit repository where the streaming service code will live:
```
aws codecommit create-repository --repository-name MythicalMysfitsStreamingService-Repository
```

In the response to that command, copy the value for `"cloneValueUrl"`.  It should be of the form:
`https://git-codecommit.region-xyz-1.amazonaws.com/v1/repos/MythicalMysfitsStreamingService-Repository`

Next, let's clone that new and empty repository into our IDE:
```
cd ~/environment/
```

```
git clone {insert the copied cloneValueUrl from above}
```

Now, let's move our working directory into this new repository:
```
cd ~/environment/MythicalMysfitsStreamingService-Repository/
```

Then, copy the module-5 application components into this new repository directory:
```
cp -r ~/environment/aws-modern-application-workshop/module-5/app/streaming/* .
```

And let's copy the CloudFormation template for this module as well.

```
cp ~/environment/aws-modern-application-workshop/module-5/cfn/* .
```

Now, we have the repository directory set with all of the provided artifacts:
* A CFN template for creating the full stack.
* A Python script that contains the code for our Lambda function: `streamProcessor.py`

This is a common approach that AWS customers take - to store their CloudFormation templates alongside their application code in a repository. That way, you have a single place where all changes to application and it's environment can be tracked together.

But, if you look at the code inside the `streamProcessor.py` file, you'll notice that it's using the `requests` Python package to make an API requset to the Mythical Mysfits service you created previously.  External libraries are not automatically included in the AWS Lambda runtime environment, because different AWS customers may depend on different versions of various libraries, etc.  You will need to package all of your library dependencies together with your Lambda code function prior to it being uploaded to the Lambda service.  We will use the Python package manager `pip` to accomplish this.  In the Cloud9 terminal, run the following command to install the `requests` package and it's dependencies locally alongside your function code:

```
pip install requests -t .
```

Once this command completes, you will see several additional python package folders stored within your repository directory.  

Next, we have one code change to make prior to our Lambda function code being completely ready for deployment.  There is a line within the `streamProcessor.py` file that needs to be replaced with the ApiEndpoint for your Mysfits service API - the same service ApiEndpoint that you created in module-4 and used on the website frontend.

![replace me](/images/module-5/replace-api-endpoint.png)

That service is responsible for integrating with the MysfitsTable in DynamoDB, so even though we could write a Lambda function that directly integrated with the DynamoDB table as well, doing so would intrude upon the purpose of the first microservice and leave us with multiple/separate code bases that integrated with the same table.  Instead, we will integrate with that table through the existing service and have a much more decoupled and modular application architecture.

Let's commit our code changes to the new repository so that they're saved in CodeCommit:

```
git add .
```

```
git commit -m "New stream processing service."
```

```
git push
```

### Creating the Streaming Service Stack

With that line changed in the Python file, and our code committed, we are ready to use the AWS SAM CLI to package all of our function code, upload it to S3, and create the deployable CloudFormation template to create our streaming stack.

First, use the AWS CLI to create a new S3 bucket where our Lambda function code packages will be uploaded to.  S3 bucket names need to be globally unique among all AWS customers, so replace the end of this bucket name with a string that's unique to you:

```
aws s3 mb s3://mythical-mysfits-streaming-code-bucket-name/
```

With our bucket created, we are ready to use the SAM CLI to package and upload our code and transform the CloudFormation template, be sure to replace the last command parameter with the bucket name you just created above (this command also assumes your terminal is still in the repository working directory):

```
sam package --template-file ./real-time-streaming.yml --output-template-file ./transformed-streaming.yml --s3-bucket replace-with-your-bucket-name
```

If successful, you will see the newly created `transformed-streaming.yml` file exist within the `./cfn/` directory, if you look in its contents, you'll see that the sourceUri parameter of the serverless Lambda function has been updated with the object location where the SAM CLI has uploaded your packaged code.

Also returned by the SAM CLI command is the CloudFormation command needed to be executed to create our new full stack.  But because our stack creates IAM resources, you'll need to add one additional parameter to the command.  Execute the following command to deploy the streaming stack:

```
aws cloudformation deploy --template-file /home/ec2-user/environment/MythicalMysfitsStreamingService-Repository/cfn/transformed-streaming.yml --stack-name MythicalMysfitsStreamingStack --capabilities CAPABILITY_IAM
```

Once this stack creation is complete, the full real-time processing microservice will be created.  

In future scenarios where only code changes have been made to your Lambda function, and the rest of your CloudFormation stack remains unchanged, you can repeat the same AWS SAM CLI and CloudFormation commands as above. This will result in the infrastructure environment remaining unchanged, but a code deployment occurring to your Lambda function.

### Sending Mysfit profile clicks to our new microservice
With the streaming stack up and running, we now need to publish a new version of our Mythical Mysfits frontend that includes the JavaScript that sends events to our service whenever a mysfit profile is clicked by a user.

The new index.html file is included at: `~/environment/aws-modern-application-workshop/module-5/app/web/index.html`

This file contains the same placeholders as module-4 that need to be updated, as well as an additional placeholder for the new stream processing service endpoint you just created.  For the previous variable values, you can refer to the previous `index.html` file you updated as part of module-4.

Perform the following command for the new streaming stack to retrieve the new API Gateway endpoint for your stream processing service:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsStreamingStack
```

Replace the final value within `index.html` for the streamingApiEndpoint and you are ready to publish your final Mythical Mysfits home page update:

```
aws s3 cp ~/environment/aws-modern-application-workshop/module-5/web/index.html s3://YOUR-S3-BUCKET/
```

Refresh your Mythical Mysfits website in the browser once more and you will now have a site that records and publishes each time a user clicks on a mysfits profile!

To view the records that have been processed, they will arrive in the destination S3 bucket created as part of your MythicalMysfitsStreamingStack.  

Now that you have a completed modern application architecture, we encourage you now to explore the AWS Console and all the various services you've created to launch Mythical Mysfits!


### Workshop Clean-Up
Be sure to delete all of the resources created during the workshop in order to ensure that billing for the resources does not continue for longer than you intend.  We reccomend that you utilize the AWS Console to explore the resources you've created and delete them when you're ready.  

For the two cases where you provisioned resources using AWS CloudFormation, you can remove those resources by simply running the following CLI command for each stack:

```
aws cloudformation delete-stack --stack-name STACK-NAME-HERE
```

To remove all of the created resources, you can visit the following AWS Consoles, which contain resources you've created during the MYthical Mysfits workshop:
* [AWS Kinesis](https://console.aws.amazon.com/kinesis/home)
* [AWS Lambda](https://console.aws.amazon.com/lambda/home)
* [Amazon S3](https://console.aws.amazon.com/s3/home)
* [Amazon API Gateway](https://console.aws.amazon.com/apigateway/home)
* [Amazon Cognito](https://console.aws.amazon.com/cognito/home)
* [AWS CodePipeline](https://console.aws.amazon.com/codepipeline/home)
* [AWS CodeBuild](https://console.aws.amazon.com/codebuild/home)
* [AWS CodeCommit](https://console.aws.amazon.com/codecommit/home)
* [Amazon DynamoDB](https://console.aws.amazon.com/dynamodb/home)
* [Amazon ECS](https://console.aws.amazon.com/ecs/home)
* [Amazon EC2](https://console.aws.amazon.com/ec2/home)
* [Amazon VPC](https://console.aws.amazon.com/vpc/home)
* [AWS IAM](https://console.aws.amazon.com/iam/home)
* [AWS CloudFormation](https://console.aws.amazon.com/cloudformation/home)

# Conclusion

This experience was meant to give you a taste of what it's like to be a developer designing and building modern application architectures on top of AWS.  Developers on AWS are able to programmatically provision resources using the AWS CLI, reuse infrastructure definitions via AWS CloudFormation, automatically build and deploy code changes using the AWS developer tool suite of Code services, and take advantage of multiple different compute and application service capabilities that do not require you to provision or manage any servers at all!

As a great next step, to learn more about the inner workings of the Mythical Mysfits website that you've created, dive into the provided CloudFormation templates and the resources declared within them.

We hope you have enjoyed the AWS Modern Application Workshop!  If you find any issues or have feedback/questions, don't hesitate to open an issue or send an email to andbaird@amazon.com.

Thank you!
