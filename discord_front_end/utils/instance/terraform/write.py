import sys

f = open("../inventory", "w")
f.write("[mc_ec2_group]\nec2host ansible_ssh_host=" + sys.argv[1] + "	ansible_user=ec2-user	ansible_ssh_private_key_file=~/.ssh/createEC2.pem	ansible_ssh_common_args='-o StrictHostKeyChecking=no'")
f.close()

f = open("../ip.txt", "w")
f.write(sys.argv[1])
f.close()

if(len(sys.argv) > 2):
	f = open("../instanceID.txt", "w")
	f.write(sys.argv[2])
	f.close()