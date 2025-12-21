from rest_framework.renderers import JSONRenderer
import time

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        success = status_code < 400
        message = "Request successful" if success else "Request failed"
        
        response_data = {
            "success": success,
            "code": status_code,
            "timestamp": int(time.time()),
        }

        if isinstance(data, dict):
            if 'message' in data:
                message = data.pop('message')
            
            if not success:
                response_data['errors'] = data
                response_data['data'] = None
            else:
                response_data['data'] = data
                
        elif isinstance(data, list):
            response_data['data'] = data
        else:
            response_data['data'] = data

        response_data['message'] = message

        return super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)