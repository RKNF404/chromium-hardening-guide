# Setup Guide

The following guide will assist in setting up and using a Chromium based browser with the flags and policies present in this repo. It will cover 3 main sections: selecting a browser (covering forks, options for different OSes and alternatives to Chromium should they be viable), applying policies (only for Linux and Windows, maybe MacOS, but notes for other OSes where applicable), and persisting flags (only covering a few OSes since not all of them support proper flag persistence). The primary focus will be on **Linux** and **Windows**, but notes for Android and MacOS will be spread throughout where it makes sense.
\
\
Please note that while I intend for this to be as comprehensive as possible, there will be gaps. For example, I do not have a Mac so I am not capable of offering up-to-date info on methods or options for those systems.

## Contents

- [Selecting a browser](BROWSER_SELECTION.md)
- [Automatic Config Generation](CONFIG_GEN.md)
- [Manual Config Creation](MANUAL_CONFIG.md)
- [Basic Setup](#basic-setup)
  - [Content Blocking](#content-blocking)
- [My Setup](#my-setup) (in case you care)

## Basic Setup

This is just preferences, so see [PREFERENCES.md](PREFERENCES.md). Everything else is covered by policies.

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

## My Setup

In case you are curious, this is my personal setup. The main purpose is to demonstrate the usage of this guide.
\
\
Lets start with OSs. I have an Android and a few Linux machines. They are GrapheneOS, Fedora Workstation, and a few laptops with secureblue. Because of this, your setup may vary.
\
\
On GrapheneOS, I use Vanadium. It is without a doubt the best option on Android, but due to a lack of availability outside of GrapheneOS, it is difficult to recommend. Therefore, the next best option I would use is Chrome. Yes, Chrome with some settings changed and some flags altered in `chrome://flags`. Is this ideal? Not really, but it's the next best thing below Vanadium. For watching Youtube without ads, I use NewPipe, so adblocking isn't a big enough deal for my browsing to justify selecting a browser based around it. *Not-so-subtle suggestion against Brave.*
\
\
On Fedora, I use Trivalent, secureblue's default browser. It is sort of a port of Vanadium to desktop Linux, as it comes with a lot of neat defaults and hardening. For RPM based distros, it is definitely the best option. Due to Trivalent's defaults, it requires no usage of this guide or its configs. Otherwise, say on a Debian-based distro, I would use Chrome with the application of this guide. It's the closest you can get to Trivalent/Vanadium. The same is true for secureblue, Trivalent is best used on secureblue due to the SELinux confinement offered specifically for Trivalent.
