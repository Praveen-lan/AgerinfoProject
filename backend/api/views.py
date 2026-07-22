from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count
from .models import News, Gallery, Slider, Topic
from .serializers import NewsSerializer, GallerySerializer, SliderSerializer, TopicSerializer


# ========== AUTH ==========
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'email': user.email})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


# ========== COUNTS ==========
@api_view(['GET'])
def get_counts(request):
    return Response({
        'news': News.objects.count(),
        'gallery': Gallery.objects.count(),
        'slider': Slider.objects.count(),
        'topics': Topic.objects.count(),
    })


# ========== NEWS ==========
@api_view(['GET'])
def news_list(request):
    items = News.objects.all()
    return Response(NewsSerializer(items, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def news_create(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def news_detail(request, pk):
    try:
        item = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(NewsSerializer(item).data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def news_update(request, pk):
    try:
        item = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = NewsSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def news_delete(request, pk):
    try:
        item = News.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ========== GALLERY ==========
@api_view(['GET'])
def gallery_list(request):
    items = Gallery.objects.all()
    return Response(GallerySerializer(items, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gallery_create(request):
    serializer = GallerySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gallery_detail(request, pk):
    try:
        item = Gallery.objects.get(pk=pk)
    except Gallery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(GallerySerializer(item).data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def gallery_update(request, pk):
    try:
        item = Gallery.objects.get(pk=pk)
    except Gallery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = GallerySerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def gallery_delete(request, pk):
    try:
        item = Gallery.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Gallery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ========== SLIDER ==========
@api_view(['GET'])
def slider_list(request):
    items = Slider.objects.all()
    return Response(SliderSerializer(items, many=True).data)


@api_view(['GET'])
def slider_detail(request, pk):
    try:
        item = Slider.objects.get(pk=pk)
    except Slider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(SliderSerializer(item).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def slider_create(request):
    serializer = SliderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def slider_update(request, pk):
    try:
        item = Slider.objects.get(pk=pk)
    except Slider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SliderSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def slider_delete(request, pk):
    try:
        item = Slider.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Slider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ========== TOPICS ==========
@api_view(['GET'])
def topics_list(request):
    items = Topic.objects.all()
    return Response(TopicSerializer(items, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topics_create(request):
    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def topics_detail(request, pk):
    try:
        item = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(TopicSerializer(item).data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def topics_update(request, pk):
    try:
        item = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TopicSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def topics_delete(request, pk):
    try:
        item = Topic.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
