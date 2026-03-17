def test_import_text(client) -> None:
    response = client.post("/api/v1/imports/text", json={"content": "openai.com\ninvalid"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["valid_rows"] == 1
    assert payload["data"]["invalid_rows"] == 1


def test_import_csv_file(client) -> None:
    response = client.post(
        "/api/v1/imports/file",
        files={"file": ("domains.csv", b"domain\nopenai.com\ninvalid\n", "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["data"]["source_type"] == "csv"


def test_import_file_rejects_unsupported_extension(client) -> None:
    response = client.post(
        "/api/v1/imports/file",
        files={"file": ("domains.json", b"[]", "application/json")},
    )

    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "value_error"
