from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
)
from constructs import Construct
from cdk_nag import NagSuppressions

class AwsCdkHelloworldStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        queue = sqs.Queue(
            self, "AwsCdkHelloworldQueue",
            visibility_timeout=Duration.seconds(300),
        )

        # Supressions

        NagSuppressions.add_resource_suppressions(queue, 
                                                  [
                                                      { 
                                                          "id": "AwsSolutions-SQS3", 
                                                          "reason": "AwsSolutions-SQS3 est null" 
                                                       },
                                                      { 
                                                          "id": "AwsSolutions-SQS4", 
                                                          "reason": "AwsSolutions-SQS4 est null" 
                                                       }
                                                  ]
                                                  )
