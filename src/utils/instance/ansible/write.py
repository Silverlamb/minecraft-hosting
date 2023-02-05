import sys
sys.path.insert(1, '../')

f = open("../../{}/inventory".format(sys.argv[1]), "w")
f.write("[mc_ec2_group]\nec2host ansible_ssh_host=" + sys.argv[2] + "	ansible_user=ec2-user	ansible_ssh_private_key_file=~/.ssh/createEC2.pem	ansible_ssh_common_args='-o StrictHostKeyChecking=no'")
f.close()