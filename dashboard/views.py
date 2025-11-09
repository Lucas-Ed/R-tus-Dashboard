from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import ObjectId
from decimal import Decimal, InvalidOperation
from mongoengine.errors import ValidationError as MEValidationError
from .api_utils import document_to_dict
from .models import Receita, Ingrediente


# ---------- Páginas ----------
def index(request):
    return render(request, 'dashboard/index.html', {'app_name': 'Rótus'})


def dash(request):
    return render(request, 'dashboard/dash.html', {'app_name': 'Rótus'})


# ---------- Ingredientes (CRUD completo) ----------
@csrf_exempt
def ingredientes_list_create(request):
    """
    GET -> lista todos os ingredientes
    POST -> cria um novo ingrediente
    """
    if request.method == 'GET':
        try:
            ingredientes = Ingrediente.objects.all()
            data = [document_to_dict(i) for i in ingredientes]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))

            ingrediente = Ingrediente(
                nome=payload.get('nome'),
                alimento=payload.get('alimento'),
                peso_bruto=Decimal(str(payload.get('peso_bruto', 0))),
                peso_liquido=Decimal(str(payload.get('peso_liquido', 0))),
                peso_processado=Decimal(str(payload.get('peso_processado', payload.get('peso_liquido', 0))))
            )

            # Se tiver receita_id no payload, relaciona
            if payload.get('receita_id'):
                try:
                    receita = Receita.objects.get(id=ObjectId(payload['receita_id']))
                    ingrediente.receita = receita
                except Receita.DoesNotExist:
                    return JsonResponse({'error': 'Receita não encontrada.'}, status=404)

            ingrediente.save()
            return JsonResponse(document_to_dict(ingrediente), status=201)

        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def ingrediente_detail(request, ingrediente_id):
    """
    GET -> retorna um ingrediente
    PUT -> atualiza um ingrediente
    DELETE -> exclui um ingrediente
    """
    try:
        ingrediente = Ingrediente.objects.get(id=ObjectId(ingrediente_id))
    except Exception:
        return JsonResponse({'error': 'Ingrediente não encontrado.'}, status=404)

    if request.method == 'GET':
        return JsonResponse(document_to_dict(ingrediente))

    elif request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode('utf-8'))

            for field in ['nome', 'unidade', 'quantidade']:
                if field in payload:
                    setattr(ingrediente, field, payload[field])

            ingrediente.save()
            return JsonResponse(document_to_dict(ingrediente))
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    elif request.method == 'DELETE':
        ingrediente.delete()
        return HttpResponse(status=204)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

@csrf_exempt
def ingredientes_create_for_receita(request, receita_id):
    """Adiciona ingredientes a uma receita existente"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            receita = Receita.objects.get(id=ObjectId(receita_id))
            ingredientes_data = data.get("ingredientes", [])
            ingredientes_criados = []

            for ing in ingredientes_data:
                ingrediente = Ingrediente(
                    receita=receita,
                    alimento=ing.get("nome"),
                    peso_bruto=Decimal(str(ing.get("peso_bruto", 0))),
                    peso_liquido=Decimal(str(ing.get("peso_liquido", 0))),
                    peso_processado=Decimal(str(ing.get("peso_processado", ing.get("peso_liquido", 0))))
                )

                if ing.get("alimento_id"):
                    try:
                        ingrediente.alimento = AlimentoTaco.objects.get(id=ObjectId(ing["alimento_id"]))
                    except Exception:
                        ingrediente.alimento = None

                ingrediente.save()
                ingredientes_criados.append(document_to_dict(ingrediente))

            return JsonResponse({
                "message": "Ingredientes adicionados com sucesso.",
                "ingredientes": ingredientes_criados
            }, status=201)

        except Receita.DoesNotExist:
            return JsonResponse({"error": "Receita não encontrada."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método não permitido."}, status=405)

# ---------- Receitas ----------
@csrf_exempt
def receitas_list_create(request):
    """
    GET -> lista receitas
    POST -> cria receita (com ingredientes opcionais no body)
    """
    # === GET ===
    if request.method == 'GET':
        try:
            receitas = Receita.objects.order_by('-created_at')
            data = [document_to_dict(r) for r in receitas]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    # === POST ===
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            print("Payload recebido:", payload)  # debug

            nome = payload.get('nome')
            if not nome:
                return HttpResponseBadRequest(json.dumps({'error': 'O campo "nome" é obrigatório.'}),
                                              content_type='application/json')

            # Helpers seguros
            def safe_decimal(val):
                try:
                    return Decimal(str(val)) if val not in (None, '', 'null') else Decimal('0')
                except (InvalidOperation, ValueError, TypeError):
                    return Decimal('0')

            def safe_int(val):
                try:
                    return int(val)
                except (ValueError, TypeError):
                    return 0

            # Criação da receita
            receita = Receita(
                nome=nome.strip(),
                categoria=(payload.get('categoria') or '').strip(),
                tempo_preparo_horas=safe_int(payload.get('tempo_preparo_horas', 0)),
                tempo_preparo_minutos=safe_int(payload.get('tempo_preparo_minutos', 0)),
                porcao_individual=safe_decimal(payload.get('porcao_individual')),
                medida=payload.get('medida', 'g'),
                modo_preparo=(payload.get('modo_preparo') or '').strip(),
            )
            receita.save()

            # Ingredientes opcionais
            ingredientes_payload = payload.get('ingredientes', [])
            ingredientes_criados = []
            for ing in ingredientes_payload:
                ingrediente = Ingrediente(
                    receita=receita,
                    alimento=ing.get('nome'),
                    peso_bruto=safe_decimal(ing.get('peso_bruto')),
                    peso_liquido=safe_decimal(ing.get('peso_liquido')),
                    peso_processado=safe_decimal(ing.get('peso_processado', ing.get('peso_liquido'))),
                )

                if ing.get('alimento_id'):
                    try:
                        ingrediente.alimento = AlimentoTaco.objects.get(id=ObjectId(ing['alimento_id']))
                    except Exception:
                        ingrediente.alimento = None

                ingrediente.save()
                ingredientes_criados.append(document_to_dict(ingrediente))

            resp = document_to_dict(receita)
            resp['ingredientes'] = ingredientes_criados
            return JsonResponse(resp, status=201)

        except MEValidationError as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def receita_detail(request, receita_id):
    """
    GET, PUT, DELETE para receita específica
    """
    try:
        receita = Receita.objects.get(id=ObjectId(receita_id))
    except Exception:
        return HttpResponse(status=404)

    # GET
    if request.method == 'GET':
        r = document_to_dict(receita)
        ingredientes = Ingrediente.objects(receita=receita)
        r['ingredientes'] = [document_to_dict(i) for i in ingredientes]
        return JsonResponse(r)

    # PUT
    if request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode('utf-8'))

            for field in ['nome', 'categoria', 'modo_preparo', 'medida']:
                if field in payload:
                    setattr(receita, field, payload[field])

            if 'porcao_individual' in payload:
                receita.porcao_individual = Decimal(str(payload['porcao_individual']))
            if 'tempo_preparo_horas' in payload:
                receita.tempo_preparo_horas = int(payload['tempo_preparo_horas'])
            if 'tempo_preparo_minutos' in payload:
                receita.tempo_preparo_minutos = int(payload['tempo_preparo_minutos'])

            receita.save()
            return JsonResponse(document_to_dict(receita))

        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

    # DELETE
    if request.method == 'DELETE':
        Ingrediente.objects(receita=receita).delete()
        receita.delete()
        return HttpResponse(status=204)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])