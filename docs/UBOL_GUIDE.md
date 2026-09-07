---
icon: "lucide/shield-ban"
---

# :lucide-shield-ban: Extensions (WIP)

## Manifest v3

A lot of people are under the impression that Chromium, and Manifest Version 3, make ad-blocking very very difficult. This is a untrue. In-fact, ad-blocking is practically equivalent in Manifest Version 3 (MV3) content blockers as it was in Manifest Version 2 (MV2).

This idea comes from 2 main factors: that Google proposed MV3, and that they are an advertising revenue-model company. There is no technical argument for why ad-blocking would no longer work, only that "it will be less effective" without clear reasoning as to what that even means.

The following subsections detail common talking points about MV3 and why they are wrong, invalid, or overblown.

### Rule Limits

Those who cite this often do not understand what rule limits refer to. A lot of people assume that an MV3 rule equates to one filter, like blocking a single site or element. In reality, a "[rule](https://developer.chrome.com/docs/extensions/reference/api/declarativeNetRequest#build-rules)" refers a single action and static filters on how that action is applied. For example, a "block' action on 10 thousand domains, that is 1 rule, **not** 10 thousand. The rule limit is pretty hard to hit if the filter-to-rule converter is well optimized, and for example uBlock Origin Lite's converter is pretty good. With everything enabled in the default extension (English-centric), it totals out to 24 thousand rules. The limit dedicated for a single extension is [30 thousand](https://developer.chrome.com/blog/improvements-to-content-filtering-in-manifest-v3#:~:text=allow%20up%20to%2030%2C000%20of%20these), plus [5 thousand](https://developer.chrome.com/blog/improvements-to-content-filtering-in-manifest-v3#:~:text=The%20rule%20limit%20for%20all%20other%20dynamic%20net%20request%20rules%20stays%20at%205%2C000) for unsafe rules, plus an additional 300 thousand that is [shared among all of your extensions](https://developer.chrome.com/docs/extensions/develop/concepts/content-filtering#bundle_filter_rules_with_your_extension). Hitting this limit is not easy. Should the limit be higher? Probably, but the idea that it's "too low" or "there to inhibit ad-blockers" is false, most ad-blocker will not hit limit if they aren't trying to and will not suffer from reduced filter efficiency.

### Filter Updates

Initially, updating filter-lists for extensions was a hassle, since you cannot remotely update filters so they need to be bundled with the extension which means it needs to go through the update verification process on the web-store. This is obviously not good and bottlenecks filter efficiency. Due to criticism, Google added a way to [skip these checks](https://developer.chrome.com/docs/webstore/skip-review) specifically for filter updates. So it's now fine, not only is it fine but extensions can load remote filters anyway (within limits). uBOL currently has support for remote filters, granted cosmetic filtering and scriptlets don't work without an additional permission.

In addition, a big concern with MV2-style filter updates is that they are not protected or signed. These lists downloaded from arbitrary sources with the only protection being the TLS certificate system (https). Filter-lists are powerful, they can execute scriptlets, run regex, or manipulate responses of pages in real-time (granted not unrestricted access to any of these but even partial script execution is a potential problem). In the past, uBlock Origin cosmetic filtering [was exploited to exfiltrate data](https://portswigger.net/research/ublock-i-exfiltrate-exploiting-ad-blockers-with-css) from sites, this was patched but it shows that filter-lists are not just simple text files and yield real attack surface. With MV2, and similar ad-blocking mechanism such as Brave's adblock-rs for example, there is no root-of-trust that ensures the filters being updated are correct so every update yields risk of malicious tampering. By contrast MV3 filters, since they are bundled, are signed along with the rest of the extension, so the assurance that the filters used by the ad-blocker are authentic are significantly higher.

### Filter Efficiency

According to an [independent study in August of 2026](https://arxiv.org/html/2503.01000), "The empirical findings indicate no statistically significant reduction in ad-blocking or anti-tracking effectiveness for MV3 ad blockers compared to their MV2 counterparts. Some of our results even suggest slight improvements in blocking trackers for specific ad blockers following the MV3 update." This paper has limitations, as indicated in [section 7](https://arxiv.org/html/2503.01000#S7). These limitations do not appear to have any clear bias towards MV2 results or MV3 results, so at best we can assume ideal-case all around.

#### Youtube Adblock

Yes, it works. No idea why people thought it wouldn't. The mechanism by which YouTube ad-block works involves injecting JavaScript that prevents YouTube from loading video ads. This is not content blocking in the traditional sense since it isn't actually filtering anything, and therefore not within scope of the Web Request Blocking API deprecation. MV3 explicitly did not affect script injection on web pages if the extension has permitted access to said page, so ad-blocking on YouTube was never at risk.
