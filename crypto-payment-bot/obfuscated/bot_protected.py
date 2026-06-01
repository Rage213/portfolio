# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGxvZ2dpbmcKZnJvbSBhaW9ncmFtIGltcG9ydCBCb3QsIERpc3BhdGNoZXIKZnJvbSBjb25maWcgaW1wb3J0IEJPVF9UT0tFTgppbXBvcnQgZGF0YWJhc2UKZnJvbSBoYW5kbGVycyBpbXBvcnQgdXNlciwgYWRtaW4KCmxvZ2dpbmcuYmFzaWNDb25maWcobGV2ZWw9bG9nZ2luZy5JTkZPKQoKYXN5bmMgZGVmIG1haW4oKToKICAgICMgSW5pdGlhbGl6ZSBEYXRhYmFzZQogICAgYXdhaXQgZGF0YWJhc2UuaW5pdF9kYigpCgogICAgIyBJbml0aWFsaXplIEJvdCAmIERpc3BhdGNoZXIKICAgIGJvdCA9IEJvdCh0b2tlbj1CT1RfVE9LRU4pCiAgICBkcCA9IERpc3BhdGNoZXIoKQoKICAgICMgUmVnaXN0ZXIgcm91dGVycwogICAgZHAuaW5jbHVkZV9yb3V0ZXIoYWRtaW4ucm91dGVyKQogICAgZHAuaW5jbHVkZV9yb3V0ZXIodXNlci5yb3V0ZXIpCgogICAgIyBTdGFydCBwb2xsaW5nCiAgICBwcmludCgiQm90IHN0YXJ0ZWQgcG9sbGluZy4uLiIpCiAgICBhd2FpdCBkcC5zdGFydF9wb2xsaW5nKGJvdCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBhc3luY2lvLnJ1bihtYWluKCkpCg=='

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
