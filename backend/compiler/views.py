from rest_framework.views import APIView
from rest_framework.response import Response
from .compiler import run_code 
import uuid
import re

class CompileCodeView(APIView):
    code_storage = {} 

    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', '').lower()

        if not code or not language:
            return Response({'error': 'Code and Language are required fields.'}, status=400)
        
        code_id = str(uuid.uuid4())
        CompileCodeView.code_storage[code_id] = {
            'code': code,
            'language': language
        }

        if not re.search(r"\{\{.*?\}\}", code):
            # No placeholders, run immediately
            output = run_code(language, code)
            return Response({
                'output': output,
                'code_id': code_id,
                'message': 'Code executed successfully (no inputs required).'
            })

        return Response({
            'message': 'Code stored successfully. Waiting for inputs...',
            'code_id': code_id
        })

    def put(self, request):
        code_id = request.data.get('code_id', '')
        new_inputs = request.data.get('inputs', {})

        if not code_id or not new_inputs:
            return Response({'error': 'Code ID and inputs are required fields.'}, status=400)

        if code_id not in CompileCodeView.code_storage:
            return Response({'error': 'Invalid Code ID.'}, status=404)

        saved_code = CompileCodeView.code_storage[code_id]['code']
        language = CompileCodeView.code_storage[code_id]['language']

        for placeholder, value in new_inputs.items():
            saved_code = saved_code.replace(f"{{{{{placeholder}}}}}", str(value))

        output = run_code(language, saved_code)

        return Response({
            'output': output,
            'message': 'Code executed with provided inputs.'
        })
