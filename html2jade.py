import urllib2
import json
import sublime
import sublime_plugin


class HtmlToJadeFromFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        source = self.view.file_name()
        if source.endswith(".html"):
            target = source + '.jade'
        if target:
            with open(source, 'r') as f:
                html = f.read()
            jade = HTJTools.post_html_return_jade(html)
            if jade != None:
                with open(target, 'w') as f:
                    f.write(jade)
                self.view.window().open_file(target)

    def is_enabled(self):
        return True  #return (self.view.file_name().endswith(".html") or self.view.file_name().endswith(".erb"))


class HtmlToJadeFromSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                html = self.view.substr(region)
                jade = HTJTools.post_html_return_jade(html)
                if jade != None:
                    self.view.replace(edit, region, jade)

    def is_enabled(self):
        return True #return self.view.file_name().endswith(".jade")


class HtmlToJadeFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        html = sublime.get_clipboard()
        jade = HTJTools.post_html_return_jade(html)
        if jade != None:
            for region in self.view.sel():
                self.view.replace(edit, region, jade)

    def is_enabled(self):
        return True #return self.view.file_name().endswith(".jade")


class HTJTools:
    @classmethod
    def post_html_return_jade(self, html):
        html = html.strip()
        host = 'http://html2jade.aaron-powell.com/convert'
        data = {'html': html}
        data_json = json.dumps(data)
        req = urllib2.Request(host, data_json, {'content-type': 'application/json'})
        response_stream = urllib2.urlopen(req)
        result = json.loads(response_stream.read())

        if result["jade"]:
            if html.startswith('<!DOCTYPE') or html.lower().startswith('<html>'):
                return result["jade"]
            else:
                return result["jade"][len("html\\n  body\\n"):]
        else:
            return None
