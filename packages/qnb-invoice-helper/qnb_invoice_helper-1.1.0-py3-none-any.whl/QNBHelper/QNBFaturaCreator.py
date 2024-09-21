import json
from zeep.client import Client
from zeep.wsse.username import UsernameToken
from zeep.wsse.utils import WSU
import datetime
from QNBHelper.models import Request, Response, Return

class QNBEarsivHelper:
    WSDL_URL: str = "https://earsivconnector.efinans.com.tr/earsiv/ws/EarsivWebService?wsdl"
    
    @classmethod
    def create_username_token(cls, username: str, password: str) -> UsernameToken:
        timestamp_token = WSU.Timestamp()
        today_datetime = datetime.datetime.today()
        expires_datetime = today_datetime + datetime.timedelta(minutes=10)
        timestamp_elements = [
        WSU.Created(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
        WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        timestamp_token.extend(timestamp_elements)
        username_token = UsernameToken(username, password, timestamp_token=timestamp_token)
        return username_token
    
    @classmethod
    def create_client(cls, username_token: UsernameToken) -> Client:
        if not isinstance(username_token, UsernameToken):
            raise TypeError("username_token must be a UsernameToken object")
        client = Client(cls.WSDL_URL, wsse=username_token)
        return client
    
    @classmethod
    def fatura_olustur(cls, client: Client, request: Request) -> Response:
        if not isinstance(client, Client):
            raise TypeError("client must be a Client Object")
        
        if not isinstance(request, Request):
            raise TypeError("request must be a Request Object")
        
        node = client.service.faturaOlustur(input=request.input_str, fatura={"belgeFormati":request.belgeFormati, "belgeIcerigi":request.belgeIcerigi})
        output = node.output
        return_ = node["return"]
        return Response(
            output=output,
            return_=Return(
                resultCode=return_.resultCode, resultExtra=None,
                resultText=return_.resultText
            )
        )
    
        





