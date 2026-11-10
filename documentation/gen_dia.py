"""Generate Dia (.dia) UML class diagrams for the Notifications variant."""
import gzip, sys, os
from xml.sax.saxutils import escape

PUB, PRIV, PROT = 0, 1, 2
ABSTRACT, LEAF = 0, 2


class Diagram:
    def __init__(self):
        self.objs = []
        self.classes = {}  # name -> (id, x, y, w, h, nops)

    def nid(self):
        return "O%d" % len(self.objs)

    def cls(self, name, x, y, ops, abstract=False, w=None, attrs=()):
        """ops: list of (name, rettype, visibility, inh, [(pname, ptype), ...])"""
        oid = self.nid()
        if w is None:
            wname = len(name) * 0.62 + 1.0
            wops = max([0] + [self._oplen(o) * 0.405 + 0.6 for o in ops] + [(len(a[0]) + len(a[1]) + 4) * 0.405 + 0.6 for a in attrs])
            w = round(max(wname, wops, 5.0), 3)
        h = 2.8 + 0.8 * (len(ops) + len(attrs)) + (0.0 if ops else 0.0)
        ops_xml = ""
        for (n, t, vis, inh, params) in ops:
            pxml = "".join(
                f"""<dia:composite type="umlparameter">
<dia:attribute name="name"><dia:string>#{pn}#</dia:string></dia:attribute>
<dia:attribute name="type"><dia:string>#{pt}#</dia:string></dia:attribute>
<dia:attribute name="value"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="comment"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="kind"><dia:enum val="0"/></dia:attribute>
</dia:composite>""" for pn, pt in params)
            ops_xml += f"""<dia:composite type="umloperation">
<dia:attribute name="name"><dia:string>#{n}#</dia:string></dia:attribute>
<dia:attribute name="stereotype"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="type"><dia:string>#{t}#</dia:string></dia:attribute>
<dia:attribute name="visibility"><dia:enum val="{vis}"/></dia:attribute>
<dia:attribute name="comment"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="abstract"><dia:boolean val="{'true' if inh == ABSTRACT else 'false'}"/></dia:attribute>
<dia:attribute name="inheritance_type"><dia:enum val="{inh}"/></dia:attribute>
<dia:attribute name="query"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="class_scope"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="parameters">{pxml}</dia:attribute>
</dia:composite>"""
        attrs_xml = "".join(
            f"""<dia:composite type="umlattribute">
<dia:attribute name="name"><dia:string>#{an}#</dia:string></dia:attribute>
<dia:attribute name="type"><dia:string>#{at}#</dia:string></dia:attribute>
<dia:attribute name="value"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="comment"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="visibility"><dia:enum val="{av}"/></dia:attribute>
<dia:attribute name="abstract"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="class_scope"><dia:boolean val="false"/></dia:attribute>
</dia:composite>""" for an, at, av in attrs)
        ab = "true" if abstract else "false"
        xml = f"""<dia:object type="UML - Class" version="0" id="{oid}">
<dia:attribute name="obj_pos"><dia:point val="{x},{y}"/></dia:attribute>
<dia:attribute name="obj_bb"><dia:rectangle val="{x-0.05},{y-0.05};{x+w+0.05},{y+h+0.05}"/></dia:attribute>
<dia:attribute name="elem_corner"><dia:point val="{x},{y}"/></dia:attribute>
<dia:attribute name="elem_width"><dia:real val="{w}"/></dia:attribute>
<dia:attribute name="elem_height"><dia:real val="{h}"/></dia:attribute>
<dia:attribute name="name"><dia:string>#{name}#</dia:string></dia:attribute>
<dia:attribute name="stereotype"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="comment"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="abstract"><dia:boolean val="{ab}"/></dia:attribute>
<dia:attribute name="suppress_attributes"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="suppress_operations"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="visible_attributes"><dia:boolean val="true"/></dia:attribute>
<dia:attribute name="visible_operations"><dia:boolean val="true"/></dia:attribute>
<dia:attribute name="visible_comments"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="wrap_operations"><dia:boolean val="true"/></dia:attribute>
<dia:attribute name="wrap_after_char"><dia:int val="40"/></dia:attribute>
<dia:attribute name="comment_line_length"><dia:int val="17"/></dia:attribute>
<dia:attribute name="comment_tagging"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="line_width"><dia:real val="0.1"/></dia:attribute>
<dia:attribute name="line_color"><dia:color val="#000000"/></dia:attribute>
<dia:attribute name="fill_color"><dia:color val="#ffffff"/></dia:attribute>
<dia:attribute name="text_color"><dia:color val="#000000"/></dia:attribute>
<dia:attribute name="normal_font"><dia:font family="monospace" style="0" name="Courier"/></dia:attribute>
<dia:attribute name="abstract_font"><dia:font family="monospace" style="8" name="Courier-Oblique"/></dia:attribute>
<dia:attribute name="polymorphic_font"><dia:font family="monospace" style="0" name="Courier"/></dia:attribute>
<dia:attribute name="classname_font"><dia:font family="sans" style="80" name="Helvetica-Bold"/></dia:attribute>
<dia:attribute name="abstract_classname_font"><dia:font family="sans" style="88" name="Helvetica-BoldOblique"/></dia:attribute>
<dia:attribute name="comment_font"><dia:font family="sans" style="0" name="Helvetica"/></dia:attribute>
<dia:attribute name="normal_font_height"><dia:real val="0.8"/></dia:attribute>
<dia:attribute name="polymorphic_font_height"><dia:real val="0.8"/></dia:attribute>
<dia:attribute name="abstract_font_height"><dia:real val="0.8"/></dia:attribute>
<dia:attribute name="classname_font_height"><dia:real val="1"/></dia:attribute>
<dia:attribute name="abstract_classname_font_height"><dia:real val="1"/></dia:attribute>
<dia:attribute name="comment_font_height"><dia:real val="0.7"/></dia:attribute>
<dia:attribute name="attributes">{attrs_xml}</dia:attribute>
<dia:attribute name="operations">{ops_xml}</dia:attribute>
<dia:attribute name="template"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="templates"/>
</dia:object>"""
        self.objs.append(xml)
        self.classes[name] = (oid, x, y, w, h, len(ops) + len(attrs))
        return name

    @staticmethod
    def _oplen(o):
        n, t, vis, inh, params = o
        return len(n) + 4 + sum(len(p[0]) + len(p[1]) + 3 for p in params) + len(t)

    # geometry helpers
    def top(self, c):    _, x, y, w, h, _ = self.classes[c]; return (x + w / 2, y)
    def bottom(self, c): _, x, y, w, h, _ = self.classes[c]; return (x + w / 2, y + h)
    def left(self, c):   _, x, y, w, h, _ = self.classes[c]; return (x, y + h / 2)
    def right(self, c):  _, x, y, w, h, _ = self.classes[c]; return (x + w, y + h / 2)
    def center_cp(self, c): return 8 + 2 * self.classes[c][5]
    CP = {"TL": 0, "TM": 1, "TR": 2, "LM": 3, "RM": 4, "BL": 5, "BM": 6, "BR": 7}
    def cp(self, c, where):
        _, x, y, w, h, _ = self.classes[c]
        return {"TL": (x, y), "TM": (x + w / 2, y), "TR": (x + w, y), "LM": (x, y + h / 2),
                "RM": (x + w, y + h / 2), "BL": (x, y + h), "BM": (x + w / 2, y + h), "BR": (x + w, y + h)}[where]

    def _line(self, kind, pts, src, dst, extra="", scp=None, dcp=None):
        oid = self.nid()
        if len(pts) == 2:  # orthogonal lines need >= 3 segments: add a zero-length middle segment
            (x1, y1), (x2, y2) = pts
            xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
            pts = [(x1, y1), (xm, ym), (xm, ym), (x2, y2)]
        orient = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            prev = orient[-1] if orient else None
            if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
                orient.append(1 - prev if prev is not None else 1)
            else:
                orient.append(0 if abs(y1 - y2) < 1e-6 else 1)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pxml = "".join(f'<dia:point val="{round(x,3)},{round(y,3)}"/>' for x, y in pts)
        oxml = "".join(f'<dia:enum val="{o}"/>' for o in orient)
        xml = f"""<dia:object type="UML - {kind}" version="1" id="{oid}">
<dia:attribute name="obj_pos"><dia:point val="{round(pts[0][0],3)},{round(pts[0][1],3)}"/></dia:attribute>
<dia:attribute name="obj_bb"><dia:rectangle val="{min(xs)-0.5},{min(ys)-0.5};{max(xs)+0.5},{max(ys)+0.5}"/></dia:attribute>
<dia:attribute name="meta"><dia:composite type="dict"/></dia:attribute>
<dia:attribute name="orth_points">{pxml}</dia:attribute>
<dia:attribute name="orth_orient">{oxml}</dia:attribute>
<dia:attribute name="orth_autoroute"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="text_colour"><dia:color val="#000000"/></dia:attribute>
<dia:attribute name="line_colour"><dia:color val="#000000"/></dia:attribute>
<dia:attribute name="name"><dia:string>##</dia:string></dia:attribute>
<dia:attribute name="stereotype"><dia:string>##</dia:string></dia:attribute>
{extra}<dia:connections>
<dia:connection handle="0" to="{self.classes[src][0]}" connection="{self.CP[scp] if scp else self.center_cp(src)}"/>
<dia:connection handle="1" to="{self.classes[dst][0]}" connection="{self.CP[dcp] if dcp else self.center_cp(dst)}"/>
</dia:connections>
</dia:object>"""
        self.objs.append(xml)

    def generalization(self, child, parent, ymid):
        cx, cy = self.top(child); px, py = self.bottom(parent)
        self._line("Generalization", [(cx, cy), (cx, ymid), (px, ymid), (px, py)], child, parent)

    def generalization_pts(self, pts, child, parent, scp=None, dcp=None):
        self._line("Generalization", pts, child, parent, scp=scp, dcp=dcp)

    def dependency(self, pts, src, dst, scp=None, dcp=None):
        self._line("Dependency", pts, src, dst,
                   '<dia:attribute name="draw_arrow"><dia:boolean val="true"/></dia:attribute>\n', scp, dcp)

    def text(self, s, x, y):
        oid = self.nid()
        s = escape(s)
        self.objs.append(f"""<dia:object type="Standard - Text" version="1" id="{oid}">
<dia:attribute name="obj_pos"><dia:point val="{x},{y}"/></dia:attribute>
<dia:attribute name="obj_bb"><dia:rectangle val="{x},{y-0.7};{x+5},{y+0.2}"/></dia:attribute>
<dia:attribute name="text"><dia:composite type="text">
<dia:attribute name="string"><dia:string>#{s}#</dia:string></dia:attribute>
<dia:attribute name="font"><dia:font family="sans" style="0" name="Helvetica"/></dia:attribute>
<dia:attribute name="height"><dia:real val="0.8"/></dia:attribute>
<dia:attribute name="pos"><dia:point val="{x},{y}"/></dia:attribute>
<dia:attribute name="color"><dia:color val="#000000"/></dia:attribute>
<dia:attribute name="alignment"><dia:enum val="0"/></dia:attribute>
</dia:composite></dia:attribute>
<dia:attribute name="valign"><dia:enum val="3"/></dia:attribute>
</dia:object>""")

    def save(self, path):
        body = "\n".join(self.objs)
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">
<dia:diagramdata>
<dia:attribute name="background"><dia:color val="#ffffff"/></dia:attribute>
<dia:attribute name="pagebreak"><dia:color val="#000099"/></dia:attribute>
<dia:attribute name="paper"><dia:composite type="paper">
<dia:attribute name="name"><dia:string>#A4#</dia:string></dia:attribute>
<dia:attribute name="tmargin"><dia:real val="2.8222"/></dia:attribute>
<dia:attribute name="bmargin"><dia:real val="2.8222"/></dia:attribute>
<dia:attribute name="lmargin"><dia:real val="2.8222"/></dia:attribute>
<dia:attribute name="rmargin"><dia:real val="2.8222"/></dia:attribute>
<dia:attribute name="is_portrait"><dia:boolean val="false"/></dia:attribute>
<dia:attribute name="scaling"><dia:real val="1"/></dia:attribute>
<dia:attribute name="fitto"><dia:boolean val="false"/></dia:attribute>
</dia:composite></dia:attribute>
<dia:attribute name="grid"><dia:composite type="grid">
<dia:attribute name="width_x"><dia:real val="1"/></dia:attribute>
<dia:attribute name="width_y"><dia:real val="1"/></dia:attribute>
<dia:attribute name="visible_x"><dia:int val="1"/></dia:attribute>
<dia:attribute name="visible_y"><dia:int val="1"/></dia:attribute>
<dia:composite type="color"/>
</dia:composite></dia:attribute>
<dia:attribute name="color"><dia:color val="#d8e5e5"/></dia:attribute>
<dia:attribute name="guides"><dia:composite type="guides">
<dia:attribute name="hguides"/><dia:attribute name="vguides"/>
</dia:composite></dia:attribute>
</dia:diagramdata>
<dia:layer name="Arrière-plan" visible="true" active="true">
{body}
</dia:layer>
</dia:diagram>
"""
        with gzip.open(path, "wb") as f:
            f.write(xml.encode("utf-8"))


ENVOYER = ("envoyer", "void", PUB, LEAF, [("destinataire", "String"), ("message", "String")])
ENVOYER_ABS = ("envoyer", "void", PUB, ABSTRACT, [("destinataire", "String"), ("message", "String")])


def _column_children(d, parent, children):
    """Generalizations from the left side of each stacked child up to the parent's bottom-left corner."""
    px, py = d.cp(parent, "BL")
    for c in children:
        lx, ly = d.cp(c, "LM")
        d.generalization_pts([(lx, ly), (px, ly), (px, py)], c, parent, "LM", "BL")


