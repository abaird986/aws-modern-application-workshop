# Build a Modern Application on AWS (Python)

**AWS Experience: Beginner**

**Time to Complete: 2-3 hours**

**Cost to Complete: Many of the services used are included in the AWS Free Tier. For those that are not, the sample application will cost, in total, less than $1/day. **

**Tutorial Prereqs:**

* **An AWS Account and Administrator-level access to it**

Please be sure to terminate all of the resources created during this workshop to ensure that you are no longer charged.

**Note:**  Estimated workshop costs assume little to no traffic will be served by your demo website created as part of this workshop.

### **Overview**

AWS provides all the services and features required for a developer to create a modern application, and the tools to build it using modern development methodologies.  This tutorial will walk you through the steps to create a sample web application that leverages concepts and approaches such as containers, infrastructure as code, CI/CD, and serverless.  You will build, from the ground up, a sample website called **Mythical Mysfits** that enables visitors to adopt a fantasy creature as a pet.  You can see a working sample of this website available at: www.mythicalmysfits.com

The site will present *mysfits* available for adoption with some different characteristics about each. Users will be able to vote on which mysfits are their favorites, and then choose to adopt the mysfit they'd like to reserve for adoption.  The Mythical Mysfits website you create will also allow you to gather insights about user behavior for future analyses.

This sample application will use many different AWS services and features that modern applications leverage on AWS. But, learning about *what* those individual services and their features are is not the primary objective of this workshop.  Instead, this workshop is meant to give you an experience of *how* developers are able to use developer tools and services provided by AWS throughout the SDLC of their modern applications.

### Application Architecture

The Mythical Mysfits website serves it's static content directly from Amazon S3, provides a microservice API backend deployed as a container through AWS Fargate on Amazon ECS, stores data in a managed NoSQL database provided by Amazon DynamoDB, with authentication and authorization for the application enabled through AWS API Gateway and it's integration with Amazon Cognito.  The user website clicks will be sent as records to an Amazon Kinesis Firehose Delivery stream where those records will be processed by serverless AWS Lambda functions and then stored in Amazon S3.

You will be creating and deploying changes to this application completely programmatically.  We have provided AWS CloudFormation templates that define the required infrastructure components as code, which includes a fully managed CI/CD stack utilizing AWS CodeCommit, CodeBuild, and CodePipeline.  Finally, you will complete the development tasks required all within your own browser by leveraging the cloud-based IDE, AWS Cloud9.

So, you will not be manually creating each individual resource inside AWS, completed CloudFormation templates will instead do that work for you.  In order to dive deeper into the service and their features that the Mythical Mysfits website uses, you should review these CloudFormation templates as needed. CloudFormation allows AWS developers to declaratively define their full AWS environments as JSON or YAML files. So all of the required features and services that your application will use are there for you to see and review inside the provided templates.

# Module 1: IDE Setup and Static Website Hosting

**Time to complete:** 20 minutes

**Services used:**
* AWS Cloud9
* AWS CloudFormation
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


Click “Create Environment”:
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

Next, we will create the infrastructure components needed for hosting a static website in Amazon S3 via AWS CloudFormation.  In the cloned repository, we have included a CloudFormation template that can create the Amazon S3 bucket required, as well as configure it to be usable for static website hosting.  To create the stack represented by the CloudFormation template, run the following CloudFormation command via the AWS Command Line Interface:

```
aws cloudformation create-stack --stack-name MythicalMysfitsWebsiteBucket --template-body file://~/environment/aws-modern-application-workshop/module-1/cfn/s3-website.yml
```

The output of this command will indicate a new stack is being created by CloudFormation with the StackId in the response:

```
{
    "StackId": "arn:aws:cloudformation:us-east-1:xxxx:stack/MythicalMysfitsWebsiteBucket/xxxx"
}
```

