from django.http import JsonResponse

def health_check(request):
    """GCP Cloud Run 상태 확인용 API"""
    return JsonResponse({"status": "ok", "message": "이음 서버가 정상적으로 작동 중입니다!"}, status=200)