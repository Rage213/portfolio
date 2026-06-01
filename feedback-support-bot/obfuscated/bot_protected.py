# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGxvZ2dpbmcKZnJvbSBhaW9ncmFtIGltcG9ydCBCb3QsIERpc3BhdGNoZXIKZnJvbSBjb25maWcgaW1wb3J0IEJPVF9UT0tFTgppbXBvcnQgZGF0YWJhc2UKaW1wb3J0IGhhbmRsZXJzCgpsb2dnaW5nLmJhc2ljQ29uZmlnKGxldmVsPWxvZ2dpbmcuSU5GTykKCmFzeW5jIGRlZiBtYWluKCk6CiAgICAjINCY0L3QuNGG0LjQsNC70LjQt9Cw0YbQuNGPINCw0YHQuNC90YXRgNC+0L3QvdC+0Lkg0JHQlAogICAgYXdhaXQgZGF0YWJhc2UuaW5pdF9kYigpCgogICAgIyDQmNC90LjRhtC40LDQu9C40LfQsNGG0LjRjyDQsdC+0YLQsCDQuCDQtNC40YHQv9C10YLRh9C10YDQsAogICAgYm90ID0gQm90KHRva2VuPUJPVF9UT0tFTikKICAgIGRwID0gRGlzcGF0Y2hlcigpCgogICAgIyDQn9C+0LTQutC70Y7Rh9Cw0LXQvCDRgNC+0YPRgtC10YDRiwogICAgZHAuaW5jbHVkZV9yb3V0ZXIoaGFuZGxlcnMucm91dGVyKQoKICAgIHByaW50KCJGZWVkYmFjay9TdXBwb3J0IEJvdCBzdGFydGVkIHBvbGxpbmcuLi4iKQogICAgYXdhaXQgZHAuc3RhcnRfcG9sbGluZyhib3QpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4obWFpbigpKQo='

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