You can either visit the CloudFormation console to view the creation status of your stack, or execute the following CLI command:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsWebsiteBucket
```

When you see the StackStatus of “CREATE_COMPLETE”, your S3 bucket has been created.  Find the “Outputs” object within the response to find the HTTPS URL that you can use to access your new website, save this for reference.  Also, within the URL you can find the name of the S3 bucket that has been created.  Save this for reference as well, the bolded section below represents the bucket name that can be found within the Output S3BucketSecureURL:

```
{
    "Description": "Name of S3 bucket to hold website content",
    "OutputKey": "S3BucketSecureURL",
    "OutputValue": "https://**mythicalmysfitswebsitebucket-s3bucket-xxxxx**.amazonaws.com"
}
```


Now we need to copy the first version of Mythical Mysfits homepage to the bucket.  This is included as an index.html file within the /module-1/web/ directory of the repository you cloned.  We will accomplish this using the AWS CLI using the following command, which will use the S3 bucket name that you save from above (the bolded component):

```
aws s3 cp ./module-1/web/index.html s3://**mythicalmysfitswebsitebucket-s3bucket-xxxx**/index.html
```

Now, if you visit the full URL saved earlier, you can see that the initial Mythical Mysfits website is up and running!

[TODO include image of website]

That concludes Module 1.


# Module 2: Creating a Service with AWS Fargate

**Time to complete:** 60 minutes

**Services used:**
* AWS CloudFormation
* AWS Identity and Access Management (IAM)
* Amazon Virtual Private Cloud (VPC)
* Amazon Elastic Load Balancing
* Amazon Elastic Container Service (ECS) with AWS Fargate
* AWS Elastic Container Registry (ECR)
* AWS CodeCommit
* AWS CodePipeline
* AWS CodeDeploy
* AWS CodeBuild


### Overview

In Module 2, you will create a new microservice hosted with AWS Fargate on Amazon Elastic Container Service so that your Mythical Mysfits website can have a application backend to integrate with. AWS Fargate is a feature of Amazon ECS that allows you to deploy containers without having to manage any clusters or servers. For our Mythical Mysfits backend, we will use Python and create a Flask app in a Docker container behind a Network Load Balancer. These will form the microservice backend for the frontend website to integrate with.

### Creating the Core Infrastructure

Before we can create our service, we need to create the core infrastructure environment that the service will use, including the networking infrastructure in Amazon VPC, and the AWS Identity and Access Management Roles that will define the permissions that ECS and our containers will have on top of AWS.  It is common on many teams to have separate teams with elevated access in AWS that are responsible for creating and modifying Network and Security resources. We have followed that model here to demonstrate how CloudFormation can help enforce separation of duties on AWS for your team through modular templates.  We have provided a CloudFormation template to create all of the necessary Network and Security resources in /module-2/cfn/core.yml.  This template will create the following resources:

* **An Amazon VPC** - a network environment that contains four subnets (two public and two private) in the 10.0.0.0/16 private IP space, as well as all the needed Route Table configurations.
* **Two NAT Gateways** (one for each public subnet) - allows the containers we will eventually deploy into our private subnets to communicate out to the Internet to download necessary packages, etc.
* **A DynamoDB Endpoint** - our microservice backend will eventually integrate with Amazon DynamoDB for persistence (as part of module 3).
* **A Network Load Balancer** - A high throughput and low latency TCP load balancer that will route requests from the Internet to your service containers.
* **A Security Group** - Allows your docker containers to receive traffic on port 8080 from the Internet through the Network Load Balancer.
* **Two IAM Roles** - Two Identity and Access Management Roles are created. One for the Amazon ECS service that allow it to interact with the infrastructure environment as needed. Another that will provide your docker containers with the permissions they require for interacting with AWS services like DynamoDB and CloudWatch Logs.

To create these resources, run the following command in the Cloud9 terminal (will take ~10 minutes for stack to be created):

```
aws cloudformation create-stack --stack-name MythicalMysfitsCoreStack --capabilities CAPABILITY_IAM --template-body file://~/environment/aws-modern-application-workshop/module-2/cfn/core.yml   
```

Remember you can check on the status of your stack creation either via the AWS Console or by running the command:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsCoreStack
```

