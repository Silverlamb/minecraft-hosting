terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 4.14.0"
    }
  }
}

provider "aws" {
	region = "us-east-2"
	access_key = var.provider_access_key
  secret_key = var.provider_secret_key
}

resource "aws_instance" "minecraft_instance" {
  ami = "ami-077e31c4939f6a2f3"
  instance_type = "t2.medium"
  key_name = "createEC2"
  vpc_security_group_ids = [aws_security_group.instance.id]

  provisioner "remote-exec" {
    inline = ["echo remote started"]

    connection {
      type     = "ssh"
      user     = "ec2-user"
      private_key = file("~/.ssh/createEC2.pem")
      host     = "${self.public_ip}"
    }
  }

  provisioner "local-exec"{
    command = "python3 write.py ${self.public_ip} ${self.id};"
  }

  tags = {
    Name = "minecraft-instance"
  }
}

resource "aws_security_group" "instance" {
  ingress {
    from_port   = var.server_port_inbound
    to_port     = var.server_port_inbound
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = var.server_port_inbound_mc
    to_port     = var.server_port_inbound_mc
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

variable "server_port_inbound" {
  description = "This port will used for SSH requests"
  type        = number
  default     = 22
}

variable "server_port_inbound_mc" {
  description = "This port will use for mc requests"
  type        = number
  default     = 25565
}
