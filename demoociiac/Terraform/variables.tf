# main-vars.tf
############################################
# Compartments
############################################

variable "compartment_id" {
  description = "The OCID of the parent compartment where the resources will be created."
  type        = string
}

variable "compartment_name" {
  description = "Compartment Name"
  type        = string
  default     = "cloudquicklabs-compartment"
}

variable "compartment_description" {
  description = "Compartment Description"
  type        = string
  default     = "test-compartment description"
}

############################################
# VCN
############################################

variable "vcn1" {
  description = "The details of VCN1."
  default = {
    cidr_blocks : ["10.23.0.0/20"]
    display_name : "vcn01"
  }
}

############################################
# Public Subnet, Route Table, and Internet Gateway
############################################

variable "subnetA_pub" {
  description = "The details of the subnet"
  default = {
    cidr_block : "10.23.11.0/24"
    display_name : "IC_pub_snet-A"
    is_public : true
    route_table : {
      display_name = "routeTable-Apub"
      description  = "routeTable-Apub"
    }
  }
}

variable "internet_gateway_A" {
  description = "The details of the internet gateway"
  default = {
    display_name : "IC_IG-A"
    ig_destination = "0.0.0.0/0"
  }
}

############################################
# Compute Instance
############################################

variable "ic_pub_vm_A" {
  description = "The details of the compute instance"
  default = {
    display_name : "IC_pub_vm-A"
    assign_public_ip : true
    availability_domain : "RjRj:US-SANJOSE-1-AD-1"
    image_ocid : "ocid1.image.oc1.us-sanjose-1.aaaaaaaaoy3dg6f2w5edbvow2i7yymcyxlswnut5xf5ffad7us2eft6kp7oq"
    shape : {
      name          = "VM.Standard.E2.1.Micro"
      ocpus         = 1
      memory_in_gbs = 1
    }
    ssh_authorized_keys = ["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3qjNb/fSTmjHXClwcI2oARKrB5jH7RePjYWVfXPi6rhvOLN5u7spg3RtuU7mJpF6yEFm/p26rYPrGQWCZaHnDtwbE+U5QxGZYibI02S5cCzvULdcFiuno3F5S8b56ir0LEPHAOaNAKjPIOjQpIFBbN1boEXDq9VF6hFCb/YSCs03tnnVwicIi/BnL/5zhIPKLT/LG3DjZLxgcomnichvdxpNaYphqJnBuCjfoS9yvFxdgvzC0JheUMsWa4xgviYC7D9LoQOx3mIVlLOoh0kzcGcbwjfXQrAb2RFv/etFPibvSB0cmaDxWkwlkaHM0ZrnnAgWuSWig+sh/jOTVCUCP rsa-key-20240817"]
  }
}