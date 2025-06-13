from django.test import TestCase
from .models import Persona  # Uncomment if you have a Persona model defined
from django.urls import reverse_lazy

# Create your tests here.
class PersonaViewsTestCase(TestCase):
    def setUp(self):
        # Create a Persona instance for testing
        self.persona = Persona.objects.create(nombre="Test", edad=30, email="test@test.com")
        self.list_url = reverse_lazy('persona:lista')
        self.detail_url = reverse_lazy('persona:detalle', kwargs={'pk': self.persona.pk})
        self.create_url = reverse_lazy('persona:crear')
        self.update_url = reverse_lazy('persona:editar', kwargs={'pk': self.persona.pk})
        self.delete_url = reverse_lazy('persona:eliminar', kwargs={'pk': self.persona.pk})
    
    def test_persona_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/lista.html')
        self.assertContains(response, self.persona.nombre)
    
    def test_persona_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/detalle.html')
        self.assertContains(response, self.persona.nombre)
    
    def test_persona_create_view(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/crear.html')
        
        # Test POST request to create a new Persona
        response = self.client.post(self.create_url, {
            'nombre': 'New Persona',
            'edad': 25,
            'email': 'persona@personas.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Persona.objects.filter(nombre='New Persona').exists())
    
    def test_persona_update_view(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/crear.html')
        
        # Test POST request to update the Persona
        response = self.client.post(self.update_url, {
            'nombre': 'Updated Persona',
            'edad': 35,
            'email': 'persona.nuevomail@personas.com'
        })
        self.assertEqual(response.status_code, 302)
        self.persona.refresh_from_db()
        self.assertEqual(self.persona.nombre, 'Updated Persona')
        self.assertEqual(self.persona.edad, 35)
        self.assertEqual(self.persona.email, 'persona.nuevomail@personas.com')
    
    def test_persona_delete_view(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/eliminar.html')
        
        # Test POST request to delete the Persona
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Persona.objects.filter(pk=self.persona.pk).exists())

    def test_persona_search_view(self):
        search_url = reverse_lazy('persona:buscar')
        response = self.client.get(search_url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/buscar.html')
        self.assertContains(response, self.persona.nombre)
        
        # Test search with no results
        response = self.client.get(search_url, {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'persona/buscar.html')
        self.assertNotContains(response, self.persona.nombre)
       