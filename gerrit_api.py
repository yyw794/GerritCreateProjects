from requests.auth import HTTPDigestAuth
from pygerrit2.rest import GerritRestAPI
from pprint import pprint
import os

if __name__=="__main__":
    user='10064088'
    password=os.getenv('GERRIT_PASSWORD')
    auth = HTTPDigestAuth(user,password)
    url = 'http://gerrit.zte.com.cn'
    #url = 'http://10.43.177.99'
    rest = GerritRestAPI(url=url,auth=auth)
    #changes=rest.get("/changes/?q=owner:self%20status:open")
    #changes=rest.get("/accounts/self/groups")
    #changes=rest.put("/projects/Power-RD-Projects")
    #changes = rest.delete("/groups/465526c73496969c10b3412a2b76aecf5dda4df9")
    changes = rest.get("/projects/")
    pprint(changes)
