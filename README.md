GoAutoDeclare
=============

GoAutoDeclare is a Sublime Text plugin which automatically corrects short
variable declaration ':=' and assignment operator '=' mistakes on save.


Usage
-----

Code such as the following,

```go
a = "a"
var b int
b := 1
```

will be corrected on save to:

```go
a := "a"
var b int
b = 1
```


Install
-------

Install Sublime Package Control (if you haven't done so already) from http://wbond.net/sublime_packages/package_control. Be sure to restart ST to complete the installation.

Bring up the command palette (default ctrl+shift+p or cmd+shift+p) and start typing Package Control: Install Package then press return or click on that option to activate it. You will be presented with a new Quick Panel with the list of available packages. Type GoAutoDeclare and press return or on its entry to install GoAutoDeclare. If there is no entry for GoAutoDeclare, you most likely already have it installed.

The default Go environment variables are set as folows:

```javascript
{
    "env": { "GOPATH": "$HOME/go", "GOROOT": "$HOME/.gvm/gos/go1.2.1", "PATH": "$PATH:$GOPATH" },
}
```

Set your Go environment variables by copying the above into  `Preferences > Package Settings > GoAutoDeclare > Settings-User` and editing accordingly.


Dependencies
------------
GoAutoDeclare relies on a version of Go that reports the following errors: "cannot assign to" and "no new variables on left side of". 


Copyright, License & Contributors
=================================

GoAutoDeclare is released under the MIT license. See [LICENSE.md](LICENSE.md)