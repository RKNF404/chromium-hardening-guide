# Chromium Hardening Guide

Last updated for: `144`

Changes in latest version:
```
removed Enable feature ContentSettingsPartitioning
added policy SearchContentSharingSettings
updated:
  -LocalNetworkAccessChecks:LocalNetworkAccessChecksWarn/false,LocalNetworkAccessChecksWebRTC
  +LocalNetworkAccessChecksWebRTC,LocalNetworkAccessChecksWebSockets,LocalNetworkAccessChecksWebTransport
added Enable feature PrintCompositorLPAC
added Enable feature WinSboxStrictHandleChecks
removed policy TLS13EarlyDataEnabled
removed policy UserAgentReduction
```

Hardening guide for (theoretically) any Chromium browser.

Some of the flips and toggles come from other projects such as [Vanadium](https://github.com/GrapheneOS/Vanadium) or [Trivalent](https://github.com/secureblue/Trivalent).

If you're having any trouble applying the guide or have any general questions or inquiries, please feel free to open a [discussion thread](https://github.com/RKNF404/chromium-hardening-guide/discussions).
If want to suggest something, please open an [issue](https://github.com/RKNF404/chromium-hardening-guide/issues) for it.
If you have my Discord, feel free to message me there about this guide.

In the short future, the manual style of creating config files will be deprecated. I am actively working on a script to generate configuration outputs from a formatted json database as input. The configuration input file and the python script are already in `configs/`, though only Linux is currently supported. Once at least Windows is also supported, I will update the guide to account for script usage instead of manual creation of the configs. After which point the current markdown files with all the flags/features/policies will be removed. Manual creation of configs will still be present in the guide, but downplayed compared to the ConfigGen method.

All markdown files are licensed under the Microsoft Public License (`MS-PL`), all Python scripts and configuration files are licensed under the Apache version 2.0 (`Apache-2.0`).

## Quick Links

- [Setup Guide](#setup-guide)

# Setup Guide

The following guide will assist in setting up and using a Chromium based browser with the flags and policies present in this repo. It will cover 3 main sections: selecting a browser (covering forks, options for different OSes and alternatives to Chromium should they be viable), applying policies (only for Linux and Windows, maybe MacOS, but notes for other OSes where applicable), and persisting flags (only covering a few OSes since not all of them support proper flag persistence). The primary focus will be on **Linux** and **Windows**, but notes for Android and MacOS will be spread throughout where it makes sense.
\
\
Please note that while I intend for this to be as comprehensive as possible, there will be gaps. For example, I do not have a Mac so I am not capable of offering up-to-date info on methods or options for those systems.

## Contents

- [Selecting a browser](#selecting-a-browser)
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

[Visit here](pages/BROWSER_SELECTION.md)

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
