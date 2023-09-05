from pathlib import Path

resources = Path(__file__).parent / "resources"


def test_health(client):
    response = client.get("/")
    assert b"up" in response.data


def test_upload_csv(client):
    response = client.post("/harmonise", data={
        "file": (resources / "annotate_me.csv").open("rb"),
    })
    assert response.status_code == 200


def test_upload_json(client):
    response = client.post("/harmonise", json={
        "name": "",
        "dictionary": [{
            "name": "Gender",
            "description": "gender of the patient"
        }],
    })
    assert response.json[0]["annotation"] == "gender"
