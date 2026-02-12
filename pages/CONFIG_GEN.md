# Automatic Config Generation

[>>> Back to guide <<<](SETUP_GUIDE.md#contents)

This page explains how to use the config generation script.

The script and the associated config database file is located in the [`configs`](/configs) folder. Both of these are required.

## Script Usage

To get a summary of how to use the script, you can run the script by running in the same directory as the script file:
- `python3 ConfigGen.py --help`
- `./ConfigGen.py --help` (Linux and MacOS only)

Just running the script without any arguments will automatically parse the `Configuration.json` file in the same working directory, include all configurations, and prompt for all optional configurations. It will also detect what platform you the script is being run on and produce the configuration formats and include platform-specific configs as well (most notably for Windows).

### Arguments

Currently, there are a few arguments the script takes (these can be viewed with the help command above, this will go in-depth).

- `--system SYSTEM` - takes either "linux", "macos", or "windows". This allows overriding the automatic platform detection, incase you want to generate config files for another computer.
- `--type TYPE` - allows filtering by the type of configuration file you want, i.e. commandline or policy. Commandline will only output the flags file and ignore all policies, the policy options does the inverse. The purpose is for the case where you cannot, for one reason or another, use one of these configuration types. For example, on MacOS where commandline flags are harder to persist.
- `--format FORMAT` - allows selecting between the two types of formats for the flags file. Generic is just flags separated on each line, variable is each flags being appended to a CHROMIUM_FLAGS variable in the case of the file being used in a shell script. This may get overridden if the platform only supports one type of format (example, Windows only supports generic due to how `chromewrapper` is written)
- `--tag TAG` - filter the output flags by the various tags included, such as "security", "privacy", "annoyance", etc. Can be helpful if you only need a very specific group of flags or policies.
- `--file FILE` - can be used to set a path a custom configs database.
- `--choice [y|n|yes|no]` - sets the default choice for optional configs, meant to allow for automation.
- `--recommend` - split off policies that can be recommended, recommended policies can be changed from the preferences within Chrome/Chromium, mandatory policies cannot be changed when they are set.

If something is going wrong, the script should tell you almost exactly what. If it doesn't or the error output isn't clear, feel free to ask for help by opening an issue.

### Using the output

#### Windows

Out of the box, there is really no easy way to persist flags in a way to guarentee that they will be used... but, with some reg hacking and a launch script it is possible (thanks to chrlauncher).
Using another project of mine, [chromewrapper](https://github.com/RKNF404/chromewrapper), you can persist flags, specifically for Google Chrome, but it should be trivially adjustable to any Chromium-based browser.

To do this project, run the install script chromewrapperDefaultBrowser.bat, this will add reg keys for the wrapper script to handle standard requests a browser would typically handle. (this step requires running the script as admin)
Then add `chromewrapper.bat` to the location given by `CHROMEWRAPPER_PATH` present in that script, by default it should be Chrome's binary directory (where `chrome.exe` is present), by default this should be `C:\Program Files\Google\Chrome\Application\chromewrapper.bat`.

After this, create a desktop shortcut with the following entry:
`explorer.exe "C:\Program Files\Google\Chrome\Application\chromewrapper.bat"`
Then right click that shortcut and click `Pin To Taskbar`.
And that's it, your browser will now launch with the flags in the wrapper script whenever it is opened from the icon or invoked as a handler. (The shortcut can be deleted by the way, the taskbar pin will be unaffected)

After following these steps, in the same directory as `chromewrapper.bat` add the script's resulting `80-hardening-guide-flags.conf` file (it should output to a `flags/` folder) to that directory.

If you no longer wish to use the wrapper, simply run the `chromewrapperRegCleaner.reg` registry file. It will delete all instances where chromewrapper is a handler. You can also just deselect it as the default browser in the settings to retain the functionality for later.

For policies, simply double click the `hardening-guide-policy.reg` file, it will give you some warnings and prompt you for administrator rights. Please be cautious the file is correct and properly formatted, it should never modify any registry entries outside of the Chrome policy paths.

#### Linux

(WIP)

#### MacOS

(WIP)

### Verifying output

To verify the flags are properly being added, open `chrome://version`, under the `Command Line` the added flags should be visible.

To verify policies, visit `chrome://policy`. You should see a list of applied policies. Scroll through them and check their statuses all say `Ok`. Some may say `Error, Ignored` on Windows, not much can be done about that, but they can be manually turned off in the browser's preferences anyway. If you do not see any policies or see more than a few with `Error` statuses, then something went wrong. If you are unsure, please feel free to open an issue. Include the `.reg` file used for the policies.

# [>>> Back to guide <<<](SETUP_GUIDE.md#contents)
