# Flags

##### `--component-updater=--disable-pings`
***(privacy)***\
Reduces data sent to the component updater

##### `--disable-breakpad --disable-crash-reporter`
***(privacy)***\
Disable crash reporting

##### `--extension-content-verification=enforce_strict --extensions-install-verification=enforce_strict`
***(security)***\
Forces all extensions to be validated to prevent tampering

##### `--incognito`
***(privacy OPTIONAL)***\
To encourage ephemerality, with globally persistent flags it can also launch external links in Incognito

##### `--js-flags=--jitless`
***(security)***\
Disables Just-In-Time (JIT) compiled JavaScript, JIT is a *massive* security risk, it should be disabled by default, but it can risk approx 5-50% performance loss depending on the website.\
~~If you experience issues with a site, try **disabling** V8 security for that site under `chrome://settings/content/v8`, this will enable some optimizers in reference to the default this flag offers.~~\
The above no longer works, js-flags are no longer overwritten by the V8 optimizer toggle and instead passed along. This means this flag will disable unconditionally for all sites, extensions, pages, etc. If you require WebAssembly or higher JS performance, use the JIT policy instead and create a whitelist of sites.\
*For Windows*, uses Arbitrary Code Guard (ACG) to prevent renderer processes from violating W^X, and enables the Intel hardware shadow stack to enforce backward-edge CFI

##### `--js-flags=--disable-optimizing-compilers`
***(security)***\
**DO NOT USE WITH JITLESS JS FLAG**, it will override it if used after. If you are using the JIT policy instead of the flag, use this flag to reduce attack surface of JIT code. This shouldn't cause any compatibility issues, and the slowdowns will be between 1% and 20% depending on the site, but it should be mostly transparent hardening usability-wise

##### `--no-pings`
***(privacy)***\
Disables hyperlink auditing

##### `--ozone-platform=$XDG_SESSION_TYPE`
***(security functionality LINUX_ONLY)***\
This will set your browser to launch with Wayland or X11 depending on your session default, ideally though you should use Wayland