### Creating your First Docker Image

Next, you will create a docker container image that contains all of the code and configuration required to run the Mythical Mysfits backend as a microservice API created with Flask.  We will build the docker container image within Cloud9 and then push it to the Amazon Elastic Container Registry, where it will be available to pull when we create our service using Fargate.

All of the code required to run our service backend is stored within the `/module-2/app/` directory of the repository you've cloned into your Cloud9 IDE.  If you would like to review the Python code that uses Flask to create the service API, view the `/module-2/app/service/mythicalMysfitsService.py` file.

Docker comes already installed on the Cloud9 IDE that you've created, so in order to build the docker image locally, all we need to do is run the following commands in the Cloud9 terminal:

* First change directory to ~/environment/module-2/app

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
Successfully tagged **111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest**
```

Let's test our image locally within Cloud9 to make sure everything is operating as expected. Copy the image tag that resulted from the previous camm and run the following command to deploy the container “locally” (which is actually within your Cloud9 IDE inside AWS!):

```
docker run -p 8080:8080 **111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest**
```

As a result you will see docker reporting that your container is up and running locally:

```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

To test our service with a local request, we're going to open up the build-in web browser within the Cloud9 IDE that can be used to preview applications that are running on the IDE instance.  To open the preview web browser, select **Preview > Preview Running Application** in the Cloud9 menu bar:

![preview-menu](/images/module-2/preview-menu.png)

This will open another panel in the IDE where the web browser will be available.  Append /mysfits to the end of the URI in the address bar of the preview browser and hit enter:

![preview-menu](/images/module-2/address-bar.png)

If successful you will see a response from the service that returns the JSON document stored at `/modern-application-workshop/module-2/app/service/mysfits-response.json`

With a successful test of our service locally, we're ready to create a container image repository in Amazon ECR and push our image into it.  In order to create the registry, run the following command, this creates a new repository in the default AWS ECR registry created for your account.

```
aws ecr create-repository --repository-name mythicalmysfits/service
```

The response to this command will contain additional metadata about the created repository.
In order to push container images into our new repository, we will need to obtain authentication credentials for our Docker client to the repository.  Run the following command, which will return a login command to retrieve credentials for our Docker client and then automatically execute it (include the full command including the $ below). 'Login Succeeded' will be reported if the command is successful.

```
$(aws ecr get-login --no-include-email)
```

Next, push the image you created to the Amazon ECR repository using the copied tag from above. Using this command, docker will push your image and all the images it depends on to Amazon ECR:

```
docker push 111111111111.dkr.ecr.us-east-1.amazonaws.com/mythicalmysfits/service:latest
```

Run the following command to see your newly pushed docker image stored inside the ECR repository:

```
aws ecr describe-images --repository-name mythicalmysfits/service
```

### Creating your first Fargate Service

Now,  we have an image available in ECR that we can deploy to a service hosted on Amazon ECS using AWS Fargate.  The same service you tested locally via the terminal in Cloud9 as part of the last module will now be deployed in the cloud and publicly available behind a Network Load Balancer.  We have provided a CloudFormation template to accomplish this, representing all of the infrastructure you need as code.  This CloudFormation template will create the following resources:

