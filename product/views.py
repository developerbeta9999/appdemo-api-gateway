import os
import uuid
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .producer import publish

MS_PRODUCT_URL = os.environ.get('MS_PRODUCT_URL', 'http://ms-products')

@csrf_exempt
def gateway_products(request):
    if request.method == 'GET':
        # GET sigue siendo síncrono (HTTP) por ahora
        try:
            response = requests.get(f"{MS_PRODUCT_URL.rstrip('/')}/products/")
            return JsonResponse(response.json(), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'POST':
        # POST se vuelve ASÍNCRONO (Kafka)
        try:
            data = json.loads(request.body)
            new_uuid = str(uuid.uuid4())
            data['product_uuid'] = new_uuid

            # En lugar de llamar a la API del microservicio, enviamos el evento
            publish('product-updates', 'create', data)

            # Respuesta inmediata al usuario
            return JsonResponse({
                'status': 'Accepted',
                'message': 'Producto en cola de creación',
                'product_uuid': new_uuid
            }, status=202)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
