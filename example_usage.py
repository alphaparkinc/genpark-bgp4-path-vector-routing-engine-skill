from client import BGP4RoutingEngine

def main():
    print("=== Testing BGP-4 Path Vector Routing Engine ===")
    bgp = BGP4RoutingEngine(local_as=65001)
    bgp.add_peer("192.0.2.1", 65002)
    bgp.add_peer("192.0.2.2", 65003)

    ok1, _ = bgp.receive_update("192.0.2.1", "10.0.0.0/24", [65002, 65010], "192.0.2.1", local_pref=100)
    ok2, _ = bgp.receive_update("192.0.2.2", "10.0.0.0/24", [65003], "192.0.2.2", local_pref=100)
    assert ok1 and ok2

    best = bgp.loc_rib["10.0.0.0/24"]
    print("Best route selected:", best)
    assert len(best["as_path"]) == 1
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
