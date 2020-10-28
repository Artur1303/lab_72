from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import QuotePermissions
from api.serializers import QuoteCreateSerializer, QuoteUpdateSerializer, QuoteSerializer
from webapp.models import Quote, Vote


class QuoteViewSet(ModelViewSet):
    permission_classes = [QuotePermissions]

    def get_queryset(self):
        if self.request.method == 'GET' and \
                not self.request.user.has_perm('webapp.quote_view'):
            return Quote.get_moderated()
        return Quote.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuoteCreateSerializer
        elif self.request.method == 'PUT':
            return QuoteUpdateSerializer
        return QuoteSerializer

class VoteApiView(APIView):
        # @action(methods=['post'], detail=True)
        def post(self, request, *args, **kwargs):
            quote = get_object_or_404(Quote, pk=kwargs['pk'])
            vote, created = Vote.objects.get_or_create(quote=quote, session_key=request.user)

            if created:
                vote.rating = 1
                vote.save()
                quote.quenti()
                return Response({'pk': kwargs['pk'], 'rating': quote.rating})
            elif vote.rating != 1:
                vote.rating = 1
                vote.save()
                quote.quenti()
                return Response({'pk': kwargs['pk'], 'rating': quote.rating})
            else:
                return Response(status=403)

        # @action(methods=['delete'], detail=True)
        def delete(self, request, *args, **kwargs):
            quote = get_object_or_404(Quote, pk=kwargs['pk'])
            vote, created = Vote.objects.get_or_create(quote=quote, session_key=request.user)
            if created:
                vote.rating = -1
                vote.save()
                quote.quenti()
                return Response({'pk': kwargs['pk'], 'rating': quote.rating})
            elif vote.rating != -1:
                vote.rating = -1
                vote.save()
                quote.quenti()
                return Response({'pk': kwargs['pk'], 'rating': quote.rating})
            else:
                return Response(status=403)



#
# class VoteApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         quote = get_object_or_404(Quote, pk=kwargs.get('pk'))
#         print(quote)
#         try:
#             Vote.objects.get(session_key=self.request.session.session_key, quote_id=quote)
#             return Response({'message': 'You have already rated'}, status=200)
#         except Vote.DoesNotExist:
#             if self.request.path.split('/')[-1] == 'like':
#                 Vote.objects.create(session_key=self.request.session.session_key, quote=quote, rating=1)
#                 quote.rating += 1
#                 quote.save()
#                 return Response({'message': 'you like it'}, status=200)
#             else:
#                 Vote.objects.create(session_key=self.request.session.session_key, quote=quote, rating=-1)
#                 quote.rating -= 1
#                 quote.save()
#                 return Response({'message': 'you dislike it'}, status=200)