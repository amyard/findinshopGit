from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView,GenericAPIView,RetrieveAPIView
from rest_framework.mixins  import CreateModelMixin
# from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from apps.catalog.models import Category, Item
from serializers import *

from apps.website.search import prepare_value
from apps.website.search.search import SphinxSearcher


class ListCategory(ListAPIView):
    # permission_classes = ( IsAdminUser,)
    queryset=Category.objects.all()
    serializer_class=CategoryListSerializer

class DetailCategory(RetrieveAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer


class ListItem(ListAPIView):
    queryset=Item.objects.all()
    serializer_class=ItemListSerializer


class ListItemSphinx(ListAPIView):
    serializer_class=ItemListSerializer

    def get_queryset(self):
        super 
        query =self.request.query_params
        if 'q' in query:
            qs = SphinxSearcher()
            search_dict, search_value = prepare_value(self.request)
            search_result = qs.search_api(**search_dict)
            queryset = [Item.objects.get(id=item['id']) for item in search_result]
        else: queryset=Item.objects.all()
        return queryset

    # def get_queryset(self):
    #     assert self.queryset is not None, (
    #         "'%s' should either include a `queryset` attribute, "
    #         "or override the `get_queryset()` method."
    #         % self.__class__.__name__
    #     )

    #     queryset = self.queryset
    #     if isinstance(queryset, QuerySet):
    #         # Ensure queryset is re-evaluated on each request.
    #         queryset = queryset.all()
    #     return queryset


    # def get(self, request):
    #     # rest_framework.request.Request is request
    #     print request.query_params['q']
    #     qs = SphinxSearcher()
    #     search_dict, search_value = prepare_value(request)
    #     search_result = qs.search_api(**search_dict)
    #     # print [item['id'] for item in search_result]
    #     queryset = [Item.objects.get(id=item['id']) for item in search_result]
    #     serializer = ItemListSerializer(queryset, many=True)
    #     return Response(serializer.data)


class DetailItem(RetrieveAPIView):
    queryset=Item.objects.all()
    serializer_class=ItemSerializer
