# Policies
Windows note: All policies with a value of `true` and `false` are represented as `1` and `0` in the registry respectively

#### `AlternateErrorPagesEnabled`
Value: `false`\
***(privacy)***

#### `AudioSandboxEnabled`
Value: `true`\
***(security)***

#### `AutofillAddressEnabled`
Value: `false`\
***(security RECOMMENDABLE)***

#### `AutofillCreditCardEnabled`
Value: `false`\
***(security RECOMMENDABLE)***

#### `AutofillPredictionSettings`
Value: `2`\
***(privacy)***\
Disables AI for autofill

#### `BackgroundModeEnabled`
Value: `false`\
***(annoyance performance privacy RECOMMENDABLE)***

#### `BlockExternalExtensions`
Value: `true`\
***(security)***

#### `BlockThirdPartyCookies`
Value: `true`\
***(privacy RECOMMENDABLE)***

#### `BrowserLabsEnabled`
Value: `false`\
***(annoyance)***\
Removes UI bloat and experimental garbage no-one needs

#### `BrowserSignin`
Value: `0`\
***(privacy annoyance)***\
Disables account sign-in with the browser

#### `BuiltInAIAPIsEnabled`
Value: `false`\
***(annoyance privacy)***\
Disables exposing local AI models to websites

#### `ChromeVariations`
Value: `2`\
***(privacy annoyance)***\
Prevents Chromium from overriding features remotely

#### `ClearBrowsingDataOnExitList`
***(privacy ~security OPTIONAL)***\
Clears data on exit, use **one-of** the following 2 options

###### `ClearBrowsingDataOnExitList (Option 1)`
Value: `["download_history","cached_images_and_files","autofill","hosted_app_data"]`\
***(privacy OPTIONAL)***\
Clears some useless data on exit, this can be configured if something is needed

###### `ClearBrowsingDataOnExitList (Option 2)`
Value: `["browsing_history","download_history","cookies_and_other_site_data","cached_images_and_files","password_signin","autofill","site_settings","hosted_app_data"]`\
***(privacy ~security OPTIONAL)***\
Clears all data on exit, **WILL RESULT IN DATA LOSS**

#### `ClickToCallEnabled`
Value: `false`\
***(privacy)***\
Disables phone number sharing for Chromium browsers across devices

#### `CloudAPAuthEnabled`
Value: `false`\
***(privacy WINDOWS_ONLY)***\
Disables automatic Microsoft cloud identity authentication

#### `CloudPrintProxyEnabled`
Value: `false`\
***(privacy)***\
Disables sharing printers with Google

#### `CreateThemesSettings`
Value: `2`\
***(privacy)***\
Disables AI for theme creation

#### `DefaultBrowserSettingEnabled`
Value: `false`\
***(annoyance)***

#### `DefaultJavaScriptJitSetting`
Value: `2`\
***(security OPTIONAL)***\
This can also be used to disable JIT, the only difference between this and the flag is that the flag disables JIT for extensions and internal (`chrome://` and `file://`) pages as well whereas this policy only disables it for websites. If you have an extension that requires JIT (i.e. not compatible with the flag), use this policy to compensate, you can whitelist sites using the `JavaScriptJitAllowedForSites` policy.

