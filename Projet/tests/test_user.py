# Test de création d'un nouvel utilisateur
def test_register_user(client, test_user_data):
    response = client.post("/users/register", json=test_user_data)  # <-- On crée un utilisateur
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    
# Test d'authentification --> un utilisateur enregistré peut se connecter et reçoit un token
def test_auth(client, test_user_data):
    response = client.post("/users/register", json=test_user_data)  # <-- On crée un utilisateur
    
    response_auth = client.post(                        # crée un token avec les credentials de l'utilisateur
        "/token",
        data = {"username":test_user_data["username"],    
                "password":test_user_data["password"]})
    
    assert response_auth.status_code == 200     # On vérifie que l'authentification a réussi (code 200 = OK)
    data = response_auth.json() # convertit la réponse en JSON (dictionnaire python)
    assert "access_token" in data   # Vérifie que la réponse contient bien un token
    