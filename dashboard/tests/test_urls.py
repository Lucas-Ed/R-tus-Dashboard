from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard import views

class DashboardUrlsTest(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('dashboard:index')
        self.assertEqual(resolve(url).func, views.index)

    def test_api_rotulos_list_resolves(self):
        url = reverse('dashboard:rotulos_list')
        self.assertEqual(resolve(url).func, views.rotulos_list)

    def test_api_indicadores_resolves(self):
        url = reverse('dashboard:indicadores')
        self.assertEqual(resolve(url).func, views.indicadores)
