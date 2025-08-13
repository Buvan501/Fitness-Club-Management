from models import db, User, Role


def test_home_page(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'FitClub' in resp.data or b'Fitness' in resp.data


def test_services_page(client):
    resp = client.get('/services')
    assert resp.status_code == 200


def test_register_and_login(client, app_context):
    # Ensure member role exists
    if not Role.query.filter_by(name='member').first():
        db.session.add(Role(name='member'))
        db.session.commit()

    # Register
    resp = client.post('/register', data={
        'username': 'pytest_user',
        'email': 'py@test.com',
        'password': 'pytest_pw',
        'confirm_password': 'pytest_pw',
        'first_name': 'Py',
        'last_name': 'Test',
        'phone': '1112223333',
    }, follow_redirects=True)
    assert resp.status_code == 200
    # After registration we redirect to login; assert login page is shown (navbar Login link present)
    assert b'Login' in resp.data

    # Login
    resp = client.post('/login', data={
        'username': 'pytest_user',
        'password': 'pytest_pw',
    }, follow_redirects=True)
    assert resp.status_code == 200


def test_contact_page(client):
    resp = client.get('/contact')
    assert resp.status_code == 200
    assert b'Contact' in resp.data or b'Get in Touch' in resp.data


def test_admin_requires_login(client):
    resp = client.get('/admin', follow_redirects=True)
    assert resp.status_code == 200
    # Should redirect to login page
    assert b'Login' in resp.data or b'Please log in' in resp.data