* **An ECS Cluster**: The cluster of “servers” that your service containers will be deployed to.  Servers is in quotations here because you will in fact be using AWS Fargate, which allows you to specify that your containers be deployed to a cluster without having to actually provision or manage any servers yourself.
* **An AWS CloudWatch Logs Group**: The logs that your container generates will automatically be pushed to AWS CloudWatch logs as part of this group. Especially important when using AWS Fargate since you will not have access to the server infrastructure where your containers are running.
* **An ECS Task Definition** A Task in ECS defines one or more containers that are deployed together to a cluster and the resources and configuration options that those containers require to run.  The container included in this task definition is the image that we pushed into ECR as part of the last module.
* **An ECS Service** The service itself.  Here we define that the Task above will be what is deployed and run as the service, that the Tasks should be deployed to Fargate so that they may be run serverless, indicate that this service and it's containers should be registered to the network load balancer and allow the traffic we permitted in the Security Groups created with the core.yml CloudFormation template used in Module 2A.

To create these resources using the CloudFormation template included, run the following command in the Cloud9 terminal:

```
aws cloudformation create-stack --stack-name MythicalMysfitsServiceStack --template-body file://~/environment/aws-modern-application-workshop/module-2/cfn/service.yml
```

Once the stack has been created, let's try sending a request to the network load balancer (NLB) to confirm our service is up and available.  To find the URL of the NLB, execute the following command in the terminal to see the outputs we have configured in the MythicalMysfitsCoreStack we created earlier with CloudFormation:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsCoreStack
```

In the response JSON, you will see an Output listed called “ExternalUrl”, whose OutputValue is the URL to be used to send a request to the created NLB.  See below:

```
{
  "Description": "The url of the external load balancer",
  "ExportName": "MythicalMysfitsCoreStack:ExternalUrl",
  "OutputKey": "ExternalUrl",
  "OutputValue": "**http://Mythi-Publi-123456789-abc123456.elb.us-east-1.amazonaws.com**"
}
```

Let's copy that URL and send a request to it using the preview browser (or by simply any web browser, since this time our service is available on the Internet with the retrieved URL):

```
http://Mythi-Publi-123456789-abc123456.elb.us-east-1.amazonaws.com/mysfits
```

A response showing the same JSON response we received earlier when testing the docker container locally in Cloud9 means your Flask API is up and running on AWS Fargate.

Next, we need to integrate our website with your new API backend instead of using the hard coded data that we previously uploaded to S3.  You'll need to update the following file to use the same NLB URL for API calls (do not inlcude the /mysfits path): /module-2/web/index.html
Open the file in Cloud9 and replace the highlighted area below between the quotes with the NLB URL:

![before replace](/images/module-2/before-replace.png)

After pasting, the line should look similar to below:

![after replace](/images/module-2/after-replace.png)

To upload this file to your S3 hosted website, use the bucket name again that was created during Module 1, and run the following command:

```
aws s3 cp ~/environment/modern-application-workshop/module-2/web/index.html s3://INSERT-YOUR-BUCKET-NAME/index.html
```

 Open your website using the same URL used at the end of Module 1 in order to see your new Mythical Mysfits website, which is retrieving JSON data from your Flask API running within a docker container deployed to AWS Fargate!

### Automating Deployments using AWS Code Services

Now that you have a service up and running, you may think of code changes that you'd like to make to your Flask service.  It would be a bottleneck for your development speed if you had to go through all of the same steps above every time you wanted to deploy a new feature to your service. That's where Continuous Integration and Continuous Delivery or CI/CD come in!

In this module, you will create a fully managed CI/CD stack that will automatically deliver all of the code changes that you make to your code base to the service you created during the last module.  To help you accomplish this, we have included another CloudFormation template that will create the following resources for you:

* **An AWS CodeCommit Repository**: A fully managed and private Git repository where your code will be stored.
* **An AWS CodeBuild Project**: Will automatically provision a build server to our configuration and execute the steps required to build our docker image and push a new version of it to the ECR repository we created.  These steps are included in the `/module-3/app/buildspec.yml` file.  The **buildspec.yml** file is what you create to instruct CodeBuild what steps are required for a build execution within the service.
* **An Amazon ECR Repository***: We will recreate the repository you created by through the command line during the last module so that all of the pieces of our CI/CD stack can be represented by the same CloudFormation template.
* An AWS CodePipeline Pipeline: Orchestrates the entire CI/CD process from beginning to end.  Detects when changes are pushed into our CodeCommit repository, triggers a build to occur for those changes in our CodeBuild project, and then takes those completed changes and deploys them to the ECS service we created above in Module 2.
* IAM Roles - IAM roles required for the services above to execute within your account with the required permissions.

First, let's delete the repository you created by hand during the last module so that CloudFormation can create it anew as part of this holistic CI/CD stack.  Run the following in the terminal:

```
aws ecr delete-repository —repository-name mythicalmysfits/service —force
```

**Note:** In a real-world scenario, you would more typically create this CI/CD stack as development begins and then create the service stack once you need to first deploy the code you've written.  But, for this workshop we had you create the service first to become familiar with its concepts before deploying to it with automation.

To use CloudFormation to create the CI/CD stack for your Mythical Mysfits service, run the following command in the terminal:

```
aws cloudformation create-stack --stack-name MythicalMysfitsCICDStack --capabilities CAPABILITY_NAMED_IAM --template-body file://~/environment/aws-modern-application-workshop/module-2/cfn/devtools.yml
```

When that stack has been created successfully, we first must integrate our Cloud9 IDE with the new CodeCommit code repository that was just created.

First, we need to generate git credentials to interact with the created repository. AWS CodeCommit provides a credential helper for git that we will use to make integration easy.  Run the following commands in sequence the terminal (neither will report any response if successful):

```
`git config --global user.name "*Your Name*"`
```

```
git config --global user.email your.name*`@example.*com*`*
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