def _use(d, src, dst, scp, dcp):
    (x1, y1), (x2, y2) = d.cp(src, scp), d.cp(dst, dcp)
    if scp == "LM" and dcp == "TM":
        pts = [(x1, y1), (x2, y1), (x2, y2)]
    elif scp == "RM" and dcp == "TM":
        pts = [(x1, y1), (x2, y1), (x2, y2)]
    elif scp == "BM" and dcp == "TM":
        ym = (y1 + y2) / 2
        pts = [(x1, y1), (x1, ym), (x2, ym), (x2, y2)]
    elif scp == "BM" and dcp == "RM":
        pts = [(x1, y1), (x1, y2), (x2, y2)]
    else:  # LM -> RM, straight line
        pts = [(x1, y1), (x2, y2)]
    d.dependency(pts, src, dst, scp, dcp)
    return pts


def variante_factory_method(path):
    d = Diagram()
    d.cls("Client", 30, 2, [("main", "void", PUB, LEAF, [("args", "String[]")])])
    d.cls("Notification", 2, 10, [ENVOYER_ABS], abstract=True)
    d.cls("EmailNotification", 6, 17, [ENVOYER])
    d.cls("SMSNotification", 6, 24, [ENVOYER])
    d.cls("PushNotification", 6, 31, [ENVOYER])
    d.cls("NotificationFactory", 38, 17,
          [("creerNotification", "Notification", PUB, LEAF, [("canal", "String")])])
    prods = ("EmailNotification", "SMSNotification", "PushNotification")
    _column_children(d, "Notification", prods)
    _use(d, "Client", "Notification", "LM", "TM")
    _use(d, "Client", "NotificationFactory", "BM", "TM")
    for c in prods:
        pts = _use(d, "NotificationFactory", c, "BM", "RM")
        (x2, y2) = pts[-1]
        d.text("<<instantiate>>", x2 + 2.5, y2 - 0.3)
    d.save(path)


