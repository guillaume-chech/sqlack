# Sqlack

A serverless Postgresql client built for slack slash command integration.
## Getting Started

Clone this repository on your local system.

`git clone https://github.com/heetch/sqlack.git`

### Prerequisites and Installation
To install and run the app you'll need Python 3.7 and node 12.15.0.

You need to get the serverless framework working on your machine.
To get serverless and upgrade plugins run.
```
npm install -g serverless
```
and then
```
npm install
```

You will also need to setup your AWS credentials. Usually you should have a `~/.aws/config` file somewhere with your keys stored. If not get your hands on yours access and secret keys and run .
```
serverless config credentials
```
 or follow this guide if you want a more in depth walkthrough :
https://serverless.com/framework/docs/providers/aws/guide/credentials/

You'll finally need to install the requirements 
```
pip install -r requirements.txt
```

## Deployment

Simply hit this command, stage can be dev or prod and will defer in the secret and log level.

```
serverless deploy --stage dev --verbose
```
## Secrets
Secrets must be store in the `secrets.dev.yml` and `secrets.prod.yml` files. Those files are usually writen during CI stage. You can modify this logic by using env variable or AWS SSM if you wish . The logic is written in the serverless.yml file and transcript the files into env variable.