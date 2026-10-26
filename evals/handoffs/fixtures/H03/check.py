"""Emit frozen local observations; never executes a payment."""
import json

print(json.dumps({"revision":"r8","environment":"local","normal":{"passed":True,"charges":1},"timeout_retry":{"passed":False,"idempotency_key":"order-17","charges":["c101","c102"],"trace":"queue-delivery-2"}}))
raise SystemExit(1)
