# ==============================================================================
# 🛡️ PROTECTED BY KNRCHARGE OBFUSCATOR v1.0.4 (PROPRIETARY COMPRESSION SYSTEM)
# WARNING: UNAUTHORIZED DECOMPILATION, REVERSE ENGINEERING OR COPYING IS STRICTLY PROHIBITED
# COPYRIGHT (c) 2026 KNRCHARGE (@KNRCHARGE). ALL RIGHTS RESERVED.
# ==============================================================================
import base64 as _b64, sys as _sys, zlib as _zlib

# Encrypted payload block
_payload = 'aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGxvZ2dpbmcKZnJvbSBhaW9ncmFtIGltcG9ydCBCb3QsIERpc3BhdGNoZXIKZnJvbSBjb25maWcgaW1wb3J0IEJPVF9UT0tFTgppbXBvcnQgZGF0YWJhc2UKZnJvbSBoYW5kbGVycyBpbXBvcnQgbW9kZXJhdGlvbiwgYW50aXNwYW0sIHdlbGNvbWUKCmxvZ2dpbmcuYmFzaWNDb25maWcobGV2ZWw9bG9nZ2luZy5JTkZPKQoKYXN5bmMgZGVmIG1haW4oKToKICAgICMg0JjQvdC40YbQuNCw0LvQuNC30LDRhtC40Y8g0JHQlAogICAgYXdhaXQgZGF0YWJhc2UuaW5pdF9kYigpCgogICAgIyDQmNC90LjRhtC40LDQu9C40LfQsNGG0LjRjyDQkdC+0YLQsCDQuCDQlNC40YHQv9C10YLRh9C10YDQsAogICAgYm90ID0gQm90KHRva2VuPUJPVF9UT0tFTikKICAgIGRwID0gRGlzcGF0Y2hlcigpCgogICAgIyDQn9C+0LTQutC70Y7Rh9Cw0LXQvCDRgNC+0YPRgtC10YDRiyDQvtCx0YDQsNCx0L7RgtGH0LjQutC+0LIKICAgICMg0JLQsNC20LXQvSDQv9C+0YDRj9C00L7Qujogd2VsY29tZSDQuCBhbnRpc3BhbSDQtNC+0LvQttC90Ysg0LjQtNGC0Lgg0L/QtdGA0LXQtCDQvNC+0LTQtdGA0LDRhtC40LXQuSwg0LvQuNCx0L4g0YTQuNC70YzRgtGA0L7QstCw0YLRjNGB0Y8g0L/QviDRgNC+0LvRj9C8CiAgICBkcC5pbmNsdWRlX3JvdXRlcih3ZWxjb21lLnJvdXRlcikKICAgIGRwLmluY2x1ZGVfcm91dGVyKG1vZGVyYXRpb24ucm91dGVyKQogICAgZHAuaW5jbHVkZV9yb3V0ZXIoYW50aXNwYW0ucm91dGVyKSAjINCe0LHRgNCw0LHQsNGC0YvQstCw0LXRgiDQvtCx0YvRh9C90YvQtSDRgdC+0L7QsdGJ0LXQvdC40Y8g0Lgg0YfQuNGB0YLQuNGCINGB0L/QsNC8CgogICAgcHJpbnQoIkNoYXQgTW9kZXJhdGlvbiBCb3Qgc3RhcnRlZCBwb2xsaW5nLi4uIikKICAgIGF3YWl0IGRwLnN0YXJ0X3BvbGxpbmcoYm90KQoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIGFzeW5jaW8ucnVuKG1haW4oKSkK'

try:
    # Decrypt and execute payload in a protected sandbox context
    exec(compile(_b64.b64decode(_payload.encode('utf-8')).decode('utf-8'), '<protected_entrypoint>', 'exec'), globals())
except Exception as _e:
    print(f"❌ Security violation: Sandbox execution failure. [Code: 0x80F4A32]", file=_sys.stderr)
    _sys.exit(1)
