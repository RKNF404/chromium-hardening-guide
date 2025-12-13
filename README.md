# Chromium Hardening Guide

Last updated for: `143`

Changes in latest version:
```
PartitionAllocWithAdvancedChecks:enabled-processes/all-processes
```

Hardening guide for (theoretically) any Chromium browser.

Some of the flips and toggles come from other projects such as [Vanadium](https://github.com/GrapheneOS/Vanadium) or [Trivalent](https://github.com/secureblue/Trivalent).

If you're having any trouble applying the guide or have any general questions or inquiries, please feel free to open a [discussion thread](https://github.com/RKNF404/chromium-hardening-guide/discussions).
If want to suggest something, please open an [issue](https://github.com/RKNF404/chromium-hardening-guide/issues) for it.
If you have my Discord, feel free to message me there about this guide.

## Config Priority

1) Upstream Default
2) Preferences
3) Management Policy / Feature Toggle / Flag

I intend to add more redundancy in the policies, UI flips, and flags/features. Mainly because in some cases not every kind of configuration is available (i.e. on some platforms policies or flags or both may not be an option to enable hardening features). I want to account for cases where one is missing. Because currently, if say a policy does the same thing as a flag, I won't add the flag. In future I will add both.
\
~~This will likely result in a rewrite where I create a table where each entry is a desired effect and the corresponding flag, policy, and preference to get said effect. For example disabling default browser checks has both a flag and policy, both do the same thing.~~
\
So, this didn't seem viable, instead I will unify the configuration documents into one database file and generate a script to generate configs for the various platforms (i.e. WINDOWS_ONLY, LINUX_ONLY, etc), flag/policy tags (i.e. annoyance, privacy, security, etc), by optional, and creating a recommended config. This will probably take some time. "Why not a seperate file for every config?" Because I don't intend to maintain 15 different files at once where half of them have the same entries.

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
Please note that while I intend for this to be as comprehensive as possible, there will be gaps. For example, I do not have a Mac so I am not capable of offering up-to-date info on methods or options for those systems.

## Contents

