import logging

import teachers_gitlab.main as tg

def test_remove_member_that_doesnt_exist(mock_gitlab):
    entries = [
        {'login': 'alpha'},
    ]

    mock_gitlab.register_project(42, 'student/alpha', members =[
        {
            "id": 2157753,
            "username": "mario",
            "name": "xxx",
            "state": "active",
            "web_url": "https://gitlab.com/mario",
            "access_level": 50,
            "membership_state": "active"
        },
        {
            "id": 834534,
            "username": "sonic",
            "name": "xxx",
            "state": "active",
            "web_url": "https://gitlab.com/sonic",
            "access_level": 50,
            "membership_state": "active"
        }]
    )

    mock_gitlab.on_api_get(
        'projects/42/members/5',
        response_404=True
    )

    mock_gitlab.on_api_get(
        'users?username=alpha',
        response_json=[
            {
                'id': 5,
                'username': 'alpha',
            }
        ]
    )

    mock_gitlab.report_unknown()

    tg.action_remove_member(
        mock_gitlab.get_python_gitlab(),
        logging.getLogger("removemember"),
        tg.ActionEntries(entries),
        'login',
        False,
        'student/{login}',
    )

def test_remove_member(mock_gitlab):
    entries = [
        {'login': 'mario'},
    ]

    mock_gitlab.register_project(42, 'student/mario', members =[
        {
            "id": 2157753,
            "username": "mario",
            "name": "xxx",
            "state": "active",
            "web_url": "https://gitlab.com/mario",
            "access_level": 50,
            "membership_state": "active"
        },
        {
            "id": 834534,
            "username": "sonic",
            "name": "xxx",
            "state": "active",
            "web_url": "https://gitlab.com/sonic",
            "access_level": 50,
            "membership_state": "active"
        }]
    )

    mock_gitlab.on_api_get(
        'projects/42/members/2157753',
        response_json={
        }
    )

    mock_gitlab.on_api_get(
        'users?username=mario',
        response_json=[
            {
                'id': 2157753,
                'username': 'mario',
            }
        ]
    )

    mock_gitlab.on_api_delete(
       'projects/42/members'
    )

    mock_gitlab.report_unknown()

    tg.action_remove_member(
        mock_gitlab.get_python_gitlab(),
        logging.getLogger("removemember"),
        tg.ActionEntries(entries),
        'login',
        False,
        'student/{login}',
    )
