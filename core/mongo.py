from django.conf import settings
from mongoengine import connect


# Descomentar esta função se for usar o MongoDB local.
# def connect_db():
#     """
#     Estabelece a conexão com o MongoDB usando as configurações do Django.
#     """
#     mongo_host = getattr(settings, "MONGO_HOST", None)
#     mongo_db = getattr(settings, "MONGO_DB", "default_db")
#     mongo_user = getattr(settings, "MONGO_USER", None)
#     mongo_pass = getattr(settings, "MONGO_PASS", None)

    # if not mongo_host:
    #     raise ValueError("MONGO_HOST não está configurado no settings.py")

    # Conexão com autenticação opcional
    # connect(
    #     db=mongo_db,
    #     host=mongo_host,
    #     username=mongo_user,
    #     password=mongo_pass,
    #     alias="default",
    # )



# Comentar esta função se for usar o MongoDB local.
def connect_db():
    uri = (
        f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASS}"
        f"@{settings.MONGO_HOST}/{settings.MONGO_DB}?retryWrites=true&w=majority"
    )

    connect(
        db=settings.MONGO_DB,
        host=uri,
        alias="default"
    )