Now, we are ready to clone our repository using the following terminal command (be sure to replace us-east-1 with the region you are using for the workshop, if needed):

```
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/MythicalMysfitsService-Repository
```

This will tell us that our repository is empty!  Let's fix that by copying the application files into our repository directory using the following command:

```
cp -r ~/environment/modern-application-workshop/module-2/app/* ~/environment/MythicalMysfitsService-Repository/
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

**Time to complete:** 30 minutes

**Services used:**
* AWS CloudFormation
* Amazon DynamoDB

### Overview

Now that you have a service deployed and a working CI/CD pipeline to deliver changes to that service automatically whenever you update your code repository, you can quickly move new application features from conception to available for your Mythical Mysfits customers.  With this increased agility, let's add another foundational piece of functionality to the Mythical Mysfits website architecture, a data tier.  In this module you will create a table in Amazon DynamoDB, a managed and scalable NoSQL database service on AWS with super fast performance.  Rather than have all of the Mysfits be stored in a static JSON file, we will store them in a database to make the websites future more extensible and scalable.

### Creating A DynamoDB Table using CloudFormation

To add the DynamoDB table to the architecture, we have included another CloudFormation template that contains the resource definition required to create a table called **MysfitsTable**. This table will have a primary index defined by a hash key attribute called **MysfitId**, and two more secondary indexes.  The first secondary index will have the hash key of **Species** and a range key of **MysfitId**, and the second secondary index will have the hash key of **Alignment** and a range key of **MysfitId**.  These two secondary indexes will allow us to execute queries against the table to retrieve all of the mysfits that match a given Species or Alignment to enable the filter functionality you may have noticed isn't yet working on the website.

To create the table using CloudFormation, execute the following command in the Cloud9 terminal:

```
aws cloudformation update-stack --stack-name MythicalMysfitsServiceStack --template-body file://~/environment/aws-modern-application-workshop/module-3/cfn/service-with-ddb.yml
```

After the stack completes updating, you can view your newly created table either in the DynamoDB  console or by executing the following AWS CLI command in the terminal:

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
aws dynamodb batch-write-item --request-items file://~/environment/modern-application-workshop/lib/populate-dynamodb.json
```

Now, if you run the same command to scan all of the table contents, you'll find the items have been loaded into the table:

