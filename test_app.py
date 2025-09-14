import unittest
import os
import tempfile
from app import app, get_db_connection, init_db

class ExpenseTrackerTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and database"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Initialize test database
        with app.app_context():
            init_db()
    
    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_index_redirect(self):
        """Test that index redirects to login when not authenticated"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.location)
    
    def test_signup_page(self):
        """Test signup page loads"""
        response = self.app.get('/auth/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.app.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_signup_process(self):
        """Test user signup process"""
        response = self.app.post('/auth/signup', data={
            'name': 'Test User',
            'age': '25',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully', response.data)
    
    def test_duplicate_email_signup(self):
        """Test that duplicate email signup fails"""
        # First signup
        self.app.post('/auth/signup', data={
            'name': 'Test User 1',
            'age': '25',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Second signup with same email
        response = self.app.post('/auth/signup', data={
            'name': 'Test User 2',
            'age': '30',
            'email': 'test@example.com',
            'password': 'testpassword456'
        })
        
        self.assertIn(b'Email already registered', response.data)
    
    def test_login_process(self):
        """Test user login process"""
        # First create a user
        self.app.post('/auth/signup', data={
            'name': 'Test User',
            'age': '25',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Then login
        response = self.app.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_invalid_login(self):
        """Test invalid login credentials"""
        response = self.app.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertIn(b'Invalid email or password', response.data)
    
    def test_dashboard_requires_auth(self):
        """Test that dashboard requires authentication"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.location)
    
    def test_add_transaction_requires_auth(self):
        """Test that add transaction requires authentication"""
        response = self.app.get('/transactions/new')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.location)

if __name__ == '__main__':
    unittest.main()