def variante_fabrique_abstraite(path):
    d = Diagram()
    d.cls("Client", 30, 2, [("main", "void", PUB, LEAF, [("args", "String[]")])])
    d.cls("Notification", 2, 10, [ENVOYER_ABS], abstract=True)
    d.cls("EmailNotification", 6, 17, [ENVOYER])
    d.cls("SMSNotification", 6, 24, [ENVOYER])
    d.cls("PushNotification", 6, 31, [ENVOYER])
    d.cls("NotificationFactory", 40, 10, [
        ("notifier", "void", PUB, LEAF, [("destinataire", "String"), ("message", "String")]),
        ("creerNotification", "Notification", PROT, ABSTRACT, []),
    ], abstract=True)
    d.cls("EmailNotificationFactory", 44, 17, [("creerNotification", "Notification", PROT, LEAF, [])])
    d.cls("SMSNotificationFactory", 44, 24, [("creerNotification", "Notification", PROT, LEAF, [])])
    d.cls("PushNotificationFactory", 44, 31, [("creerNotification", "Notification", PROT, LEAF, [])])
    prods = ("EmailNotification", "SMSNotification", "PushNotification")
    facts = ("EmailNotificationFactory", "SMSNotificationFactory", "PushNotificationFactory")
    _column_children(d, "Notification", prods)
    _column_children(d, "NotificationFactory", facts)
    _use(d, "Client", "Notification", "LM", "TM")
    _use(d, "Client", "NotificationFactory", "RM", "TM")
    for f, c in zip(facts, prods):
        pts = _use(d, f, c, "LM", "RM")
        (x1, y1), (x2, _) = pts[0], pts[-1]
        d.text("<<instantiate>>", (x1 + x2) / 2 - 2.5, y1 - 0.3)
    d.save(path)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    variante_factory_method(os.path.join(out, "notification_factory_method.dia"))
    variante_fabrique_abstraite(os.path.join(out, "notification_factory_abstraite.dia"))
    print("ok")
