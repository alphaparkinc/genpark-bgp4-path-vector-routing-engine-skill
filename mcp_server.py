import sys
import json
from client import BGP4RoutingEngine

def main():
    engine = BGP4RoutingEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "receive_update":
            ok, msg = engine.receive_update(
                params.get("peer_ip"),
                params.get("prefix"),
                params.get("as_path", []),
                params.get("next_hop"),
                params.get("local_pref", 100),
                params.get("med", 0)
            )
            res = {"status": ok, "message": msg}
        elif method == "get_loc_rib":
            res = {"loc_rib": engine.loc_rib}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
