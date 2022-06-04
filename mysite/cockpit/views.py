from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# Create your views here.
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
from rest_framework.decorators import api_view

# Configs can be set in Configuration class directly or using helper utilitys
@api_view(['POST'])
def submit_cert(request):
    if request.method == 'POST':
        #serializer = SnippetSerializer(data=request.data)
        #if serializer.is_valid():
         #   serializer.save()
         #   return Response(serializer.data, status=status.HTTP_201_CREATED)
        cert = open("ca.crt", "w")
        cert.write(request.data['cert'])
        print(request.data['cert'])
        response = {
            "certificate": "created"
        }
        return Response(response, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getrs(request):
    if request.method == 'GET':
        config.load_kube_config()
        # configuration = client.Configuration()
        # configuration.host = "https://" + request.GET['api_server']
        #configuration.verify_ssl = False
        # configuration.api_key = {"authorization": request.META.get('HTTP_AUTHORIZATION')}
        # configuration.ssl_ca_cert = "./ca.crt"
        apiClient = client.ApiClient()
        print(request.GET['namespace'])       
    
        v1 = client.AppsV1Api(apiClient)
        if request.GET['namespace'] == "all":   
            ret = v1.list_deployment_for_all_namespaces(watch=False)
            data={}
            data2=[]
            for i in ret.items:
                # data["name"] = i.metadata.name
                # data["namepsace"] = i.metadata.namespace
                data={
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace
                }
                data2.append(data)
                #print(data2)
        else:
            ns = request.GET['namespace']
            rs = v1.list_namespaced_deployment(namespace=ns, pretty='true', watch=False)
            data={}
            data2=[]
            for i in rs.items:
                # data["name"] = i.metadata.name
                # data["namepsace"] = i.metadata.namespace
                data={
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace
                }
                data2.append(data)
            print(data2)
        return HttpResponse(json.dumps(data2, indent=4))