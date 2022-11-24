import pulumi
import pulumi_eks as eks
import pulumi_aws as aws
import pulumi_kubernetes as k8s

cluster_name = "eks-tutorial-cluster"
cluster_tag = f"kubernetes.io/cluster/{cluster_name}"

public_subnet_cidrs = ["172.31.0.0/20", "172.31.48.0/20"]

# Use 2 AZs for our cluster
avail_zones = ["us-east-1a", "us-east-1b"]

# Create VPC for EKS Cluster
vpc = aws.ec2.Vpc(
	"eks-vpc",
	cidr_block="172.31.0.0/16"
)

igw = aws.ec2.InternetGateway(
	"eks-igw",
	vpc_id=vpc.id,
)

route_table = aws.ec2.RouteTable(
	"eks-route-table",
	vpc_id=vpc.id,
	routes=[
		{
			"cidr_block": "0.0.0.0/0",
			"gateway_id": igw.id
		}
	]
)

public_subnet_ids = []

# Create public subnets that will be used for the AWS Load Balancer Controller
for zone, public_subnet_cidr  in zip(avail_zones, public_subnet_cidrs):
    public_subnet = aws.ec2.Subnet(
        f"eks-public-subnet-{zone}",
        assign_ipv6_address_on_creation=False,
        vpc_id=vpc.id,
        map_public_ip_on_launch=True,
        cidr_block=public_subnet_cidr,
        availability_zone=zone,
        tags={
	     			# Custom tags for subnets
            "Name": f"eks-public-subnet-{zone}",
            cluster_tag: "owned",
            "kubernetes.io/role/elb": "1",
        }
    )

    aws.ec2.RouteTableAssociation(
        f"eks-public-rta-{zone}",
        route_table_id=route_table.id,
        subnet_id=public_subnet.id,
    )
    public_subnet_ids.append(public_subnet.id)

# Create an EKS cluster.
cluster = eks.Cluster(
    cluster_name,
	name=cluster_name,
    vpc_id=vpc.id,
    instance_type="t2.medium",
    desired_capacity=2,
    min_size=1,
    max_size=2,
    provider_credential_opts=kube_config_opts,
    public_subnet_ids=public_subnet_ids,
    create_oidc_provider=True,
)

# Export the cluster's kubeconfig.
pulumi.export("kubeconfig", cluster.kubeconfig)