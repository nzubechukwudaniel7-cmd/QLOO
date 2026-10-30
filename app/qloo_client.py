import time
import urllib.parse
from typing import List, Dict, Any, Optional
import httpx
from app.config import settings

class QlooClientError(Exception):
    """Base error for Qloo Developer Cloud operations."""
    pass

class QlooAuthenticationError(QlooClientError):
    """Raised when API key is missing or invalid."""
    pass

class QlooClient:
    def __init__(self):
        self.api_key = settings.qloo_api_key
        self.base_url = settings.qloo_base_url.rstrip("/")
        self.telemetry_history: List[Dict[str, Any]] = []
        self._cache: Dict[str, Any] = {}

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key or self.api_key == "your_api_key_here":
            raise QlooAuthenticationError(
                "Qloo Developer Cloud API Key is missing or unconfigured. "
                "The NeuroTaste engine strictly requires active Qloo Developer Cloud authentication."
            )
        return {
            "X-Api-Key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "NeuroTaste-Caregiver-Agent/1.0"
        }

    def _record_telemetry(self, endpoint: str, params: Dict[str, Any], status: int, latency_ms: float, count: int):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "endpoint": endpoint,
            "params": params,
            "status_code": status,
            "latency_ms": round(latency_ms, 2),
            "results_count": count
        }
        self.telemetry_history.append(log_entry)
        # Keep last 50 logs
        if len(self.telemetry_history) > 50:
            self.telemetry_history.pop(0)

    async def search_entity(self, query: str, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for entities in Qloo's Taste Graph (Artists, Movies, Books, Places, Brands).
        """
        cache_key = f"search:{query}:{entity_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        start_time = time.time()
        params = {"query": query}
        if entity_type:
            params["type"] = entity_type

        encoded_params = urllib.parse.urlencode(params)
        url = f"{self.base_url}/search?{encoded_params}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                resp = await client.get(url, headers=self._get_headers())
                latency = (time.time() - start_time) * 1000

                if resp.status_code == 401 or resp.status_code == 403:
                    raise QlooAuthenticationError("Qloo API key unauthorized or expired.")

                resp.raise_for_status()
                data = resp.json()
                raw_results = data.get("results")
                if isinstance(raw_results, list):
                    results = raw_results
                elif isinstance(raw_results, dict):
                    results = raw_results.get("entities", [])
                else:
                    results = []

                self._record_telemetry("/search", params, resp.status_code, latency, len(results))
                self._cache[cache_key] = results
                return results

            except httpx.HTTPStatusError as e:
                latency = (time.time() - start_time) * 1000
                self._record_telemetry("/search", params, e.response.status_code, latency, 0)
                raise QlooClientError(f"Qloo Cloud HTTP error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                latency = (time.time() - start_time) * 1000
                self._record_telemetry("/search", params, 500, latency, 0)
                raise QlooClientError(f"Qloo Cloud connection failure: {str(e)}")

    async def get_cross_domain_insights(
        self,
        seed_entity_ids: List[str],
        target_type: str,
        take: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Query Qloo's /v2/insights for cross-domain affinities based on seed entity signals.
        target_type: 'urn:entity:artist', 'urn:entity:movie', 'urn:entity:book', etc.
        """
        if not seed_entity_ids:
            return []

        cache_key = f"insights:{target_type}:{','.join(sorted(seed_entity_ids))}:{take}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        start_time = time.time()
        
        # Build query string with multiple signal.interests.entities params
        query_parts = [
            f"filter.type={urllib.parse.quote(target_type)}",
            f"take={take}"
        ]
        for eid in seed_entity_ids:
            query_parts.append(f"signal.interests.entities={urllib.parse.quote(eid)}")

        url = f"{self.base_url}/v2/insights?{'&'.join(query_parts)}"
        telemetry_params = {"filter.type": target_type, "signals": seed_entity_ids, "take": take}

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                resp = await client.get(url, headers=self._get_headers())
                latency = (time.time() - start_time) * 1000

                if resp.status_code == 401 or resp.status_code == 403:
                    raise QlooAuthenticationError("Qloo API key unauthorized or expired.")

                resp.raise_for_status()
                data = resp.json()
                raw_results = data.get("results")
                if isinstance(raw_results, dict):
                    entities = raw_results.get("entities", [])
                elif isinstance(raw_results, list):
                    entities = raw_results
                else:
                    entities = []

                self._record_telemetry("/v2/insights", telemetry_params, resp.status_code, latency, len(entities))
                self._cache[cache_key] = entities
                return entities

            except httpx.HTTPStatusError as e:
                latency = (time.time() - start_time) * 1000
                self._record_telemetry("/v2/insights", telemetry_params, e.response.status_code, latency, 0)
                raise QlooClientError(f"Qloo Cloud Insights HTTP {e.response.status_code}: {e.response.text}")
            except Exception as e:
                latency = (time.time() - start_time) * 1000
                self._record_telemetry("/v2/insights", telemetry_params, 500, latency, 0)
                raise QlooClientError(f"Qloo Cloud Insights connection failure: {str(e)}")

# Singleton instance
qloo_client = QlooClient()
