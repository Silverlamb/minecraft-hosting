import os
from utils.mongo_gateway import MongoGateway
from UserMessageResponder import UserMessageResponder
import boto3
import time
import dotenv

class InstanceManager:
    CREATED_STATUS = "Created (Stopped)"

    def __init__(self, guild_instances_path = 'guild_instances', file_send = 'file_send', instance_file_path = 'utils/instance') -> None:
        self.guild_instances_path = guild_instances_path
        self.file_send = file_send
        self.instance_file_path = instance_file_path
        self.dot_terraform_file_path = "{}.terraform".format(os.path.abspath(__file__).replace(os.path.basename(__file__), ''))
        dotenv.load_dotenv(dotenv.find_dotenv())
        os.environ["TF_DATA_DIR"] = self.dot_terraform_file_path
        self.mongo_gateway = MongoGateway()

    """
    Creates a new folder with given path
    """
    def create_folder(self, path) -> None:
        if isinstance(path, str):
            folders = path.split('/')
            folder_paths = []

            for i, folder in enumerate(folders):
                path_string = ""
                for j in range(i+1):
                    path_string += "{}/".format(folders[j])
                folder_paths.append(path_string)

                if os.path.isdir(path_string):
                    pass
                else:
                    os.mkdir(path_string)

    """
    Creates a new file with data given
    """
    def create_file(self, path, data = "") -> None:
        max_path_index = max([i for i, ltr in enumerate(path) if ltr == "/"])
        self.create_folder(path[:max_path_index])
        with open(path, 'w') as f:
            f.write(data)

    """
    Pastes an already existing folder in a new path (relative or absolute path)
    """
    def copy_file(self, path_copy, path_paste) -> None:
        if path_copy != path_paste and not os.path.isdir(path_paste):
            if os.path.isdir(path_copy):
                os.system("cp -r {} {}".format(path_copy, path_paste))
            else:
                os.system("cp {} {}".format(path_copy, path_paste))
        else:
            pass

    """
    Checks if the instance's state is 'stopped'
    TODO: Add a timeout functionality
    """
    def state_ready_stopped(self, guild_id: int, instance_id) -> None:
        stopped_instance = False
        while(not stopped_instance):
            ec2_resource = boto3.resource(
                'ec2', 
                region_name='us-east-2',
                aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
                )
            instance = ec2_resource.Instance(instance_id)

            if instance.state['Name'] == 'stopped':
                stopped_instance = True
                time.sleep(10)
            time.sleep(1)

    """
    Checks if the instance's state is 'running'
    #TODO: Add a timeout functionality
    """
    def state_ready_running(self, guild_id: int, instance_id) -> None:
        running_instance = False
        while(not running_instance):
            ec2_resource = boto3.resource('ec2', 
                region_name='us-east-2',
                aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
            instance = ec2_resource.Instance(instance_id)

            if instance.state['Name'] == 'running':
                running_instance = True
                time.sleep(30)
            time.sleep(1)

    """
    Sets up file system locally
    """
    def local_setup(self, guild_id):
        self.create_file("{}/{}/ip.txt".format(self.guild_instances_path, guild_id), "")
        
        self.create_file("{}/{}/instanceID.txt".format(self.guild_instances_path, guild_id), "")
        
        self.create_folder("{}/{}/back_up".format(self.guild_instances_path, guild_id))

        self.copy_file("{}/terraform".format(self.instance_file_path), "{}/{}/terraform".format(self.guild_instances_path, guild_id))

    """
    Sets up file system remotely
    """
    def remote_instance_setup(self, guild_id: int) -> None:
        os.system("cd {}/{}/terraform; terraform init".format(self.guild_instances_path, guild_id))
        os.system("cd {}/{}/terraform; terraform apply -auto-approve".format(self.guild_instances_path, guild_id))
        os.system('cd {}/ansible; ansible-playbook on_create.yml -e "jre_path={} paper_server_path={} server_service_path={}" -i ../../../{}/{}/inventory'.format(
            "{}instance".format(os.path.abspath(__file__).replace(os.path.basename(__file__), '')),
            "{}/jre/19.0.2_7.tar.gz".format(self.file_send),
            "{}/paperMC".format(self.file_send),
            "{}/service/server.service".format(self.file_send),
            self.guild_instances_path,
            guild_id
        ))

    """
    Stops the server after create
    """
    def server_stop_on_create(self, guild_id, instance_id):
        self.state_ready_running(guild_id, instance_id)
        os.system('aws ec2 stop-instances --region us-east-2 --instance-ids {}'.format(instance_id))

    """
    Creates a server based on guild id
    """
    def server_create(self, guild_id, channel_id = None, responder: UserMessageResponder = None):
        instance_data = self.mongo_gateway.find_instance_one(guild_id)

        try:
            if not instance_data["server_state"] and not instance_data["server_present"] and not instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": True})
                self.local_setup(guild_id)
                self.remote_instance_setup(guild_id)
                
                with open("{}/{}/instanceID.txt".format(self.guild_instances_path, guild_id), "r") as f:
                    instance_id = f.read()
                
                self.mongo_gateway.update_instance_one(guild_id, {"instance_id": instance_id})

                self.server_stop_on_create(guild_id, instance_id)

                self.mongo_gateway.update_instance_one(
                    guild_id, {
                    "server_state": True,
                    "server_present": False,
                    "server_status": self.CREATED_STATUS,
                    })

                self.mongo_gateway.update_instance_one(guild_id, {"is_process": False})
                responder.send_remote_message('server_created', channel_id)
            else:
                pass
                responder.send_remote_message('server_created', channel_id)
        except Exception as e: # reset everything back to normal state
            current_instance_data = self.mongo_gateway.find_instance_one(guild_id)
            if not instance_data["is_process"] and current_instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": False})
            responder.send_remote_message('server_state_err', channel_id)
            print(e)

    """
    Starts already set up file system remotely
    """
    def remote_instance_start(self, guild_id, instance_id):
        self.state_ready_stopped(guild_id, instance_id)
        os.system('aws ec2 start-instances --region us-east-2 --instance-ids {}'.format(instance_id))
        self.state_ready_running(guild_id, instance_id)
        os.system('aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --instance-ids {} --output=text > {}/{}/ip.txt'.format(instance_id, self.guild_instances_path, guild_id))
        

        
        with open("{}../{}/{}/ip.txt".format(os.path.abspath(__file__).replace(os.path.basename(__file__), ''), self.guild_instances_path, guild_id), "r") as f:
            instance_ip = f.read()
        os.system("cd {}/ansible; python3 write.py {}../{}/{} {}".format(self.instance_file_path, os.path.abspath(__file__).replace(os.path.basename(__file__), ''), self.guild_instances_path, guild_id, instance_ip))
        os.system("cd {}/ansible; ansible-playbook on_start.yml -i ../../../{}/{}/inventory".format(
            self.instance_file_path, self.guild_instances_path, guild_id))
        return instance_ip

    """
    Starts a server based on guild id
    """
    def server_start(self, guild_id, channel_id = None, responder: UserMessageResponder = None):
        instance_data = self.mongo_gateway.find_instance_one(guild_id)
        try:
            if instance_data["server_state"] and not instance_data["server_present"] and not instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": True})
                instance_ip = self.remote_instance_start(guild_id, instance_data['instance_id']).replace('\n', '')

                self.mongo_gateway.update_instance_one(guild_id, {
                        "server_present": True,
                        "server_status": "Started",
                        "ip": instance_ip
                    })

                if instance_data['server_status'] == self.CREATED_STATUS:
                    responder.send_remote_message('first_server_started', channel_id)
                    print("This is a new server")
                else:
                    responder.send_remote_message('server_started', channel_id, [instance_ip])
                    print("This is not a new server")
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": False})
        except Exception as e:
            current_instance_data = self.mongo_gateway.find_instance_one(guild_id)
            if not instance_data["is_process"] and current_instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": False})
            responder.send_remote_message('server_state_err', channel_id)
            print(e)

    """
    Stops already set up file system remotely
    """
    def remote_instance_stop(self, guild_id, instance_id):
        self.state_ready_running(guild_id, instance_id)
        os.system("cd {}/ansible; ansible-playbook on_stop.yml -i ../../../{}/{}/inventory".format(
            self.instance_file_path, self.guild_instances_path, guild_id))
        os.system('aws ec2 stop-instances --region us-east-2 --instance-ids {}'.format(instance_id))

    """
    Stops a server based on guild id
    """
    def server_stop(self, guild_id = None, channel_id = None, responder: UserMessageResponder = None):
        instance_data = self.mongo_gateway.find_instance_one(guild_id)
        try:
            if instance_data["server_state"] and instance_data["server_present"] and not instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": True})

                self.remote_instance_stop(guild_id, instance_data['instance_id'])


                self.mongo_gateway.update_instance_one(guild_id, {
                        "server_present": False,
                        "server_status": "Stopped",
                        "is_process": False,
                        "ip": ""
                    })
                responder.send_remote_message('server_stopped', channel_id, [])
                print("Server stopped")
        except Exception as e:
            current_instance_data = self.mongo_gateway.find_instance_one(guild_id)
            if not instance_data["is_process"] and current_instance_data["is_process"]:
                self.mongo_gateway.update_instance_one(guild_id, {"is_process": False})
            responder.send_remote_message('server_state_err', channel_id)
            print(e)

    """
    Destroys entire remote system
    """
    def server_destroy(self, guild_id):
        self.mongo_gateway.update_instance_one(guild_id, {"is_process": True})
        os.system("cd {}/{}/terraform; terraform destroy -auto-approve".format(self.guild_instances_path, guild_id))
        self.mongo_gateway.update_instance_one(guild_id, {
            "server_state": False,
            "server_present": False,
            "server_status": "Not Created Yet",
            "ip": "",
            "instance_id": "",
            "is_process": False
        })