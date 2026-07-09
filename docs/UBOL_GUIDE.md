---
icon: "lucide/shield-ban"
---

# :lucide-shield-ban: Using uBlock Origin Lite (WIP)

## Manifest v3

A lot of people are under the impression that Chromium, and MV3, make adblocking impossible (or very very difficult). This is a untrue. Infact, adblocking is practically equivalent in MV3 content blockers as it was in MV2.

This idea comes from 2 main factors: that Google proposed MV3, and that they are an advertising revenue-model company. There is no technical argument for why adblocking would no longer work, only that "it will be less effective" without clear reasoning as to what that even means.

The following subsections detail common talking points about MV3 and why they are wrong, invalid, or overblown

### Rule Limits

Those who cite this often do not understand what this refers to. A lot of people assume that an MV3 rule equates to one filter, like a single site or element block. In reality, a "rule" refers a single action and filters on how that action is applied. For example, a "block' action on 10 thousand domains, that is 1 rule, not 10 thousand. The rule limit is pretty hard to hit is the filter-to-rule converter is well optimized, and uBlock Origin Lite's converter is very well optimized. With everything enabled in the default extension (English-centric), it totals out to 24 thousand rules. The limit for a single extension 30 thousand, plus 5 thousand for unsafe rules, plus an additional 300 thousand [shared among all of your extensions](https://developer.chrome.com/docs/extensions/develop/concepts/content-filtering#bundle_filter_rules_with_your_extension). Hitting this limit is not easy. Should the limit be higher? Probably, but the idea that it's "too low" or "there to inhibit adblockers" is false, most adblocker will not hit limit if they aren't trying to.

### Filter Updates

Initially, updating filterlists for extensions was a hassle, since you cannot remotely update filters so they need to bundled with the extension which means it needs to go through the update verification process on the webstore. This is obviously not good. Due to critisicm, they added a way to [skip these checks](https://developer.chrome.com/docs/webstore/skip-review). So it's now fine, not only is it fine but extensions can load remote filters anyway (within limits). uBOL currently has support for remote filters, granted cosmetic filtering and scriptlets don't work without an additional permission but this has pluses to it.

### Filter Efficiency

(WIP)

#### Youtube Adblock

Yes, it works. No idea why people thought it wouldn't. The mechanism by which Youtube adblock hasn't changed, it still involves injection JavaScript that prevents the ads from loading, MV3 didn't do anything to affect script injection.
