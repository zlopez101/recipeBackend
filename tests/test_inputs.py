import pytest


def test_messaging(test_client):
    # from a non-user
    response = test_client.post(
        "/msg",
        data=dict(From="+11234567890", Body="sign me up"),
        follow_redirects=True,
    )
    assert (
        b"Hello! Looks like you are a new user, please use the link to sign up for our service. Thanks!"
        in response.data
    )

    # from a user but not sending a url
    # this will currently fail, need a way to add users to the mock database -> incoming with user registration project
    response = test_client.post(
        "/msg",
        data=dict(From="+17134306973", Body="sign me up", follow_redirects=True),
    )
    # assert b"What do you want?" in response.data

    # go straight there
    # from a user sending a url
    # response = test_client.post(
    #     "/msg",
    #     data=dict(
    #         From="+17134306973",
    #         Body="https://www.halfbakedharvest.com/queso-fundido-taquitos/",
    #         follow_redirects=True,
    #     ),
    # )
    # print(response.data)
    # assert b"was added to your recipes!" in response.data
