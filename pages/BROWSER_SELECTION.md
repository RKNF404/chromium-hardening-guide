# Selecting a browser

## Contents

- [Baseline Criteria](#baseline-criteria)
- [Proprietary vs Open-Source](#proprietary-vs-open-source)
- [Resisting Fingerprinting](#resisting-fingerprinting) (WIP)
- [Popular Options](#popular-options)
  - [Chrome](#chrome)
  - [Edge](#Edge)
  - [Opera](#Opera)
  - [Brave](#Brave)
  - [Vivaldi](#Vivaldi)
  - [Vanilla Chromium](#vanilla-chromium)
    - [ungoogled-chromium](#ungoogled-chromium)
  - [Helium](#helium)
  - [Thorium](#thorium)
  - [Flatpak](#flatpak-linux) (Linux)
  - [QtWebEngine](#qtwebengine)
- [Other Browsers](#other-browsers)
  - [Firefox](#firefox)
    - [FF Flatpak](#ff-flatpak)
    - [Firefox Forks](#firefox-forks)
  - [Safari/Webkit](#safariwebkit)
    - [Epiphany/WebkitGTK](#epiphanywebkitgtk)
  - [Android Webview Browsers](#android-webview-browsers)
- [Popular Security-Centric Options](#popular-security-centric-options)
  - [Vanadium](#vanadium)
  - [Cromite](#cromite)
  - [Trivalent](#trivalent)
  - [IronFox](#ironfox)

## Baseline Criteria

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

## Proprietary vs Open-Source

Long story short, it makes no difference. Open-source is preferable for transparency reasons, but has little effect on anything in the baseline criteria. Consider the option more like a tie-breaker than a genuine advantage to consider.

## Resisting Fingerprinting

Browser fingerprinting can be best summarized as websites identifying a browser using a collection of metrics which could individually identify two browsers from each other. A common example is graphical rendering APIs, such as Canvas and WebGL, these can vary based on a system's graphics card, the graphics driver, the system's processor, the display used, etc. This alone allows for an unimaginable amount of combinations that all cause a unique "fingerprint", due to how each one varies slightly. Mind you, this is one metric, there are several, some more revealing and some less.
\
Resisting fingerprinting usually is done one of two ways: randomization and unified crowd blending. Randomizing is the most common and simple technique, basically it adds noise or fake data to exisiting metrics to make them different across visits and sessions. Ideally, this fully evades fingerprinting, since you will look different to every site. Typically it is generated per-load, meaning if you visit a webpage, then reload the webpage, the fingerprint will be slightly different. Brave offers a slightly different approach by offering a per-site per-session fingerprint, this is done by binding the randomized metrics to a site's randomized session key. This will cause each site to have one static fingerprint for the session, but each site will have a different random fingerprint.
\
The other approach is unified crowd blending (idk if this is an official term or anything and I'm too lazy to search it up), this is often done in tandem with randomization to mask metrics that may be unique. Basically, the goal is to get all users to look as similar as possible. The most popular approach would be Apple's Safari. Since Apple has good control their hardware production, and Safari basically only runs on their hardware, then most of the metrics that depend on unique hardware combinations are basically identical. This gives the impression that most Safari users are potentially the same user. To my knowledge, Safari doesn't really use randomization and it doesn't really need to.

Quick Summary:
- Nice to have, not a priority
- Should not be focal point of the selection process
- Generally very ineffective, even something more comprehensive like Brave is very flawed
- If you absolutely need it, use a VM and use Tor Browser, do not use Tor outside a VM

## Popular Options

### Chrome

This is the baseline/standard, everything else must either match or beat this to be considered. This guide assumes the usage of Chrome in certain sections, since it is the most general and most common. Chrome has the fastest update cycle and is the most functional/well tested. It is constantly improving and even if it has weak defaults, it is trivial to improve many of them. If you don't know what option to pick, use Chrome.
\
The only downside is that Chrome is proprietary. This has no effect on security nor significant effect on privacy, it is essentially vanilla Chromium with a few proprietary additions and licenced libraries. Most of the intrusive stuff is disabled by following this guide.

### Edge

A very highly regarded option, Edge makes decent security improvements on-top of Chrome, especially on Windows. Such as their Enhanced Security Mode, previously [Super Duper Secure Mode](https://microsoftedge.github.io/edgevr/posts/Super-Duper-Secure-Mode/), the use of the Code Integrity Guard (CIG) mitigation on the main browser process (since it prevents non-MS signed binaries from being executed, Edge is the only browser that can fully enable it), and the default use of AppContainer sandboxing for renderer processes on Windows. On Linux, it also offers a feature to enforce memory W^X on renderers with JIT disabled (last I checked this enforcement was disabled by default, but it can be enabled through `edge://flags`), which is currently only offered by Edge and [Trivalent](https://github.com/secureblue/Trivalent/blob/live/vanadium_patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch) (courtesy of [Vanadium](https://github.com/GrapheneOS/Vanadium/blob/main/patches/0188-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch)).
\
The main issue with Edge is telemetry, it is *mandatory* without Windows Enterprise/Educational editions. This makes it a non-contender for privacy but decent for security. It's update cycle can occasionally be spotty, skipping release every now-and-again. Overall, it's about equal to Chrome.
\
This guide does not cover hardening Edge but other such guides exist, such as [Tommy Tran's Edge policies](https://github.com/TommyTran732/Microsoft-Edge-Policies) for Linux and MacOS or [Topaz's Equivalent](https://github.com/topaz8/windows-edge-policies) for Windows.

### Opera

Avoid. It has mandatory telemetry, a poor update cycle, and tons of feature bloat. It has very few if any advantages over Chrome. It does have a decent content-blocker, but I'm not certain if it has decent security (more on this later). Overall, not a great option.

### Brave

Not terrible, but a weak option. Most of this browser is either matching vanilla Chromium, a degredation, or modifies a default. For example, they enable MV2 support when that format is actively being deprecated in Chromium. MV2 is awful for security, since it allows unrestricted access to all websites and all features to extensions. MV3, while not perfect, fixes many of these issues. In general, extensions are bad for security, but enabling MV2 is a step backwards. It should be noted that Brave only enables MV2 for [4 extensions](https://brave.com/blog/brave-shields-manifest-v3/), but this doesn't solve anything. The issue isn't that any extension can be MV2, it's the use of MV2 extensions themselves. See the [content blocking](#content-blocking) section why MV2 is specifically an issue. Whitelisting these extensions doesn't solve the issues with MV2 and only puts more users at risk, especially since they whitelist uMatrix (they admit it in their own blog post), which is no longer maintained.
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

### Vivaldi

***Horrific*** update cycle. It is proprietary, which isn't the worst, but it is difficult to analyze how good it really is, build-wise. Though they do publish gapped [source code](https://vivaldi.com/source) (meaning some parts of the code are missing, for reference vanilla Chromium is around 3.5-4 gigs when compressed, Vivaldi is around 2 if I recall correctly). It makes little improvements on Chrome, it does allow you to disable some intrusive integrations and has a content-blocker, but these are minor additions. It also has ***massive*** feature bloat. Again, mandatory telemetry which is surprisingly common.

### Vanilla Chromium

This depends heavily, but usually these are just open-source variants of Chrome with worse update-cycles. As mentioned in the [baseline](#baseline) section, some have terrible building standards, like disabling CFI or unbundling everything under the sun. Some variants (used to) go further by disabling the default memory allocator (PartitionAlloc), Debian for example used to use tcmalloc which is borderline a zero-security allocator built for performance. Replacing the allocator was deprecated in Chromium for security reasons so no variants offer that anymore. Some builds lack CFI (this has been improving recently it seems), Fedora linux  and many simple distros like [Arch](https://gitlab.archlinux.org/archlinux/packaging/packages/chromium/-/blob/cd8f1d1e907b39dd2f1f494febba26d535f9b18a/PKGBUILD#L168) keep it enabled. Research your specific distro, see what they do, how much do they bundle/unbundle.

#### ungoogled-chromium

[Bad](https://qua3k.github.io/ungoogled/). The update cycle is inconsistent at best, slow at worst. It disables the component updater which Chromium depends on for security reasons, since many features such as CRLSets (used for certificate revocation) are updated as a component. The privacy isn't terrible, in the sense that no data can be collected, but the substantial security risk it offers is a massive negative.
\
It suffers the issues of typical vanilla builds, but with the added issues of ungoogled-chromium itself. For example, usage of [tcmalloc in the past](https://github.com/ungoogled-software/ungoogled-chromium-debian/commit/9f7246d1c29d58cd467c540d580ab15bcc9e8b88).

### Helium

[Helium](https://helium.computer/) is a browser based on UGC (ungoogled-chromium). It makes use of patches from many sources, including its own. Most of the patches are usability focused, such as [bangs support](https://github.com/imputnet/helium/blob/main/patches/helium/core/add-native-bangs.patch) and a custom service that acts as a provider for various things throughout the browser (that can be self-hosted). The most notable issue though is the preloading of an extension, uBlock Origin. Some may consider this positive, but [it is not](#content-blocking). This a decently large source of fingerprinting and attack surface, even if it were uBlock Origin Lite (uBO MV3 variant), this is still not a good idea. Extensions should be avoided where possible, and baking them in is an anti-feature, even if they provide useful functionality. Despite it being based on UGC, Helium's services feature provides a proxy for performing component updates, which is very nice but is also only a fix for an issue in UGC, it isn't an actual improvement over Chromium.
\
Additionally, the developers do seem to have strong security focus on not regressing existing features within the browser. Such is the case with [Flatpak support](https://github.com/imputnet/helium-linux/issues/46#issuecomment-3735501507) for Helium devs seem disliken to the fact that Flatpak regresses browser sandboxes, big respect.
\
On that note, I am unsure if this browser is worth using over Chrome, or even Brave, for security. It does not really do much to improve on the security of Chromium, most patches are focused on usability and de-regessing the security of UGC. It is sitting in the same spot as Brave, where it has some nice features but most of what it does is adjacent to Chrome or a security regression in some way. I cannot recommend it currently. The update cycle looks to be a few days past upstream releases, which is fine and matches what most major non-rolling Linux distros can do, if not better.

### Thorium

[The update cycle](https://github.com/Alex313031/thorium/releases) is giving me a panic attack. They used to release once every few months (alike to how Vivaldi releases) and were still usually a few releases behind. Just recently they switched to the LTS branch of Chromium, which isn't ideal. Security fixes are pushed out weekly, the LTS branch updates features twice a year but still updates in between for security patches. I don't know how this will be handled, but I don't believe the minor version bumps will be handled by Thorium which is a concern. Cannot recommend for any reasonable level of security concern,

### Flatpak (Linux)

As mentioned in the [Brave](#brave) section, ***avoid***! Flatpak's security is... questionable for a number of reasons, but what's worse is Chromium's security in Flatpak. Because Flatpak restricts the usage of Linux namespaces and prevents the use of SUID (for good reason), Chromium's sandbox will literally not work. The solution is [zypak](https://github.com/refi64/zypak) or a [direct patch](https://github.com/flathub/org.chromium.Chromium/blob/master/patches/chromium/flatpak-Add-initial-sandbox-support.patch), the problem is these methods are very poorly configured to the point they essentially break the typically very strong sandboxing that Chromium provides. These solutions are closer to compatibility layers than they are genuine [security solutions](https://issues.chromium.org/issues/40753165#comment11). Upstream (Chromium devs) have expressed they do no intend to support Flatpak [anytime soon](https://issues.chromium.org/issues/40928753#comment5) for reasons alike to this. Flatpak *significantly* inhibits Chromium's sandboxing, and there is no faithful implementation currently.

### QtWebEngine

Browsers based on QtWebEngine (for example [KDE’s Falkon](https://apps.kde.org/falkon/)) should generally be avoided. QtWebEngine forks a specific Chromium version at feature freeze and then [cherry‑picks security fixes](https://www.qt.io/blog/putting-updates-of-chromium-in-qtwebengine-on-a-timeline) from newer upstream releases. That approach can leave a longer exposure window than browsers that track Chromium directly. Cherry‑picking is error‑prone and may miss fixes that rely on broader refactors or API changes, increasing the likelihood that patches are incomplete.

## Other Browsers

Anything *not* directly based on Chromium.

### Firefox

Firefox is [inherently insecure](https://madaidans-insecurities.github.io/firefox-chromium.html). I can already see the responses to that source, "Last updated March 2022", "2/3 year old article", "Biased and outdated", but these are often said in a hand-wave manner with the hope that time has fixed the issues present in the article... it has not. Saying the article is old actually makes Firefox look *worse*, since it hasn't significantly improved in 3 years. To be fair, there has been improvement but not enough of it to make it comparible to Chromium based browsers (even from 3 years ago). This is especially true on Linux where the sandboxing is very poor, and Android where there is no website sandbox at all. The current Android implementation of the Firefox sandbox (Fission) is not enabled by default (except by [IronFox](https://gitlab.com/ironfox-oss/IronFox/-/blob/19a251e506afc775b34446a92c53c2b3e0548f5d/patches/preferences/phoenix-android.js#L1463)), even if it was enabled the implementation does not use Android's [isolatedProcess](https://developer.android.com/guide/topics/manifest/service-element#isolated) flag, which ensures that subprocesses are properly isolated and cannot trivially escalate privilege within the application. Equivalent to Android, Firefox does not have complete sandboxing in Flatpak, it doesn't even offer a compatibility layer alike to zypak, it just opts to cripple its own security (only recently have they begun offering a warning in environments without user namespaces that sandbox may be degraded, **but** this warning doesn't show up in the official and verified Flatpak for Firefox).

#### FF Flatpak

Despite Firefox's poor security, the browser does have some form of sandboxing, which is critical to what little security it has. Above there is a section about how Flatpak interferes with the Chromium sandboxing architecture. Well, the same is true for Firefox, FF depends on userns for a portion of its sandboxing. The question is how does Firefox account for a lack of usernamespaces? Simple. It doesn't. Firefox just... pretends they don't exist, but only in Flatpak. They did add a warning about a lack of userns access for environments without userns and that sandboxing and security may suffer, but this warning is just disabled in the *official* Firefox Flatpak package. If you are really deadset on using Firefox then at the very least *avoid* the Flatpak. Just a general rule of thumb for all browsers really.

#### Firefox Forks

I don't think I need to go too much in depth, most FF forks are just regular Firefox with either UI changes or some changes to user-hostile defaults. They typically suffer from slower update cycles.
\
Although, I will talk about 2 desktop forks specifically, Librewolf and Pale Moon. Librewolf is just Firefox with defaults changed... nothing else. They don't even maintain the defaults, they just use [arkenfox-user.js](https://github.com/arkenfox/user.js/). They may have some deviated changes but fundamentally it is just arkenfox built into Firefox with a slower update cycle. Pale Moon uses *ancient* code with some security patches backported, and it is single-process so it cannot utilize any modern sandboxing technology (such as seccomp or namespaces, or the adjacents on other platforms). You can manually sandbox the browser but that doesn't isolate sites from each other. This also means that newer security features FF adds (as rare as that is) will not get properly added if they get added at all.

### Safari/Webkit

I don't use Apple devices, but security-wise, Safari/Webkit is pretty decent. It may be behind on web standards but it has strong partitioning, strong sandboxing, and robust mitigations on all supported platforms. Additionally, it can disable JIT JavaScript (and many other web features) on iOS and MacOS per-site using Lockdown Mode to be W^X compliant, though most websites will likely break.

#### Epiphany/WebkitGTK

(I believe) WebkitGTK is the official Webkit port to Linux. It shares many of the same features of regular Webkit, sans some stuff that are iOS/MacOS/Apple specific. It is the only browser to support proper sandboxing in Flatpak but said sandboxing is notably weaker than native (non-Flatpak, non-Snap) Chromium.

### Android Webview Browsers

These browsers cannot offer site-isolation due to how Android WebView is designed, websites are only isolated from the system not each other. Typically they do not have strong partitioning and are very minimal in their feature set.

## Popular Security-Centric Options

This section is dedicated to a few options people often recommend explicitly for security reasons, but the options themselves are rather niche. For example, Brave is *not* a security option but it is a very popular recommendation for "security" but it is not itself a security focused browser. Same follows for other projects claiming the same thing, such as Librewolf. This section has projects that actually *try* to improve browser security.

### Vanadium

This is the GrapheneOS default browser. I feel I don't need to explain why it is one of, if not the best option currently for privsec. Very few browsers are as comprehensive with their hardening or as consistent with their update cycle. Unfortunately, the browser is only available on GrapheneOS so most may not be able to use it. An Android-wide release is planned but the expected release of that is unknown (at least to me).

### Cromite

Cromite is [not a security-focused browser](https://discuss.grapheneos.org/d/16562-browser-mulch-vs-cromite/10). Cromite has some problematic changes included which reduce privacy and security. For example, it includes the Eyeo filtering engine which has all the [issues of Brave's adblock-rs](#content-blocking) but is written in C++ (so memory unsafe), essentially increasing the attack surface massively. Additionally, Cromite [enables Manifest V2 Extensions](https://github.com/uazo/cromite/blob/6d6ce62db92b0a6b415c55e9b8fd861da13bfd6e/docs/FEATURES.md?plain=1#L165) in full, which adds a lot of additional attack surface over Chrome/Chromium. So they add a very risky adblocking engine to avoid extensions, but then enable MV2 likely for the purpose of content blocking, which results in adding a bunch of attack surface with only the benefit of one or the other. With that said, the developer does seem very receptive and transparent to change for issues raised about Cromite.
\
[Cromite also does not enable CFI on Android](https://github.com/uazo/cromite/issues/1537). It used to, but it caused issues.
\
Cromite, from what I have seen, is in the same spot as Brave. It doesn't improve that much on-top of Chromium security-wise, mostly just a vague privacy and freedom promiting way. It has many of the same flaws as Brave and not as many of the same benefits. I wouldn't call the browser security-focused currently, nor do I see a reason to use it for improved security over something like Chrome or a decent Chromium build.

### Trivalent

Full disclosure, I am a frequent contributor to Trivalent. This wouldn't affect my opinion of it anyway, as it is currently. The explanation is below.
\
Essentially, this is Vanadium for desktop Linux, somewhat literally. Do note that despite getting as close as possible, it does not match to Vanadium currently due to poor security in the desktop Linux ecosystem and a lack of availability of hardware security features like MTE. Many patches from Vanadium that are not Android-specific are used. Not only that, it expands on many desktop and Linux-centric hardening. Additionally, due to a decent amount of automation work, weekly updates are often shipped same-day as upstream or the day after, at a very consistent pace.
\
Beyond that, I won't go too in depth because it will sound more like marketing than a "review"... which I guess these are now... so just know, it's good. Use.

### IronFox

[See](#firefox) [here](#firefox-forks). Firefox based browsers, especially on Android, have terrible security. IronFox isn't exactly free of these issues. It does do some work to reduce some attack surface of base Firefox, but this is not significant or substantial enough to justify its use over any Chromium based browser. But, if you are for some unholy reason forced to use a Firefox based browser on Android, IronFox is your best bet, but still note it's nothing to depend on security-wise.
