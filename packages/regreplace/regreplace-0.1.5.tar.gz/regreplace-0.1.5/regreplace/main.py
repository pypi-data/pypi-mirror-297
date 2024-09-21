import re

class Replacer:
    
    def __init__(self, pattern=r".*?_(?P<date>\d{8}-\d{6}( \(1\))*)(?P<ext>\..+$)"):
        """
        Instanciate the Match Replacer with a Regex Pattern containing named groups.
        `(?P<group_name>...)` => `...` is the pattern to which you assign a `group_name`.
        """
        self.re = re.compile(pattern)
    
    def match(self, s, group_name):
        """
        This method should return what was matched under a certain `group_name` in the pattern.
        """
        m = self.re.match(s)
        dct = m.groupdict()
        return dct[group_name] if group_name in dct else None
    
    def replace(self, s, group_name, replacement):
        """
        This method replaces what was matched under the `group_name` by the `replacement`.
        The replacement could be the result of a processing of something `.match()`ed by any of the groups!
        """
        m = self.re.match(s)
        if m.group(group_name) not in [None, '']:
            start, end = m.start(group_name), m.end(group_name)
            return f"{s[:start]}{replacement}{s[end:]}"
        else:
            return m.group()
