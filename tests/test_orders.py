import pytest
@pytest.mark.asyncio

async def test_order_creation(client):

#1st register karke token bhi lena hoga kyoki ye prtected route hai 
  await client.post("/register_user",json={
        "user_name":"Test User",
        "user_email": "test1@gmail.com",
        "user_password": "test123",
        "user_phoneno": 9999999999,
        "user_role": "user"

  })

  #login usi test user say 
  login_response=await client.post("/login",json={
      "email": "test1@gmail.com",
      "password": "test123"
  })

  token=login_response.json()["token"]

  # 3. create order with token
  response = await client.post("/create_order",json={
    "name_of_product":"Test Product",
    "quantity":1,
    "status":"pending"
      },
      headers={"Authorization":f"Bearer {token}"}
  
  )

  assert response.status_code == 200
  data = response.json()
  assert data["message"] == "order created successfully"
  assert "order_id" in data





@pytest.mark.asyncio
async def test_admin_can_delete_any_user(client):

    # admin
    await client.post("/register_user", json={
        "user_name": "Admin",
        "user_email": "admin@gmail.com",
        "user_password": "1234",
        "user_phoneno": 9999999999,
        "user_role": "admin"
    })

    # normal user
    await client.post("/register_user", json={
        "user_name": "User2",
        "user_email": "user2@gmail.com",
        "user_password": "1234",
        "user_phoneno": 9999999999,
        "user_role": "user"
    })

    # login as admin
    res = await client.post("/login", json={
        "email": "admin@gmail.com",
        "password": "1234"
    })
    token = res.json()["token"]

    # delete user2 ✔
    response = await client.delete(
        "/delete_user/user2@gmail.com",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
