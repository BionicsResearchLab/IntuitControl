from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path
from typing import Any


CORTEX_API_DIR = Path(__file__).resolve().parents[1] / "cortex-api"
if str(CORTEX_API_DIR) not in sys.path:
    sys.path.insert(0, str(CORTEX_API_DIR))

from cortex import Cortex  # noqa: E402


class CortexSession:
    """Own one Cortex websocket connection and expose safe API snapshots."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._client: Cortex | None = None
        self._thread: threading.Thread | None = None
        self._status = "idle"
        self._error: str | None = None
        self._headset_id: str | None = None
        self._session_id: str | None = None
        self._streams: list[str] = []
        self._latest_eeg: dict[str, Any] | None = None
        self._eeg_history: list[list[float]] = [[] for _ in range(5)]
        self._last_data_at: float | None = None
        self._device: dict[str, Any] = {"batteryPercent": None, "signal": None, "name": None}

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "status": self._status,
                "error": self._error,
                "headsetId": self._headset_id,
                "sessionId": self._session_id,
                "streams": list(self._streams),
                "device": dict(self._device),
                "latestEeg": self._latest_eeg,
                "eegHistory": self._eeg_history,
                "lastDataAt": self._last_data_at,
                "hasSignal": self._has_signal(self._device["signal"]),
            }

    def start(self, headset_id: str | None = None, streams: list[str] | None = None) -> dict[str, Any]:
        with self._lock:
            if self._status in {"starting", "connected"}:
                return self.snapshot()

            client_id = os.getenv("EMOTIV_CLIENT_ID", "")
            client_secret = os.getenv("EMOTIV_CLIENT_SECRET", "")
            if not client_id or not client_secret:
                raise RuntimeError("EMOTIV_CLIENT_ID and EMOTIV_CLIENT_SECRET must be configured")

            requested_streams = streams or ["eeg", "dev"]
            invalid_streams = set(requested_streams) - {"eeg", "dev", "mot", "met", "pow"}
            if invalid_streams:
                raise ValueError(f"Unsupported streams: {', '.join(sorted(invalid_streams))}")

            self._status = "starting"
            self._error = None
            self._streams = requested_streams
            self._headset_id = headset_id or None
            self._latest_eeg = None
            self._eeg_history = [[] for _ in range(5)]
            self._last_data_at = None
            self._client = Cortex(client_id, client_secret, debug_mode=False, headset_id=headset_id or "")
            self._client.bind(create_session_done=self._on_session_created)
            self._client.bind(new_eeg_data=self._on_eeg)
            self._client.bind(new_dev_data=self._on_device)
            self._client.bind(inform_error=self._on_error)
            self._thread = threading.Thread(target=self._run_client, name="cortex-session", daemon=True)
            self._thread.start()
            return self.snapshot()

    def stop(self) -> dict[str, Any]:
        with self._lock:
            client = self._client
            self._status = "stopped"
            self._session_id = None
            self._client = None

        if client is not None:
            try:
                if getattr(client, "session_id", ""):
                    client.close_session()
            except Exception as error:  # noqa: BLE001
                self._set_error(str(error))
            finally:
                try:
                    client.close()
                except Exception:
                    pass
        return self.snapshot()

    def _run_client(self) -> None:
        try:
            self._client.open()  # type: ignore[union-attr]
        except Exception as error:  # noqa: BLE001
            self._set_error(str(error))

    def _on_session_created(self, *args: Any, **kwargs: Any) -> None:
        session_id = kwargs.get("data")
        with self._lock:
            self._session_id = session_id
            self._status = "connected"
            client = self._client
            streams = list(self._streams)
        if client is not None:
            client.sub_request(streams)

    def _on_eeg(self, *args: Any, **kwargs: Any) -> None:
        eeg_data = kwargs.get("data") or {}
        samples = eeg_data.get("eeg") or []
        with self._lock:
            self._latest_eeg = eeg_data
            self._last_data_at = time.time()
            for channel_index, sample in enumerate(samples[:len(self._eeg_history)]):
                try:
                    history = self._eeg_history[channel_index]
                    history.append(float(sample))
                    del history[:-128]
                except (TypeError, ValueError):
                    continue

    def _on_device(self, *args: Any, **kwargs: Any) -> None:
        device_data = kwargs.get("data") or {}
        with self._lock:
            self._device.update({
                "batteryPercent": device_data.get("batteryPercent"),
                "signal": device_data.get("signal"),
                "name": device_data.get("dev"),
            })
            self._last_data_at = time.time()

    @staticmethod
    def _has_signal(signal: Any) -> bool:
        if signal is None:
            return False
        if isinstance(signal, (list, tuple)):
            return any(CortexSession._has_signal(value) for value in signal)
        if isinstance(signal, str):
            return signal not in {"", "0", "none", "None"}
        if isinstance(signal, (int, float)):
            return signal > 0
        return bool(signal)

    def _on_error(self, *args: Any, **kwargs: Any) -> None:
        error_data = kwargs.get("error_data") or {}
        self._set_error(error_data.get("message", str(error_data)))

    def _set_error(self, message: str) -> None:
        with self._lock:
            self._status = "error"
            self._error = message
