from django.http import JsonResponse
from django.shortcuts import render


class Result:
    @staticmethod
    def success(data=None):
        return JsonResponse({'success': True, 'data': data})

    @staticmethod
    def error(message):
        return JsonResponse({'success': False, 'message': message})


class Result_page:
    @staticmethod
    def success(data=None, paginator=None, page_number=1, page_html='', request=None):
        response_data = {
            'success': True,
            'data': data,
            'count': paginator.count,
            'pages': paginator.num_pages,
            'page': page_number,
        }

        if request.is_ajax():
            return JsonResponse(response_data)
        else:
            return render(request, page_html, response_data)

    @staticmethod
    def error(message, total=0):
        return JsonResponse({'success': False, 'message': message, 'total': total})
