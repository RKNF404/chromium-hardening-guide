# Chromium Hardening Guide

### CURRENTLY RESTRUCTURING

Last updated for: `144`

Changes in latest version:
```
removed Enable feature ContentSettingsPartitioning
added policy SearchContentSharingSettings
updated:
  -LocalNetworkAccessChecks:LocalNetworkAccessChecksWarn/false,LocalNetworkAccessChecksWebRTC
  +LocalNetworkAccessChecksWebRTC,LocalNetworkAccessChecksWebSockets,LocalNetworkAccessChecksWebTransport
added Enable feature PrintCompositorLPAC
added Enable feature WinSboxStrictHandleChecks
removed policy TLS13EarlyDataEnabled
removed policy UserAgentReduction
```

Hardening guide for (theoretically) any Chromium browser.

Some of the flips and toggles come from other projects such as [Vanadium](https://github.com/GrapheneOS/Vanadium) or [Trivalent](https://github.com/secureblue/Trivalent).

If you're having any trouble applying the guide or have any general questions or inquiries, please feel free to open a [discussion thread](https://github.com/RKNF404/chromium-hardening-guide/discussions).
If want to suggest something, please open an [issue](https://github.com/RKNF404/chromium-hardening-guide/issues) for it.
If you have my Discord, feel free to message me there about this guide.

# [Setup Guide](pages/SETUP_GUIDE.md)

