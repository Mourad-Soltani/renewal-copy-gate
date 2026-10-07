# Mourad.Soltani
import json
import unittest
from urllib.request import Request, urlopen

from renewal_copy_gate.audit import audit_copy
from renewal_copy_gate.server import Handler
from http.server import ThreadingHTTPServer
import threading


GOOD = (
    "Pro plan is $29 USD per month. This subscription auto-renews monthly. "
    "Cancel anytime in your account settings. Annual plan is $290 USD per year "
    "and requires 14 days notice before renewal. The 14-day free trial converts "
    "to the paid plan unless you cancel before the trial ends."
)


class AuditTests(unittest.TestCase):
    def test_good_copy_passes(self) -> None:
        report = audit_copy(GOOD)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["error_count"], 0)
        self.assertGreaterEqual(report["score"], 90)
        self.assertEqual(report["author"], "Mourad.Soltani")

    def test_missing_price_and_renewal(self) -> None:
        report = audit_copy("Subscribe to the Pro plan. Billed on a recurring basis.")
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual(report["status"], "fail")
        self.assertIn("R001", codes)
        self.assertIn("R004", codes)
        self.assertIn("R005", codes)

    def test_trial_without_conversion(self) -> None:
        report = audit_copy(
            "Start your 14-day free trial of the $19 USD per month subscription. "
            "It auto-renews. Cancel anytime in account settings."
        )
        codes = {item["code"] for item in report["findings"]}
        self.assertIn("R007", codes)

    def test_short_input(self) -> None:
        report = audit_copy("hi")
        self.assertEqual(report["findings"][0]["code"], "R000")


class HealthTests(unittest.TestCase):
    def test_health_and_audit_endpoints(self) -> None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]
        try:
            with urlopen(f"http://127.0.0.1:{port}/health") as response:
                payload = json.loads(response.read().decode())
            self.assertEqual(response.status, 200)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["author"], "Mourad.Soltani")
            body = json.dumps({"text": GOOD}).encode()
            request = Request(
                f"http://127.0.0.1:{port}/audit",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urlopen(request) as response:
                audited = json.loads(response.read().decode())
            self.assertEqual(audited["status"], "pass")
        finally:
            server.shutdown()


if __name__ == "__main__":
    unittest.main()
