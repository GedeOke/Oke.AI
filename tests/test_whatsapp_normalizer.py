from app.channels.whatsapp.whatsapp_normalizer import normalize


def test_normalize_text_message():
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "id": "wamid.test",
                                    "from": "628123456789",
                                    "timestamp": "1700000000",
                                    "type": "text",
                                    "text": {"body": "Hello"},
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    result = normalize(payload, "org-1")
    assert result["content"] == "Hello"
    assert result["external_id"] == "628123456789"
    assert result["organization_id"] == "org-1"
