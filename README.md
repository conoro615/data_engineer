Small section with comments and assumptions for questions.


## Question 1

Decided to opt for the [fixer.io](https://fixer.io/) API instead of the [Coindesk](https://www.coindesk.com/coindesk-api) as the data returned was pretty much identical so using both would be redundant. The fixer API involved a little bit more transforming the data so I wanted to show some more of that.

In terms of practical usage, a simple daily conversion table with US Dollar, British Sterling and Bitcoin all based in Euro is what I imagined this to be used for, and to track the daily rates through further analysis.

I used a local Postgres DB to test my code and changed it to the consciousgrowth.1234.com server at the end so the code wont work without a proper DB connection.

The script is divided into functions outlining the Extract, Transform and Load aspects of the task. I used Pandas for the transformations and Sqlalchemy for the DB load.

Throughout the code I added comments and console outputs for easy human readability and testing, I imagine in a more fleshed out implementation of this, the console logging would be pushed as an email upon completion or failure. 


## Question 2

By far the trickiest section for me, not only have I not much recent experience using Oauth2, the Oauth endpoint didn't exist so most of the code is mostly hypothetical. For me the main thing I wanted to show was the acquisition, usage and refreshment of access tokens, which is one of the main features of Oauth2. Most of the code is similar to Question 1 in terms of transformations and loading steps of the process. Some more typical Oauth2 implementations involves opening a redirect URL in a web browser and receiving a manual authorization code, I omitted this as this should be a automated process involving no human interaction and an API endpoint having this would be problematic to say the least.

## Question 3

The two main aspects of this question is :
- Where/How the script would be executed 
- Where would the DB exist

I opted for using AWS as a solution for this section, with a cheap but lightweight option or a more expensive but stronger and safer implementation using [RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html).
Using [AWS Batch](https://aws.amazon.com/batch/), I would run the process from inside a [docker container](https://www.docker.com/resources/what-container) from an [EC2 instance](https://aws.amazon.com/ec2/).
Decided not to go too deep into configuration, but lay out the main features of the implementation which would normally be outlined in a typical design meeting.
