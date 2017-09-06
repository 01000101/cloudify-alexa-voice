[![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow&nbsp;&#64;JoscorLLC)](https://twitter.com/JoscorLLC)

# Alexa Voice Control for Cloudify

This is the code repository for an Alexa Skill that interacts with a Cloudify manager. It's meant to
be an example for others to build Alexa Skills and it's just a neat app for Cloudify users.


## Sample Usage

*Alexa, ask Cloudify if it's running*

*Alexa, ask Cloudify what version it's on*

*Alexa, ask Cloudify how many blueprints are installed*

*Alexa, ask Cloudify how many executions are running*



## Installation

### Prerequisite reading material

If you're not familiar with the process of creating an Alexa Skill or have never used
AWS Lambda before, read the following articles:

* https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function
* http://moduscreate.com/build-an-alexa-skill-with-python-and-aws-lambda/


### Using Alexa Skills schema files

The included `alexa-skill-intent-schema.json` and `alexa-skill-sample-utterances.txt` files
are there for quick copy and paste into the Alexa Skills application
*Interaction Model* area. Simple copy and paste the data from
`alexa-skill-intent-schema.json` to *Intent Schema* and
`alexa-skill-sample-utterances.txt` to *Sample Utterances*.

There are no *Custom Slot Types* in this example but feel free to add some and extend
this project!


### Building AWS Lambda application

* Install requirements to the `lambda` directory itself by executing
  `pip install -r lambda/requirements.txt -t lambda/` assuming you're in the
  project root directory.
* Change the values for `VALID_APP_IDS` and `CFY_ENDPOINT` in `lambda.py` to
  fit your needs. Note: in most cases, you should add to `VALID_APP_IDS` your
  Alexa Skills ID and leave the placeholder there since the Alexa Skills
  test function has an ID of (literally) `amzn1.ask.skill.[unique-value-here]`.
* ZIP up the *contents* of the `lambda` directory (not including the directory itself).
* Create a new Lambda application using the ZIP file you just created. The function
  entry point will be `lambda.lambda_handler`.
* If you run a test, you should get back "Sorry, I did not understand the request".

