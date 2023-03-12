import pulumi
import pulumi_aws as aws
import pulumi_aws_native as aws_native
import pulumi_awsx as awsx
import json

# task role
task_role = aws.iam.Role(
    "app-task-role",
    inline_policies=[
        aws.iam.RoleInlinePolicyArgs(
            # name="app-task-role-policy",
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowPushPull",
                        "Effect": "Allow",
                        "Action": ["logs:*"],
                        "Resource": "*"
                    }
                ]
            })
        )
    ],
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }]
    })
)
