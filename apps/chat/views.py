# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from .rag_service import get_rag_service

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyC1FVElNBndjCdECVbr-14KZNeoJhapVaQ"

@api_view(['POST'])
def ai_chat(request):
    """
    API endpoint for AI chat using RAG (Retrieval-Augmented Generation)
    with military psychological counseling knowledge base
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return Response(
                {'error': 'Message cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get RAG service instance
        rag_service = get_rag_service(GEMINI_API_KEY)
        
        # Get counseling response using RAG
        ai_response = rag_service.get_counseling_response(user_message)
        
        # Return response directly (no database storage)
        return Response({
            'response': ai_response,
            'timestamp': None  # No timestamp needed since we don't store
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON data'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print(f"AI Chat Error: {str(e)}")
        return Response(
            {'error': 'An error occurred while processing your message. Please try again later.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
