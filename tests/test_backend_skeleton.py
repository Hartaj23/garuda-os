"""Tests for the initial FastAPI backend skeleton."""

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from services.backend.app import create_app, load_settings


class BackendSkeletonTests(unittest.TestCase):
    def test_app_starts_and_stops_cleanly(self) -> None:
        app = create_app()

        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_reports_ok(self) -> None:
        app = create_app()

        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_version_endpoint_reports_version(self) -> None:
        app = create_app()

        with TestClient(app) as client:
            response = client.get("/version")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["version"], "0.1.0a0")

    def test_configuration_loads_from_environment(self) -> None:
        with patch.dict(
            os.environ,
            {
                "GARUDA_APP_NAME": "garuda-test",
                "GARUDA_ENVIRONMENT": "test",
                "GARUDA_LOG_LEVEL": "DEBUG",
                "GARUDA_VERSION": "9.9.9",
            },
            clear=False,
        ):
            settings = load_settings()

        self.assertEqual(settings.app_name, "garuda-test")
        self.assertEqual(settings.environment, "test")
        self.assertEqual(settings.log_level, "DEBUG")
        self.assertEqual(settings.version, "9.9.9")


if __name__ == "__main__":
    unittest.main()
