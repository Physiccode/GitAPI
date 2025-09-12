#I'm defining errors in this file
class ApiKeyNotFoundc(Exception):#error if api key not found
  def __init__(self,message:str):
    super().__init__(self,message)
    self.message=message
class RateLimitc(Exception):
  def __init__(self,message:str):
    super().__init__(message)
    self.message=message
#def logRateLimits():