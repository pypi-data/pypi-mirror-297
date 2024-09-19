import oci
import sys
import os


class vm:
    config = None
    core_client = None
    vmlist = {}

    def __init__(self, config_file='~/.oci/config', profile="DEFAULT"):

        self.config = oci.config.from_file(file_location=config_file, profile_name=profile)
        self.core_client = oci.core.ComputeClient(self.config)
        self.vmlist = self.initlist()

    def initlist(self):
        response = self.core_client.list_instances(compartment_id=self.config["compartment_id"])
        templist = {}
        for item in response.data:
            name = item.display_name
            ocid = item.id
            templist[name] = ocid
        return templist
    def action(self,name,action):
        if name in self.vmlist:
            self.actionOCI(self.vmlist[name],action)
        else:
            self.vmlist = self.initlist()
            if name in self.vmlist:
                self.actionOCI(self.vmlist[name], action)
            else:
                print("Can't find the VM you input")
    def actionOCI(self,ocid,action):
        instance_action_response = self.core_client.instance_action(
            instance_id=ocid,
            action=action)


