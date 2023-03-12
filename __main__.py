import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
from iac.task_role import task_role
from iac.task_exec_role import task_exec_role
from iac.load_balancer import load_balancer, target_group

# cluster
cluster = aws.ecs.Cluster("app-cluster")

# create log group
log_group = aws.cloudwatch.LogGroup("app-log-group", retention_in_days=1)

# ecr repository
ecr = awsx.ecr.Repository("app-ecr", name="app-ecr", force_delete=True)

# image
image = awsx.ecr.Image("app", path="./docker", repository_url=ecr.url)

# create ecs fargate cluster
service = awsx.ecs.FargateService(
    "app-service",
    cluster=cluster.arn,
    desired_count=2,
    assign_public_ip=True,
    task_definition_args=awsx.ecs.FargateTaskDefinitionArgs(
        task_role=task_role,
        execution_role=task_exec_role,
        container=awsx.ecs.TaskDefinitionContainerDefinitionArgs(
            image=image.image_uri,
            cpu=256,
            memory=512,
            essential=True,
            port_mappings=[
                awsx.ecs.TaskDefinitionPortMappingArgs(
                    container_port=5000,
                    host_port=5000,
                    target_group=target_group)
            ],
            log_configuration=awsx.ecs.TaskDefinitionLogConfigurationArgs(
                log_driver="awslogs",
                options={
                    "awslogs-group": log_group.name,
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "app"
                }
            ))))


# Export the load balancer's address
pulumi.export("endpoint", load_balancer.urn)
