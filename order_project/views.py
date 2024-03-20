from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['GET'])
def login_view(request):
    print()
    return render(request, 'dish_page.html')
