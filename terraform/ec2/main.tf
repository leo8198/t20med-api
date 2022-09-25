provider "aws" {
  region = "us-east-1"     # Mention the required region
}

data "aws_availability_zones" "available" {}

resource "aws_key_pair" "mytest-key" {
  key_name = "my-test-terraform-key-new1"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCyOw3eRk/Df40+CfFrNtdn4BsgP4dyr+BAAuiep2UCRxupG3a81nbWdJ2Mzstj94MQQdInhW7B4dMUledJSLanzune3hOqpC27Yvgg8Gls6f4IcX/wG3rZCzCPOABzOq1IWG0fJixJgRfHZJ+sQ4rFfDjFZ0e4X2dSZfF63u2BjryRCWcbyHbk3C3eNCuATDk5S/8hUz/MhYRQHigSZGbhXqusP6Icnw0s9ZHX9fcoUcuGquXtROJU+D/B7mUqaJ5tcRz6kr6/gILQOL1OgEmbct7I089gPbS/P0ZM1saFppaSjizCZnpHixBL4HTM3BG0kqvoP4UbKK2Afc3ge1/5F7qFnIVHSAgb1PX11H/p5X+ey8VmA29u8rvYwmW9K3rveICLIDa5UuR5rwb1PzFTJLa3NaAoJ6MTDWYGqaDoaMbbpTsR/uFlxdVLBdBq6foensMR7PuDa6MQAGWCsCGMXxsridarjbFAfUWg4kAFE6a3IxNtah9S8YqUthaJUPs= leo@leo-VivoBook-ASUSLaptop-X512FJ-X512FJ"
}

# AMI template
data "template_file" "init" {
  template = "${file("${path.module}/template.sh")}"
}

resource "aws_instance" "my-test-instance" {
  ami = "ami-0149b2da6ceec4bb0"
  count = 2
  instance_type = "${var.instance_type}"
  vpc_security_group_ids = ["${var.security_group}"]
  key_name = "${aws_key_pair.mytest-key.id}"
  subnet_id = "${element(var.subnets, count.index )}"
  user_data = "${data.template_file.init.rendered}"
  tags = {
    Name = "ec2-dev"
  }
}

resource "aws_ebs_volume" "my-test-ebs" {
  count             = 2
  availability_zone = "${data.aws_availability_zones.available.names[count.index]}"
  size              = 1
  type              = "gp2"
}

resource "aws_volume_attachment" "my-vol-attach" {
  count        = 2
  device_name  = "/dev/xvdh"
  instance_id  = "${aws_instance.my-test-instance.*.id[count.index]}"
  volume_id    = "${aws_ebs_volume.my-test-ebs.*.id[count.index]}"
  force_detach = true
}