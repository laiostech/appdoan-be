from django.conf import settings
from django.db.models import Count
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, BaseParser
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

import boto3
import uuid
import re
import json
from .models import News
from .serializers import ImageUploadSerializer, NewsSerializer, NewsWithReactionSerializer, ImageDeleteSerializer
from ..generic_serializer import MessageResponseSerializer, ErrorResponseSerializer

def extract_first_image_from_content(content):
    """
    Extract the first image URL from news content JSON
    Returns None if no image found or content is not valid JSON
    """
    try:
        content_blocks = json.loads(content)
        if isinstance(content_blocks, list):
            for block in content_blocks:
                if isinstance(block, dict) and block.get('type') == 'image' and block.get('url'):
                    return block['url']
    except (json.JSONDecodeError, TypeError):
        pass
    return None

class RawImageParser(BaseParser):
    """
    Parser for raw image uploads with Content-Type: image/* or text/plain (iPhone compatibility)
    Supports iPhone (HEIC/HEIF), Android, and all standard image formats
    """
    media_type = '*/*'  # Accept all content types to handle iPhone uploads

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parse raw image data and convert to file-like object
        Supports formats from iPhone, Android and other mobile devices
        Only process if NOT multipart/form-data (which should be handled by MultiPartParser)
        """
        request = parser_context['request']
        content_type = request.content_type.lower()
        
        # Skip if this is multipart/form-data - let MultiPartParser handle it
        if 'multipart/form-data' in content_type:
            return {}
        
        # Read raw data first to analyze magic bytes
        raw_data = stream.read()
        
        # Debug logging
        print(f"RawImageParser - Content-Type: {content_type}")
        print(f"RawImageParser - Data size: {len(raw_data)} bytes")
        
        # If no data, reject
        if not raw_data:
            raise ValueError("No image data received")
        
        # Detect image format from magic bytes (first few bytes)
        ext = self._detect_image_format_from_bytes(raw_data, content_type)
        
        print(f"Detected image format: {ext} from Content-Type: {content_type}")
        
        # Generate meaningful filename
        timestamp = uuid.uuid4().hex[:8]
        filename = f'mobile_upload_{timestamp}.{ext}'
        
        # Create InMemoryUploadedFile
        file_buffer = io.BytesIO(raw_data)
        file_buffer.seek(0)  # Reset to beginning
        
        file_obj = InMemoryUploadedFile(
            file=file_buffer,
            field_name='image',
            name=filename,
            content_type='image/jpeg' if ext == 'jpg' else f'image/{ext}',  # Fix content-type for proper processing
            size=len(raw_data),
            charset=None
        )
        
        print(f"Created file object: {filename}, size: {len(raw_data)}, content_type: {file_obj.content_type}")
        return {'image': file_obj}
        
    def _detect_image_format_from_bytes(self, data, content_type):
        """
        Detect image format from magic bytes and content-type
        """
        # Check magic bytes first (more reliable than content-type)
        if data.startswith(b'\xff\xd8\xff'):
            return 'jpg'  # JPEG
        elif data.startswith(b'\x89PNG'):
            return 'png'  # PNG
        elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
            return 'gif'  # GIF
        elif data.startswith(b'RIFF') and b'WEBP' in data[:12]:
            return 'webp'  # WebP
        elif data.startswith(b'\x00\x00\x00\x20ftypheic') or data.startswith(b'\x00\x00\x00\x18ftypheic'):
            return 'heic'  # HEIC (iPhone)
        elif data.startswith(b'\x00\x00\x00\x20ftypheif') or data.startswith(b'\x00\x00\x00\x18ftypheif'):
            return 'heif'  # HEIF (iPhone)
        elif data.startswith(b'BM'):
            return 'bmp'  # BMP
        elif data.startswith(b'II*\x00') or data.startswith(b'MM\x00*'):
            return 'tiff'  # TIFF
        
        # Fallback to content-type analysis
        if 'jpeg' in content_type or 'jpg' in content_type:
            return 'jpg'
        elif 'png' in content_type:
            return 'png'
        elif 'gif' in content_type:
            return 'gif'
        elif 'webp' in content_type:
            return 'webp'
        elif 'heic' in content_type:
            return 'heic'
        elif 'heif' in content_type:
            return 'heif'
        elif 'avif' in content_type:
            return 'avif'
        elif 'bmp' in content_type:
            return 'bmp'
        elif 'tiff' in content_type or 'tif' in content_type:
            return 'tiff'
        # Handle iPhone sending text/plain for images
        elif 'plain' in content_type and len(data) > 1000:  # Likely an image if substantial data
            # Try to guess from data structure
            if b'JFIF' in data[:100] or b'Exif' in data[:100]:
                return 'jpg'
            else:
                return 'jpg'  # Default for iPhone
        
        # Final fallback
        return 'jpg'

@extend_schema(
    tags=['News'],
    request=NewsSerializer,
    responses={
        200: NewsWithReactionSerializer(many=True),
        201: NewsSerializer,
        400: ErrorResponseSerializer
    }
)
class NewsAllListView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def get(self, request):
        news_list = News.objects.annotate(reaction_count=Count('reaction'))

        data = [
            {
                "id": news.id,
                "title": news.title,
                "summary": news.summary or "",  # Include summary with fallback to empty string
                "content": news.content,
                "create_at": news.create_at,
                "update_at": news.update_at,
                "category": news.category,
                "reaction_count": news.reaction_count,
                "image": extract_first_image_from_content(news.content),  # Extract first image from content
            }
            for news in news_list
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['News'],
    request=NewsSerializer,  # For PUT
    responses={
        200: NewsSerializer,
        400: ErrorResponseSerializer,
        204: MessageResponseSerializer
    }
)
class NewsDetailView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def get(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
            serializer = NewsSerializer(news)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response({'detail': 'News not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, news_id):
        news = News.objects.get(id=news_id)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_id):
        news = News.objects.get(id=news_id)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['News'],
    responses={200: NewsSerializer(many=True)}
)
class NewsByCategoryView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def get(self, request, category):
        news_list = News.objects.filter(category=category).annotate(reaction_count=Count('reaction'))
        
        data = [
            {
                "id": news.id,
                "title": news.title,
                "summary": news.summary or "",  # Include summary with fallback to empty string
                "content": news.content,
                "create_at": news.create_at,
                "update_at": news.update_at,
                "category": news.category,
                "reaction_count": news.reaction_count,
                "image": extract_first_image_from_content(news.content),  # Extract first image from content
            }
            for news in news_list
        ]
        return Response(data, status=status.HTTP_200_OK)
    
@extend_schema(
    tags=['Images'],
    request=ImageUploadSerializer,
    responses={201: ImageUploadSerializer}
)
class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser, RawImageParser]  # Use MultiPartParser for multipart/form-data

    def post(self, request, *args, **kwargs):
        # Enhanced debug logging
        print("=== IMAGE UPLOAD REQUEST DEBUG ===")
        print(f"Content-Type: {request.content_type}")
        print(f"Request data keys: {list(request.data.keys()) if hasattr(request, 'data') else 'No data'}")
        print(f"Request FILES keys: {list(request.FILES.keys()) if hasattr(request, 'FILES') else 'No FILES'}")
        
        # Get image from FILES (MultiPartParser) or data (RawImageParser)
        image_file = request.FILES.get('image') or request.data.get('image')
        
        if image_file:
            print(f"Found image: {type(image_file)}")
            print(f"Image file name: {getattr(image_file, 'name', 'No name')}")
            print(f"Image file size: {getattr(image_file, 'size', 'No size')}")
            print(f"Image content type: {getattr(image_file, 'content_type', 'No content_type')}")
            if hasattr(image_file, 'file'):
                print(f"Image file position: {image_file.file.tell()}")
                image_file.file.seek(0)  # Reset to beginning
        else:
            print("No image found in request.FILES or request.data")
            return Response({'error': 'No image file found in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        print("=====================================")
        
        serializer = ImageUploadSerializer(data={'image': image_file})
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['image']
        id = uuid.uuid4().hex
        file_name = f"uploads/{id}_{image.name}"

        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL or 'http://localhost:9000',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        s3.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'})

        return Response({'id': id}, status=status.HTTP_201_CREATED)
    
@extend_schema(
    tags=['Images'],
    request=ImageDeleteSerializer,
    responses={200: dict}
)
class ImageBatchDeleteView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        serializer = ImageDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uuids = serializer.validated_data['ids']
        deleted_keys = []

        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL or 'http://localhost:9000',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='uploads/')
        all_keys = [obj['Key'] for obj in response.get('Contents', [])]

        for uid in uuids:
            pattern = re.compile(rf'^uploads/{re.escape(uid)}_[^/]+$')
            for key in all_keys:
                if pattern.match(key):
                    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
                    deleted_keys.append(key)

        if not deleted_keys:
            return Response({'detail': 'No matching files found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'deleted': deleted_keys}, status=status.HTTP_200_OK)

@extend_schema(
    tags=['Images'],
    responses={200: 'Image file'}
)
class ImageServeView(APIView):
    """
    Serve images from MinIO through Django backend
    """
    def get(self, request, filename):
        try:
            s3 = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL or 'http://localhost:9000',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            
            # Get the object from MinIO
            response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f'uploads/{filename}')
            
            # Return the image data
            from django.http import HttpResponse
            content_type = response.get('ContentType', 'image/jpeg')
            return HttpResponse(response['Body'].read(), content_type=content_type)
            
        except Exception as e:
            from django.http import Http404
            raise Http404("Image not found")