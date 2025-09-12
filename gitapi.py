#external libraries
from datetime import datetime #for logger functions(optional)
import requests #normal requests
import asyncio #async
import aiohttp #async
import os #environment variable check
from rich import print #colors
import json #loading json
import argparse #Parsing arguments


#internal configuration files
from app_utils.Errors import ApiKeyNotFoundc #throws error if api key wasnt found
from app_utils.utils import GitApi #Core logic
path_for_verbose_configuration="app_config/verbose.json"
path_for_proxy_configuration="app_config/proxy.json"
path_for_log_configuration="app_config/log.json"
path_for_api_key_configuration="app_config/apikey.json"
  #load json  configuration:



with open(path_for_verbose_configuration,"r") as f:
  verbosityconf = json.load(f) #verbosityconf is now a dictionary containing my configuration
with open(path_for_log_configuration,"r") as fl:
  logconf=json.load(fl)
verbose = verbosityconf["VerboseOnload"]
logFunctionUsageToFile=logconf["LogFunctionUsageToFile"] 
LogActivityToFile=logconf["LogActivityToFile"]
#IMPORTANT:ADD WEBHOOK SUPPORT LATER


def main():#starting point



  if verbose:print("[yellow][*]Checking for github api key in environment variables[/yellow]")
  #Check if github api key is in environment variable:
  github_api_key = os.getenv("GITHUB_API_KEY")
  if github_api_key:

    if verbose:
      print("[green][+]Github api key found in environment variables![/green]")
    #update:having api key is no longer needed

  else:
    #IMPORTANT:IN THE FUTURE MAKE IT SO THE USER CAN USE API KEY WITHOUT ENVIRONMENT 
    #also,add an environment variables tutorial.txt  where people can know when to remove or add environment variable keys
    print( "\n[red][!]Github api key not found in environment variables[/red]\n" 
    "[yellow]You can generate one here:https://github.com/settings/tokens[/yellow]\n" 
    "[yellow]You can export it to your environment variables like this:[/yellow]\n"
    "[yellow]Linux/MacOs: export GITHUB_API_KEY='your_api_key_here'[/yellow]\n"
    "[yellow]Windows:set GITHUB_API_KEY='your_api_key_here'[/yellow]\n")
    raise ApiKeyNotFoundc("Github api key not found in environment variables,make sure to restart your IDE or terminal after you set it up")

  #start parsing arguments:
  parser=argparse.ArgumentParser(description="Github API CLI")
  parser.add_argument("--Username","-us",required=True,help="Target username")
  parser.add_argument("--Countrepos","-cr",action="store_true",help="Count how many repos an username has")
  parser.add_argument("--Get-username-info","-gui",action="store_true",help="Gets information about an username")
  parser.add_argument("--rate_limit","-rl",type=int,default=5,help="Rate limit your requests")

  args=parser.parse_args()

  username=args.Username
  gitobj=GitApi(github_api_key)
  if args.Countrepos:
    listofrepos:list[str]=gitobj.getreposfromowner(username)
    #print each repository name in the list:
    print(f"[yellow]Enumerating repositories of {username}:[/yellow]")
    for i in listofrepos:
      print(f"   [green]{i}[/green]")
if __name__=="__main__":
  main()

  #future:add a functionality that allow users to gather info about multiple owners
#On the end disable verbose on load