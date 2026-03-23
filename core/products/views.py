"""View legado simples mantida apenas como referencia."""

from django.http import JsonResponse


def legacy_products_index(_request):
    """Direciona o leitor para a API versionada do modulo."""
    return JsonResponse({'detail': 'Use a API DRF em /api/v1/products/.'})
