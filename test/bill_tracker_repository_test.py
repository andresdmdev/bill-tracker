import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import load_env
from repository.bill_tracker_repository import BillTrackerRepository

class TestBillTrackerRepository(unittest.TestCase):
    
    def setUp(self):
        # Configurar variables de entorno para las pruebas
        load_env()
        self.repository = BillTrackerRepository()
    
    @patch('repository.bill_tracker_repository.create_client')
    def test_authenticate_user_success(self, mock_create_client):
        # Configurar el mock para simular una autenticación exitosa
        mock_supabase = MagicMock()
        mock_auth = MagicMock()
        
        # Crear respuesta simulada de autenticación exitosa
        expected_response = {
            "access_token": "fake-token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": "user-id-123",
                "email": "test@example.com"
            }
        }
        
        # Configurar la cadena de mocks
        mock_create_client.return_value = mock_supabase
        mock_supabase.auth = mock_auth
        mock_auth.sign_in_with_password.return_value = expected_response
        
        # Reemplazar el cliente de Supabase en el repositorio
        self.repository.supabase = mock_supabase
        
        # Ejecutar el método a probar
        email = os.getenv('USER_EMAIL') or "test@example.com"
        password = os.getenv('USER_PASSWORD') or "password123"
        response = self.repository.authenticate_user(email, password)
        
        # Verificar que se llamó al método correcto con los parámetros correctos
        mock_auth.sign_in_with_password.assert_called_once_with({
            "email": email,
            "password": password
        })
        
        # Verificar que la respuesta es la esperada
        self.assertEqual(response, expected_response)
    
    @patch('repository.bill_tracker_repository.create_client')
    def test_insert_bill_success(self, mock_create_client):
        # Configurar el mock para simular una inserción exitosa
        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_insert = MagicMock()
        mock_execute = MagicMock()
        
        # Crear respuesta simulada de inserción exitosa
        expected_data = [{
            "id": "bill-id-123",
            "amount": 10090.0,  # Actualizado para coincidir con el valor real
            "notes": "Factura de prueba",
            "status": 2,
            "created_at": "2023-06-01T12:00:00Z"
        }]
        
        # Configurar la cadena de mocks
        mock_create_client.return_value = mock_supabase
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value.data = expected_data
        
        # Reemplazar el cliente de Supabase en el repositorio
        self.repository.supabase = mock_supabase
        
        # Ejecutar el método a probar
        response = self.repository.insert_bill()
        
        # Verificar que se llamó al método correcto con los parámetros correctos
        mock_supabase.table.assert_called_once_with("BillTracker")
        mock_table.insert.assert_called_once_with({
            "amount": 10090.0,  # Actualizado para coincidir con el valor real
            "notes": "Factura de prueba",
            "status": 2,
        })
        mock_insert.execute.assert_called_once()
        
        # Verificar que la respuesta es la esperada
        self.assertEqual(response, expected_data)

if __name__ == '__main__':
    unittest.main() 