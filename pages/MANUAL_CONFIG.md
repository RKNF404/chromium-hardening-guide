# Policies

See [POLICIES.md](/configs/POLICIES.md) for what policies can be used and their respective values

## Linux

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

## Windows

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

## MacOS

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

## Linux

There is no one answer, most Linux distibutions offer a way to persist flags for their build of Chromium, and sometimes even offer a way to persist for Google Chrome as well.
\
For example, Arch notably offers a [flag persistence method](https://wiki.archlinux.org/title/Chromium#Configuration) for both Chromium and Chrome. Fedora also offers a method via `/etc/chromium/chromium.conf`. Most other common distros like Ubuntu, Debian, Gentoo, Nix, etc. also offer methods that are either specific or similar.
\
Research into your specific distro and find out how it handles flag persistence. It can sometimes help to just search around `/etc` for a Chromium directory or set of Chromium files.

## Windows

Out of the box, there is really no easy way to persist flags in a way to guarentee that they will be used... but, with some reg hacking and a launch script it is possible (thanks to chrlauncher).
\
Using another project of mine, [chromewrapper](https://github.com/RKNF404/chromewrapper), you can persist flags, specifically for Google Chrome, but it should be trivially adjustable to any Chromium-based browser.
\
\
To do this project, run the install script `chromewrapperDefaultBrowser.bat`, this will add reg keys for the wrapper script to handle standard requests a browser would typically handle. (this step requires running the script as admin)
\
Then add `chromewrapper.bat` to the location given by `CHROMEWRAPPER_PATH` present in that script, by default it should be Chrome's binary directory (where `chrome.exe` is present), by default this should be `C:\Program Files\Google\Chrome\Application\chromewrapper.bat`.

After this, create a desktop shortcut with the following entry:
\
`explorer.exe "C:\Program Files\Google\Chrome\Application\chromewrapper.bat"`
\
Then right click that shortcut and click `Pin To Taskbar`.
\
And that's it, your browser will now launch with the flags in the wrapper script whenever it is opened from the icon or invoked as a handler. (The shortcut can be deleted by the way, the taskbar pin will be unaffected)
\
To get custom flags to persist, create a file next to `chromewrapper.bat` in the same directory called `80-hardening-guide-flags.conf`. Within it, add whatever flags you want, separating each with a new line (enter key).
\
\
If you no longer wish to use the wrapper, simply run the `chromewrapperRegCleaner.reg` registry file. It will delete all instances where chromewrapper is a handler. You can also deselect it as the default browser in the settings to retain the functionality for later.

## Android

There is a way to add flags via ADB, but I know very little about it and would advise against.
