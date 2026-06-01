# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGxvZ2dpbmcKZnJvbSBhaW9ncmFtIGltcG9ydCBCb3QsIERpc3BhdGNoZXIKZnJvbSBjb25maWcgaW1wb3J0IEJPVF9UT0tFTgppbXBvcnQgZGF0YWJhc2UKaW1wb3J0IGhhbmRsZXJzCmZyb20gc2NoZWR1bGVyIGltcG9ydCBzY2hlZHVsZXIsIGxvYWRfc2NoZWR1bGVkX2pvYnMKCmxvZ2dpbmcuYmFzaWNDb25maWcobGV2ZWw9bG9nZ2luZy5JTkZPKQoKYXN5bmMgZGVmIG1haW4oKToKICAgICMg0JjQvdC40YbQuNCw0LvQuNC30LDRhtC40Y8g0JHQlAogICAgYXdhaXQgZGF0YWJhc2UuaW5pdF9kYigpCgogICAgIyDQmNC90LjRhtC40LDQu9C40LfQsNGG0LjRjyDQkdC+0YLQsCDQuCDQlNC40YHQv9C10YLRh9C10YDQsAogICAgYm90ID0gQm90KHRva2VuPUJPVF9UT0tFTikKICAgIGRwID0gRGlzcGF0Y2hlcigpCgogICAgIyDQn9C+0LTQutC70Y7Rh9Cw0LXQvCDRgNC+0YPRgtC10YDRiwogICAgZHAuaW5jbHVkZV9yb3V0ZXIoaGFuZGxlcnMucm91dGVyKQoKICAgICMg0JfQsNC/0YPRgdC60LDQtdC8INC/0LvQsNC90LjRgNC+0LLRidC40LogQVBTY2hlZHVsZXIKICAgIHNjaGVkdWxlci5zdGFydCgpCiAgICAKICAgICMg0JfQsNCz0YDRg9C20LDQtdC8INGB0L7RhdGA0LDQvdC10L3QvdGL0LUg0LfQsNC00LDRh9C4INCyINC/0LvQsNC90LjRgNC+0LLRidC40LoKICAgIGF3YWl0IGxvYWRfc2NoZWR1bGVkX2pvYnMoYm90KQoKICAgIHByaW50KCJBdXRvLVBvc3RpbmcgQm90IHN0YXJ0ZWQgcG9sbGluZy4uLiIpCiAgICB0cnk6CiAgICAgICAgYXdhaXQgZHAuc3RhcnRfcG9sbGluZyhib3QpCiAgICBmaW5hbGx5OgogICAgICAgIHNjaGVkdWxlci5zaHV0ZG93bigpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4obWFpbigpKQo='

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
