# Manual deployment of a Python Lambda function

## Requirements

- The AWS tools (`pip install awscli`) and [credentials](http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html) already set up
- Select one AWS region to deploy your instance to (`my-aws-region`)

## Steps

### Create the code package

For example, one provided in the file `hello_python.py`:

```python
def my_handler(event, context):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])
    return { 'message' : message }
```

Create the `.zip` package:

```
zip deployment-package.zip hello_python.py
```

### Create the appropriate IAM role and attach the policy

```
aws iam create-role \
--role-name my_basic_execution_role \
--assume-role-policy-document '{ "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }'
```

Take note of the role arn (`role-arn`). Then, attach the policy that grants basic execution of Lambda:

```
aws iam attach-role-policy --role-name my_basic_execution_role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### Upload the package

```
aws lambda create-function \
--region <my-aws-region> \
--function-name HelloPython \
--zip-file fileb://deployment-package.zip \
--role <role-arn> \
--handler hello_python.my_handler \
--runtime python3.6 \
--timeout 15 \
--memory-size 512
```

The lambda function is up and running! Take note of the `FunctionArn` (`function-arn`)

### Test the function

Invoke the lambda function with an input event as payload:

```
aws lambda invoke \
--function-name <function-arn> \
--payload '{"first_name":"Margaret", "last_name":"Hamilton"}'
out.json
```

The output of the function will be inside `out.json`:

```
{"message": "Hello Margaret Hamilton!"}
```
