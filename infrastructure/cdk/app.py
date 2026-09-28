#!/usr/bin/env python3
import aws_cdk as cdk
from demand_sensing_stack import DemandSensingStack
app=cdk.App()
DemandSensingStack(app,"DemandSensingStack")
app.synth()
