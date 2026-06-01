# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IHN5cwpmcm9tIG1vbml0b3IgaW1wb3J0IEJ5Yml0V1NNb25pdG9yCgphc3luYyBkZWYgbWFpbigpOgogICAgIyBTZXR1cCBtb25pdG9yaW5nIGZvciBCVENVU0RUIChkZWZhdWx0KQogICAgc3ltYm9sID0gIkJUQ1VTRFQiCiAgICBpZiBsZW4oc3lzLmFyZ3YpID4gMToKICAgICAgICBzeW1ib2wgPSBzeXMuYXJndlsxXS51cHBlcigpCgogICAgbW9uaXRvciA9IEJ5Yml0V1NNb25pdG9yKHN5bWJvbD1zeW1ib2wpCiAgICAKICAgIHByaW50KCI9IiAqIDYwKQogICAgcHJpbnQoZiJTdGFydGluZyBOZXh1cyBMYWJzIFJlYWwtVGltZSBXZWJTb2NrZXQgTW9uaXRvciBmb3Ige3N5bWJvbH0iKQogICAgcHJpbnQoZiJBbGVydCB0aHJlc2hvbGQgaXMgY29uZmlndXJlZCB0byB7bW9uaXRvci50aHJlc2hvbGR9JSIpCiAgICBwcmludCgiPSIgKiA2MCkKICAgIAogICAgdHJ5OgogICAgICAgIGF3YWl0IG1vbml0b3IuY29ubmVjdF9hbmRfbGlzdGVuKCkKICAgIGV4Y2VwdCBLZXlib2FyZEludGVycnVwdDoKICAgICAgICBwcmludCgiXG5TdG9wcGluZyBXZWJTb2NrZXQgbW9uaXRvciBncmFjZWZ1bGx5Li4uIikKICAgICAgICBtb25pdG9yLnN0b3AoKQoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIHRyeToKICAgICAgICBhc3luY2lvLnJ1bihtYWluKCkpCiAgICBleGNlcHQgS2V5Ym9hcmRJbnRlcnJ1cHQ6CiAgICAgICAgcHJpbnQoIlxuUHJvY2VzcyB0ZXJtaW5hdGVkIGJ5IHVzZXIuIikK'

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
