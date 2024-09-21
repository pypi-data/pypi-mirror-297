from ..utils import *
from abstract_apis import *

async def asyncCallRequest(endpoint,*args,**kwargs):
  url = getEndpointUrl(endpoint)
  return await asyncPostRequest(url,kwargs)

def callSolcatcherRpc(endpoint=None,**kwargs):
  url = getEndpointUrl(endpoint)
  return asyncio.run(asyncPostRequest(url=url,data=kwargs))

async def get_meta(mint):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://192.168.0.100:3000/fetchMetadata', json={"mintAddress": mint}) as response:
            return await response.json()
          
def getMetaData(mint)
    return makeLimitedDbCall(tableName='getmetadata',searchValue=mint,dbNName=dbName,dbType=dbType,function=get_meta,mint=mint)
