#!/usr/bin/env python
# coding=utf-8
from string import Template
import os
from requests.auth import HTTPDigestAuth
from pygerrit2.rest import GerritRestAPI
from pprint import pprint
import sys 

class GerritApi():
    def __init__(self):
        self.user = '10064088'
        self.password = os.getenv('GERRIT_PASSWORD')
        auth = HTTPDigestAuth(self.user, self.password)
        #gerrit site
        ip="gerrit.zte.com.cn"
        self.url = 'http://{}'.format(ip)
        self.ssh_url = 'ssh://{}@{}:29418'.format(self.user,ip)
        self.rest = GerritRestAPI(url=self.url,auth=auth)
        self.project_info = 'projects_info.txt'
        self.project_config_template="project_config.template"
        self.group_types = ('admin', 'core', 'team')
    def create_projects(self):
        with open(self.project_info,'r') as f:
            projects= f.readlines()
        for repo in projects:
            proj_repo, group = repo.split(':')
            group = group.strip('\r\n')
            
            self.create_project(proj_repo)
            self.update_project_group_config(proj_repo, group)

    def update_project_group_config(self, proj_repo, group):
        #make groups
        groups = ['{}-{}'.format(group, x) for x in self.group_types]
        #set yourself the owner
        #data={"owner":"10064088"}
        #self.rest.put("/groups/{}/owner",data=data)

        #modify project config
        cmd = 'git clone {}/{}'.format(self.ssh_url, proj_repo)
        os.system(cmd)
        origin_folder = os.getcwd()
        folder_name = proj_repo.split('/')[-1]
        os.chdir(folder_name)

        os.system('git fetch origin refs/meta/config:refs/meta/config')
        os.system('git checkout refs/meta/config')

        self.generate_groups_UUID_map(groups)
        #self.generate_project_config(proj_repo.split('/')[0], group)
        self.generate_project_config("Power-RD-Projects", group)

        os.system('git add .')
        os.system('git commit -m "update config access"')
        os.system('git push origin HEAD:refs/meta/config')

        #you should chdir back
        os.chdir(origin_folder)
        #os.system("rm -rf {}".format(folder_name)) 


    def create_project(self, proj_repo):
        #create
        #you must do this replacement, or else if fails
        proj_repo_id = proj_repo.replace('/','%2F')

        #you must add this! or else you cannot visit the project after created the project unless you are in administrators
        payload = {"parent":"Power-RD-Projects"}
        #IMPORTART: json=payload is ok, data=payload is not ok!!! fuck! wasting my debug time!
        try:
            ret = self.rest.put('/projects/{}'.format(proj_repo_id), json=payload)
        except:
            print("project {} exists".format(proj_repo))
        


    def generate_groups_UUID_map(self,groups):
        with open('groups', 'w') as f:
            for group in groups:
                print(group)
                ret = self.rest.get('/groups/{}'.format(group))
                f.write("{}\t{}\n".format(ret['id'],group))


    def generate_project_config(self, institute, group):
        with open(os.path.join("..",self.project_config_template), 'r') as f:
            config_template = Template(f.read())

        with open('project.config', 'w') as f:
            f.write(config_template.substitute(Institute=institute, Group=group))



if __name__ == '__main__':
    GerritApi().create_projects()