#### `DefaultJavaScriptOptimizerSetting`
Value: `1`\
***(~security OPTIONAL)***\
Locks the V8 security setting so the [JITless](https://github.com/RKNF404/chromium-hardening-guide/blob/main/configs/FLAGS.md#--js-flags--jitless) flag can properly disable JIT for all sites, disabling V8 optimizers acts as a whitelist for WebAssembly. If you need to configure JIT/WASM per-site, do not set this policy

#### `DefaultSensorsSetting`
Value: `2`\
***(security privacy)***

#### `DefaultWebUsbGuardSetting`
Value: `2`\
***(security privacy)***\
Block access to WebUSB

#### `DesktopSharingHubEnabled`
Value: `false`\
***(annoyance)***

#### `DevToolsGenAiSettings`
Value: `2`\
***(privacy)***\
Disables AI for dev tools/console

#### `Disable3DAPIs`
Value: `true`\
***(privacy security OPTIONAL)***\
Disables Pepper 3D and WebGL

#### `DnsOverHttpsMode`
***(privacy ~security)***\
Enable encrypted DNS, use values from **one-of** the next 2 options

###### `DnsOverHttpsMode (Option 1)`
Value: `"automatic"`\
***(~privacy ~security)***\
Enable automatic use of encrypted DNS if available by the system/network DNS

###### `DnsOverHttpsMode (Option 2)`
Value: `"secure"`\
***(privacy ~security OPTIONAL)***\
Enable encrypted DNS if the next policy is set

#### `DnsOverHttpsTemplates`
Value: `"https://freedns.controld.com/p2"`\
***(REQUIRES_[DnsOverHttpsMode-Option-2](#dnsoverhttpsmode-option-2))***\
The default DNS used here offers a variety of DNS security features including ECH and content blocking, but any decent DNS resolver could go here instead

#### `DynamicCodeSettings`
Value: `1`\
***(security WINDOWS_ONLY)***\
Uses ACG for the browser process to enforce W^X

#### `EnableMediaRouter`
Value: `false`\
***(privacy)***\
Disable Chrome Cast

#### `ExtensionAllowedTypes`
Value: `["extension", "theme"]`\
***(security)***\
Block extensions that are not either themes or regular extensions (example of blocked type, user script)

#### `ExtensionDeveloperModeSettings`
Value: `1`\
***(privacy)***\
Disables extension developer mode

#### `ExtensionInstallAllowlist`
Value: `["ddkjiahejlhfcafbddmgiahcphecmpfh"]`\
***(-security OPTIONAL)***\
Allow an extension, this specific value only allows uBlock Origin Lite

#### `ExtensionInstallBlocklist`
Value: `["*"]`\
***(security)***\
Block all extensions by default

#### `GeminiSettings`
Value: `1`\
***(privacy)***\
Disables Gemini integrations

#### `GenAILocalFoundationalModelSettings`
Value: `1`\
***(privacy)***\
Disables AI model downloading

#### `GoogleSearchSidePanelEnabled`
Value: `false`\
***(privacy)***\
Disables some other AI features that deal with Google search and the side-panel

#### `HardwareAccelerationModeEnabled`
Value: `false`\
***(security ~privacy OPTIONAL)***\
Disable HWAccel, reduces attack surface and prevents some HW based fingerprinting but reduces performance, also disables WebGL and WebGPU

#### `HelpMeWriteSettings`
Value: `2`\
***(privacy)***\
Disables AI for writing

#### `HistoryClustersVisible`
Value: `false`\
***(annoyance)***

#### `HistorySearchSettings`
Value: `2`\
***(privacy)***\
Disables AI for history searches

#### `HttpsOnlyMode`
Value: `"force_enabled"`\
***(security)***

#### `LensOverlaySettings`
Value: `1`\
***(privacy)***\
Disables performing Google searches using webpage screenshots

#### `LensRegionSearchEnabled`
Value: `false`\
***(privacy)***\
Disables context menu image searches with Lens

#### `LiveTranslateEnabled`
Value: `false`\
***(privacy)***\
Disables translation in realtime through a Google service

#### `MediaRecommendationsEnabled`
Value: `false`\
***(privacy annoyance)***

#### `MetricsReportingEnabled`
Value: `false`\
***(privacy)***

#### `NativeMessagingBlocklist`
Value: `["*"]`\
***(security)***\
Prevents extensions from communicating with native apps

#### `NetworkPredictionOptions`
Value: `2`\
***(privacy -performance RECOMMENDABLE)***

#### `NetworkServiceSandboxEnabled`
Value: `true`\
***(security)***
Enables various mitigations when used on Windows, but requires running the following command to enable it:
```
cd <where_is_the_exe>
icacls . /grant "*S-1-15-2-2:(OI)(CI)(RX)"
```
[(Thank you Cromite)](https://github.com/uazo/cromite?tab=readme-ov-file#enable-network-process-sandbox-in-windows)

#### `NTPCardsVisible`
Value: `false`\
***(privacy annoyance)***\
Disables new tab page service integrations and utilities

#### `PasswordLeakDetectionEnabled`
Value: `false`\
***(-security ~privacy OPTIONAL)***\
Dubious benefit to having it available

#### `PasswordManagerEnabled`
Value: `false`\
***(security RECOMMENDABLE)***\
Technically *optional*, but you should really just use a dedicated app or something

#### `PaymentMethodQueryEnabled`
Value: `false`\
***(security)***

#### `PrivacySandboxAdMeasurementEnabled`
Value: `false`\
***(privacy)***\
Disable privacy sandbox ad tracking

#### `PrivacySandboxAdTopicsEnabled`
Value: `false`\
***(privacy)***\
Disable privacy sandbox ad personalization

#### `PrivacySandboxPromptEnabled`
Value: `false`\
***(privacy)***\
Disables Privacy Sandbox prompt, needed for other privacy sandbox options

#### `PrivacySandboxSiteEnabledAdsEnabled`
Value: `false`\
***(privacy)***\
Disable privacy sandbox ad personalization

#### `PrivateNetworkAccessRestrictionsEnabled`
Value: `true`\
***(security)***\
Restricts access to local (private) addresses for websites

#### `PromotionsEnabled`
Value: `false`\
***(privacy)***

#### `PromptForDownloadLocation`
Value: `true`\
***(security)***

#### `RelatedWebsiteSetsEnabled`
Value: `false`\
***(privacy)***\
Prevents sites from sharing cookies with "related" sites

#### `RemoteAccessHostAllowRemoteAccessConnections`
Value: `false`\
***(security privacy)***\
Why is there remote access in a browser?

#### `RemoteAccessHostAllowRemoteSupportConnections`
Value: `false`\
***(security privacy)***\
Ibid

#### `RemoteAccessHostFirewallTraversal`
Value: `false`\
***(security privacy)***\
Disables firewall awareness for remote access connections

#### `RemoteDebuggingAllowed`
Value: `false`\
***(security)***

#### `SafeBrowsingDeepScanningEnabled`
Value: `false`\
***(privacy -security OPTIONAL)***\
Sending downloaded files to the cloud to be scanned is not a good idea privacy-wise and has little security benefit

#### `SafeBrowsingExtendedReportingEnabled`
Value: `false`\
***(privacy)***

#### `SafeBrowsingProtectionLevel`
Value: `1`\
***(security OPTIONAL RECOMMENDABLE)***\
Enable safe browsing, not needed but still better than nothing

#### `SafeBrowsingProxiedRealTimeChecksAllowed`
Value: `false`\
***(privacy -security OPTIONAL)***\
Sacrifice minor security in favor of not sending websites to Google for Safe Browsing

#### `SafeBrowsingSurveysEnabled`
Value: `false`\
***(privacy)***

#### `SearchSuggestEnabled`
Value: `false`\
***(privacy RECOMMENDABLE)***

#### `SharedClipboardEnabled`
Value: `false`\
***(privacy)***

#### `ShoppingListEnabled`
Value: `false`\
***(privacy)***

#### `ShowFullUrlsInAddressBar`
Value: `true`\
***(annoyance OPTIONAL)***

#### `SitePerProcess`
Value: `true`\
***(security)***\
Make site isolation mandatory, disables opt-out

#### `SpellCheckServiceEnabled`
Value: `false`\
***(privacy)***\
Disables Google spellcheck service

#### `SyncDisabled`
Value: `true`\
***(privacy)***

#### `TabCompareSettings`
Value: `2`\
***(privacy)***\
Disables AI for tab analysis

#### `TranslateEnabled`
Value: `false`\
***(privacy RECOMMENDABLE)***

#### `TranslatorAPIAllowed`
Value: `false`\
***(privacy)***

#### `UrlKeyedAnonymizedDataCollectionEnabled`
Value: `false`\
***(privacy)***\
Disables URL based data reporting

#### `UrlKeyedMetricsAllowed`
Value: `false`\
***(privacy)***\
Ibid

#### `UserAgentReduction`
Value: `2`\
***(privacy)***\
Reduce information in the user agent header

#### `UserFeedbackAllowed`
Value: `false`\
***(privacy)***

#### `WebRtcIPHandling`
Value: `"disable_non_proxied_udp"`\
***(privacy)***\
Prevents IP leakage from WebRTC, can cause issues with web calling services like Discord.

#### `WebRtcTextLogCollectionAllowed`
Value: `false`\
***(privacy)***

#### `WebUsbAskForUrls`
Value: `["https://grapheneos.org"]`\
***(security)***\
Allow GrapheneOS access to ask for WebUSB, to allow for the web-based installation
