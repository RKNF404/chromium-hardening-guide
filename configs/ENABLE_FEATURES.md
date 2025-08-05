# Features (Enable)
(`--enable-features=`)

##### `CapReferrerToOriginOnCrossOrigin`
***(privacy)***\
Limits the referrer to only send the origin of the URL\
E.g. just "google.com" instead of "google.com/search"

##### `ClearCrossSiteCrossBrowsingContextGroupWindowName`
***(privacy DISFUNCTIONAL)***\
Prevents the window.name property from being leaked across sites

##### `ContentSettingsPartitioning`
***(privacy)***\
Isolate Content Settings by Origin

##### `EnableCsrssLockdown`
***(security WINDOWS_ONLY)***\
Prevents renderer processes from having access to the CSRSS service

##### `HstsTopLevelNavigationsOnly`
***(privacy)***\
Prevents third-party tracking using HSTS

##### `MacSyscallSandbox`
***(security MACOS_ONLY NOT_TESTED)***\
Enables syscall filtering for the sandbox on MacOS

##### `NetworkServiceCodeIntegrity`
***(security WINDOWS_ONLY)***\
Enable Code Integrity Guard (CIG) in the Network Service process pre-launch

##### `PartitionConnectionsByNetworkIsolationKey`
***(privacy)***\
Isolates connection information to prevent cross-site tracking

##### `PrefetchPrivacyChanges`
***(privacy)***\
Limits what information is sent to prefetched sites, such as clearing the referrer and prevent access to cookies

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

##### `WinSboxRestrictCoreSharingOnRenderer`
***(security WINDOWS_ONLY)***\
Prevents renderers from sharing a core with other processes, to prevent Hyperthreading/SMT based side-channel attacks

