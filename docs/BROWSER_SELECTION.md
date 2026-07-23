---
icon: "lucide/globe-lock"
---

# :lucide-globe-lock: Selecting a Browser

!!! tip "Summary"
    - **:material-microsoft: Windows** — Google Chrome
    - **:material-apple: MacOS** — Google Chrome
    - **:material-android: Android** — Google Chrome or Brave, depending on need, since you cannot configure policies for flags for Chrome so you can miss some decent improvements that Brave does offer (such as JITless V8 mode), but Brave has more attack surface and a worse update cycle. Brave also comes with an adblocker.
        - **:simple-grapheneos: GrapheneOS** — Vanadium
    - **:material-apple: iOS** — Safari
    - **:material-linux: Linux** — Google Chrome or Brave Origin
        - **:material-fedora: Fedora-based** — [Trivalent](https://github.com/secureblue/Trivalent)
        - **:material-arch: Arch Linux** — [official repository's packaging of Chromium](https://archlinux.org/packages/extra/x86_64/chromium/)
        - **:material-nix: NixOS** — [Nixpkgs Chromium package](https://github.com/NixOS/nixpkgs/tree/master/pkgs/applications/networking/browsers/chromium)

## :lucide-arrow-down-to-line: Baseline Criteria

The most important security detail of a browser is 100% update cycle. Everything else security-wise is useless if the browser is updated only once every few months. Vulnerabilities pile up, and the longer they go unpatched, the worse it gets. For reference, Chromium/Chrome is usually updated weekly or biweekly excluding holidays. Each update usually has at least one high-severity vulnerability, or at least a few medium/low. 2 months without updates essentially results in 6+ high severity vulnerabilities, plus the other severity vulnerabilities. No amount of hardening will compensate for that.

The next most important element is build quality, i.e. `does it offer at least Chromium's default or higher?` Most often this is control-flow integrity (CFI), it is an upstream default in Chromium on Linux yet for some reason many forks or Linux distros [explicitly disable it](https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/rules?ref_type=heads#L104). CFI is not common outside of desktop Linux and ChromeOS (for Chromium that is), though there are some exceptions such as [Vanadium on Android](https://github.com/GrapheneOS/Vanadium/blob/main/args.gn#L30). Windows Chromium uses the platform's Control Flow Guard (CFG) mitigation, most Chromium based browsers have this enabled by default. On Linux, many distributions opt to dynamically link as many dependencies as possible to system libraries, mainly for package size and updateability. This is a security regression, since system shared libraries cannot provide CFI protections without [Cross-DSO-CFI](https://clang.llvm.org/docs/ControlFlowIntegrity.html#shared-library-support) which is not used in Chromium. The more bundled, the better. I'm not aware if this issue is present on other operating systems.

The last aspect is additional features on top of vanilla Chromium and more secure/private defaults. This also includes the ability to control insecure or non-private features such as telemetry, WebAssembly, etc. This isn't that important and can be optionally ignored, but it is something to be aware of.

**TL;DR:** If the variant does something worse than Chrome, avoid it. The only leeway is on update cycle, it is physically impossible to beat Chrome's releases. Anything within 2-3 days is acceptable, but the sooner the better. Less resourced projects have more leeway in this regard, as it is unreasonable to expect that level of speed from them. If the variant does something better for security/privacy, that is a reason to use it, but it shouldn't overshadow downsides.

## :lucide-lock: Proprietary vs. Open-Source

Long story short, it makes no difference. Open-source is preferable for transparency reasons, but has little effect on anything in the baseline criteria. Consider the option more like a tie-breaker than a genuine advantage to consider.

## :lucide-fingerprint-pattern: Resisting Fingerprinting

Browser fingerprinting can be best summarized as websites identifying a browser using a collection of metrics which could individually identify two browsers from each other. A common example is graphical rendering APIs, such as Canvas and WebGL, these can vary based on a system's graphics card, the graphics driver, the system's processor, the display used, etc. This alone allows for an unimaginable amount of combinations that all cause a unique "fingerprint", due to how each one varies slightly. Mind you, this is one metric, there are several, some more revealing and some less.

Resisting fingerprinting usually is done one of two ways: randomization and unified crowd blending. Randomizing is the most common and simple technique, basically it adds noise or fake data to existing metrics to make them different across visits and sessions. Ideally, this fully evades fingerprinting, since you will look different to every site. Typically it is generated per-load, meaning if you visit a webpage, then reload the webpage, the fingerprint will be slightly different. Brave offers a slightly different approach by offering a per-site per-session fingerprint, this is done by binding the randomized metrics to a site's randomized session key. This will cause each site to have one static fingerprint for the session, but each site will have a different random fingerprint.

The other approach is unified crowd blending (unofficial term I'm using for convenience). This is often done in tandem with randomization to mask metrics that may be unique (such as Canvas rendering). Basically, the goal is to get all users to look as similar as possible. The most popular approach would be Apple's Safari. Since Apple has good control over their hardware production, and Safari basically only runs on their hardware, then most of the metrics that depend on unique hardware combinations are basically identical. This gives the impression that most Safari users are potentially the same user. To my knowledge, Safari doesn't really use randomization and it doesn't really need to.

The issue with most anti-fingerprinting attempts is they rarely achieve either of these approaches very effectively. Firefox is often cited as a more privacy-friendly choice over Chrome, partly due to some fingerprinting resistance. The resistance Firefox offers is [actually very weak](https://wiki.mozilla.org/Fingerprinting), even when configured to be as strong as possible. Firefox does not really unify its userbase's metrics, and the randomization it does offer is limited to basically just Canvas when Resist FingerPrinting or FingerPrinting Protections are on. There is also another major issue with toggling on these protections, the number of users doing the same.

This is one of the biggest issues with fingerprinting protection configurations of common browsers, they often create small userbases that look somewhat-similar to each other but are drastically different from 99% of the browser userbase. An example metaphor: you can wear a mask in a crowd, and yes no one can see your face, but you're the only one wearing a mask in a crowd. There is a similar problem for more comprehensive solutions, like Brave and Mullvad Browser. They do offer a somewhat decent anti-fingerprinting solutions out of the box, but they also encourage customization (Mullvad via extensions, and Brave through Shields, flags, or the various bloat and crypto features), which in turn makes you unique.

The point with this section is to say, anti-fingerprinting takes a lot of consideration to actually be useful. Most of the time, the protections are transparent and do very little, and often times prioritizing them results in a loss of tangible security and privacy. This is not about "threat modelling", it is about what is actually helping you vs what you think is helping you. Your "threat model" is not an excuse to use a less secure product for a protection you don't need or are using incorrectly.

If you want a simple solution, use Tor Browser in a virtual machine. It provides the most comprehensive solution available, and compensates for the [limited security](#tor-browser-tor-browser) of Tor Browser by isolating it from your main system in a virtual machine. Anything else is most likely either incomplete or insecure.

### :lucide-arrow-left-right: Using Multiple Browsers

This is a very outdated and ineffective practice. The core idea stems from having two browsers separates your online persona into two profiles which is *supposed* to isolate your fingerprint.

This is essentially privacy theatre. In reality, using different browsers doesn't solve this issue. It just doubles the required trust on your device and increases attack surface, especially if you are mixing different browser engines (e.g. Firefox and Chromium) or browsers with significantly different update cycles. You can still be fingerprinted across browsers. Yes, it is harder to do that, but it is still feasible and more likely you will accidentally associate yourself across browsers. If you need the fingerprinting resistance, use Tor with your other main browser, otherwise you aren't really achieving anything other than increasing attack surface.

A significantly better approach is using your browser's built-in profile management system and creating a second profile, this keeps just one browser and achieves effectively the same thing. Does it resist fingerprinting? Not really, but it does isolate data and reduce browsing data overlap between personas, if that is what you are aiming to do.

---

<!-- by the way, "its" is not a typo. -->

!!! warning
    This guide will link to each browser's website so you can learn more about it. Browser marketing pages are not representative of the actual browser or what advanced configurations are available under the hood. You should do your own research instead of taking browser websites at face value. A browser may actually be better or worse than the contents of its website.

**Browsers with a :lucide-scroll-text: have policies which expose additional options. See [Manual Configuration](MANUAL_CONFIG.md) for where these policies should go.**

## :lucide-star: Popular Options

### :material-google-chrome: {{ b("Google Chrome", "https://www.google.com/chrome/", "chrome") }}

This is the baseline/standard, other browsers must either match or beat Chrome to be considered a decent option. The guide assumes the usage of Chrome in certain sections, since it is the most common browser and the best browser option in most cases. Chrome has the fastest update cycle and is one of the most functional/well tested browsers out there. It is constantly improving and even if it has weak defaults, it is trivial to improve many of them. If you don't know what option to pick, use Chrome.

The only downside is that Chrome is proprietary. This has no effect on security nor significant effect on privacy, it is essentially vanilla Chromium with a few proprietary additions and licensed libraries. Most of the intrusive stuff is disabled by following this guide.

### :material-microsoft-edge: {{ b("Microsoft Edge", "https://explore.microsoft.com/en-us/edge", "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies" )}}

A very highly regarded option, Edge makes decent security improvements on-top of Chrome, especially on Windows. Such as their Enhanced Security Mode, previously [Super Duper Secure Mode](https://microsoftedge.github.io/edgevr/posts/Super-Duper-Secure-Mode/), the use of the Code Integrity Guard (CIG) mitigation on the main browser process (since it prevents non-MS signed binaries from being executed, Edge is the only browser that can fully enable it), and the default use of AppContainer sandboxing for renderer processes on Windows. On Linux, it also offers a feature to enforce memory W^X on renderers with JIT disabled (last I checked this enforcement was disabled by default, but it can be enabled through `edge://flags`), which is currently only offered by Edge and [Trivalent](https://github.com/secureblue/Trivalent/blob/8b0a3cb6666df76e6bdd421fbb547bcb399c4f59/vanadium_patches/0173-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch) (courtesy of [Vanadium](https://github.com/GrapheneOS/Vanadium/blob/83d42785c127719cc52d00014bb8853f4ad18900/patches/0173-Restriction-of-dynamic-code-execution-via-seccomp-bp.patch)).

The main issue with Edge is telemetry, it is *mandatory* without Windows Enterprise/Educational editions. This makes it a non-contender for privacy outside of those OS configurations, but decent for security. It's update cycle can occasionally be spotty, skipping release every now-and-again. Overall, it's about equal to Chrome. Recently though, Edge seems rather [negligent of security issues](https://www.forbes.com/sites/daveywinder/2026/05/19/microsoft-does-u-turn-on-edge-by-design-password-vulnerability/), in this case they openly disregarded the issue and went back to fix it after criticism. Edge used to be recommended beside Chrome in this guide, but due to their described behavior it is difficult to recommend them.

This guide does not cover hardening Edge but other such guides exist, such as [Tommy Tran's Edge policies](https://github.com/TommyTran732/Microsoft-Edge-Policies) for Linux and macOS or [Topaz's Equivalent](https://github.com/topaz8/windows-edge-policies) for Windows.

### :material-opera: {{ b("Opera", "https://www.opera.com", "chrome")}}

Avoid. It has mandatory telemetry, a poor update cycle, and tons of feature bloat. It has very few if any advantages over Chrome. It does have a decent content blocker, but I'm not certain if it has decent security (more on this later). Overall, not a great option.

### :fontawesome-brands-brave: {{ b("Brave", "https://brave.com", "https://support.brave.app/hc/en-us/articles/360039248271-Group-Policy" )}}

Not terrible, but a weak option. Most of this browser is either matching vanilla Chromium, a degradation, or modifies a default. For example, they enable MV2 support when that format is actively being deprecated in Chromium. MV2 is awful for security, since it allows unrestricted access to all websites and all features to extensions. MV3, while not perfect, fixes many of these issues. In general, extensions are bad for security, but enabling MV2 is a step backwards. It should be noted that Brave only enables MV2 for [4 extensions](https://brave.com/blog/brave-shields-manifest-v3/), but this doesn't solve anything. The issue isn't that any extension can be MV2, it's the use of MV2 extensions themselves. See the [content blocking](index.md#content-blocking) section why MV2 is specifically an issue. Whitelisting these extensions doesn't solve the issues with MV2 and only puts more users at risk, especially since they whitelist uMatrix (they admit it in their own blog post), which is no longer maintained.

They also verified their Flathub app. See the [Flatpak](#flatpak-flatpak-linux) section as to why that is a problem. The issue is not that Brave is packaged as a Flatpak, many Chromium browsers are, but they officially endorse it, which is a flagrant disregard for security. They do recommend against using the Flatpak [on their website](https://brave.com/linux/#flatpak), but this notice isn't present in the Flathub description nor do they give a notice after installing it, so most users will not see it. It wouldn't be surprising if most Brave Flatpak users were unaware of Brave's official stance on this. At the very least, if it were not verified, it would push more cautious users away to not use unofficial packages.

Also, there is lots of attack surface related to crypto stuff and heavy privacy marketing (despite being rather intrusive by default), and rather ineffective fingerprinting resistance (has gaps making the mitigations bypassable). The company itself is also questionable in its practices, but that is for you to decide.

In the realm of attack surface, the content blocker can be a problem. It is written in Rust and all, but Rust only prevents exploits targeting the adblock engine itself, not the browser or sites. See the [content blocking](index.md#content-blocking) section for more details.

To give some credit where it is due, Brave does have some decent changes. For example they proxy [a large number of requests](https://github.com/brave/brave-browser/wiki/Deviations-from-Chromium-(features-we-disable-or-remove)#services-we-proxy-through-brave-servers), for which they have a better privacy policy on their services than Google. This does have some issues but it is still nice nonetheless. They do also offer some partitioning improvements, though the amount of which isn't too big since upstream has added a lot of said improvements themselves.

Overall, on desktop, Brave is rather useless. It is filled with bloat and any security or privacy advantages, even the adblocker, can be achieved with Chrome. However, on Android, if you do not have access to Vanadium, then Brave is probably the next best choice. Chrome on Android isn't bad, but Brave offers more in terms of configurability and the bloat is way less noticeable and easier to turn off. Brave also offers "JITless V8 mode" via a flag which basically makes the "JavaScript Security & Performance" permission actually control JIT, and not just disable higher-tier optimizing compilers as is the case with traditional Chromium, this can put it slightly ahead of Chrome if this mode is used.

Another note, Brave does have decently private and end-to-end encrypted browser data sync. This is rare among Chromium browsers (sadly), so if you need sync then Brave would be a fine option.

While the guide does not cover hardening Brave, other such configurations/"debloaters" exist. One such debloater is [this one](https://github.com/Anxarden/brave-debloater), the default DNS server choice isn't my favorite but it can be changed if desired. It only officially supports Windows and Linux, to use this on Mac you would need to manually convert the policies to [MacOS compliant ones](MANUAL_CONFIG.md#macos).

#### :fontawesome-brands-brave-reverse: {{ b("Brave Origin", "https://brave.com/origin", "https://support.brave.app/hc/en-us/articles/360039248271-Group-Policy") }}

This is basically Brave, but preconfigured with all the stuff people usually disable disabled out of the box. For example, telemetry, Brave wallet, the crypto networking stuff, and advertising are all removed. On paper, great idea. The issue is it costs $60 USD, this gives you a limited number of installs (re-installs included). I cannot recommend anyone spend money on any browser, let alone this one. That said, the browser is 100% free on Linux, so it is a decent enough option there if Chrome is not cutting it for you.

## :lucide-star-half: Notable Options

Options that are frequently referenced and talked about but have very little market share.

### :simple-vivaldi: {{b("Vivaldi", "https://vivaldi.com", "chrome")}}

Vivaldi uses the extended stable channel and updates weekly, so they are keeping up with security updates. They used to have a horrific update cycle of once every several months, but this seems to have improved.

It is proprietary, which isn't the worst, but it is difficult to analyze how good it really is, build-wise. Though they do publish gapped [source code](https://vivaldi.com/source) (meaning some parts of the code are missing, for reference vanilla Chromium is around 3.5-4 gigs when compressed, Vivaldi is around 2 if I recall correctly). It makes little improvements on Chrome, it does allow you to disable some intrusive integrations and has a content-blocker, but these are minor additions. It also has ***massive*** feature bloat. Again, there is mandatory telemetry which is surprisingly common.

### :material-google-chrome: {{ b("Vanilla Chromium", "", "chrome") }}

This depends heavily, but usually these are just open-source variants of Chrome with worse update cycles. As mentioned in the [baseline](#baseline-criteria) section, some have terrible building standards, like disabling CFI or unbundling everything under the sun. Some variants (used to) go further by disabling the default memory allocator (PartitionAlloc), Debian for example used to use tcmalloc which is borderline a zero-security allocator built for performance. Replacing the allocator was deprecated in Chromium for security reasons so no variants offer that anymore. Some builds lack CFI (this has been improving recently it seems), Fedora Linux and many simple distros like [Arch](https://gitlab.archlinux.org/archlinux/packaging/packages/chromium/-/blob/cd8f1d1e907b39dd2f1f494febba26d535f9b18a/PKGBUILD#L168) keep it enabled. Research your specific distro's packaging, see what they do, how much do they bundle/unbundle.

#### :lucide-circle: {{b("ungoogled-chromium", "https://github.com/ungoogled-software/ungoogled-chromium", "chrome")}}

[Bad](https://qua3k.github.io/ungoogled/). The update cycle is inconsistent at best, slow at worst. It disables the component updater which Chromium depends on for security reasons, since many features such as CRLSets (used for certificate revocation) are updated as a component. The privacy isn't terrible, in the sense that no data can be collected, but the substantial security risk it offers is a massive negative.

It suffers the issues of typical vanilla builds, but with the added issues of ungoogled-chromium itself. For example, usage of [tcmalloc in the past](https://github.com/ungoogled-software/ungoogled-chromium-debian/commit/9f7246d1c29d58cd467c540d580ab15bcc9e8b88).

### :lucide-puzzle: {{ b("Cromite", "https://github.com/uazo/cromite", "chrome") }}

Cromite is [not a security-focused browser](https://discuss.grapheneos.org/d/16562-browser-mulch-vs-cromite/10). Cromite has some problematic changes included which reduce privacy and security. For example, it includes the Eyeo filtering engine which has all the [issues of Brave's adblock-rs](index.md#content-blocking) but is written in C++ (so memory unsafe), essentially increasing the attack surface massively. Additionally, Cromite [enables Manifest V2 Extensions](https://github.com/uazo/cromite/blob/6d6ce62db92b0a6b415c55e9b8fd861da13bfd6e/docs/FEATURES.md?plain=1#L165) in full, which adds a lot of additional attack surface over Chrome/Chromium. So they add a very risky adblocking engine to avoid extensions, but then enable MV2 likely for the purpose of content blocking, which results in adding a bunch of attack surface with only the benefit of one or the other. With that said, the developer does seem very receptive and transparent to change for issues raised about Cromite.

[Cromite also does not enable CFI on Android](https://github.com/uazo/cromite/issues/1537). It used to, but it caused issues.

Cromite, from what I have seen, is in the same spot as Brave. It doesn't improve that much on top of Chromium security-wise, mostly just a vague privacy and freedom promoting way. It has many of the same flaws as Brave and not as many of the same benefits. I wouldn't call the browser security-focused currently, nor do I see a reason to use it for improved security over something like Chrome or a decent Chromium build.

As of recently, [according to the developer](https://github.com/uazo/cromite/issues/2884#issuecomment-4388203683), Cromite's maintenance will be spotty until September of 2026. At the time of writing this, Cromite last updated on April 10th (for v147.0.7727.56 released on [April 7th](https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop.html)), on May 21st there are approximately 300 CVEs patched since the last target release. For now, until the situation improves, you should avoid using Cromite.

### :material-airballoon-outline: {{b("Helium", "https://helium.computer/", "chrome" )}}

[Helium](https://helium.computer/) is a browser based on UGC (ungoogled-chromium). It makes use of patches from many sources, including its own. Most of the patches are usability focused, such as [bangs support](https://github.com/imputnet/helium/blob/main/patches/helium/core/add-native-bangs.patch) and a custom service that acts as a provider for various things throughout the browser (that can be self hosted). The most notable issue though is the preloading of an extension, uBlock Origin. Some may consider this positive, but [it is not](index.md#content-blocking). This is a decently large source of fingerprinting and attack surface, even if it were uBlock Origin Lite (uBO MV3 variant), this is still not a good idea. Extensions should be avoided where possible, and baking them in is an anti-feature, even if they provide useful functionality. Despite it being based on UGC, Helium's services feature provides a proxy for performing component updates, which is very nice but is also only a fix for an issue in UGC, it isn't an actual improvement over Chromium.

Additionally, the developers do seem to have strong security focus on not regressing existing features within the browser. Such is the case with [Flatpak support](https://github.com/imputnet/helium-linux/issues/46#issuecomment-3735501507) where the Helium devs seem to dislike the fact that Flatpak regresses browser sandboxes, big respect.

On that note, I am unsure if this browser is worth using over Chrome, or even Brave, for security. It does not really do much to improve on the security of Chromium, most patches are focused on usability and de-regressing the security of UGC. It is sitting in the same spot as Brave, where it has some nice features but most of what it does is adjacent to Chrome or a security regression in some way. Currently, it is not an option that can be recommended. The update cycle looks to be a few days past upstream releases, which is fine and matches what most major non-rolling Linux distros can do, if not better.

### :material-speedometer: {{b("Thorium", "https://thorium.rocks/", "chrome")}}

[The update cycle](https://github.com/Alex313031/thorium/releases) is giving me a panic attack. They used to release once every few months (alike to how Vivaldi releases) and were still usually a few releases behind. Just recently they switched to the LTS branch of Chromium, which isn't ideal. Security fixes are pushed out weekly, the LTS branch updates features twice a year but still updates in between for security patches. Thorium since the start of 2026 has updated twice. In fact, Chromium's LTS branch has already promoted [from 138 to 144](https://chromereleases.googleblog.com/2026/04/long-term-support-lts-channel-for.html) since April of 2026, Thorium released the 144 beta on [Jun 8 of 2026](https://github.com/Alex313031/thorium/releases/tag/M144.0.7559.254), which is itself more of a notification and *not* a proper release. The developer doesn't seem to have the time to maintain it, so a new developer stepped in. This may improve the situation, but to be explicit, you should not use Thorium for any reason currently.

### :material-microsoft-windows: {{b("Supermium", "https://www.win32subsystem.live/supermium/", "chrome")}}

This is a browser mainly designed for legacy OSes, like Windows 7, that modern browsers no longer support. It is hard to comment on this without the expected "do not use Windows 7, update to something modern". That said, if you are forced to use an OS that Supermium does support a modern browser doesn't, for one reason or another, then it isn't the *worst* option.

It aims for updates within a week of upstream. This is pretty bad, CVEs should ideally be fixed within a few days. That said, it is hard to compare it to anything else that can still update on Win7. So by virtue of it being the only workable option, it's fine. In any other situation though, this browser should be strictly avoided.

### :simple-flatpak: Flatpak (Linux)

As mentioned in the [Brave](#brave) section, ***avoid***! Flatpak's security is... questionable for a number of reasons, but what's worse is Chromium's security in Flatpak. Because Flatpak restricts the usage of Linux namespaces and prevents the use of SUID (for good reason), Chromium's sandbox will literally not work. The solution is [zypak](https://github.com/refi64/zypak) or a [direct patch](https://github.com/flathub/org.chromium.Chromium/blob/master/patches/chromium/flatpak-Add-initial-sandbox-support.patch), the problem is these methods are very poorly configured to the point they essentially break the typically very strong sandboxing that Chromium provides. These solutions are closer to compatibility layers than they are genuine [security solutions](https://issues.chromium.org/issues/40753165#comment11). Upstream (Chromium devs) have expressed they do not intend to support Flatpak [anytime soon](https://issues.chromium.org/issues/40928753#comment5) for reasons alike to this. Flatpak *significantly* inhibits Chromium's sandboxing, and there is no faithful implementation currently.

### :simple-qt: {{b("QtWebEngine", "https://doc.qt.io/qt-6/qtwebengine-overview.html", "")}}

Browsers based on QtWebEngine (for example [KDE’s Falkon](https://apps.kde.org/falkon/)) should generally be avoided. QtWebEngine forks a specific Chromium version at feature freeze and then [cherry‑picks security fixes](https://www.qt.io/blog/putting-updates-of-chromium-in-qtwebengine-on-a-timeline) from newer upstream releases. That approach can leave a longer exposure window than browsers that track Chromium directly. Cherry‑picking is error‑prone and may miss fixes that rely on broader refactors or API changes, increasing the likelihood that patches are incomplete.

## :lucide-square-star: Popular Security-Centric Options

This section is dedicated to a few options people often recommend explicitly for security reasons, but the options themselves are rather niche. For example, Brave is *not* a security option but it is a very popular recommendation for "security" but it is not itself a security focused browser. Same follows for other projects claiming the same thing, such as LibreWolf. This section has projects that actually *try* to improve browser security.

### :lucide-shield: {{b("Vanadium", "https://github.com/GrapheneOS/Vanadium", "")}}

This is the GrapheneOS default browser. It almost goes without saying that it is one of, if not the best option currently for privsec. Very few browsers are as comprehensive with their hardening or as consistent with their update cycle. Unfortunately, the browser is only available on GrapheneOS, so most may not be able to use it. An Android-wide release is planned but the expected release of that is unknown (at least to the public).

### :material-google-chrome: {{b("Trivalent", "https://github.com/secureblue/Trivalent", "chrome")}}

Full disclosure, I am a frequent contributor to Trivalent. This wouldn't affect my opinion of it anyway, as it is currently. The explanation is below.

Essentially, this is Vanadium for desktop Linux, somewhat literally. Do note that despite getting as close as possible, it does not match to Vanadium currently due to poor security in the desktop Linux ecosystem and a lack of availability of hardware security features like MTE. Many patches from Vanadium that are not Android-specific are used. Not only that, it expands on many desktop and Linux-centric hardening. Additionally, due to a decent amount of automation work, weekly updates are often shipped same-day as upstream or the day after, at a very consistent pace.

Beyond that, I won't go too in depth because it will sound more like marketing than a "review".

### :fontawesome-brands-firefox-browser: {{b("IronFox", "https://gitlab.com/ironfox-oss/IronFox", "")}}

[See](#firefox) [here](#firefox-forks). Firefox based browsers, especially on Android, have terrible security. IronFox isn't exactly free of these issues. It does do some work to reduce some attack surface of base Firefox, but this is not significant or substantial enough to justify its use over any Chromium based browser. But, if you are for some unholy reason forced to use a Firefox based browser on Android, IronFox is your best bet, but still note it's nothing to depend on security-wise.

### :simple-torbrowser: {{b("Tor Browser", "https://www.torproject.org", "firefox")}}

I don't think this should be controversial, but Tor is *not* a security focused browser. For starters, it is just [Firefox](#firefox) fundamentally, it doesn't fix any of the architectural issues of FF, it just adds anti-fingerprinting protections.

Yes, Tor is decent for anti-fingerprinting, it is hard to argue that any other browser even comes close. That does not translate into security benefit, as security is one of Tor's biggest flaws. It also uses Firefox ESR, which is basically Firefox but 2 months out-of-date and CVEs backported. In general, the best use-case for Tor is inside a virtual machine, otherwise you are putting yourself at risk.

#### :simple-mullvad: {{b("Mullvad Browser", "https://mullvad.net/en/browser", "firefox")}}

Mullvad is Tor Browser without Tor, it has literally no advantages and only regresses on Tor's base anti-fingerprinting model. It adds uBlock Origin, which can cause nearly infinite variation in users by filter versions and custom filters, and fingerprinting system uptimes based on that. A big part of Tor's resistance to fingerprinting is the Tor network, Mullvad substitutes this by using their own VPN service, but not all users have that so the benefit is significantly weaker. Mullvad does have a mode to [randomize where you connect](https://github.com/mullvad/browser-extension/releases/tag/v0.9.8-firefox-beta), this adds some parity to how you expect Tor to work if enabled, which can prevent fingerprinting based on Mullvad server choice. Fundamentally this is a downstream of a downstream, that being Tor and Firefox, so updates will be twice as delayed. It is roughly in the same ballpark as LibreWolf, in that it actually has very little to offer beyond convenience of setup.

### :simple-librewolf: {{b("LibreWolf", "https://www.librewolf.net", "firefox")}}

Consider it roughly in the same camp as [Ironfox](#ironfox), many of the points that aren't Android-specific apply here as well. LibreWolf is a fork of Firefox designed to harden it. The update cycle looks [very consistent](https://codeberg.org/librewolf/source/tags) with [Firefox's upstream release cycle](https://www.firefox.com/en-US/releases/), which is good, they hit within the same-day ballpark with exceptions. A while back this was not the case, and they fell behind on updates frequently, that has clearly since changed and gotten much better.

Some positives over Firefox. It does enable a few build hardening options, [but very few currently](https://codeberg.org/librewolf/source/src/commit/d26f260211b19ce69898202a562d6afa69aad3f6/assets/mozconfig.new#L33). LibreWolf also offers permission toggles [for various features](https://codeberg.org/librewolf/source/src/commit/d26f260211b19ce69898202a562d6afa69aad3f6/patches/lw-permissions.patch) that base Firefox does not, such as WebGL and web DRM. Beyond that, most of LibreWolf's hardening is just flipping privacy toggles and patching out privacy intrusive features.

There are two points of concern that demonstrate some anti-security patterns. One is the preloading of uBlock Origin. Extensions are a security risk, and preloading them should be avoided, that goes twice for an MV2 extension. It also cannot be removed, only disabled. The other point is about having a verified Flatpak, similar to [Brave](#brave). Firefox in particular is really bad [as a Flatpak](#flatpak-firefox-flatpak), marking a Firefox-based browser as official on Flathub is a bad sign.

That said, this section was written as a re-assessment of LibreWolf (since the old mention was based on outdated information) and, based on what I could find, it is at its core an improvement over Firefox. If you disable uBlock Origin and avoid Flatpak browsers, then it is definitely one of the better Firefox-based browsers, and is probably your best choice should such a browser be required. That said, it is still Firefox-based and should be avoided on that notion; its security is nothing to depend on.

## :lucide-star-off: Other Browsers

Anything *not* directly based on Chromium.

### :fontawesome-brands-firefox: {{b("Firefox", "https://www.firefox.com", "firefox")}}

Firefox is [inherently insecure](https://madaidans-insecurities.github.io/firefox-chromium.html). I can already see the responses to that source, "Last updated March 2022", "4-5 year old article", "Biased and outdated", but these are often said in a hand-wave manner with the hope that time has fixed the issues present in the article... it has not. Saying the article is old actually makes Firefox look *worse*, since it hasn't significantly improved in 4+ years. To be fair, there has been improvement but not enough of it to make it comparable to Chromium based browsers (even from 3 years ago). This is especially true on Linux where the sandboxing is very poor, and Android where *there is no website sandbox at all*. The current Android implementation of the Firefox sandbox (Fission) is very weak (was recently enabled by default in [v147](https://www.firefox.com/en-US/firefox/android/147.0/releasenotes/)), out of the box it does not use Android's [isolatedProcess](https://developer.android.com/guide/topics/manifest/service-element#isolated) flag, which ensures that subprocesses are properly isolated and cannot trivially escalate privilege within the application. This flag can be enabled as an experiment in some forks, but even still the sandboxing design they have is very new for Firefox and is likely going to take some time to stabilize and be relatively bug-free.

If you are deadset on using Firefox (even though you should not be for any valid reason I can think of ...other than Firefox sync maybe), I would recommend using [arkenfox user.js](https://github.com/arkenfox/user.js/). It does reduce attack surface a bit and frankly makes Firefox somewhat useable.
However, [Arkenfox user.js is going EoL soon](https://github.com/arkenfox/user.js/issues/2042). A potential alternative is [Phoenix](https://github.com/celenityy/Phoenix).

#### :simple-flatpak: Firefox Flatpak

Despite Firefox's poor security, the browser does have some form of sandboxing, which is critical to what little security it has. Above there is a section about how Flatpak interferes with the Chromium sandboxing architecture. Well, the same is true for Firefox, Firefox depends on userns for a portion of its sandboxing. The question is how does Firefox account for a lack of usernamespaces? Simple. It doesn't. Firefox just... pretends they don't exist, but only in Flatpak. They did add a warning about a lack of userns access for environments without userns and that sandboxing and security may suffer, but this warning is just disabled in the *official* Firefox Flatpak package. If you are really deadset on using Firefox then at the very least *avoid* the Flatpak. Just a general rule of thumb for all browsers really.

#### :lucide-git-fork: Firefox Forks

Most Firefox forks are just regular Firefox with either UI changes or some changes to user-hostile defaults. They typically suffer from slower update cycles.

Although, I will mention one fork specifically, Pale Moon. Pale Moon uses *ancient* code with some security patches backported, and it is single-process so it cannot utilize any modern sandboxing technology (such as seccomp or namespaces, or the adjacents on other platforms). You can manually sandbox the browser but that doesn't isolate sites from each other. This also means that newer security features Firefox adds (as rare as that is) will not get properly added, if they get added at all.

### :material-apple-safari: {{b("Safari/WebKit", "https://www.apple.com/safari", "https://support.apple.com/en-us/guide/deployment/depb514ccd65/web")}}

Security-wise, Safari/WebKit is pretty decent. It may be behind on web standards but it has strong partitioning, strong sandboxing, and robust mitigations on all supported platforms. Additionally, it can disable JIT JavaScript (and many other web features) on iOS and macOS per-site using Lockdown Mode to be W^X compliant, though most websites will likely break. That said, Webkit lacks full site isolation, it currently only offers tab-isolation. This has caused [some vulnerabilities](https://open-web-advocacy.org/blog/slap-and-flop--apples-lack-of-full-site-isolation-and-ios-browser-ban-puts-users-at-risk/), so it is something to be cautious of. Because of this fact, you should prefer Chromium-based browsers where possible, since they have a much more mature isolation scheme.

Safari itself has poor update handling, both in the effort to ship fixes and technology around shipping updates. Safari updates [like a system component](https://support.apple.com/en-ca/102665), which means a full system update is needed to update Safari. This has changed on Apple OS versions [since 26.1](https://support.apple.com/en-us/102657), so if you are up-to-date then it will update asynchronously to the rest of the OS. While not entirely a problem, iOS and MacOS don't update that often, especially not often enough to keep up with Safari/WebKit CVEs. On top of this, Safari doesn't ship updates that quickly, or at least [they didn't always](https://projectzero.google/2022/02/a-walk-through-project-zero-metrics.html).

#### :material-gnome: {{b("Epiphany/WebKitGTK", "https://apps.gnome.org/Epiphany/", "")}}

(I believe) WebKitGTK is the official WebKit port to Linux. It shares many of the same features of regular WebKit, sans some stuff that are iOS/macOS/Apple specific. It is the only browser to support proper sandboxing in Flatpak but said sandboxing is notably weaker than native (non-Flatpak, non-Snap) Chromium.

### :material-android: Android WebView Browsers

These browsers cannot offer site-isolation due to how Android WebView is designed, websites are only isolated from the system not each other. Typically they do not have strong partitioning and are very minimal in their feature set. While they are Chromium-based, they are so much worse-off by comparison that it is hard to put them in the same classification.
