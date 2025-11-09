from bson import ObjectId
from decimal import Decimal
import datetime
from mongoengine.base.datastructures import BaseDict

def _convert_value(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, Decimal):
        # converter Decimal para float (ou str se preferir precisão)
        return float(v)
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    if isinstance(v, BaseDict):
        return dict(v)
    # arrays/dicts recursion
    if isinstance(v, list):
        return [_convert_value(x) for x in v]
    if isinstance(v, dict):
        return {k: _convert_value(val) for k, val in v.items()}
    return v

def document_to_dict(doc):
    """
    Converte um documento MongoEngine (Document) em dict JSON-friendly.
    Remove referências internas de MongoEngine e converte ObjectId/Decimal/datetime.
    """
    # Usa to_mongo() para obter um dict bruto
    raw = doc.to_mongo().to_dict()
    # _id -> id string
    if '_id' in raw:
        raw['id'] = str(raw.pop('_id'))
    # _cls/_sa4/etc podem aparecer dependendo das configurações - remover campos indesejados
    raw.pop('_cls', None)
    raw.pop('_types', None)

    # Converte recursivamente valores
    result = {}
    for k, v in raw.items():
        result[k] = _convert_value(v)
    return result