---
layout: post
date: 2018-09-20  00:00:00
categories: APIConnect
title: |
    Installing IBM Cloud Private install 3.1 or 2.1 on Amazon Web Service
    (AWS)
---
# Installing IBM Cloud Private install 3.1 or 2.1 on Amazon Web Service (AWS)

![](https://cdn-images-1.medium.com/max/600/0*KL_6rSvcBPvTDmXv.gif)

I was asked to install ICP on AWS for a demo.

My friendly local tech seller linked me to the terraform scripts. These
can be cloned from
`https://github.com/IBM/deploy-ibm-cloud-private/tree/master/terraform/aws`

The read me is very informative, in summary

1.  [Upload your ICP binary to S3 in the same region you wish to deploy
    ICP to.]
2.  [Create a user in AWS with full admin rights.]
3.  [Create an SSH Key Pair]
4.  [Install Terraform locally]

```
brew install terraform #for osx
```

3\. Create a file called`terraform.tfvars`
and place it in the aws directory you cloned

```
access_key = “<AWS Access Key>”
secret_key = “<AWS Secret Key>”
aws_region = “us-east-2”
key_name = “<SSH Key Pair>”
image_location = “s3://<S3 bucket>/ibm-cloud-private-x86_64–3.1.0.tar.gz” #Location of the install binary
icp_inception_image = “ibmcom/icp-inception-amd64:3.1.0-ee”
azs = [“a”]
```

If you need it deployed over multiple availability zones change the last
line to

```
azs=["a","b","c"]
```

4\. Edit the the `variables.tf` file and
update the bastion variable so it has `nodes=1`

```
variable "bastion" {
  type = "map"
  default = {
    nodes     = "1"
    type      = "t2.micro"
    ami       = "" // Leave blank to let terraform search for Ubuntu 16.04 ami. NOT RECOMMENDED FOR PRODUCTION
    disk      = "10" //GB
  }
}
```

5\. If you do not want an HA environment, modify the veraiables.tf and
replace all lines where `nodes = “3”` to
`nodes = “1”`

6\. run

```
terraform apply
```

Wait about 60--90 minutes.

7\. When the terraform script comes to an ending (20--30mins) it then
starts a silent installer for ICP. This takes another hour ish. If it
fails to install you need to ssh to the Bastion node, then ssh to the
master. The log file is in
`/var/log/cloud-init.output.log`

Notes: If you are installing 3.1 of ICP you need to make a slight change
to the installer, I have created a pull request and I am awaiting for it
to be accepted or declined. My fork is available here,
<https://github.com/ChrisPhillips-cminion/deploy-ibm-cloud-private> .
But I will not be keeping this updated with other changes to the master.





By [Chris Phillips](https://medium.com/@cminion) on
[September 20, 2018](https://medium.com/p/ef183475daef).

[Canonical
link](https://medium.com/@cminion/installing-ibm-cloud-private-install-3-1-or-2-1-on-amazon-web-service-aws-ef183475daef)

Exported from [Medium](https://medium.com) on April 6, 2019.
