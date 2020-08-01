from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime


from eph_calendar.models import RegisteredDate
from eph_calendar.serializers import (
    RegisteredDateSerializer
)


class DatesViewSet(APIView):
    serializer_class = RegisteredDateSerializer

    def get(self, request, format=None):
        queryset = RegisteredDate.objects.all()
        dia = self.request.query_params.get('dia', None)

        if not dia:
            serializer = RegisteredDateSerializer(queryset, many=True)
            return Response(serializer.data)

        date = DatesViewSet._valid_date(dia)
        if date is None:
            return Response(
                "Parámetro dia con formato inadecuado", status=400)

        today = queryset.filter(date=date).order_by("title")
        month = queryset.filter(date__month=date.month, date__year=date.year).order_by("date__day")
        data_dict = DatesViewSet._make_data_dict(today, month)

        return Response(data_dict)

    @staticmethod
    def _valid_date(date):
        response = None
        try:
            response = datetime.strptime(date, "%Y-%m-%d").date()
        except Exception:
            pass
        return response

    @staticmethod
    def _list_of_days_titles(days):
        return [td.title for td in days]


    @staticmethod
    def _make_data_dict(today, month):
        data_dict = {
            "hoy": DatesViewSet._list_of_days_titles(today),
            "mes": {
                td.date.day: DatesViewSet._list_of_days_titles(
                    month.filter(date=td.date)) for td in month.only("date").distinct()
            }
        }
        return data_dict
