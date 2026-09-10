class BGP4RoutingEngine:
    """
    BGP-4 Path Vector Routing Engine maintaining Adj-RIB-In and Loc-RIB
    with loop prevention and standard path selection heuristics.
    """
    def __init__(self, local_as=65001):
        self.local_as = local_as
        self.rib_in = {}
        self.loc_rib = {}
        self.peers = set()

    def add_peer(self, peer_ip, peer_as):
        self.peers.add((peer_ip, peer_as))

    def receive_update(self, peer_ip, prefix, as_path, next_hop, local_pref=100, med=0):
        if self.local_as in as_path:
            return False, "AS_PATH_LOOP_DETECTED"

        route = {
            "prefix": prefix,
            "as_path": as_path,
            "next_hop": next_hop,
            "local_pref": local_pref,
            "med": med,
            "peer": peer_ip
        }
        if peer_ip not in self.rib_in:
            self.rib_in[peer_ip] = []
        self.rib_in[peer_ip].append(route)
        self._select_best_route(prefix)
        return True, "ROUTE_ACCEPTED"

    def _select_best_route(self, prefix):
        candidates = []
        for peer, routes in self.rib_in.items():
            for r in routes:
                if r["prefix"] == prefix:
                    candidates.append(r)
        if not candidates:
            return

        def bgp_key(r):
            return (-r["local_pref"], len(r["as_path"]), r["med"])

        candidates.sort(key=bgp_key)
        self.loc_rib[prefix] = candidates[0]
