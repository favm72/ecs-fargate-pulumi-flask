import pulumi
import pulumi_aws as aws
import pulumi_aws_native as aws_native
import pulumi_awsx as awsx
import json

# task role
task_exec_role = aws.iam.Role(
    "app-task-exec-role",
    managed_policy_arns=[
        "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
    ],
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement":
            [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ],
        }
    ),
)
