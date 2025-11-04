from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Documento, RotuloNutricional, RotuloFrontal
from bson import ObjectId
from decimal import Decimal

def index(request):
    return render(request, 'dashboard/index.html', {'app_name': 'Rótus'})

def to_dict_rotulo(r):
    return {
        "id": str(r.id),
        "documento_id": str(r.documento.id) if r.documento else None,
        "nome_receita": r.documento.nome_receita if r.documento else "",
        "energia_kcal_100": float(r.energia_kcal_100) if r.energia_kcal_100 is not None else None,
        "proteinas_g_100": float(r.proteinas_g_100) if r.proteinas_g_100 is not None else None,
        "sodio_mg_100": float(r.sodio_mg_100) if r.sodio_mg_100 is not None else None,
        "created_at": r.created_at.isoformat(),
    }

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
@csrf_exempt
def rotulos_list(request):
    if request.method == "GET":
        rotulos = RotuloNutricional.objects.order_by('-created_at').limit(200)
        data = [to_dict_rotulo(r) for r in rotulos]
        return JsonResponse({"results": data})
    else:  # POST create
        try:
            payload = json.loads(request.body)
            # criar Documento se necessário
            doc_data = payload.get('documento') or {"nome_receita": payload.get("nome_receita", "Receita")}
            doc = Documento(**doc_data)
            doc.save()
            # criar rótulo
            r = RotuloNutricional(
                documento=doc,
                porcao_definida_g_ml = payload.get('porcao_definida_g_ml', 100),
                fator_densidade = payload.get('fator_densidade', 1),
                energia_kcal_100 = Decimal(str(payload.get('energia_kcal_100', 0))),
                proteinas_g_100 = Decimal(str(payload.get('proteinas_g_100', 0))),
                carboidratos_g_100 = Decimal(str(payload.get('carboidratos_g_100', 0))),
                acucares_totais_g_100 = Decimal(str(payload.get('acucares_totais_g_100', 0))),
                sodio_mg_100 = Decimal(str(payload.get('sodio_mg_100', 0))),
            )
            r.save()
            return JsonResponse({"result": to_dict_rotulo(r)}, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def rotulos_detail(request, id):
    try:
        r = RotuloNutricional.objects.get(id=id)
    except RotuloNutricional.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"result": to_dict_rotulo(r)})

    if request.method == "PUT":
        try:
            payload = json.loads(request.body)
            # atualiza alguns campos de exemplo
            for f in ['energia_kcal_100', 'proteinas_g_100', 'sodio_mg_100', 'porcao_definida_g_ml']:
                if f in payload:
                    setattr(r, f, payload[f])
            r.save()
            return JsonResponse({"result": to_dict_rotulo(r)})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    if request.method == "DELETE":
        r.delete()
        return JsonResponse({"status": "deleted"})

@require_http_methods(["GET"])
def indicadores(request):
    # Exemplo de indicadores: média de energia, counts por categoria alto_sodio etc.
    total = RotuloNutricional.objects.count()
    avg_energy = RotuloNutricional.objects.aggregate(*[
        {"$group": {"_id": None, "avgEnergy": {"$avg": "$energia_kcal_100"}}}
    ])
    # aggregate retornará cursor - mas para simplicidade faremos manual:
    energia_vals = [float(r.energia_kcal_100 or 0) for r in RotuloNutricional.objects.only('energia_kcal_100')]
    avg_energy_val = sum(energia_vals)/len(energia_vals) if energia_vals else 0

    # Top 10 receitas por energia (exemplo)
    top = RotuloNutricional.objects.order_by('-energia_kcal_100').limit(10)
    top_list = [{"nome": r.documento.nome_receita if r.documento else "", "energia": float(r.energia_kcal_100 or 0)} for r in top]

    return JsonResponse({
        "total_rotulos": total,
        "avg_energy_kcal_100": avg_energy_val,
        "top_energy": top_list
    })