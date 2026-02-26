# Helper pour obtenir les headers d'authentification
def get_auth_headers(client, user_data):
    client.post("/users/register", json=user_data)
    response = client.post(
        "/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


# Test de création d'une collection
def test_create_collection(client, test_user_data, test_collection_data):
    headers = get_auth_headers(client, test_user_data)
    response = client.post("/collection/", json=test_collection_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_collection_data["title"]
    assert data["description"] == test_collection_data["description"]
    
    
# test de récupération d'une collection
def test_get_a_collection(client, test_user_data, test_collection_data):
    headers = get_auth_headers(client, test_user_data)
    response = client.post("/collection/", json=test_collection_data, headers=headers)
    data = response.json()
    response = client.get(f"/collection/{data['id']}", headers=headers)
    assert response.status_code == 200
    collection = response.json()
    assert collection["title"] == test_collection_data["title"]
    
    