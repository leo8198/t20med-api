provider "aws" {
  region = "us-east-1"
}

resource "aws_db_instance" "my-test-sql" {
  instance_class          = "${var.db_instance}"
  engine                  = "postgres"
  engine_version          = "13.7"
  multi_az                = true
  storage_type            = "gp2"
  allocated_storage       = 20
  db_name                 = "postgres"
  username                = "postgres"
  password                = "leotarla"
  apply_immediately       = "true"
  backup_retention_period = 7
  skip_final_snapshot     = "true"
 # backup_window           = "09:46-10:16"
  db_subnet_group_name    = "${aws_db_subnet_group.my-rds-db-subnet.name}"
  vpc_security_group_ids  = ["${aws_security_group.my-rds-sg.id}"]
}

resource "aws_db_subnet_group" "my-rds-db-subnet" {
  name       = "my-rds-db-subnet"
  subnet_ids = ["${var.rds_subnet1}", "${var.rds_subnet2}"]
}

resource "aws_security_group" "my-rds-sg" {
  name   = "my-rds-sg"
  vpc_id = "${var.vpc_id}"
}

resource "aws_security_group_rule" "my-rds-sg-rule" {
  from_port         = 5432
  protocol          = "tcp"
  security_group_id = "${aws_security_group.my-rds-sg.id}"
  to_port           = 5432
  type              = "ingress"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "outbound_rule" {
  from_port         = 0
  protocol          = "-1"
  security_group_id = "${aws_security_group.my-rds-sg.id}"
  to_port           = 0
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
}
