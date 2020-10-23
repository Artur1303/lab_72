from rest_framework.viewsets import ModelViewSet

from api.serializers import QuoteCreateSerializer, QuoteUpdateSerializer, QuoteSerializer
from webapp.models import Quote

class QuoteViewSet(ModelViewSet):
    queryset = Quote.objects.all()



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuoteCreateSerializer
        elif self.request.method == 'PUT':
            return QuoteUpdateSerializer
        return QuoteSerializer