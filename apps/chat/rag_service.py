# -*- coding: utf-8 -*-
"""
RAG Service for Military Counseling AI
Handles knowledge base and context-aware responses
"""
import os
import google.generativeai as genai


class MilitaryCounselingRAG:
    """
    RAG Service for Military Psychological Counseling
    Uses Gemini AI with knowledge base from docs
    """
    
    def __init__(self, api_key: str):
        """
        Initialize RAG service
        
        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> str:
        """Load knowledge base from markdown file"""
        try:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(current_dir, 'knowledge_base.md')
            
            with open(kb_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Knowledge base file not found")
            return ""
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            return ""
    
    def get_counseling_response(self, user_message: str) -> str:
        """
        Generate counseling response using RAG
        
        Args:
            user_message: User's question or concern
            
        Returns:
            AI-generated counseling response based on knowledge base
        """
        if not self.knowledge_base:
            return "Xin lỗi, tôi không thể truy cập cơ sở dữ liệu tư vấn. Vui lòng liên hệ quản trị viên."
        
        # Create enhanced prompt with knowledge base
        prompt = f"""
Bạn là một Chính trị viên chuyên nghiệp được hỗ trợ bởi AI, có nhiệm vụ tư vấn tâm lý và định hướng tư tưởng cho quân nhân.

KIẾN THỨC CHUYÊN MÔN CỦA BẠN:
{self.knowledge_base}

YÊU CẦU KHI TƯ VẤN:
1. Phân tích kỹ tình huống dựa trên kiến thức chuyên môn được cung cấp
2. Nhận diện các dấu hiệu liên quan từ cơ sở kiến thức
3. Đưa ra những biện pháp phòng ngừa và giải pháp cụ thể
4. Trả lời bằng văn bản thuần túy, KHÔNG sử dụng ký tự markdown (như **, ##, -, *)
5. Sử dụng ngôn ngữ chính trị chuẩn mực, thể hiện tính nhân văn và định hướng
6. Nếu tình huống nghiêm trọng, khuyến nghị báo cáo lãnh đạo hoặc tìm kiếm hỗ trợ chuyên môn

CÂU HỎI/VẤN ĐỀ CỦA QUÂN NHÂN:
{user_message}

Hãy tư vấn cụ thể, thiết thực và có tính định hướng dựa trên kiến thức chuyên môn.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của đồng chí. Vui lòng thử lại sau."


# Singleton instance
_rag_service = None

def get_rag_service(api_key: str) -> MilitaryCounselingRAG:
    """
    Get or create RAG service singleton
    
    Args:
        api_key: Gemini API key
        
    Returns:
        MilitaryCounselingRAG instance
    """
    global _rag_service
    if _rag_service is None:
        _rag_service = MilitaryCounselingRAG(api_key)
    return _rag_service

