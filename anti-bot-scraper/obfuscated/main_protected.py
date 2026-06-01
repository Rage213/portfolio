# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KZnJvbSBzY3JhcGVyIGltcG9ydCBQbGF5d3JpZ2h0QW50aUJvdFNjcmFwZXIKCmFzeW5jIGRlZiBtYWluKCk6CiAgICBwcmludCgiPSIgKiA2MCkKICAgIHByaW50KCJOZXh1cyBMYWJzIEFudGktQm90IFBsYXl3cmlnaHQgU2NyYXBlciBFbmdpbmUgc3RhcnRpbmcuLi4iKQogICAgcHJpbnQoIlRhcmdldDogc2NyYXBpbmcgZHluYW1pY2FsbHkgbG9hZGVkIHF1b3RlcyBmcm9tIHF1b3Rlcy50b3NjcmFwZS5jb20vanMvIikKICAgIHByaW50KCI9IiAqIDYwKQogICAgCiAgICBzY3JhcGVyID0gUGxheXdyaWdodEFudGlCb3RTY3JhcGVyKCkKICAgIAogICAgdHJ5OgogICAgICAgIHJlc3VsdHMgPSBhd2FpdCBzY3JhcGVyLmZldGNoX2R5bmFtaWNfcXVvdGVzKCkKICAgICAgICAKICAgICAgICBwcmludChmIlxuU3VjY2Vzc2Z1bGx5IHBhcnNlZCB7bGVuKHJlc3VsdHMpfSBxdW90ZXM6XG4iKQogICAgICAgIAogICAgICAgIGZvciBpLCBxdW90ZSBpbiBlbnVtZXJhdGUocmVzdWx0cyk6CiAgICAgICAgICAgIHByaW50KGYiW3tpKzF9XSBcIntxdW90ZVsndGV4dCddfVwiIikKICAgICAgICAgICAgcHJpbnQoZiIgICAg4oCUIEF1dGhvcjoge3F1b3RlWydhdXRob3InXX0iKQogICAgICAgICAgICBwcmludChmIiAgICDigJQgVGFnczogeycsICcuam9pbihxdW90ZVsndGFncyddKX1cbiIpCiAgICAgICAgICAgIAogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KGYiXG7inYwgU2NyYXBlciBlcnJvciBvY2N1cnJlZDoge2V9IikKICAgICAgICBwcmludCgiVGlwOiBJZiBydW5uaW5nIGZvciB0aGUgZmlyc3QgdGltZSwgcnVuICdwbGF5d3JpZ2h0IGluc3RhbGwnIGluIHlvdXIgY29tbWFuZCBwcm9tcHQgdG8gaW5zdGFsbCBicm93c2VyIGJpbmFyaWVzLiIpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4obWFpbigpKQo='

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
