from typing import Callable,Any,TypeVar
import requests
from datetime import datetime
import json
#Loading configuration JSON:
with open("app_config/log.json","r") as f:
  logconf=json.load(f)
#Logging functions(optional):
#IMPORTANT:fix decorator funclogger and append it to all functions in the classs GitApi
T = TypeVar("T")
def funclogger( func:Callable[...,Any] ) -> Callable[...,Any]:
  def wrapper(*args:Any,**kwargs:Any)->Any:
    if logconf["LogFunctionUsageToFile"]:#check if logging is enabled
      usage:dict[str,Any] = {
        'Function name':func.__name__,
        'Datetime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Arguments':args,
        'Keyword arguments':kwargs
      }

      #append usage to json file
      try:
        with open("app_logs/function_logs.json","r") as f:
          file:list[dict[str,Any]]=json.load(f)
      except FileNotFoundError:
        file=[] #decide what happens myself
      
      file.append(usage)

      with open("app_logs/function_logs.json","w") as fa:
        json.dump(file,fa,indent=4)
    result = func(*args,**kwargs)
    return result #execute function
  return wrapper

      
url="https://api.github.com"
#listing repos of an owner's endpoint:url/users/{owner}/repos
class GitApi:
  def __init__(self,token:str,headers:dict[str,str] | None=None):
    self.token=token
    self.headers = headers if headers is not  None else{
      "Authorization":f"token {token}"
    } if token else {}

  def getreposfromowner(self,owner:str):
    repos:list[str] = []#Create a void list to store repository names
    page = 1 #github has a max limit of content per page,so we'll iterate throught each page untill we cant get no more pages
    while True:#condition
      totalurl = f"{url}/users/{owner}/repos?per_page=100&page={page}" #total url
      r = requests.get(totalurl,headers=self.headers)
      response = r.json() #response is returned in JSON

      if not response:break#break from loop if page doesnt exist

      repos.extend([ repo["name"] for repo in response ])

      #After extending repos,now its time to increase page count
      page += 1
    #after the loop finishes:
    return repos
  def getrepositoryinfo(self,owner:str,repo:str):
    print("")

  #getrepoissues
  #def getrepoinfo():
  #def countlinesofrepo:
 # def

