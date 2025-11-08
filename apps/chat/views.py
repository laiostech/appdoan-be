# -*- coding: utf-8 -*-
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBfy5Ii-qZ6FrFKfYqzIlLgn55DF3ZX7lI"
genai.configure(api_key=GEMINI_API_KEY)

@api_view(['POST'])
def ai_chat(request):
    """
    API endpoint for AI chat using Gemini (no history storage)
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return Response(
                {'error': 'Message cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create context for AI - instruct AI to respond in Vietnamese
        context = """
        Ban la mot tro ly AI thong minh va huu ich. Hay luon tra loi bang tieng Viet. 
        Ban co the giup nguoi dung voi nhieu van de khac nhau nhu:
        - Tra loi cau hoi chung
        - Giai thich kien thuc
        - Ho tro giai quyet van de
        - Tu van va dua ra goi y
        
        Hay tra loi mot cach than thien, chinh xac va huu ich.
        """
        
        # Combine context with user message
        full_prompt = f"{context}\n\nCau hoi cua nguoi dung: {user_message}"
        
        # Send message to Gemini AI
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
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