```
aws dynamodb scan --table-name MysfitsTable
```

### Committing your first *real* Code change

Now that we have our data included in the table, let's modify our application code to read from this table instead of returning the static JSON file response that was used in Module 2.  We have included a new set of Python files for your Flask microservice, but now instead of reading the static JSON file will make a request to DynamoDB.

The request is formed using the AWS Python SDK called **boto3**. This SDK is a powerful yet simple way to interact with AWS services via Python code. It enables you to use service client definitions and functions that have great symmetry with the AWS APIs and CLI commands you've already been executing as part of this workshop.  Translating those commands to working Python code is simple when using **boto3**.  To copy the new files into your CodeCommit repository directory, execute the following command in the terminal:

```
cp ~/environment/modern-application-workshop/module-3/app/service/* ~/environment/MythicalMysfitsService-Repository/service/
```

Now, we need to check in these code changes to CodeCommit using the git command line client.  Run the following commands to check in the new code changes and kick of your CI/CD pipeline:

```
cd ~/environment/MythicalMysfitsRepository
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

Finally, we need to publish a new index.html page to our S3 bucket so that the new API functionality using query strings to filter responses will be used.  The new index.html file is located at ~/environment/modern-application-workshop/module-3/web/index.html.  Open this file in your Cloud9 IDE and replace the string indicating “REPLACE_ME” just as you did in Module 1, with the appropriate NLB endpoint.  Refer to the file you already edited in the /module-1/ directory if you need to.  After replacing the endpoint to point at your NLB, upload the new index.html file by running the following command (replacing with the name of the bucket you created in Module 1:

```
aws s3 cp ~/environment/modern-application-workshop/module-3/web/* s3://{your_bucket_here}/
```

Re-visit your Mythical Mysfits website to see the new population of Mysfits loading from your DynamoDB table and how the Filter functionality is working!

That concludes module 3.

# Module 4: Adding User and API features with Amazon API Gateway and AWS Cognito

**Time to complete:** 40 minutes

**Services used:**
* AWS CloudFormation
* Amazon Cognito
* Amazon API Gateway
* Amazon Simple Storage Service (S3)

### Overview

### Creating the API and User pool

In order to add some more critical aspects to the Mythical Mysfits website, like allowing users to vote for their favorite mysfit and adopt a mysfit, we need to first have users register on the website.  To enable registration and authentication of website users, we will create a User Pool in AWS Cognito - a fully managed user identity management service.  Then, to make sure that only registered users are authorized to like or adopt mysfits on the website, we will deploy an API with Amazon API Gateway to sit in front of our network load balancer. Amazon API Gateway is also a managed service, and provides critical REST API capabilities out of the box like SSL termination, request authorization, request throttling, and much more.
You will again use infrastructure as code through CloudFormation to deploy the needed resources to AWS. The CloudFormation template for this module is stored at `/module-4/cfn/service-with-apigw`. It contains the same resources as the previous Service CloudFormation templates with the following additions:

* The **Cognito User Pool** described above.
* The **Amazon API Gateway REST API** described above.
* An **Amazon API Gateway VPC Link** that enables APIs created with API Gateway to privately communicate with a service fronted by a Network Load Balancer like we deployed during this workshop.  **Note:** For the purposes of this workshop, we created the NLB to be internet-facing so that it could be called directly in earlier modules. Because of this, even though we will be requiring Authorization tokens in our API after this module, our NLB will still actually be open to the public behind the API Gateway API.  In a real-world scenario, you should create your NLB to be internal from the beginning, knowing that API Gateway would be your strategy for Internet-facing API authorization.

Another change to this CloudFormation template is that it uses the AWS **Serverless Application Model (SAM)** to define the new API. You can see this by looking at the second line of the template, where a Transform declaration is made.

```
Transform: AWS::Serverless-2016-10-31
```

AM gives us the ability to simply define serverless resources like APIs and Lambda functions using simplified resource definitions in JSON or YAML.  SAM also provides additional capabilities related to the packaging and testing of Lambda functions, which you'll see later in Module 5. The Transformation declaration above tells CloudFormation that our template should be transformed using the specified version of SAM.  For this module, we'll use SAM to let us define our API in-line using a Swagger 2.0 definition.  
In order to push this update out to the service stack in CloudFormation, we'll use a different command than before, called **deploy**.

This command will take the SAM template that we have created and transform it into typical CloudFormation, generate the **change set** to be applied to our stack (indicating which resources in the stack will be created, modified or deleted), then subsequently execute the changes to the stack using the same update-stack command we used in the last module.  To add the Cogntio User Pool and API Gateway API to our service stack run the following command in your terminal:

```
aws cloudformation deploy --stack-name MythicalMysfitsServiceStack --template-file ~/environment/modern-application-workshop/module-4/cfn/service-with-apigw.yml
```

Once the stack has updated, run the following command to show the Output of the CloudFormation stack.  This latest version includes an Output of the REST API endpoint for your newly deployed API, as swell as additional outputs related to the Cognito UserPool and Cognito Client that have been created:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsServiceStack
```

Below is an example output you should find in the response to the above command for the ApiEndpoint:

```
{
    "Description": "The endpoint for the REST API created with API Gateway",
    "OutputKey": "ApiEndpoint",
    "OutputValue": "https://abcde12345.execute-api.us-east-1.amazonaws.com/prod"
}
```

Copy the OutputValue listed for the OutputKeys of ApiEndpoint, UserPoolId, and UserPoolClientId and save them to a text editor or similar so that you can reference them in the next step.

### Editing and Publishing the Website

Open the new version of the Mythical Mysfits index.html file we will push to S3 shortly, it is located at: **~/environment/modern-application-workshop/module-4/app/web/index.html**
In this new index.html file, you'll notice additional HTML and JavaScript code that is being used to add a user registration and login experience.  This code is interacting with the AWS Cognito JavaScript SDK to help manage registration, authentication, and authorization to all of the API calls that require it.

In this file, replace the strings 'REPLACE_ME' inside the single quotes with the endpoint OutputValues you copied from above and save the file:

![before-replace](/images/module-4/before-replace.png)

Now, lets copy this file, as well as the Cognito JavaScript SDK to the S3 bucket hosting our Mythical Mysfits website content so that the new features will be published online.

```
aws s3 cp ~/environment/modern-application-workshop/module-4/web/* s3://YOUR-S3-BUCKET/
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

Modern application design principles prefer focused, decoupled, and modular services.  So rather than add additional methods and capabilities within the existing Mysfits service that you have been working with so far, we will create a new and decoupled service for the purpose of receiving user click events from the Mysfits website. This approach to modular and decoupled microservices should not only apply to the services themselves, but also to infrastructure as code templates.  Infrastructure as code templates and application code repositories that are shared among many different service components can become just as unwieldy and complex as monolithic applications.  Rather than updating the existing service stack that you've been working with in the past few modules, you will create a new CloudFormation stack - this will allow all of the components that relate to the streaming stack to exist fully decoupled from the rest of the architecture you've created thus far.

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
aws codecommit create-respository --repository-name MythicalMysfitsStreamingService-Repository
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
cp r ~/environment/aws-modern-application-workshop/module-5/app/streaming/* .
```

Now, we have the repository directory set with all of the provided artifacts:
* A CFN template for creating the full stack.
* A Python script that contains the code for our Lambda function: `streamProcessor.py`

But, if you look at the code inside the `streamProcessor.py` file, you'll notice that it's using the `requests` Python package to make an API requset to the Mythical Mysfits service you created previously.  External libraries are not automatically included in the AWS Lambda runtime environment.  You will need to package all of your library dependencies together with your Lambda code function prior to it being uploaded to the Lambda service.  We will use the Python package manager `pip` to accomplish this.  In the Cloud9 terminal, run the following command to install the `requests` package and it's dependencies locally alongside your function code:

```
pip install requests -t .
```

Once this command completes, you will see several additional python package folders stored within your repository directory.  

Next, we have one code change to make prior to our Lambda function code being completely ready for deployment.  There is a line within the `streamProcessor.py` file that needs to be replaced with the ApiEndpoint for your Mysfits service API - the same service ApiEndpoint that you created in module-4 and used on the website frontend.

~[replace me](/images/module-5/replace-api-endpoint.png)

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
aws s3 mb s3://mythical-mysfits-streaming-code-uniquestringhere/
```

With our bucket created, we are ready to use the SAM CLI to package and upload our code and transform the CloudFormation template, be sure to replace the last command parameter with the bucket name you just created above (this command also assumes your terminal is still in the repository working directory):

```
sam package --template-file ./cfn/real-time-streaming.yml --output-template-file ./cfn/transformed-streaming.yml --s3-bucket replace-with-your-bucket-name
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

This file contains the same placeholders as module-4 that need to be updated, as well as an additional placeholder for the new stream processing service endpoint you just created.  For the previous variable values, you can either refer to the previous `index.html` file you updated as part of module-4, or refer back to the AWS CloudFormation Stack created as part of module-4:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsServiceStack
```

Perform the same command for the new streaming stack to retreieve the new API Gateway endpoint for your stream processing serivce:

```
aws cloudformation describe-stacks --stack-name MythicalMysfitsStreamingStack
```

Replace the final value within `index.html` for the streamingApiEndpoint and you are ready to publish your final Mythical Mysfits home page update:

```
aws s3 cp ~/environment/aws-modern-application-workshop/module-5/app/web/index.html s3://YOUR-S3-BUCKET/
```

Refresh your Mythical Mysfits website in the browser once more and you will now have a site that records and publishes each time a user clicks on a mysfits profile!

To view the records that have been processed, they will arrive in the destination S3 bucket created as part of your MythicalMysfitsStreamingStack.  

Now that you have a completed modern application architecture, we encourage you now to explore the AWS Console and all the various services you've created to launch Mythical Mysfits!


### Workshop Clean-Up
Our use of CloudFormation makes cleanup of your workshop artifacts easy, you simply need to delete the stacks created during the workshop, and all of the resources we've created will be deleted.  *However*, there are some resources that CloudFormation will not programmatically delete if they still contain other created resources - in our case this includes S3 buckets, and our Elastic Container Registry repositories.
Navigate to the S3 console and delete any buckets created there, and the ECS console to delete the created repositories.  Also keep in mind that we created our Lambda function code package without the use of CloudFormation, so it should be deleted by hand in the Console as well.

Once that is completed, you can delete the other CloudFormation stacks we've created. Because some of our created stacks have dependencies on previous stacks that you created, you should delete them in **reverse order** of how they were created (StreamingStack -> ServiceStack -> CICDStack -> CoreStack) using either the CloudFormation Console, or the following CLI command for each:

```
aws cloudformation delete-stack --stack-name STACK-NAME-HERE
```

# Conclusion

This experience was meant to give you a taste of what it's like to be a developer designing and building modern application architectures on top of AWS.  Developers on AWS are able to programmatically provision and reuse infrastructure definitions via AWS CloudFormation, automatically build and deploy code changes using the AWS developer tool suite of Code services, and take advantage of multiple different compute and appliation service capabilities that do not require you to provision or manage any servers at all!

As a great next step, to learn more about the inner workings of the Mythical Mysfits website that you've created, dive into the provided CloudFormation templates and the resources declared within them.

We hope you have enjoyed the AWS Modern Application Workshop!  If you have any feedback or questions, don't hesitate to post a comment or send an email to andbaird@amazon.com.

Thank you!
