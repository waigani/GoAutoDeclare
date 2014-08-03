# Copyright (c) 2014 Jesse Meek <https://github.com/waigani>
# This program is Free Software see LICENSE file for details.

""" GoAutoDeclare is a Sublime Text plugin which automatically corrects short
variable declaration ':=' and assignment operator '=' mistakes on save.
"""

import sublime, sublime_plugin, subprocess, re

errs  = ["cannot assign to","no new variables on left side of"]


class GoAutoDeclareCommand(sublime_plugin.TextCommand):
    """ Command gets called on save.
    """

    def run(self, edit, output):
        for s in output.split("\n"):
            self.auto_correct(edit, 0, s)
            self.auto_correct(edit, 1, s)

    def auto_correct(self, edit, err, output):
        """ Automatically correct assignment errors i.e. ':=' vs '='.
        """

        v = self.view
        regex = r"\:([^\:]*)\:.*(%s)" % errs[err]

        g = re.search(regex, output)
        if g is not None:
            p = v.text_point(int(g.group(1))-1, 0)
            line = v.line(p)
            lineContents = v.substr(line)
            if err == 0:
                lineContents = lineContents.replace("=",":=", 1)
            else:
                lineContents = lineContents.replace(":=", "=", 1)
            self.view.replace(edit, line, lineContents) 
            

class GoAutoDeclareEventListener(sublime_plugin.EventListener):
    """ GoAutoDeclare formatter event listener class.
    """

    def on_pre_save_async(self, view):
        """ Called just before the file is going to be saved.
        """

        fn = view.file_name()
        output = "No errs found"
        if view.file_name()[-3:] == ".go":
            if view.file_name()[-8:] == "_test.go":
               output = self.run_cmd("test", fn)
            else:
               output = self.run_cmd("build", fn)

        # Run a new command to use the edit object for this view.
        view.run_command('go_auto_declare', {
            'output': output[1]})

    def run_cmd(self, cmd, fn):
        """ Runs cmd with fn as first arg and returns errors.
        """

        env = get_setting("env")

        # Build cmd.
        cmd = "export GOPATH=\"%(go_path)s\"; export GOROOT=\"%(go_root)s\"; export PATH=%(path)s; $GOROOT/bin/go %(cmd)s %(fn)s;" % {
        "go_path": env["GOPATH"],
        "go_root": env["GOROOT"],
        "path": env["PATH"],
         "cmd": cmd,
         "fn": fn}

        # Run the cmd.
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        result, err = p.communicate()
        return result.decode('utf-8'), err.decode('utf-8')

def get_setting(key, default=None):
    """ Returns the user setting if found, otherwise it returns the
    default setting. If neither are set the 'default' value passed in is returned.
    """

    val = sublime.load_settings("User.sublime-settings").get(key)
    if not val:
        val = sublime.load_settings("Default.sublime-settings").get(key)
    if not val:
        val = default
    return val