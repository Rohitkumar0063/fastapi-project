import pytest
@pytest.mark.asyncio

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/register_user", json={
        "user_name": "Test User",
        "user_email": "test@gmail.com",
        "user_password": "test123",
        "user_phoneno": 9999999999,
        "user_role": "user"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "user created successfully"


async def test_login(client):
    # pehle register karo isi DB mein
    await client.post("/register_user", json={
        "user_name": "Test User",
        "user_email": "test@gmail.com",
        "user_password": "test123",
        "user_phoneno": 9999999999,
        "user_role": "user"
    })
    # ab login karo
    response = await client.post("/login", json={
        "email": "test@gmail.com",
        "password": "test123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/register_user", json={
        "user_name": "Test User",
        "user_email": "test@gmail.com",
        "user_password": "test123",
        "user_phoneno": 9999999999,
        "user_role": "user"
    })
    response = await client.post("/login", json={
        "email": "test@gmail.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_wrong_email(client):
    response = await client.post("/login", json={
        "email": "wrong@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 404
