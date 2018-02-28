from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins, generics

class SnippetList(generics.ListCreateAPIView): 
    queryset = Snippet.objects.all() 
    serializer_class = SnippetSerializer

class SnippetDetail(generics.RetrieveUpdateDestoryAPIView): 
    queryset = Snippet.objects.all() 
    serializer_class = SnippetSerializer