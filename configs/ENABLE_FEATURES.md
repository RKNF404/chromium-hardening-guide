# Features (Enable)
(`--enable-features=`)

##### `CapReferrerToOriginOnCrossOrigin`
***(privacy)***\
Limits the referrer to only send the origin of the URL\
E.g. just "google.com" instead of "google.com/search"

##### `ClearCrossSiteCrossBrowsingContextGroupWindowName`
***(privacy DISFUNCTIONAL)***\
Prevents the window.name property from being leaked across sites

##### `EnableCsrssLockdown`
***(security WINDOWS_ONLY)***\
Prevents renderer processes from having access to the CSRSS service

##### `HstsTopLevelNavigationsOnly`
***(privacy)***\
Prevents third-party tracking using HSTS

##### `LocalNetworkAccessChecksWebRTC,LocalNetworkAccessChecksWebSockets,LocalNetworkAccessChecksWebTransport`
***(security privacy)***\
Prevents sites from being able to access localhost addresses

##### `MacSyscallSandbox`
***(security MACOS_ONLY NOT_TESTED)***\
Enables syscall filtering for the sandbox on MacOS

##### `NetworkServiceCodeIntegrity`
***(security WINDOWS_ONLY)***\
Enable Code Integrity Guard (CIG) in the Network Service process pre-launch

##### `PartitionAllocWithAdvancedChecks:enabled-processes/all-processes`
***(security)***\
Enable stricter memory security checks

##### `PartitionConnectionsByNetworkIsolationKey`
***(privacy)***\
Isolates connection information to prevent cross-site tracking

##### `PrintCompositorLPAC`
***(security WINDOWS_ONLY)***\
Enables various mitigations and restrictions for the printing process

##### `ReduceAcceptLanguage`
***(privacy)***\
Reduces data transmitted by the Accept-Language header

##### `RendererAppContainer`
***(security WINDOWS_ONLY)***\
Enables the use of AppContainers on renderers to improve the sandboxing

##### `ScopeMemoryCachePerContext`
***(privacy DISFUNCTIONAL)***\
Limits memory cache access to the context it was created from

##### `SplitCodeCacheByNetworkIsolationKey,SplitCacheByNetworkIsolationKey,SplitCacheByIncludeCredentials,SplitCacheByNavigationInitiator`
***(privacy)***\
Isolates cache to prevent cross-site tracking

##### `StrictOriginIsolation`
***(security)***\
Strengthens origin isolation

##### `ValidateNetworkServiceProcessIdentity`
***(security MAC_ONLY NOT_TESTED)***\
Mandates code signing on the network process on MacOS

##### `WinSboxNetworkServiceSandboxIsLPAC`
***(security WINDOWS_ONLY)***\
Enable LPAC restrictions on the network service process (if enabled)

##### `WinSboxRestrictCoreSharingOnRenderer`
***(security WINDOWS_ONLY)***\
Prevents renderers from sharing a core with other processes, to prevent Hyperthreading/SMT based side-channel attacks

##### `WinSboxStrictHandleChecks`
***(security WINDOWS_ONLY)***\
Enables Windows process mitigation for sandboxed processes
