"""Integration and smoke tests for the backend/frontend shell."""

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from services.backend.app import Settings, create_app, load_settings


class BackendFrontendIntegrationTests(unittest.TestCase):
    def test_backend_health_and_version_are_reachable(self) -> None:
        app = create_app(Settings(version="1.2.3"))

        with TestClient(app) as client:
            health_response = client.get("/health")
            version_response = client.get("/version")

        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(health_response.json(), {"status": "ok"})
        self.assertEqual(version_response.status_code, 200)
        self.assertEqual(version_response.json(), {"version": "1.2.3"})

    def test_backend_allows_frontend_origin_for_cors(self) -> None:
        app = create_app(Settings(allowed_origins=("http://localhost:3000",)))

        with TestClient(app) as client:
            response = client.options(
                "/health",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("access-control-allow-origin"), "http://localhost:3000"
        )

    def test_settings_load_allowed_origins_from_environment(self) -> None:
        with patch.dict(
            os.environ,
            {"GARUDA_ALLOWED_ORIGINS": "http://localhost:3000,https://app.example"},
            clear=False,
        ):
            settings = load_settings()

        self.assertEqual(settings.allowed_origins, ("http://localhost:3000", "https://app.example"))


if __name__ == "__main__":
    unittest.main()
