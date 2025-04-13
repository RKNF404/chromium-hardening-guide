# Chromium Hardening Guide

Last updated for: `135` (policies only)

Hardening guide for (theoretically) any Chromium browser.

Some of the flips and toggles come from other projects such as [Vanadium](https://github.com/GrapheneOS/Vanadium) or [Trivalent](https://github.com/secureblue/Trivalent).

## Config Priority

1) Upstream Default
2) Management Policy
3) Preferences
4) Feature Toggle
5) Flag

## Quick Links

- [Setup Guide](#setup-guide)
- [Preferences](/configs/PREFERENCES.md)
- [Policies](/configs/POLICIES.md)
- [Flags](/configs/FLAGS.md)
- [Features (Enable)](/configs/ENABLE_FEATURES.md)
- [Features (Disable)](/configs/DISABLE_FEATURES.md)

# Setup Guide

The following guide will assist in setting up and using a Chromium based browser with the flags and policies present in this repo. It will cover 3 main sections: selecting a browser (covering forks, options for different OSes and alternatives to Chromium should they be viable), applying policies (only for Linux and Windows, maybe MacOS, but notes for other OSes where applicable), and persisting flags (only covering a few OSes since not all of them support proper flag persistence). The primary focus will be on **Linux** and **Windows**, but notes for Android and MacOS will be spread throughout where it makes sense.
\
\
Please note that while I intend for this to be as comprehensive as possible, there will be gaps. For example, I do not have a Mac so I am not capable of offering up-to-date info on methods or options for those systens.

## Quick Links

- [Selecting a browser](#selecting-a-browser)
  - [Baseline](#baseline)
  - [Proprietary vs Open-Source](#proprietary-vs-open-source)
  - [Popular Options](#popular-options)
  - [Other Browsers](#other-browsers)
- [Basic Setup](#basic-setup)
  - [Content Blocking](#content-blocking)
- [Policies](#policies)
  - [Linux](#linux)
  - [Windows](#windows)
  - [MacOS](#macos)
- [Flags](#persisting-flags)
  - [Linux](#linux-1)
  - [Windows](#windows-1)
  - [Android](#android)
- [My Setup](#my-setup) (in case you care)

## Selecting a browser

### Baseline

The most important security detail of a browser is 100% update cycle. Everything else security-wise is useless if the browser is updated once every few months. Vulnerabilities pile up and the more go unpatched, the worse it gets. For reference, chromium/Chrome is usually updated weekly or biweekly excluding holidays. Each update usually has at least one high-severity vuln, or at least a few medium/low. 2 months without updates essentially results in 6+ high severity vulnerabilities, plus the other severity vulns. No amount of hardening will compensate for that.
\
\
The next most important element is build quality, i.e. does it offer at least chromium's default or higher. Most often this is control-flow integrity (CFI), it is an upstream default in chromium on Linux yet for some reason many forks or Linux distros [explicitly disable it](https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/rules?ref_type=heads#L104). CFI is not common outside of desktop Linux and ChromeOS (for chromium that is), though there are some exceptions such as [Vanadium on Android](https://github.com/GrapheneOS/Vanadium/blob/main/args.gn#L30). Windows chromium uses the platform's Control Flow Guard (CFG) mitigation, most chromium based browsers have this enabled by default. On Linux, many distributions opt to dynamically link as many dependencies as possible to system libraries, mainly for package size and updateability. This is a security regression, since system shared libraries cannot provide CFI protections without [Cross-DSO-CFI](https://clang.llvm.org/docs/ControlFlowIntegrity.html#shared-library-support) which is not used in chromium. The more bundled, the better. I'm not aware if this issue is present on other operating systems.
\
\
The last aspect is additional features on top of vanilla chromium and more secure/private defaults. This also includes the ability to control insecure or unprivate features such as telemetry, or web assembly, etc. This isn't that important and can be optionally ignored, but it is something to be aware of.
\
\
TLDR; If the variant does something worse than Chrome, avoid it. The only leeway is on update cycle, it is physcially impossible to beat Chrome's releases. Anything within 2-3 days is acceptable, but the sooner the better. Less resourced projects have more leeway in this regard. If the variant does something better for security/privacy, that is a reason to use it, but it shouldn't overshadow downsides.

### Proprietary vs Open-Source

Long story short, it makes no difference. Open-source is preferable for transparency reasons, but has little effect on anything in the baseline criteria. Consider the option more like a tie-breaker than a genuine advantage to consider.

### Popular Options

#### Chrome

This is the baseline/standard, everything else must either match or beat this to be considered. This guide assumes the usage of Chrome in certain sections, since it is the most general and most common. Chrome has the fastest update cycle and is the most functional/well tested. It is constantly improving and even if it has weak defaults, it is trivial to improve many of them. If you don't know what option to pick, use Chrome.
\
The only downside is that Chrome is proprietary. This has no effect on security nor significant effect on privacy, it is essentially vanilla Chromium with a few proprietary additions and licenced libraries. Most of the intrusive stuff is disabled by following this guide.

#### Edge

A very highly regarded option, Edge makes decent security improvements on-top of Chrome, especially on Windows. Such as their Enhanced Security Mode, previously [Super Duper Secure Mode](https://microsoftedge.github.io/edgevr/posts/Super-Duper-Secure-Mode/), the use of the Code Integrity Guard (CIG) mitigation on the main browser process (since it prevents non-MS signed binaries from being executed, Edge is the only browser that can fully enable it), and the default use of AppContainer sandboxing for renderer processes. On Linux, it also offers a feature to enforce memory W^X on renderers with JIT disabled (last I checked this enforcement was disabled by default, but it can be enabled through `edge://flags`), which is currently only offered by Edge and [Trivalent](https://github.com/secureblue/Trivalent/blob/live/vanadium_patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch) (courtesy of [Vanadium](https://github.com/GrapheneOS/Vanadium/blob/main/patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch)).
\
The main issue with Edge is telemetry, it is *mandatory* without Windows Enterprise/Educational editions. This makes it a non-contender for privacy but decent for security. It's update cycle can occasionally be spotty, skipping release every now-and-again. Overall, it's about equal to Chrome.
\
This guide does not cover hardening Edge but other such guides exist, such as [Tommy Tran's Edge policies](https://github.com/TommyTran732/Microsoft-Edge-Policies) for Linux and MacOS or [Topaz's Equivalent](https://github.com/topaz8/windows-edge-policies) for Windows.

#### Opera

Avoid. It has mandatory telemetry, poor update cycle, and tons of feature bloat. It has very few if any advantages over Chrome. It does have a decent content-blocker, but I'm not certain if it has decent security (more on this later). Overall, not a great option.

#### Brave

Not terrible, but a weak option. It has one central advantage, the content-blocker. Everything else is either matching vanilla chromium, a degredation, or modifies a default. For example, they enable MV2 support when that format is actively being deprecated in chromium. MV2 is awful for security, since it allows unrestricted access to all websites and all features to extensions. MV3, while not perfect, fixes many of these issues. In general extensions are bad for security but enabling MV2 is a step backwards. 
\
They also verified their Flathub app. See the [Flatpak](#flatpak-linux) section as to why that is a problem. The issue is not that Brave is packaged as a Flatpak, many chromium browsers are, but they officially endorse it, which is a flagrant disregard for security.
\
Also lots of attack surface related to crypto stuff and heavy privacy marketing (despite being rather intrusive by default), and rather ineffective fingerprinting resistance (has gaps making the mitigations bypassable). The company itself is also questionable in its practices, but that is for you to decide.
\
To give some credit where it is due, Brave does have some decent changes. For example they proxy [a large number of requests](https://github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove)#services-we-proxy-through-brave-servers), for which they have a better pivacy policy on their services than Google. This does have some issues but it is still nice, none-the-less. They do also offer some partitioning improvements, though the amount of which isn't too big since upstream has added a lot of said improvements themselves.

#### Vivaldi

**HORRIFIC** update cycle. It is proprietary, which isn't the worst, but it is difficult to analyze how good it really is, build-wise. Though they do publish gapped [source code](https://vivaldi.com/source) (meaning some parts of the code are missing, for reference vanilla chromium is around 3.5-4 gigs when compressed, Vivaldi is around 2 if I recall correctly). It makes little improvements on Chrome, it does allow you to disable some intrusive integrations and has a content-blocker, but these are minor additions. It also has **MASSIVE** feature bloat. Again, mandatory telemetry which is surprisingly common.

#### Vanilla Chromium

This depends heavily, but usually these are just open-source variants of Chrome with worse update-cycles. Like mentioned in the [baseline](#baseline) section, some have terrible building standards, like disabling CFI or unbundling everything under the sun. Some variants (used to) go further by disabling the default memory allocator (PartitionAlloc), Debian for example used to use tcmalloc which is borderline a zero-security allocator built for performance. Replacing the allocator was deprecated in chromium for security reasons so no variants offer that anymore. Some builds lack CFI (this has been improving recently it seems), ~Fedora Linux only [recently](https://src.fedoraproject.org/rpms/chromium/c/d90f112feba409f4d6875033f98ff559919e35a6?branch=rawhide) started using it~ [Fedora disabled CFI again](https://src.fedoraproject.org/rpms/chromium/c/98aabf1afa6e37394cd7338d588cfdc5e35c0970?branch=rawhide), and many simple distros like [Arch](https://gitlab.archlinux.org/archlinux/packaging/packages/chromium/-/blob/cd8f1d1e907b39dd2f1f494febba26d535f9b18a/PKGBUILD#L168) keep it enabled. Research your specific distro, see what they do, how much do they bundle/unbundle.

##### ungoogled-chromium

[Bad](https://qua3k.github.io/ungoogled/). The update cycle is inconsistent at best, slow at worst. It disables the component updater which chromium depends on for security reasons, since many features such as CRLSets (used for certificate revocation) are updated as a component. The privacy isn't terrible, in the sense that no data can be collected, but the substantial security risk it offers is a massive negative.
\
It suffers the issues of typical vanilla builds, but with the added issues of ungoogled-chromium itself. For example, usage of [tcmalloc in the past](https://github.com/ungoogled-software/ungoogled-chromium-debian/commit/9f7246d1c29d58cd467c540d580ab15bcc9e8b88).

##### Flatpak (Linux)

As mentioned in the [Brave](#brave) section, ***AVOID***! Flatpak's security is... questionable for a number of reasons, but what's worse is chromium's security in Flatpak. Because Flatpak restricts the usage of Linux namespaces and prevents the use of SUID (for good reason), chromium's sandbox will literally not work. The solution is [zypak](https://github.com/refi64/zypak) or a [direct patch](https://github.com/flathub/org.chromium.Chromium/blob/master/patches/chromium/flatpak-Add-initial-sandbox-support.patch), the problem is these methods are very poorly configured to the point they essentially break the typically very strong sandboxing chromium provides. These solutions are closer to compatibility layers than they are genuine [security solutions](https://issues.chromium.org/issues/40753165#comment11). Upstream (chromium devs) have expressed they do no intend to support Flatpak [anytime soon](https://issues.chromium.org/issues/40928753#comment5) for reasons alike to this. Flatpak *significantly* inhibits chromium's sandboxing, and there is no faithful implementation currently.

### Other Browsers

#### Firefox

Firefox is [inherently insecure](https://madaidans-insecurities.github.io/firefox-chromium.html). I can already see the responses to that source, "Last updated March 2022", "2/3 year old article", "Biased and outdated", but these are often said in a hand-wave manner with the hope that time has fixed the issues present in the article... it has not. Saying the article is old actually makes Firefox look *worse*, since it hasn't significantly improved in 3 years. To be fair, there has been improvement but not enough of it to make it comparible to Chromium based browsers (even from 3 years ago). This is especially true on Linux where the sandboxing is very poor, and Android where there is no website sandbox at all. The current Android implementation of the Firefox sandbox (Fission) is not enabled by default (except by [IronFox](https://gitlab.com/ironfox-oss/IronFox/-/blob/dev/patches/enable-fission.patch?ref_type=heads)), even if it was enabled the implementation does not use Android's [isolatedProcess](https://developer.android.com/guide/topics/manifest/service-element#isolated) flag, which ensures that subprocesses are properly isolated and cannot trivially escalate privilege within the application. Equivalent to Android, Firefox does not have complete sandboxing in Flatpak, it doesn't even offer a compatibility layer alike to zypak, it just opts to cripple its own security.

##### Firefox Forks

I don't think I need to go too much in depth, most FF forks are just regular Firefox with either UI changes or some changes to user-hostile defaults. They typically suffer slower update cycles.
\
I will talk about 2 specifically, Librewolf and Palemoon. Librewolf is just Firefox with defaults changed... nothing else. They don't even maintain the defaults, they just use [arkenfox-user.js](https://github.com/arkenfox/user.js/). They may have some changes but fundamentally it is just arkenfox built-into Firefox with a slower update cycle. Palemoon uses *ancient* code with some security patches backported, and it is single-process so it cannot utilize any modern sandboxing technology (such as seccomp or namespaces, or the adjacents on other platforms). You can manually sandbox the browser but that doesn't isolate sites from each other. This also means that newer security features FF adds (as rare as that is) will not get properly added if they get added at all.

#### Safari (Webkit)

I don't use Apple devices but security-wise Safari/Webkit is pretty decent. It may be behind on web standards but it has strong partitioning, strong sandboxing, and robust mitigations on all supported platforms. Additionally, it can disable JIT JavaScript (and many other web features) on iOS and MacOS per-site using Lockdown Mode to be W^X compliant, though most websites will likely break.

##### Epiphany (WebkitGTK)

WebkitGTK is the (I think) official Webkit port to Linux. It shares many of the same features of regular Webkit, sans some stuff that are iOS/MacOS/Apple specific. It is the only browser to support proper sandboxing in Flatpak but said sandboxing is notably weaker than native (non-flatpak, non-snap) chromium.

#### Android Webview Browsers

These browsers cannot offer site-isolation due to how Android webview is designed, websites are only isolated from the system not each other. Typically they do not have strong partitioning and are very minimal in their feature set.

## Basic Setup

This is just preferences, so see [PREFERENCES.md](/configs/PREFERENCES.md). Everything else is covered by policies.

### Content Blocking

Content blocking is usually done one of 3 ways, Extensions, Native/Internal, and DNS/Network. Some are blatantly better than others.
\
\
For starters extensions are always bad. Especially MV2 extensions, like uBlock Origin. Since MV2 extensions can access any site as well as a great many features without permission. MV3 prevents this but isn't too much better since many extensions just ask for access to all sites anyway to work properly, but at least it offers the user control. With that in mind uBOL (uBlock Origin Light) in `Basic` mode is pretty good, since it has no access to sites while still being able to deliver decent content-blocking. It also allows granting access to specific sites, such as Youtube (yes it works), for better filtering if needed. Other extensions and uBOL global modes risk security and weaken site isolation.
\
\
Native/Interal can mean one of 2 (technically 3) things. One is using chromium's internal subresource filter (as done by [Vanadium](https://github.com/GrapheneOS/Vanadium) and [Trivalent](https://github.com/secureblue/trivalent-subresource-filter)), this is approx on-par with uBOL in `Basic` mode in terms of filtering capabilities. This is also the most secure since it is already built directly into chromium so no extra capabilities, features, or code is added or enabled. The second option is to integrate a third-party filtering engine, this is done by Brave, Vivaldi, Opera, Cromite, and many other browsers. This can vary between a new engine, like [Brave](https://github.com/brave/adblock-rust/), or integrating an extension, like [Cromite](https://github.com/uazo/cromite/blob/master/build/patches/Eyeo-Adblock-for-Cromite.patch). Both have more attack surface, but extension integration is much worse.
\
\
DNS/Network is arguably the most secure but the least effective (since it can only filter by domain, and not paths, e.g. all of `google.com` and not just `google.com/tracking`) of any method. With most content blocking you have to add trust in multiple entities and add extra attack surface. With DNS filtering, you are placing your trust in something you already have to trust (DNS resolution). I would still suggest the usage of some DNS filtering in your browser, even if you have another content-blocking solution. It also has no performance impact and can resist some forms of censorship and tracking by encrypting not only DNS traffic but also the Client Hello (via [ECH](https://wiki.mozilla.org/Security/Encrypted_Client_Hello)). Non-DNS network filtering has the same effectiveness with the added benefit of IP blocking, depending on the implementation. It should be noted that CNAME tracking can be fully mitigated through DNS filtering.
\
\
There is technically a sub-category of network filtering that is more comprehensive in its ability to filter, but it is a massive security risk. HTTPS interception filtering is a method where your content blocker will intercept your encrypted web traffic using its own certificate, this forces you to trust said content blocker with certificate handling and website data. This is not recommended, and you are better off just using DNS with/or a native blocking solution or extension.
\
\
Last note on remotely updated filters for systems like Brave, Opera, and uBlock Origin (MV2). The main problem here is that filters can still modify requests, run regex (which can be exploited in the browser engine), use cosmetic filters (which has been used to exfil data from sites in the past), and execute JavaScript via scriptlets. While scriptlets themselves aren't risky, even when limiting execution capabilities it is still arbitrary execution and therefore has massive risk. These filters are themselves arbitrary and unsigned, meaning you are OTA downloading random files that are an exploit away from reading the contents on all sites or worse. At least with MV3 extensions the filters have to bundled, so they are effectively signed along with the rest of the extension, so much better than most if not all integrated engines.

## Policies

See [POLICIES.md](/configs/POLICIES.md) for what policies can be used and their respective values

### Linux

Policies on Linux can vary in location, typically browsers will have their own directories under which to place policy files.
\
Policies for vanilla chromium, on most systems, will be located at `/etc/chromium/policies/managed/` for mandatory policies and `/etc/chromium/policies/recommended/` for recommended policies. Most policies must go in the managed directory, but some can go into recommended, these policies can be overridden in the user preferences. Policies that can be recommended will be labeled as such. Google Chrome policies will be located at `/etc/opt/chrome/policies/` with identical folders for mandatory and recommended policies.
\
The structure of Linux policy files is standard `json` with each policy represented as a string and it's associated value. See below (this is just an example policy, it will not do anything):
```
{
  "PolicyString": "string_value",
  "PolicyBoolean": true,
  "PolicyInteger": 22,
  "PolicyArray": ["array", "input"],
  "PolicyDictionary": { "BooleanEntry": false, "StringEntry": "dictionary_string", "DictionaryEntry": { "TestEntry": 0 } }
}
```
The formatting is very strict and will result in your policies not loading if they are formatted incorrectly.

> [!NOTE]
> When adding your file, make sure it is globally readable, some stricter umask values can result in this being an issue. For example, with umask 077. If you have this issue, run (as root) `chmod a+r /path/to/policies/managed/*`

### Windows

Windows policies rely on using the registry. Most browsers, similar to Linux, have different locations for their policies. Google Chrome will use policies from `HKEY_LOCAL_MACHINE/SOFTWARE/Policies/Google/Chrome`.
\
To add a policy, you need to make sure to add the right value type. Most often, there are only 2 reg values used, string value and DWORD (32-bit).
\
For any instance of a boolean value (true or false), use a DWORD and set it to `1` for true and `0` for false. The result under the `Data` column should look like `0x00000001` or `0x00000000` for true and false respectively.
\
Any policy using an integer (1, 2, 5, etc.), use a DWORD and set the value to that number. It should look similar to a boolean policy in the `Data` column but with the number you used at the end.
\
For strings, just enter them directly without quotes. For example, the policy `HttpsOnlyMode` has the string value `force_enable`, enter that as it is. Do not enter `"force_enable"`, it will not work.
\
Policy arrays and dictionaries also use the string values, they have the same formatting as presented, nothing special.

### MacOS

Policies for Mac are similar to Linux in the sense that they are formatted files located in a global config directory. Instead of JSON, MacOS uses plist (XML formatted) files to handle prefs and policies.
\
\
Aa far as I can tell, mandatory policies always go under `/Library/Managed Preferences/` and recommended go under `/Library/Preferences/`. The variance between browsers would be the file names, since they are related to the application identifier.
\
For Google Chrome, to apply policies, create a file `com.google.Chrome.plist` in the respective directory, i.e. managed or recommended. Then add policies in the proper formatting (see below).
\
\
MacOS policies follow this format (this policy do nothing, they just demonstrate how to format each policy value type):

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>PolicyString</key>
    <string>string_value</string>
    <key>PolicyBoolean</key>
    <true />
    <key>PolicyInteger</key>
    <integer>2</integer>
    <key>PolicyArray</key>
    <array>
      <string>string_value1</string>
      <string>string_value2</string>
    </array>
    <key>PolicyDictionary</key>
    <dict>
      <key>BooleanEntry</key>
      <false />
      <key>StringEntry</key>
      <string>dictionary_string</string>
      <keyDictionaryEntry</key>
      <dict>
        <key>TestEntry<key>
        <integer>0</integer>
      </dict>
    </dict>
  </dict>
</plist>
```

> [!NOTE]
> I do not have a Mac, I have zero idea if this is correct or works. If this doesn't work, open an issue.

# Persisting Flags

See [FLAGS.md](/configs/FLAGS.md) for what flags to include.
\
As well as [ENABLE_FEATURES.md](/configs/ENABLE_FEATURES.md) and [DISABLE_FEATURES.md](/configs/DISABLE_FEATURES.md) to see what features to enable and disable respectively.

### Linux

There is no one answer, most Linux distibutions offer a way to persist flags for their build of chromium, and sometimes even offer a way to persist for Google Chrome as well.
\
For example, Arch notably offers a [flag persistence method](https://wiki.archlinux.org/title/Chromium#Configuration) for both chromium and Chrome. Fedora also offers a method via `/etc/chromium/chromium.conf`. Most other common distros like Ubuntu, Debian, Gentoo, Nix, etc. also offer methods that are either specific or similar.
\
Research into your specific distro and find out how it handles flag persistence. It can sometimes help to just search around `/etc` for a chromium directory or set of chromium files.

### Windows

Out of the box, there is really no easy way to persist flags in a way to guarentee that they will be used... but, with some reg hacking and a launch script it is possible (thanks to chrlauncher).
\
Using another project of mine, [chromewrapper](https://github.com/RKNF404/chromewrapper), you can persist flags, specifically for Google Chrome, but it should be trivially adjustable to any chromium-based browser.
\
\
To do this project, run the install script `chromewrapperDefaultBrowser.bat`, this will add reg keys for the wrapper script to handle standard requests a browser would typically handle. (this step requires running the script as admin)
\
Then add `chromewrapper.bat` to the location given by `CHROMEWRAPPER_PATH` present in that script, by default it should be Chrome's binary directory (where `chrome.exe` is present), by default this should be `C:\Program Files\Google\Chrome\Application\chromewrapper.bat`.
> [!NOTE]
> Don't forget to update the flags present in `chromewrapper.bat`, they are not frequently updated because... lazy... see the flags and features files for this

After this, create a desktop shortcut with the following entry:
\
`explorer.exe "C:\Program Files\Google\Chrome\Application\chromewrapper.bat"`
\
Then right click that shortcut and click `Pin To Taskbar`.
\
And that's it, your browser will now launch with the flags in the wrapper script whenever it is opened from the icon or invoked as a handler. (The shortcut can be deleted by the way, the taskbar pin will be unaffected)
\
\
If you no longer wish to use the wrapper, simply run the `chromewrapperRegCleaner.reg` registry file. It will delete all instances where chromewrapper is a handler. You can also deselect it as the default browser in the settings to retain the functionality for later.

### Android

There is a way to add flags via ADB, but I know very little about it and would advise against.

## My Setup

In case you are curious, this is my personal setup. The main purpose is to demonstrate the usage of this guide.
\
\
Lets start with OSes, I have an Android, Linux, and Windows machines. They are GrapheneOS, Fedora Workstation, and Windows 11 respectively. Because of this, your setup may vary.
\
\
On GrapheneOS, I use Vanadium. Without a doubt the best option on Android, but due to a lack of availability outside of GrapheneOS, it is difficult to recommend. So, the next best option I would use is Chrome. Yes, Chrome with some settings changed and some flags altered in `chrome://flags`. Is this ideal, not really, but it's the next best thing below Vanadium. For watching Youtube without ads, I use Newpipe, so adblocking isn't a big enough deal for me in browsing to justify selecting a browser based around it. *Not so subtle suggestion against Brave.*
\
\
On Fedora, I use Trivalent, secureblue's default browser. It is sort of a port of Vanadium to desktop Linux, comes with a lot of neat defaults and hardening. For RPM based distros, it is definitely the best option. Due to Trivalent's default, it requires no usage of this guide or its configs. Otherwise, say on a Debian or Arch distro, I would use Chrome with the application of this guide. It's the closest you get to Trivalent/Vanadium.
\
\
On Windows 11. I use Chrome, 90% of the time Chrome is the best option, obviously with the application of [this guide](#windows-1) (including chromewrapper). I don't consider any other options to be better than Chrome. Edge is a decent contender but I would not, mainly because it is way more intregrated with MS services than Chrome is with Google services, some of those services cannot be turned off (or require Windows Enterprise to be turned off, like the Telemetry), and the update cycle is spotty (or it was when I used it). Some of these things may not be of concern for you, but they are for me, and the security benefit Edge offers is not too major when Chrome is configured properly (ideally the gap would be smaller if chromium ***actually decided to maintain drumbrake*** (the web assembly interpreter) ***properly***... but who knows when that will happen).