- [Selecting a browser](#selecting-a-browser)
  - [Baseline](#baseline)
  - [Proprietary vs Open-Source](#proprietary-vs-open-source)
  - [Popular Options](#popular-options)
  - [Popular Security-Centric Options](#popular-security-centric-options)
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

The most important security detail of a browser is 100% update cycle. Everything else security-wise is useless if the browser is updated once every few months. Vulnerabilities pile up, and the more they go unpatched, the worse it gets. For reference, Chromium/Chrome is usually updated weekly or biweekly excluding holidays. Each update usually has at least one high-severity vuln, or at least a few medium/low. 2 months without updates essentially results in 6+ high severity vulnerabilities, plus the other severity vulns. No amount of hardening will compensate for that.
\
\
The next most important element is build quality, i.e. does it offer at least Chromium's default or higher? Most often this is control-flow integrity (CFI), it is an upstream default in Chromium on Linux yet for some reason many forks or Linux distros [explicitly disable it](https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/rules?ref_type=heads#L104). CFI is not common outside of desktop Linux and ChromeOS (for Chromium that is), though there are some exceptions such as [Vanadium on Android](https://github.com/GrapheneOS/Vanadium/blob/main/args.gn#L30). Windows Chromium uses the platform's Control Flow Guard (CFG) mitigation, most Chromium based browsers have this enabled by default. On Linux, many distributions opt to dynamically link as many dependencies as possible to system libraries, mainly for package size and updateability. This is a security regression, since system shared libraries cannot provide CFI protections without [Cross-DSO-CFI](https://clang.llvm.org/docs/ControlFlowIntegrity.html#shared-library-support) which is not used in Chromium. The more bundled, the better. I'm not aware if this issue is present on other operating systems.
\
\
The last aspect is additional features on top of vanilla Chromium and more secure/private defaults. This also includes the ability to control insecure or non-private features such as telemetry, WebAssembly, etc. This isn't that important and can be optionally ignored, but it is something to be aware of.
\
\
TLDR; If the variant does something worse than Chrome, avoid it. The only leeway is on update cycle, it is physically impossible to beat Chrome's releases. Anything within 2-3 days is acceptable, but the sooner the better. Less resourced projects have more leeway in this regard. If the variant does something better for security/privacy, that is a reason to use it, but it shouldn't overshadow downsides.

### Proprietary vs Open-Source

Long story short, it makes no difference. Open-source is preferable for transparency reasons, but has little effect on anything in the baseline criteria. Consider the option more like a tie-breaker than a genuine advantage to consider.

### Resisting Fingerprinting

(WIP)

Quick Summary:
- Nice to have, not a priority
- Should not be focal point of the selection process
- Generally very ineffective, even something more comprehensive like Brave is very flawed
- If you absolutely need it, use a VM and use Tor Browser, do not use Tor outside a VM

### Popular Options

#### Chrome

This is the baseline/standard, everything else must either match or beat this to be considered. This guide assumes the usage of Chrome in certain sections, since it is the most general and most common. Chrome has the fastest update cycle and is the most functional/well tested. It is constantly improving and even if it has weak defaults, it is trivial to improve many of them. If you don't know what option to pick, use Chrome.
\
The only downside is that Chrome is proprietary. This has no effect on security nor significant effect on privacy, it is essentially vanilla Chromium with a few proprietary additions and licenced libraries. Most of the intrusive stuff is disabled by following this guide.

#### Edge

A very highly regarded option, Edge makes decent security improvements on-top of Chrome, especially on Windows. Such as their Enhanced Security Mode, previously [Super Duper Secure Mode](https://microsoftedge.github.io/edgevr/posts/Super-Duper-Secure-Mode/), the use of the Code Integrity Guard (CIG) mitigation on the main browser process (since it prevents non-MS signed binaries from being executed, Edge is the only browser that can fully enable it), and the default use of AppContainer sandboxing for renderer processes on Windows. On Linux, it also offers a feature to enforce memory W^X on renderers with JIT disabled (last I checked this enforcement was disabled by default, but it can be enabled through `edge://flags`), which is currently only offered by Edge and [Trivalent](https://github.com/secureblue/Trivalent/blob/live/vanadium_patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch) (courtesy of [Vanadium](https://github.com/GrapheneOS/Vanadium/blob/main/patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch)).
\
The main issue with Edge is telemetry, it is *mandatory* without Windows Enterprise/Educational editions. This makes it a non-contender for privacy but decent for security. It's update cycle can occasionally be spotty, skipping release every now-and-again. Overall, it's about equal to Chrome.
\
This guide does not cover hardening Edge but other such guides exist, such as [Tommy Tran's Edge policies](https://github.com/TommyTran732/Microsoft-Edge-Policies) for Linux and MacOS or [Topaz's Equivalent](https://github.com/topaz8/windows-edge-policies) for Windows.

#### Opera

Avoid. It has mandatory telemetry, a poor update cycle, and tons of feature bloat. It has very few if any advantages over Chrome. It does have a decent content-blocker, but I'm not certain if it has decent security (more on this later). Overall, not a great option.

#### Brave

Not terrible, but a weak option. Most of this browser is either matching vanilla Chromium, a degredation, or modifies a default. For example, they enable MV2 support when that format is actively being deprecated in Chromium. MV2 is awful for security, since it allows unrestricted access to all websites and all features to extensions. MV3, while not perfect, fixes many of these issues. In general, extensions are bad for security, but enabling MV2 is a step backwards. It should be noted that Brave only enables MV2 for [4 extensions](https://brave.com/blog/brave-shields-manifest-v3/), but this doesn't solve anything. The issue isn't that any extension can be MV2, it's the use of MV2 extensions themselves. See the [content blocking](#content-blocking) section why MV2 is specifically an issue, whitelisting these extensions doesn't solve the issues with MV2 and only puts more users at risk. Especially since they whitelist uMatrix, which they admit in their own blog post is no longer maintained.
\
They also verified their Flathub app. See the [Flatpak](#flatpak-linux) section as to why that is a problem. The issue is not that Brave is packaged as a Flatpak, many Chromium browsers are, but they officially endorse it, which is a flagrant disregard for security. They do recommend against using the Flatpak [on their website](https://brave.com/linux/#flatpak), but this notice isn't present in the Flathub description nor do they give a notice after installing it, so most users will not see it. It wouldn't be surprising if most Brave Flatpak users were unaware of Brave's official stance on this. At the very least, if it was not verified, it would push more cautious users away to not use unofficial packages.
\
Also, there is lots of attack surface related to crypto stuff and heavy privacy marketing (despite being rather intrusive by default), and rather ineffective fingerprinting resistance (has gaps making the mitigations bypassable). The company itself is also questionable in its practices, but that is for you to decide.
\
In the realm of attack surface, the content blocker can be a problem. It is written in Rust and all, but Rust only prevents exploits targeting the adblock engine itself, not the browser or sites. See the [content blocking](#content-blocking) section for more details.
\
To give some credit where it is due, Brave does have some decent changes. For example they proxy [a large number of requests](https://github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove)#services-we-proxy-through-brave-servers), for which they have a better privacy policy on their services than Google. This does have some issues but it is still nice, none-the-less. They do also offer some partitioning improvements, though the amount of which isn't too big since upstream has added a lot of said improvements themselves.
\
Overall, on desktop, Brave is rather useless. It is filled with bloat and any security or privacy advantages, even the adblocker, can be achieved with Chrome. However, on Android, if you do not have access to Vanadium, then Brave is probably the next best choice. Chrome on Android isn't bad, but Brave actually offers more there and the bloat is way less noticeable and easier to turn off.

#### Vivaldi

***Horrific*** update cycle. It is proprietary, which isn't the worst, but it is difficult to analyze how good it really is, build-wise. Though they do publish gapped [source code](https://vivaldi.com/source) (meaning some parts of the code are missing, for reference vanilla Chromium is around 3.5-4 gigs when compressed, Vivaldi is around 2 if I recall correctly). It makes little improvements on Chrome, it does allow you to disable some intrusive integrations and has a content-blocker, but these are minor additions. It also has ***massive*** feature bloat. Again, mandatory telemetry which is surprisingly common.

#### Vanilla Chromium

This depends heavily, but usually these are just open-source variants of Chrome with worse update-cycles. As mentioned in the [baseline](#baseline) section, some have terrible building standards, like disabling CFI or unbundling everything under the sun. Some variants (used to) go further by disabling the default memory allocator (PartitionAlloc), Debian for example used to use tcmalloc which is borderline a zero-security allocator built for performance. Replacing the allocator was deprecated in Chromium for security reasons so no variants offer that anymore. Some builds lack CFI (this has been improving recently it seems), ~Fedora Linux only [recently](https://src.fedoraproject.org/rpms/chromium/c/d90f112feba409f4d6875033f98ff559919e35a6?branch=rawhide) started using it~ [Fedora disabled CFI again](https://src.fedoraproject.org/rpms/chromium/c/98aabf1afa6e37394cd7338d588cfdc5e35c0970?branch=rawhide), and many simple distros like [Arch](https://gitlab.archlinux.org/archlinux/packaging/packages/chromium/-/blob/cd8f1d1e907b39dd2f1f494febba26d535f9b18a/PKGBUILD#L168) keep it enabled. Research your specific distro, see what they do, how much do they bundle/unbundle.

##### ungoogled-chromium

[Bad](https://qua3k.github.io/ungoogled/). The update cycle is inconsistent at best, slow at worst. It disables the component updater which Chromium depends on for security reasons, since many features such as CRLSets (used for certificate revocation) are updated as a component. The privacy isn't terrible, in the sense that no data can be collected, but the substantial security risk it offers is a massive negative.
\
It suffers the issues of typical vanilla builds, but with the added issues of ungoogled-chromium itself. For example, usage of [tcmalloc in the past](https://github.com/ungoogled-software/ungoogled-chromium-debian/commit/9f7246d1c29d58cd467c540d580ab15bcc9e8b88).

##### Flatpak (Linux)

As mentioned in the [Brave](#brave) section, ***avoid***! Flatpak's security is... questionable for a number of reasons, but what's worse is Chromium's security in Flatpak. Because Flatpak restricts the usage of Linux namespaces and prevents the use of SUID (for good reason), Chromium's sandbox will literally not work. The solution is [zypak](https://github.com/refi64/zypak) or a [direct patch](https://github.com/flathub/org.chromium.Chromium/blob/master/patches/chromium/flatpak-Add-initial-sandbox-support.patch), the problem is these methods are very poorly configured to the point they essentially break the typically very strong sandboxing that Chromium provides. These solutions are closer to compatibility layers than they are genuine [security solutions](https://issues.chromium.org/issues/40753165#comment11). Upstream (Chromium devs) have expressed they do no intend to support Flatpak [anytime soon](https://issues.chromium.org/issues/40928753#comment5) for reasons alike to this. Flatpak *significantly* inhibits Chromium's sandboxing, and there is no faithful implementation currently.

##### Qt WebEngine

Browsers based on Qt WebEngine (for example [KDE’s Falkon](https://apps.kde.org/falkon/)) should generally be avoided. Qt WebEngine forks a specific Chromium version at feature freeze and then [cherry‑picks security fixes](https://www.qt.io/blog/putting-updates-of-chromium-in-qtwebengine-on-a-timeline) from newer upstream releases. That approach can leave a longer exposure window than browsers that track Chromium directly. Cherry‑picking is error‑prone and may miss fixes that rely on broader refactors or API changes, increasing the likelihood that patches are incomplete.

### Other Browsers

#### Firefox

Firefox is [inherently insecure](https://madaidans-insecurities.github.io/firefox-chromium.html). I can already see the responses to that source, "Last updated March 2022", "2/3 year old article", "Biased and outdated", but these are often said in a hand-wave manner with the hope that time has fixed the issues present in the article... it has not. Saying the article is old actually makes Firefox look *worse*, since it hasn't significantly improved in 3 years. To be fair, there has been improvement but not enough of it to make it comparible to Chromium based browsers (even from 3 years ago). This is especially true on Linux where the sandboxing is very poor, and Android where there is no website sandbox at all. The current Android implementation of the Firefox sandbox (Fission) is not enabled by default (except by [IronFox](https://gitlab.com/ironfox-oss/IronFox/-/blob/19a251e506afc775b34446a92c53c2b3e0548f5d/patches/preferences/phoenix-android.js#L1463)), even if it was enabled the implementation does not use Android's [isolatedProcess](https://developer.android.com/guide/topics/manifest/service-element#isolated) flag, which ensures that subprocesses are properly isolated and cannot trivially escalate privilege within the application. Equivalent to Android, Firefox does not have complete sandboxing in Flatpak, it doesn't even offer a compatibility layer alike to zypak, it just opts to cripple its own security (only recently have they begun offering a warning in environments without user namespaces that sandbox may be degraded, **but** this warning doesn't show up in the official and verified Flatpak for Firefox).

##### Firefox Forks

I don't think I need to go too much in depth, most FF forks are just regular Firefox with either UI changes or some changes to user-hostile defaults. They typically suffer from slower update cycles.
\
Although, I will talk about 2 desktop forks specifically, Librewolf and Pale Moon. Librewolf is just Firefox with defaults changed... nothing else. They don't even maintain the defaults, they just use [arkenfox-user.js](https://github.com/arkenfox/user.js/). They may have some deviated changes but fundamentally it is just arkenfox built into Firefox with a slower update cycle. Pale Moon uses *ancient* code with some security patches backported, and it is single-process so it cannot utilize any modern sandboxing technology (such as seccomp or namespaces, or the adjacents on other platforms). You can manually sandbox the browser but that doesn't isolate sites from each other. This also means that newer security features FF adds (as rare as that is) will not get properly added if they get added at all.

#### Safari (Webkit)

I don't use Apple devices, but security-wise, Safari/Webkit is pretty decent. It may be behind on web standards but it has strong partitioning, strong sandboxing, and robust mitigations on all supported platforms. Additionally, it can disable JIT JavaScript (and many other web features) on iOS and MacOS per-site using Lockdown Mode to be W^X compliant, though most websites will likely break.

##### Epiphany (WebkitGTK)

(I think) WebkitGTK is the official Webkit port to Linux. It shares many of the same features of regular Webkit, sans some stuff that are iOS/MacOS/Apple specific. It is the only browser to support proper sandboxing in Flatpak but said sandboxing is notably weaker than native (non-Flatpak, non-Snap) Chromium.

#### Android Webview Browsers

These browsers cannot offer site-isolation due to how Android WebView is designed, websites are only isolated from the system not each other. Typically they do not have strong partitioning and are very minimal in their feature set.

### Popular Security-Centric Options

This section is dedicated to a few options people often recommend explicitly for security reasons, but the options themselves are rather niche. For example, Brave is *not* a security option but it is a very popular recommendation for "security" but it is not itself a security focused browser. Same follows for other projects claiming the same thing, such as Librewolf. This section has projects that actually *try* to improve browser security.

#### Vanadium

This is the GrapheneOS default browser. I feel I don't need to explain why it is one of, if not the best option currently for privsec. Very few browsers are as comprehensive with their hardening or as consistent with their update cycle. Unfortunately, the browser is only available on GrapheneOS so most may not be able to use it. An Android-wide release is planned but the expected release of that is unknown (at least to me).

#### Cromite

Cromite is [not a security-focused browser](https://discuss.grapheneos.org/d/16562-browser-mulch-vs-cromite/10). Cromite has some problematic changes included which reduce privacy and security. For example, it includes the Eyeo filtering engine which has all the [issues of Brave's adblock-rs](#content-blocking) but is written in C++ (so memory unsafe), essentially increasing the attack surface massively. Additionally, Cromite [enables Manifest V2 Extensions](https://github.com/uazo/cromite/blob/6d6ce62db92b0a6b415c55e9b8fd861da13bfd6e/docs/FEATURES.md?plain=1#L165) in full, which adds a lot of additional attack surface over Chrome/Chromium. So they add a very risky adblocking engine to avoid extensions, but then enable MV2 likely for the purpose of content blocking, which results in adding a bunch of attack surface with only the benefit of one or the other. Cromite also used to enable [JPEG-XL](https://github.com/uazo/cromite/issues/351), which isn't a good sign for security since JXL adds a lot of attack surface. The patch to add it was removed but it isn't a good sign for security concern. With that said, the developer does seem very receptive and transparent to change for issues raised about Cromite, I didn't see much change in mindset before but it seems like security is a bigger concern than it used to be.
\
[Cromite also does not enable CFI on Android](https://github.com/uazo/cromite/issues/1537). It used to, but it caused issues.
\
Cromite from what I have seen is mostly feature redundant with Brave, not that Brave is a good option, but it has more to offer. Most of my criticisms about Brave equally apply here, some to greater degrees, some to lesser. Point is, this isn't any more a security-focused option compared to Brave, and Brave isn't a security-focused option.

#### Trivalent

Full disclosure, I am a frequent contributor to Trivalent. This wouldn't affect my opinion of it anyway, as it is currently. The explanation is below.
\
Essentially, this is Vanadium for desktop Linux, somewhat literally. Do note that despite getting as close as possible, it does not match to Vanadium currently due to poor security in the desktop Linux ecosystem and a lack of availability of hardware security features like MTE. Many patches from Vanadium that are not Android-specific are used. Not only that, it expands on many desktop and Linux-centric hardening. Additionally, due to a decent amount of automation work, weekly updates are often shipped same-day as upstream or the day after, at a very consistent pace.
\
Beyond that, I won't go too in depth because it will sound more like marketing than a "review"... which I guess these are now... so just know, it's good. Use.

#### IronFox

[See](#firefox) [here](#firefox-forks). Firefox based browsers, especially on Android, have terrible security. IronFox isn't exactly free of these issues. It does do some work to reduce some attack surface of base Firefox, but this is not significant or substantial enough to justify its use over any Chromium based browser. But, if you are for some unholy reason forced to use a Firefox based browser on Android, IronFox is your best bet, but still note it's nothing to depend on security-wise.

## Basic Setup

This is just preferences, so see [PREFERENCES.md](/configs/PREFERENCES.md). Everything else is covered by policies.

### Content Blocking

Content blocking is usually done one of 3 ways, Extensions, Native/Internal, and DNS/Network. Some are blatantly better than others.
\
\
For starters, extensions are always bad. Especially MV2 extensions, like uBlock Origin. Since MV2 extensions can access any site as well as a great many features without permission. MV3 prevents this, but it isn't too much better since many extensions just ask for access to all sites anyway to work properly, but at least it offers the user control. With that in mind uBOL (uBlock Origin Lite) in `Basic` mode is pretty good, since it has no access to sites while still being able to deliver decent content-blocking. It also allows granting access to specific sites, such as Youtube (yes it works), for better filtering if needed. Other extensions and uBOL global modes risk security and weaken site isolation.
\
\
Native/Interal can mean one of 2 (technically 3) things. One is using Chromium's internal subresource filter (as done by [Vanadium](https://github.com/GrapheneOS/Vanadium) and [Trivalent](https://github.com/secureblue/trivalent-subresource-filter)), this is approx on-par with uBOL in `Basic` mode in terms of filtering capabilities. This is also the most secure since it is already built directly into Chromium so no extra capabilities, features, or code is added or enabled. The second option is to integrate a third-party filtering engine, this is done by Brave, Vivaldi, Opera, Cromite, and many other browsers. This can vary between a new engine, like [Brave](https://github.com/brave/adblock-rust/), or integrating an extension, like [Cromite](https://github.com/uazo/cromite/blob/master/build/patches/Eyeo-Adblock-for-Cromite.patch). Both have more attack surface, but extension integration is much worse.
\
\
DNS/Network is arguably the most secure but the least effective (since it can only filter by domain, and not paths, e.g. all of `google.com` and not just `google.com/tracking`) of any method. With most content blocking you have to add trust in multiple entities and add extra attack surface. With DNS filtering, you are placing your trust in something you already have to trust (DNS resolution). I would still suggest the usage of some DNS filtering in your browser, even if you have another content-blocking solution. It also has no performance impact and can resist some forms of censorship and tracking by encrypting not only DNS traffic but also the Client Hello (via [ECH](https://wiki.mozilla.org/Security/Encrypted_Client_Hello)). Non-DNS network filtering has the same effectiveness with the added benefit of IP blocking, depending on the implementation. It should be noted that CNAME tracking can be fully mitigated through DNS filtering.
\
\
There is technically a sub-category of network filtering that is more comprehensive in its ability to filter, but it is a massive security risk. HTTPS interception filtering is a method where your content blocker will intercept your encrypted web traffic using its own certificate, this forces you to trust said content blocker with certificate handling and website data. This is not recommended, and you are better off just using DNS with/or a native blocking solution or extension.
\
\
Last note on remotely updated filters for systems like Brave, Opera, and uBlock Origin (MV2). The main problem here is that filters can still modify requests, run regex (which can be exploited in the browser engine), use cosmetic filters (which has been used to exfil data from sites in the past), and execute JavaScript via scriptlets. While scriptlets themselves aren't risky, even when limiting execution capabilities it is still arbitrary execution and therefore has massive risk. These filters are themselves arbitrary and unsigned, meaning you are OTA downloading random files that are an exploit away from reading the contents on all sites or worse. At least with MV3 extensions the filters have to bundled, so they are effectively signed along with the rest of the extension, so much better than most integrated engines.

## Policies

See [POLICIES.md](/configs/POLICIES.md) for what policies can be used and their respective values

### Linux

Policies on Linux can vary in location, typically browsers will have their own directories under which to place policy files.
\
Policies for vanilla Chromium, on most systems, will be located at `/etc/chromium/policies/managed/` for mandatory policies and `/etc/chromium/policies/recommended/` for recommended policies. Most policies must go in the managed directory, but some can go into recommended, these policies can be overridden in the user preferences. Policies that can be recommended will be labeled as such. Google Chrome policies will be located at `/etc/opt/chrome/policies/` with identical folders for mandatory and recommended policies.
\
The structure of Linux policy files is standard `json` with each policy represented as a string and its associated value. See below (this is just an example policy, it will not do anything):
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

There is no one answer, most Linux distibutions offer a way to persist flags for their build of Chromium, and sometimes even offer a way to persist for Google Chrome as well.
\
For example, Arch notably offers a [flag persistence method](https://wiki.archlinux.org/title/Chromium#Configuration) for both Chromium and Chrome. Fedora also offers a method via `/etc/chromium/chromium.conf`. Most other common distros like Ubuntu, Debian, Gentoo, Nix, etc. also offer methods that are either specific or similar.
\
Research into your specific distro and find out how it handles flag persistence. It can sometimes help to just search around `/etc` for a Chromium directory or set of Chromium files.

### Windows

Out of the box, there is really no easy way to persist flags in a way to guarentee that they will be used... but, with some reg hacking and a launch script it is possible (thanks to chrlauncher).
\
Using another project of mine, [chromewrapper](https://github.com/RKNF404/chromewrapper), you can persist flags, specifically for Google Chrome, but it should be trivially adjustable to any Chromium-based browser.
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
Lets start with OSs. I have an Android, Linux, and Windows machines. They are GrapheneOS, Fedora Workstation, and Windows 11 respectively. Because of this, your setup may vary. Also yes, I will swap to secureblue eventually, it is on the agenda for me.
\
\
On GrapheneOS, I use Vanadium. It is without a doubt the best option on Android, but due to a lack of availability outside of GrapheneOS, it is difficult to recommend. Therefore, the next best option I would use is Chrome. Yes, Chrome with some settings changed and some flags altered in `chrome://flags`. Is this ideal? Not really, but it's the next best thing below Vanadium. For watching Youtube without ads, I use NewPipe, so adblocking isn't a big enough deal for my browsing to justify selecting a browser based around it. *Not-so-subtle suggestion against Brave.*
\
\
On Fedora, I use Trivalent, secureblue's default browser. It is sort of a port of Vanadium to desktop Linux, as it comes with a lot of neat defaults and hardening. For RPM based distros, it is definitely the best option. Due to Trivalent's defaults, it requires no usage of this guide or its configs. Otherwise, say on a Debian-based distro, I would use Chrome with the application of this guide. It's the closest you can get to Trivalent/Vanadium.
\
\
On Windows 11, I use Chrome. 90% of the time, Chrome is the best option, obviously with the application of [this guide](#windows-1) (including chromewrapper). I don't consider any other options to be better than Chrome. Edge is a decent contender, although I would not use it mainly because it is way more intregrated with MS services than Chrome is with Google services, some of those services cannot be turned off (or require Windows Enterprise to be turned off, like the Telemetry), and the update cycle is spotty (or it was when I used it). Some of these things may not be of concern for you, but they are for me, and the security benefits Edge offers is not too major when Chrome is configured properly (ideally the gap would be smaller if Chromium ***actually decided to maintain DrumBrake*** (the WebAssembly interpreter) ***properly***... but who knows when that will happen).
