import os
from dataclasses import dataclass


_evidence_hostport = os.getenv("EVIDENCE_API_HOSTPORT")
_default_evidence_api_url = (
    f"http://{_evidence_hostport}"
    if _evidence_hostport
    else "http://127.0.0.1:8000"
)


@dataclass(frozen=True)
class Settings:
    evidence_api_url: str = os.getenv("EVIDENCE_API_URL", _default_evidence_api_url)
    max_evidence_age_hours: float = float(os.getenv("MAX_EVIDENCE_AGE_HOURS", "24"))
    gps_max_distance_km: float = float(os.getenv("GPS_MAX_DISTANCE_KM", "500"))
    request_timeout_seconds: float = float(os.getenv("EVIDENCE_API_TIMEOUT_SECONDS", "10"))


settings = Settings()
