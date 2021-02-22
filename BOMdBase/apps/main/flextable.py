from django.db.models.functions import Lower

from main.utils import rgetattr, icon

def flextable(params, tbldef, src):

    class html_gather:
        def __init__(self, i):
            self.i = i
            self.text = ''
        def start(self, text):
            self.text += (self.i * ' ') + text
        def add(self, text):
            self.text += text
        def indent(self, text):
            self.text += (self.i * ' ') + text
            self.i += 2
        def outdent(self, text):
            self.i -= 2
            self.text += (self.i * ' ') + text
        def str(self):
            return self.text

    def html_link(text, title, url, target=''):
        nonlocal params, tbldef
        if 'printable' in params or 'nolinks' in tbldef:
            if '<i class="material-icons">' in text:
                text = ''
            return text
        if text == '--' or 'None' in url:
            return '--'
        r = '<a title="' + title + '" href="' + url + '" '
        r += 'class="text-decoration-none"'
        if target:
            r += ' target="' + target + '"'
        r += '>' + text + '</a>'
        return r

    def hide_sort(name, tbldef, params):
        hidden, hide_link, unhide_link = False, '', ''
        #if not 'nohide' in options:
        if name in tbldef['hide']:
            if name in params.getlist('hide'):
                hidden = True
                unhide_params = params.copy()
                l = unhide_params.getlist('hide')
                l.remove(name)
                unhide_params.setlist('hide', l)
                unhide_link = '?' + unhide_params.urlencode()
            else:
                hide_params = params.copy()
                l = hide_params.getlist('hide')
                l.insert(0, name)
                hide_params.setlist('hide', l)
                hide_link = '?' + hide_params.urlencode()
        sort_level, sort_dir, sort_link = 0, '', ''
        #if not 'nosort' in options:
        if name in tbldef['sort']:
            sort_params = params.copy()
            l = sort_params.getlist('sort')
            if name in l:
                sort_level = 1 + l.index(name)
                sort_dir = '+'
                l[sort_level - 1] = '-' + name
            elif '-' + name in l:
                sort_level = 1 + l.index('-' + name)
                sort_dir = '-'
                l.remove('-' + name)
            else:
                l.insert(0, name)
            sort_params.setlist('sort', l)
            sort_link = '?' + sort_params.urlencode()
        return hidden, hide_link, unhide_link, sort_level, sort_dir, sort_link

    def process_head(params, tbldef, headdef, th, cols, unhide_links, level=0, parents=[]):
        total_width = 0
        if len(th)-1 < level:
            th.append([])
        for text, name, x in headdef:
            hidden, hide_link, unhide_link, sort_level, sort_dir, sort_link = \
                hide_sort(name, tbldef, params)
            if unhide_link:
                unhide_links.append((tbldef['hide'][name], unhide_link))
            if not hidden:
                if sort_link:
                    text = html_link(text, 'sort', sort_link)
                if 'printable' not in params and (hide_link or sort_link):
                    text = '<table style="width:100%"><tr>' \
                        '<td style="width:100%">' + text + '</td>'
                    if sort_link:
                        text += '<td>'
                        sort_icon = 'up' if sort_dir == '+' else \
                            'down' if sort_dir == '-' else 'updown'
                        text += html_link(icon(sort_icon), 'sort', sort_link)
                        text += '</td>'
                        if sort_level:
                            text += '<td>'
                            text += str(sort_level)
                            text += '</td>'
                    if hide_link:
                        text += '<td>'
                        text += html_link(icon('hide'), 'hide', hide_link)
                        text += '</td>'
                    text += '</tr></table>'
                if type(x) == int:
                    subcol = False
                    width = x
                elif type(x) == tuple:
                    subcol = True
                    width = process_head(params, tbldef, x, th, cols,
                        unhide_links, level+1, parents+[name])
                th[level].append([text, name, subcol, width, parents])
                cols.append(name)
                total_width += width
        return total_width

    def build_tree(obj, path, tree=[], parents=[]):
        level = len(parents)
        rows = 0
        if level == len(tree):
            tree.append([])
        if path:
            d = getattr(obj, path[0]) if obj else None
            if 'RelatedManager' in str(type(d)):
                d = d.all()
            if 'QuerySet' in str(type(d)):
                d = list(d)
            else:
                d = [d]
            if not d:
                d = [None]
            for c in d:
                rows += build_tree(c, path[1:], tree, parents + [obj])
            tree[level+1].sort(key = lambda x: [y.__str__() for y in x[0]])
            tree[level].append((parents + [obj], rows))
        else:
            tree[level].append((parents + [obj], 1))
            rows = 1
        return rows if level else tree

    def get_link_param(o, src):
        if type(src) == tuple:
            return str(rgetattr(o[src[0]], src[1]))
        elif type(src) == str:
            if src[0] == '?': # parameter
               return params.get(src[1:])
            elif src[0] == '*': # auto variable
                return str(auto[src[1:]])
            else:
                return src # static
        else:
            return '??'

    def get_link_params(o, params):
        nonlocal tbldef
        r = []
        if type(params) == dict:
            for name, alias in params.items():
                r.append(name + '=' + \
                    get_link_param(o, tbldef['aliases'][alias]) )
        elif type(params) == str:
            r.append(str(get_link_param(o, tbldef['aliases'][params])))
        return r

    if src.count() == 0:
        return '<p>No data to display.</p>'

    # init
    html = html_gather(4)
    html.add('\n')

    # process head def
    th = [[]] # processed table head data
    cols = [] # list of visible columns
    unhide_links = []
    process_head(params, tbldef, tbldef['head'], th, cols, unhide_links, 0)

    # unhide links
    if unhide_links:
        html.start('<p>Hidden columns:&nbsp;&nbsp;')
        html.add(',&nbsp;'.join( \
            [html_link(text, 'unhide ' + text, link)
            for text, link in unhide_links]
        ))
        html.add('</p>\n')

    # render table start
    html.indent('<div class="table-responsive-sm">\n')
    html.indent('<table class="table w-auto table-bordered table-sm">\n')

    # render table head
    html.indent('<thead class="thead-light">\n')
    for n, th_row in enumerate(th):
        html.indent('<tr>\n')
        for text, name, subcol, width, parents in th_row:
            html.indent('<th rowspan = "')
            html.add('1' if subcol else str(len(th) - n))
            html.add('" colspan = "' + str(width) + '" ')
            if name in tbldef['sort']:
                html.add('class="orderable">\n')
            else:
                html.add('>\n')
            html.start(text + '\n')
            html.outdent('</th>\n')
        html.outdent('</tr>\n')
    html.outdent('</thead>\n')

    # sort
    if 'sort' in params:
        sort_fields = []
        for p in params.getlist('sort'):
            f = p.replace('-', '')
            if f in tbldef['sort']:
                sort_fields.append(p.replace(f, tbldef['sort'][f]))
        for i, s in enumerate(sort_fields):
            sort_fields[i] = Lower(s[1:]).desc() if s[0] == '-' else Lower(s)
        src = src.order_by(*sort_fields)

    # render body
    auto = { 'incr1': 0 }
    html.indent('<tbody>\n')
    stripe = False
    for obj in src:

        # update auto variables
        auto['incr1'] += 1
        stripe = not stripe

        # build tree of related objects and row heights
        if 'relations' in tbldef:
            tree = build_tree(obj, tbldef['relations'], [])
        else:
            tree = [[[[obj],1]]]
        span_max = tree[0][0][1]

        # render all row(s) associated with object
        it, rt = {}, {} # index and row trackers
        for _, alias, _, _, _ in tbldef['body']:
            it[alias], rt[alias] = 0, 0
        for r in range(span_max):
            if r:
                html.indent('<tr')
            else:
                if hasattr(obj, 'id'):
                    id = getattr(obj, 'id')
                    html.indent('<tr id="' + str(id) + '"') # bookmark
            if stripe:
                html.add(' class="table-secondary">\n')
            else:
                html.add('>\n')

            for col, alias, link_text, link_url, link_params in tbldef['body']:
                if col not in cols: # handle visibility
                    continue
                if r >= rt[alias]:
                    src = tbldef['aliases'][alias]
                    span = span_max
                    link_param_list = []
                    content = None
                    if type(src) == tuple: # related data
                        node = tree[src[0]][it[alias]]
                        if src[1][0] == '#':
                            if node[0][-1]:
                                content = src[1][1:]
                            else:
                                content = '--'
                        else:
                            content = rgetattr(node[0][-1], src[1])
                            if str(type(content)) == "<class 'datetime.datetime'>":
                                content = content.strftime('%Y-%m-%d %H:%M:%S')
                            elif str(type(content)) == "<class 'bool'>":
                                content = icon('checked' if content \
                                    else 'unchecked')
                                content = '<center>' + content + '</center>'
                            elif str(type(content)) == "<class 'int'>":
                                content = str(content)
                            elif str(type(content)) == "<class 'str'>":
                                #content = content.replace('-', '&#8209;') # non-breaking hyphen
                                if content[:4] == 'http':
                                    content = html_link(content, 'link', content)
                            elif str(type(content)) == "<class 'NoneType'>":
                                content = '--'
                            else:
                                content = '??'
                        span = node[1]
                        link_param_list = get_link_params(node[0], link_params)
                    elif type(src) == str:
                        if src[0] == '$': # aggregate
                            content = str(row_src[src[1:]])
                        elif src[0] == '?': # parameter
                            content = params.get(src[1:])
                        elif src[0] == '*': # auto variable
                            content = str(auto[src[1:]])
                        else:
                            content = src # static
                        link_param_list = get_link_params([obj], link_params)
                    else:
                        content = '??'
                    # apply link
                    if link_text:
                        link_url += '&'.join(link_param_list)
                        content = html_link(
                            content, link_text, link_url,
                            '_blank' if 'search' in link_url else ''
                        )
                    # output
                    html.indent('<td  rowspan = "' + str(span) + \
                        '" class="align-top">\n')
                    html.start(content + '\n')
                    html.outdent('</td>\n')
                    # update trackers
                    rt[alias] += span
                    it[alias] += 1
            html.outdent('</tr>\n')

    html.outdent('</tbody>\n')

    # render table end
    html.outdent('</table>\n')
    html.outdent('</div>\n')

    # done
    return html.str()