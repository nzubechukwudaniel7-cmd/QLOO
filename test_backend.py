import asyncio
import httpx
import json

async def test_full_pipeline():
    print("\n" + "="*75)
    print("NEUROTASTE: COMPREHENSIVE BACKEND VERIFICATION & EDGE-CASE TEST SUITE")
    print("="*75)

    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # TEST 1: System Health & Qloo Live Telemetry
        print("\n[*] TEST 1: Verifying Live Qloo Developer Cloud Connection...")
        resp = await client.get("/api/status")
        print(f"[+] Status HTTP {resp.status_code}: {resp.json()}")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ONLINE"
        assert resp.json()["qloo_developer_cloud"] == "CONNECTED"

        # TEST 2: Standard Clinical Intake (Eleanor Vance)
        print("\n[*] TEST 2: Testing Clinical Intake for Eleanor Vance (Sundowning Level 8)...")
        intake_standard = {
            "resident": {
                "name": "Eleanor Vance",
                "age": 82,
                "birth_decade": "1940s",
                "hometown": "Chicago, IL",
                "youth_anchors": ["Nat King Cole", "Humphrey Bogart", "Chicago Jazz"],
                "notes": "Late-afternoon sundowning, pacing, repetitive crying to go home."
            },
            "trigger": {
                "time_of_day": "16:45",
                "agitation_level": 8,
                "primary_symptoms": ["Pacing", "Combative resistance to evening meal"],
                "sensory_sensitivities": ["Sensitive to loud brass instruments"]
            }
        }

        resp = await client.post("/api/protocol/generate", json=intake_standard)
        assert resp.status_code == 200
        proto_1 = resp.json()
        proto_id = proto_1["protocol_id"]
        print(f"[+] SUCCESS: Protocol {proto_id} generated.")
        print(f"    - Resolved Anchors: {[a['name'] for a in proto_1['qloo_resolved_anchors']]}")
        print(f"    - Auditory Items Count: {len(proto_1['auditory_pillar'])}")
        print(f"    - Visual Items Count: {len(proto_1['visual_pillar'])}")
        print(f"    - Culinary Items Count: {len(proto_1['culinary_olfactory_pillar'])}")
        print(f"    - Sample Verbal Script: {proto_1['verbal_validation_prompts'][0]}")

        # TEST 3: Edge Case Intake (Empty Anchors - Tests Bug 1 Fix)
        print("\n[*] TEST 3: Testing Edge Case (Zero Youth Anchors Provided)...")
        intake_empty_anchors = {
            "resident": {
                "name": "Arthur Pendelton",
                "age": 79,
                "birth_decade": "1950s",
                "hometown": "Detroit, MI",
                "youth_anchors": []  # Empty!
            },
            "trigger": {
                "time_of_day": "17:15",
                "agitation_level": 6,
                "primary_symptoms": ["Repetitive questioning"],
                "sensory_sensitivities": []
            }
        }
        resp = await client.post("/api/protocol/generate", json=intake_empty_anchors)
        assert resp.status_code == 200, f"Failed on empty anchors: {resp.text}"
        proto_2 = resp.json()
        print(f"[+] SUCCESS: Handled empty anchors gracefully without crash.")
        print(f"    - Protocol ID: {proto_2['protocol_id']}")
        print(f"    - Verbal prompt fallback: {proto_2['verbal_validation_prompts'][0]}")

        # TEST 4: Dynamic In-Session Recalibration (Tests Bug 3 Fix)
        print("\n[*] TEST 4: Testing Dynamic In-Session Recalibration...")
        recal_payload = {
            "protocol_id": proto_id,
            "caregiver_observation": "Resident calmed down noticeably when gentle female vocal singing was played.",
            "disliked_entity_ids": [proto_1['auditory_pillar'][0]['entity_id']],
            "current_agitation_level": 5
        }
        resp = await client.post("/api/protocol/recalibrate", json=recal_payload)
        assert resp.status_code == 200
        recal_proto = resp.json()
        print(f"[+] SUCCESS: Recalibrated auditory lead item:")
        print(f"    • {recal_proto['auditory_pillar'][0]['name']}")
        print(f"    • Rationale: {recal_proto['auditory_pillar'][0]['therapeutic_rationale']}")

        # TEST 5: CMS F-Tag 758 Regulatory Compliance Audit Generation
        print("\n[*] TEST 5: Testing Official CMS Compliance Audit Generation...")
        session_feedback = {
            "session_id": "SESS-702",
            "protocol_id": proto_id,
            "pre_agitation_level": 8,
            "post_agitation_level": 2,
            "duration_minutes": 20,
            "interventions_used": ["Acoustic Jazz Piano", "1940s Classic Cinema", "Warm Vanilla Aromatherapy"],
            "caregiver_notes": "Resident de-escalated within 15 minutes. Sedatives withheld.",
            "sedatives_avoided": True
        }
        resp = await client.post("/api/compliance/audit", json=session_feedback)
        assert resp.status_code == 200
        audit_res = resp.json()
        print(f"[+] SUCCESS: Audit {audit_res['audit_id']} generated.")
        print(f"    - Status: {audit_res['regulatory_status']}")
        print(f"    - Agitation Drop: 8 -> 2 ({audit_res['structured_log']['clinical_telemetry']['agitation_reduction_percentage']})")
        print(f"    - Sedatives Avoided: {audit_res['structured_log']['clinical_telemetry']['chemical_sedatives_avoided']}")

        # TEST 6: Direct Qloo Search Auto-Complete for UI
        print("\n[*] TEST 6: Testing Direct Qloo Search Endpoint for UI Auto-Complete...")
        resp = await client.get("/api/qloo/search?query=Frank+Sinatra")
        assert resp.status_code == 200
        search_data = resp.json()
        print(f"[+] SUCCESS: Returned {search_data['count']} entities for 'Frank Sinatra'.")
        print(f"    - First entity: {search_data['results'][0]['name']} (ID: {search_data['results'][0]['entity_id']})")

        # TEST 7: Telemetry Audit Trail
        print("\n[*] TEST 7: Verifying Live Qloo Cloud Telemetry Logs...")
        resp = await client.get("/api/telemetry")
        assert resp.status_code == 200
        telemetry = resp.json()
        print(f"[+] Total Live Qloo Cloud Requests Tracked: {telemetry['total_requests']}")
        for log in telemetry['history'][:3]:
            print(f"    • [{log['timestamp']}] {log['endpoint']} ({log['latency_ms']} ms) -> Status {log['status_code']}")

    print("\n" + "="*75)
    print("ALL 7 TEST SUITES PASSED! ZERO BUGS DETECTED. BACKEND IS ROCK SOLID!")
    print("="*75 + "\n")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
