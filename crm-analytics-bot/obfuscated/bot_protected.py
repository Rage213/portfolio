# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KZnJvbSBhaW9ncmFtIGltcG9ydCBCb3QsIERpc3BhdGNoZXIKZnJvbSBhaW9ncmFtLmZzbS5zdG9yYWdlLm1lbW9yeSBpbXBvcnQgTWVtb3J5U3RvcmFnZQoKaW1wb3J0IGNvbmZpZwppbXBvcnQgZGF0YWJhc2UKaW1wb3J0IGhhbmRsZXJzCgphc3luYyBkZWYgbWFpbigpOgogICAgIyAxLiBJbml0aWFsaXplIFNRTGl0ZSBEYXRhYmFzZQogICAgYXdhaXQgZGF0YWJhc2UuaW5pdF9kYigpCiAgICAKICAgICMgMi4gU2V0dXAgQm90ICYgRGlzcGF0Y2hlcgogICAgYm90ID0gQm90KHRva2VuPWNvbmZpZy5CT1RfVE9LRU4pCiAgICBkcCA9IERpc3BhdGNoZXIoc3RvcmFnZT1NZW1vcnlTdG9yYWdlKCkpCiAgICAKICAgICMgMy4gSW5jbHVkZSBSb3V0ZXJzCiAgICBkcC5pbmNsdWRlX3JvdXRlcihoYW5kbGVycy5yb3V0ZXIpCiAgICAKICAgIHByaW50KCI9IiAqIDYwKQogICAgcHJpbnQoIlN0YXJ0aW5nIE5leHVzIExhYnMgQ1JNICYgQW5hbHl0aWNzIEJvdC4uLiIpCiAgICBwcmludChmIkNvbmZpZ3VyZWQgQWRtaW4gSUQ6IHtjb25maWcuQURNSU5fSUR9IikKICAgIHByaW50KCI9IiAqIDYwKQogICAgCiAgICB0cnk6CiAgICAgICAgYXdhaXQgZHAuc3RhcnRfcG9sbGluZyhib3QpCiAgICBmaW5hbGx5OgogICAgICAgIGF3YWl0IGJvdC5zZXNzaW9uLmNsb3NlKCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICB0cnk6CiAgICAgICAgYXN5bmNpby5ydW4obWFpbigpKQogICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgIHByaW50KCJcbkJvdCBzdG9wcGVkIGJ5IHVzZXIuIikK'

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
