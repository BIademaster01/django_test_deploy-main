from rest_framework.decorators import api_view
from rest_framework.response import Response
from pythainlp.tokenize import word_tokenize

@api_view(['POST'])
def tokenize_text(request):
    text = request.data.get('text', '')

    if not text:
        return Response({"error": "No text provided"}, status=400)

    # ตัดคำโดยใช้ PyThaiNLP
    words = word_tokenize(text, engine='newmm')
    
    return Response({"words": words})
