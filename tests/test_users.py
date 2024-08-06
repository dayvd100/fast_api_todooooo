from http import HTTPStatus

from schemas.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testemeuuser',
            'email': 'teste@teste.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'testemeuuser',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'wukongzada',
            'email': 'wukongzada@example.com',
            'password': 'wukongzada123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'wukongzada',
        'email': 'wukongzada@example.com',
        'id': 1,
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'dayvd',
            'email': 'dayvd@example.com',
            'password': 'dayvd123',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}