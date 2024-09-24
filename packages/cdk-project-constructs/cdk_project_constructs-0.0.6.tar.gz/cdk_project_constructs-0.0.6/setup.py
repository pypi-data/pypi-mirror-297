"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import find_packages, setup

setup(
    name="cdk-project-constructs",
    version="0.0.6",
    description="AWS CDK resources to be used in infra projects.",
    long_description="Ready to go classes with AWS CDK resources. \n" "Supported resouces: AWS S3, AWS SNS, AWS LAMBDA, AWS KMS, AWS DynamoDB, AWS SQS",
    long_description_content_type="text/plain",
    license="MIT",
    package_dir={"": "."},
    packages=find_packages(where="."),
    install_requires=[
        "aws-cdk-lib>=2.159.0",
        "constructs>=10.0.0,<11.0.0",
        "cdk-monitoring-constructs>=8.3.0",
        "pyyaml>=6.0.0",
    ],
    python_requires=">=3.11",
    author="Madrag",
)
