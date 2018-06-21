# Build a Modern Application on AWS (Python)

![mysfits-welcome](/images/module-1/mysfits-welcome.png)

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

[Proceed to Module 1](/module-1)


### Workshop Clean-Up (Once Complete)
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
