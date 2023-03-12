
import pulumi
import pulumi_aws as aws
import pulumi_aws_native as aws_native
import pulumi_awsx as awsx

# load balancer
load_balancer = awsx.lb.ApplicationLoadBalancer("app-alb")

# target group
target_group = aws.lb.TargetGroup(
    "app-tg",
    vpc_id=load_balancer.vpc_id,
    port=5000,
    protocol="HTTP",
    target_type="ip",
    health_check=aws.lb.TargetGroupHealthCheckArgs(
        path="/",
        interval=30,
        timeout=5,
        protocol="HTTP",
        matcher="200",
        healthy_threshold=3,
        unhealthy_threshold=2
    )
)

# listener
listener = aws.lb.Listener(
    "app-listener",
    load_balancer_arn=load_balancer.load_balancer.arn,
    port=5000,
    protocol="HTTP",
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="forward",
            target_group_arn=target_group.arn
        )
    ]
)
