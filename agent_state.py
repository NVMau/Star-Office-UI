#!/usr/bin/env python3
"""
agent_state.py — Helper cho guest agents cap nhat trang thai tren Star Office UI.

Usage:
  python3 /root/Star-Office-UI/agent_state.py <join_key> <agent_name> <state> [detail]

States: idle | writing | researching | executing | syncing | error

Examples:
  python3 /root/Star-Office-UI/agent_state.py ocj_agent_coder "Coder" executing "Dang viet code"
  python3 /root/Star-Office-UI/agent_state.py ocj_agent_coder "Coder" idle "San sang"
"""

import json, os, sys, urllib.request, urllib.error

OFFICE_URL = os.environ.get("OFFICE_URL", "http://localhost:19000")
STATE_FILE_TPL = "/tmp/office_agent_{key}.json"

def load_agent_id(key):
    path = STATE_FILE_TPL.format(key=key.replace("/", "_"))
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("agentId")
    return None

def save_agent_id(key, agent_id):
    path = STATE_FILE_TPL.format(key=key.replace("/", "_"))
    with open(path, "w") as f:
        json.dump({"agentId": agent_id}, f)

def post(endpoint, data):
    req = urllib.request.Request(
        f"{OFFICE_URL}{endpoint}",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())

def main():
    if len(sys.argv) < 4:
        print("Usage: agent_state.py <join_key> <agent_name> <state> [detail]")
        sys.exit(1)

    join_key   = sys.argv[1]
    agent_name = sys.argv[2]
    state      = sys.argv[3]
    detail     = sys.argv[4] if len(sys.argv) > 4 else state

    agent_id = load_agent_id(join_key)

    # Join neu chua co agent_id
    if not agent_id:
        try:
            res = post("/join-agent", {"name": agent_name, "joinKey": join_key, "state": state, "detail": detail})
            if res.get("ok"):
                agent_id = res["agentId"]
                save_agent_id(join_key, agent_id)
            else:
                print(f"[office] join failed: {res}", file=sys.stderr)
                sys.exit(0)  # silent fail
        except Exception as e:
            print(f"[office] join error: {e}", file=sys.stderr)
            sys.exit(0)

    # Push state
    try:
        res = post("/agent-push", {"agentId": agent_id, "joinKey": join_key, "state": state, "detail": detail})
        if not res.get("ok"):
            # agentId expired — re-join lan sau
            os.remove(STATE_FILE_TPL.format(key=join_key.replace("/", "_")))
    except Exception as e:
        print(f"[office] push error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
