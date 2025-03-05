# Features (Enable)
(`--enable-features=`)

##### `AcceleratedVideoDecodeLinuxGL,AcceleratedVideoDecodeLinuxZeroCopyGL,AcceleratedVideoEncoder`
***(performance LINUX_ONLY)***\
Enable hardware accelerated video decoding and encoding on Linux platforms

##### `BlockCrossPartitionBlobUrlFetching`
***(privacy)***\
Enhances site partitioning

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

##### `MacSyscallSandbox`
***(security MACOS_ONLY NOT_TESTED)***\
Enables syscall filtering for the sandbox on MacOS

##### `NetworkServiceCodeIntegrity`
***(security WINDOWS_ONLY)***\
Enable Code Integrity Guard (CIG) in the Network Service process pre-launch

##### `PartitionConnectionsByNetworkIsolationKey`
***(privacy)***\
Isolates connection information to prevent cross-site tracking

##### `PartitionVisitedLinkDatabase`
***(privacy)***\
Isolates the visited status of sites to prevent history leaks

##### `PrefetchPrivacyChanges`
***(privacy)***\
Limits what information is sent to prefetched sites, such as clearing the referrer and prevent access to cookies

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

##### `VaapiOnNvidiaGPUs`
***(performance LINUX_ONLY NVIDIA_ONLY)***\
Enable hardware accelerated video decoding on Nvidia GPUs

##### `WinSboxRestrictCoreSharingOnRenderer`
***(security WINDOWS_ONLY)***\
Prevents renderers from sharing a core with other processes, to prevent Hyperthreading/SMT based side-channel attacks

