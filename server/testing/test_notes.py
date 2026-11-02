def create_test_note(client, headers):
    return client.post(
        "/api/notes",
        headers=headers,
        json={
            "title": "Test Note",
            "content": "This is a test note.",
            "category": "Learning",
            "priority": "High"
        }
    )


def test_create_note(client, auth_headers):
    response = create_test_note(client, auth_headers)

    assert response.status_code == 201
    assert response.get_json()["note"]["title"] == "Test Note"


def test_create_note_requires_title(client, auth_headers):
    response = client.post(
        "/api/notes",
        headers=auth_headers,
        json={
            "content": "A note without a title."
        }
    )

    assert response.status_code == 400


def test_create_note_requires_authentication(client):
    response = client.post(
        "/api/notes",
        json={
            "title": "Unauthorized Note",
            "content": "This should not be saved."
        }
    )

    assert response.status_code == 401


def test_list_notes(client, auth_headers):
    create_test_note(client, auth_headers)

    response = client.get(
        "/api/notes",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.get_json()["notes"]) == 1


def test_get_single_note(client, auth_headers):
    created = create_test_note(client, auth_headers)
    note_id = created.get_json()["note"]["id"]

    response = client.get(
        f"/api/notes/{note_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.get_json()["note"]["id"] == note_id


def test_update_note(client, auth_headers):
    created = create_test_note(client, auth_headers)
    note_id = created.get_json()["note"]["id"]

    response = client.put(
        f"/api/notes/{note_id}",
        headers=auth_headers,
        json={
            "title": "Updated Note",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.get_json()["note"]["title"] == "Updated Note"
    assert response.get_json()["note"]["completed"] is True


def test_delete_note(client, auth_headers):
    created = create_test_note(client, auth_headers)
    note_id = created.get_json()["note"]["id"]

    response = client.delete(
        f"/api/notes/{note_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    missing = client.get(
        f"/api/notes/{note_id}",
        headers=auth_headers
    )

    assert missing.status_code == 404


def test_user_cannot_access_another_users_note(
    client,
    auth_headers,
    second_user_headers
):
    created = create_test_note(client, auth_headers)
    note_id = created.get_json()["note"]["id"]

    response = client.get(
        f"/api/notes/{note_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404


def test_notes_pagination(client, auth_headers):
    for number in range(3):
        client.post(
            "/api/notes",
            headers=auth_headers,
            json={
                "title": f"Note {number}",
                "content": f"Content {number}"
            }
        )

    response = client.get(
        "/api/notes?page=1&per_page=2",
        headers=auth_headers
    )

    data = response.get_json()

    assert response.status_code == 200
    assert len(data["notes"]) == 2
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["pages"] == 2
    assert data["pagination"]["has_next"] is True


def test_invalid_pagination(client, auth_headers):
    response = client.get(
        "/api/notes?page=0",
        headers=auth_headers
    )

    assert response.status_code == 400
