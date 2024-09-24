import pulumi
import pulumi_aws as aws
from cloud_foundry.utils.logger import logger

from cloud_foundry.python_archive_builder import PythonArchiveBuilder

log = logger(__name__)


class PythonFunction(pulumi.ComponentResource):
    name: str
    handler: str
    lambda_: aws.lambda_.Function

    def __init__(
        self,
        name,
        *,
        hash: str,
        archive_location: str,
        handler: str,
        timeout: int = None,
        memory_size: int = None,
        environment: dict[str, str]=None,
        actions: list[str]=None,
        opts=None
    ):
        super().__init__("custom:cloud_forge:PythonFunction", name, {}, opts)
        self.name = name
        self.handler = handler
        self.environment = environment or {}
        self.memory_size = memory_size
        self.timeout = timeout
        self.actions = actions
        self.create_lambda_function(hash, archive_location)
        self.register_outputs({})

    def create_execution_role(self) -> aws.iam.Role:
        log.debug("creating execution role")
        assume_role_policy = aws.iam.get_policy_document(
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    principals=[
                        aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                            type="Service",
                            identifiers=["lambda.amazonaws.com"],
                        )
                    ],
                    actions=["sts:AssumeRole"],
                )
            ]
        )

        role = aws.iam.Role(
            f"{self.name}-lambda-execution",
            assume_role_policy=assume_role_policy.json,
            name=f"{pulumi.get_project()}-{pulumi.get_stack()}-{self.name}-lambda-execution",
            opts=pulumi.ResourceOptions(parent=self)
        )

        aws.iam.get_policy_document(
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=((self.actions or []) + [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ]),
                    resources=["*"],  
                )
            ]
        )

        return role

    def invoke_arn(self) -> pulumi.Output[str]:
        return self.lambda_.invoke_arn

    def create_lambda_function(self, hash: str, archive_location: str):
        log.debug("creating lambda function")

        execution_role = self.create_execution_role()

        self.lambda_ = aws.lambda_.Function(
            f"{self.name}-lambda",
            code=pulumi.FileArchive(archive_location),
            name=f"{pulumi.get_project()}-{pulumi.get_stack()}-{self.name}",
            role=execution_role.arn,
            memory_size=self.memory_size,
            timeout=self.timeout,
            handler=self.handler,
            source_code_hash=hash,
            runtime=aws.lambda_.Runtime.PYTHON3D9,
            environment=aws.lambda_.FunctionEnvironmentArgs(variables=self.environment),
            opts=pulumi.ResourceOptions(depends_on=[execution_role], parent=self),
        )

def python_function(
    name: str, *,
    handler: str,
    memory_size: int = None,
    timeout: int = None,
    sources: dict[str, str] = None,
    requirements: list[str] = None,
    environment: dict[str, str] = None,
):
    archive_builder = PythonArchiveBuilder(
        name=f"{name}-archive-builder",
        sources=sources,
        requirements=requirements,
        working_dir="temp",
    )
    return PythonFunction(
        name=name,
        hash=archive_builder.hash(),
        memory_size=memory_size,
        timeout=timeout,
        handler=handler,
        archive_location=archive_builder.location(),
        environment=environment,
    )
