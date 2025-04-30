# Policies
Windows note: All policies with a value of `true` and `false` are represented as `1` and `0` in the registry respectively

#### `AlternateErrorPagesEnabled`
Value: `false`\
***(privacy)***

#### `AudioSandboxEnabled`
Value: `true`\
***(security)***

#### `AuthSchemes`
Value: `"ntlm,negotiate"`\
***(security)***\
Restricts to more secure authentication schemes

#### `AutofillAddressEnabled`
Value: `false`\
***(security recommendable)***

#### `AutofillCreditCardEnabled`
Value: `false`\
***(security recommendable)***

#### `BackgroundModeEnabled`
Value: `false`\
***(annoyance performance privacy recommendable)***

#### `BlockExternalExtensions`
Value: `true`\
***(security)***

#### `BlockThirdPartyCookies`
Value: `true`\
***(privacy recommendable)***

#### `BrowserLabsEnabled`
Value: `false`\
***(annoyance)***\
Removes UI bloat and experimental garbage no-one needs

#### `BrowserSignin`
Value: `0`\
***(privacy annoyance)***\
Disables account sign-in with the browser

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
Disables phone number sharing for Chromium browser across devices

#### `CloudAPAuthEnabled`
Value: `false`\
***(privacy WINDOWS_ONLY)***\
Disables automatic Microsoft cloud identity authentication

#### `CloudPrintProxyEnabled`
Value: `false`\
***(privacy)***\
Disables sharing printers with Google

#### `DefaultBrowserSettingEnabled`
Value: `false`\
***(annoyance)***

#### `DefaultJavaScriptOptimizerSetting`
Value: `1`\
***(~security)***\
Locks the V8 security setting so the [JITless](https://github.com/RKNF404/chromium-hardening-guide/blob/main/configs/FLAGS.md#--js-flags--jitless) flag can properly disable JIT for all sites, disabling V8 optimizers acts as a whitelist for WebAssembly

#### `DefaultSensorsSetting`
Value: `2`\
***(security privacy)***

#### `DesktopSharingHubEnabled`
Value: `false`\
***(annoyance)***

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

#### `ExtensionSettings`
***(security)***\
Technically *optional*, but it should not be\
Limits extensions that can be installed, depending on which **one-of** the following 2 options you choose

###### `ExtensionSettings (Option 1)`
Value: `{"*":{"allowed_types":["extension"],"installation_mode":"blocked",},"ddkjiahejlhfcafbddmgiahcphecmpfh":{"installation_mode":"allowed","override_update_url": true,"update_url":"https://clients2.google.com/service/update2/crx",}}`\
***(security)***\
Block all extensions and extension types but allow uBlock Origin Lite, sets the update source to a trusted location

###### `ExtensionSettings (Option 2)`
Value: `{"*":{"installation_mode":"blocked",}}`\
***(security OPTIONAL)***\
Block all extensions

#### `GenAiDefaultSettings`
Value: `2`\
***(privacy)***\
Disable all AI generation features

#### `GenAILocalFoundationalModelSettings`
Value: `1`\
***(privacy)***\
Disables AI model downloading

#### `GoogleSearchSidePanelEnabled`
Value: `false`\
***(privacy)***\
Disables some other AI features that deal with Google search and the side-panel

#### `HistoryClustersVisible`
Value: `false`\
***(annoyance)***

#### `HttpsOnlyMode`
Value: `force_enabled`\
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

#### `MetricsReportingEnabled`
Value: `false`\
***(privacy)***

#### `NativeMessagingBlocklist`
Value: `["*"]`\
***(security)***\
Prevents extensions from communicating with native apps

#### `NetworkPredictionOptions`
Value: `2`\
***(privacy -performance recommendable)***

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

#### `PasswordManagerEnabled`
Value: `false`\
***(security recommendable)***\
Technically *optional*, but you should really just use a dedicated app or something

#### `PaymentMethodQueryEnabled`
Value: `false`\
***(security)***

#### `PrivacySandboxAdMeasurementEnabled`
Value: `false`\
***(privacy)***\
Disable privacy sandbox ad tracking


#### `PrivacySandboxAdTopicEnabled`
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

#### `SafeBrowsingProxiedRealTimeChecksAllowed`
Value: `false`\
***(privacy -security OPTIONAL)***\
Sacrifice minor security in favor of not sending websites to Google for Safe Browsing

#### `SearchSuggestEnabled`
Value: `false`\
***(privacy recommendable)***

#### `SharedClipboardEnabled`
Value: `false`\
***(privacy)***

#### `ShowFullUrlsInAddressBar`
Value: `true`\
***(annoyance OPTIONAL)***

#### `TranslateEnabled`
Value: `false`\
***(privacy recommendable)***

#### `WebRtcIPHandling`
Value: `"disable_non_proxied_udp"`\
***(privacy OPTIONAL)***\
Prevents IP leakage from WebRTC, can cause issues with web calling services like Discord

#### `WebRtcTextLogCollectionAllowed`
Value: `false`\
***(privacy)***
