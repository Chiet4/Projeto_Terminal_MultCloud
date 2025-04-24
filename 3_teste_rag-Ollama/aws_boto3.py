import boto3

def get_contexto_aws():
    ec2 = boto3.client("ec2")
    rds = boto3.client("rds")

    # VPCs
    vpcs = ec2.describe_vpcs()
    vpcs_ids = [vpc["VpcId"] for vpc in vpcs.get("Vpcs", [])]

    # Subnets
    subnets = ec2.describe_subnets()
    subnets_ids = [subnet["SubnetId"] for subnet in subnets.get("Subnets", [])]

    # Security Groups
    sgs = ec2.describe_security_groups()
    sgs_ids = [sg["GroupId"] for sg in sgs.get("SecurityGroups", [])]

    # RDS Subnet Groups
    rds_subnets = rds.describe_db_subnet_groups()
    rds_names = [r["DBSubnetGroupName"] for r in rds_subnets.get("DBSubnetGroups", [])]

    # Montar string de contexto
    contexto = (
        f"Meus subnets disponíveis: {subnets_ids}\n"
        f"Meus security Groups disponíveis: {sgs_ids}\n"
        f"Meus VPCs disponíveis: {vpcs_ids}\n"
        f"Meus RDS Subnet Groups: {rds_names}\n"
    )
    return contexto
