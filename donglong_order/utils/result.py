from django.http import JsonResponse


class Result:
    @staticmethod
    def success(data=None):
        return JsonResponse({'success': True, 'data': data})

    @staticmethod
    def error(message):
        return JsonResponse({'success': False, 'error_message': message})


class Result_page:
    @staticmethod
    def success(data=None, total=0):
        return JsonResponse({'success': True, 'data': data, 'total': total})

    @staticmethod
    def error(message, total=0):
        return JsonResponse({'success': False, 'error_message': message, 'total': total})
