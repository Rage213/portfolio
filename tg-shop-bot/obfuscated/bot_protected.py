# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGxvZ2dpbmcKaW1wb3J0IHN5cwpmcm9tIGFpb2dyYW0gaW1wb3J0IEJvdCwgRGlzcGF0Y2hlcgpmcm9tIGFpb2dyYW0uZnNtLnN0b3JhZ2UubWVtb3J5IGltcG9ydCBNZW1vcnlTdG9yYWdlCmZyb20gY29uZmlnIGltcG9ydCBCT1RfVE9LRU4KZnJvbSBoYW5kbGVycyBpbXBvcnQgcm91dGVyCmltcG9ydCBkYXRhYmFzZSBhcyBkYgoKYXN5bmMgZGVmIG1haW4oKToKICAgICMgU2V0dXAgbG9nZ2luZyB0byBzdGRvdXQKICAgIGxvZ2dpbmcuYmFzaWNDb25maWcoCiAgICAgICAgbGV2ZWw9bG9nZ2luZy5JTkZPLAogICAgICAgIGZvcm1hdD0iJShhc2N0aW1lKXMgLSAlKGxldmVsbmFtZSlzIC0gJShuYW1lKXMgLSAlKG1lc3NhZ2UpcyIsCiAgICAgICAgaGFuZGxlcnM9W2xvZ2dpbmcuU3RyZWFtSGFuZGxlcihzeXMuc3Rkb3V0KV0KICAgICkKCiAgICBpZiBub3QgQk9UX1RPS0VOOgogICAgICAgIGxvZ2dpbmcuY3JpdGljYWwoIkJPVF9UT0tFTiBpcyBlbXB0eSEgUGxlYXNlIGNvbmZpZ3VyZSBpdCBpbiAuZW52IGZpbGUuIikKICAgICAgICByZXR1cm4KCiAgICAjIEluaXRpYWxpemUgYm90IGFuZCBkaXNwYXRjaGVyCiAgICBib3QgPSBCb3QodG9rZW49Qk9UX1RPS0VOKQogICAgZHAgPSBEaXNwYXRjaGVyKHN0b3JhZ2U9TWVtb3J5U3RvcmFnZSgpKQogICAgCiAgICAjIFJlZ2lzdGVyIGhhbmRsZXJzIHJvdXRlcgogICAgZHAuaW5jbHVkZV9yb3V0ZXIocm91dGVyKQoKICAgICMgSW5pdGlhbGl6ZSBkYXRhYmFzZSBhbmQgcG9wdWxhdGUgZGVmYXVsdCBwcm9kdWN0cwogICAgbG9nZ2luZy5pbmZvKCJJbml0aWFsaXppbmcgU1FMaXRlIGRhdGFiYXNlLi4uIikKICAgIGF3YWl0IGRiLmluaXRfZGIoKQogICAgCiAgICAjIENsZWFyIGFueSBwZW5kaW5nIHVwZGF0ZXMgYW5kIHN0YXJ0IHBvbGxpbmcKICAgIGxvZ2dpbmcuaW5mbygiQ2xlYXJpbmcgdXBkYXRlcyBxdWV1ZSBhbmQgc3RhcnRpbmcgYm90IHBvbGxpbmcuLi4iKQogICAgYXdhaXQgYm90LmRlbGV0ZV93ZWJob29rKGRyb3BfcGVuZGluZ191cGRhdGVzPVRydWUpCiAgICBhd2FpdCBkcC5zdGFydF9wb2xsaW5nKGJvdCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICB0cnk6CiAgICAgICAgYXN5bmNpby5ydW4obWFpbigpKQogICAgZXhjZXB0IChLZXlib2FyZEludGVycnVwdCwgU3lzdGVtRXhpdCk6CiAgICAgICAgbG9nZ2luZy5pbmZvKCJCb3Qgc3RvcHBlZC4iKQo='

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
