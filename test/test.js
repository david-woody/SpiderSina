/**
 * Created by Administrator on 2016/6/7.
 */
<
script >
var FM = function (a, b, c) {
    function bN(b, c) {
        a.clear && (bN = a.clear)(b, c)
    }

    function bM(b, c, d) {
        a.start && (bM = a.start)(b, c, d)
    }

    function bL(a) {
        return a === null ? "" : Object.prototype.toString.call(a).slice(8, -1).toLowerCase()
    }

    function bK() {
        bv(function () {
            bH();
            for (var a in J) {
                if (I[a]) {
                    bB(P, I[a]);
                    delete I[a]
                }
                J[a]()
            }
            J = {}
        })
    }

    function bJ(a) {
        function v() {
            if (k.indexOf(bI) != 0)throw"view: csstextkey must have *" + bI + "* as prefix.";
            T(k) || bo(j, k)
        }

        function u() {
            function d() {
                --a <= 0 && t()
            }

            j && cssloadCssText();
            var a, b, c = -1;
            g = [].concat(g || []);
            i = [].concat(i || []);
            if (a = g.length) {
                h(t, K);
                while (b = g[++c])T(b) ? d() : bk(b, d, i[c])
            } else t()
        }

        function t() {
            if (!t.r) {
                t.r = 1;
                bB(M, a);
                a[P] ? r() : s()
            }
        }

        function s() {
            function b(b) {
                r();
                b || a[P] || bH()
            }

            d ? bv(function () {
                bF(d, function (f) {
                    if (!a[P] && f && e != c) {
                        bG(f, d);
                        f.innerHTML = e || "";
                        br(b);
                        delete a.html
                    } else b(!0)
                })
            }) : b(!0)
        }

        function r() {
            bB(N, a);
            a[P] ? p() : q()
        }

        function q() {
            function a() {
                bA(f, p, m)
            }

            f ? l ? h(a, l) : a() : p()
        }

        function p() {
            if (!a[P]) {
                if (b) {
                    bN(b, d);
                    bM(b, d, a)
                }
                bD(o, a)
            }
            bB(O, a)
        }

        a = a || {};
        var b = a.ns, d = a.domid, e = a.html, f = a.js, g = a.css, i = a.cssid, j = a.csstext, k = a.csstextkey = a.csstextkey || bI + "_" + x(), l = a.jsDely || 0, m = a.jsDefer, n = a.renderDely || 0, o = d || b;
        if (!!o) {
            bC(o, a);
            bB(L, a);
            n ? h(u, n) : u()
        }
    }

    function bH() {
        for (var a in J)bF(a, J[a])
    }

    function bG(a, b) {
        var c, d, e;
        for (c in H)if ((d = H[c].domid) && (d === b || (e = p(d)) && bw(a, e))) {
            bN(H[c].ns, d);
            delete H[c]
        }
    }

    function bF(a, b) {
        var c, d;
        if (d = J[a]) {
            d != b && d();
            delete J[a]
        }
        !(c = p(a)) || bE(c) ? J[a] = b : b(c)
    }

    function bE(a) {
        var b, c, d;
        for (c in I)if (!(d = I[c])[N] && (b = d.domid) && (b = p(b)) && bw(b, a))return !0
    }

    function bD(a, b) {
        if (I[a] == b) {
            H[a] = I[a];
            delete I[a]
        }
    }

    function bC(a, b) {
        I[a] && bB(P, I[a]);
        I[a] = b
    }

    function bB(a, b) {
        b[a] = r();
        G(a, b)
    }

    function bA(a, d, e) {
        var f = d, i;
        if (by && by !== a)bz.push(arguments); else {
            if (!by && e) {
                by = a;
                d = function (a, d) {
                    by = c;
                    while (i = bz.shift()) {
                        bA.apply(b, i);
                        if (i[2])break
                    }
                    f(a, d)
                }
            }
            bx && (a = bx(a));
            if (!Y(a, d)) {
                var k = bd("script"), l = !1, m, n;
                bh(k, "src", a);
                bh(k, "charset", "UTF-8");
                m = k.onerror = k.onload = k.onreadystatechange = function () {
                    if (!l && (!k.readyState || /loaded|complete/.test(k.readyState))) {
                        l = !0;
                        j(n);
                        k.onerror = k.onload = k.onreadystatechange = null;
                        g.removeChild(k);
                        Z(a)
                    }
                };
                n = h(m, 3e4);
                g.insertBefore(k, g.firstChild)
            }
        }
    }

    function bv(a) {
        bs.push(a);
        bt || bu()
    }

    function bu() {
        if (bs.length > 0) {
            bt = 1;
            bs.shift()();
            br(bu)
        } else bt = 0
    }

    function bq() {
        var a = {}, b, c, d;
        for (c in H)if (b = H[c].css || H[c].csstextkey) {
            b = [].concat(b);
            for (d = b.length; --d > -1;)b[d] && (a[b[d]] = 1)
        }
        U(a);
        bn(a)
    }

    function bp(a) {
        return a
    }

    function bo(a, b) {
        var c, d;
        if (!Y(b)) {
            c = x();
            d = bd("style");
            bh(d, "type", "text/css");
            bh(d, "id", c);
            g.appendChild(d);
            try {
                d.styleSheet.cssText = a
            } catch (f) {
                d.appendChild(e.createTextNode(a))
            }
            bi[b] = c
        }
    }

    function bn(a) {
        var b = {}, c;
        for (c in a)b[bp(c)] = 1;
        for (c in bi)if (!b[c]) {
            bm(c);
            $(c)
        }
    }

    function bm(a) {
        var b = bi[a], c, d, e = p(b);
        if (e) {
            if (m && b in bj) {
                d = b && bj[b];
                if (d && (c = A(a, d)) > -1) {
                    (e.styleSheet || e.sheet).removeImport(c);
                    d.splice(c, 1)
                }
            } else R(e);
            delete bi[a]
        }
    }

    function bl(a) {
        var b, c;
        if (m) {
            for (b in bj)if (bj[b].length < 31) {
                c = p(b);
                break
            }
            if (!c) {
                b = x();
                c = bd("style");
                bh(c, "type", "text/css");
                bh(c, "id", b);
                g.appendChild(c);
                bj[b] = []
            }
            (c.styleSheet || c.sheet).addImport(a);
            bj[b].push(a)
        } else {
            b = x();
            var d = bd("link");
            bh(d, "rel", "stylesheet");
            bh(d, "type", "text/css");
            bh(d, "href", a);
            bh(d, "id", b);
            g.appendChild(d)
        }
        bi[a] = b
    }

    function bk(a, c, d) {
        function j() {
            if (parseInt(b.getComputedStyle ? getComputedStyle(e, null)[f] : e.currentStyle && e.currentStyle[f]) === 42)i(); else if (--g > 0)h(j, 10); else {
                i();
                bm(a);
                bl(a)
            }
        }

        function i() {
            bg(e);
            Z(a)
        }

        a = bp(a);
        var e, f = "height", g = 3e3;
        if (!Y(a, c)) {
            bl(a);
            e = bd("div");
            e.id = d;
            bf(e);
            h(j, 50)
        }
    }

    function bh(a, b, c) {
        return a.setAttribute(b, c)
    }

    function bg(a) {
        be && be.removeChild(a)
    }

    function bf(a) {
        if (!be) {
            (be = bd("div")).style.cssText = "position:absolute;top:-9999px;";
            g.appendChild(be)
        }
        be.appendChild(a)
    }

    function bd(a) {
        return e.createElement(a)
    }

    function bc(a, b) {
        b && (b[ba] = b[2] - b[1] + 2);
        return function (c) {
            return !c || /^https?\:\/\//.test(c.toLowerCase()) ? c : (b ? _[c] || (_[c] = bb(b, c)) : a) + c
        }
    }

    function bb(a, b) {
        b = b.replace(/\?.*$/, "");
        var c = 0, d = 0, e, f;
        while (e = b.charCodeAt(c++))d += e;
        return a[0].replace("{n}", d % a[ba] || "")
    }

    function $(a) {
        W[a] && delete W[a];
        a in V && delete V[a]
    }

    function Z(a, b) {
        V[a] = b;
        G(X + a, b);
        F(X + a)
    }

    function Y(a, b) {
        if (a in V) {
            b && b(a, V[a]);
            return !0
        }
        b && E(X + a, function (c, d) {
            b(a, d)
        });
        if (W[a])return !0;
        W[a] = 1
    }

    function U(a) {
        var b = {}, c, d, e;
        for (d in S) {
            c = S[d].ins;
            for (e in c)if (a[e]) {
                b[d] = !0;
                break
            }
        }
        for (d in S)if (!b[d]) {
            R(S[d].el);
            delete S[d]
        }
    }

    function T(a) {
        for (var b in S)if (S[b].ins[a])return !0
    }

    function R(a) {
        a && a.parentNode.removeChild(a)
    }

    function Q(a) {
        try {
            return [].slice.call(a)
        } catch (b) {
            var c, d = 0, e = [];
            while (c = a[d])e[d++] = c;
            return e
        }
    }

    function G(a, b) {
        var d = D(a);
        b = [].concat(b || []);
        for (var e = d.length - 1; e > -1; e--)try {
            d[e] && d[e].apply(c, b)
        } catch (f) {
            a != n && G(n, ["[error][notice][" + a + "]", f])
        }
    }

    function F(a, b) {
        var c = D(a), d, e;
        if (b)(d = A(b, c)) > -1 && (e = 1); else {
            d = 0;
            e = c.length
        }
        e && c.splice(d, e)
    }

    function E(a, b) {
        D(a).unshift(b)
    }

    function D(a) {
        return C[a] || (C[a] = [])
    }

    function A(a, b) {
        if (b.indexOf)return b.indexOf(a);
        for (var c = 0, d = b.length; c < d; ++c)if (b[c] === a)return c;
        return -1
    }

    function z(a) {
        return a[y] || (a[y] = x())
    }

    function x() {
        return w + v++
    }

    function u(a) {
        t.push(a)
    }

    function r() {
        return Date.now ? Date.now() : +(new Date)
    }

    function q(a, b) {
        return (b || e).getElementsByTagName(a)
    }

    function p(a) {
        return e.getElementById(a)
    }

    function o() {
    }

    if (a)return a;
    !!b.sessionStorage && !!b.history.pushState && b.scrollTo(0, 0);
    a = a || {v: 2, t: r()};
    var d = navigator.userAgent, e = b.document, f = e.documentElement, g = e.head || q("head")[0] || f, h = b.setTimeout, i = b.location, j = b.clearTimeout, k = b.decodeURI, l = e.addEventListener, m = /msie (\d+\.\d+)/i.test(d) ? e.documentMode || +RegExp.$1 : 0, n = "log", s = "_I", t = a[s] = a[s] || [];
    a.init = function (a) {
        a = a || {};
        var b = "linkFilter", c = "history", d = "iLoader";
        b in a || (a[b] = !0);
        c in a || (a[c] = !0);
        d in a || (a[d] = !0);
        var e;
        while (e = t.shift())e(a)
    };
    var v = 1, w = "FM_" + r(), y = "__FM_ID", B = "_N", C = a[B] = a[B] || {}, H = {}, I = {}, J = {}, K = 5e3, L = "plViewReady", M = "plCssReady", N = "plRenderReady", O = "plJsReady", P = "plAbort", S = {};
    u(function () {
        var a = Q(q("link")).concat(Q(q("style"))), b, c, d;
        for (var e = 0; d = a[e++];)if (b = d.getAttribute("includes")) {
            c = z(d);
            b = b.split("|");
            var f = {};
            for (var g = 0; b[g];)f[b[g++]] = 1;
            S[c] = {el: d, ins: f}
        }
    });
    var V = {}, W = {}, X = x(), _ = {}, ba = "MODN", be, bi = {}, bj = {};
    u(function (a) {
        bp = bc(a.cssPath || "", a.mCssPath)
    });
    var br = function () {
        var a = b.requestAnimationFrame || b.webkitRequestAnimationFrame || b.mozRequestAnimationFrame || b.oRequestAnimationFrame || b.msRequestAnimationFrame, c = function (a) {
            return h(a, 2)
        };
        a && a(function () {
            c = a
        });
        return function (a) {
            return c(function () {
                a()
            })
        }
    }(), bs = [], bt = 0, bw = f.contains ? function (a, b) {
        a = a === e ? f : a;
        b = b.parentNode;
        return a === b || !!(b && a.contains && a.contains(b))
    } : f.compareDocumentPosition ? function (a, b) {
        return !!(a.compareDocumentPosition(b) & 16)
    } : function (a, b) {
        while (b = b.parentNode)if (b === a)return !0;
        return !1
    }, bx, by, bz = [];
    u(function (a) {
        bx = bc(a.jsPath || "", a.mJsPath)
    });
    var bI = "csstext:";
    u(function (a) {
        var b = a.cssTimeOut;
        bL(b) === "number" && (K = b)
    });
    E("vf", bK);
    E("vd", bq);
    var bO = "_NC", bP = G;
    G = function (b, c) {
        bP(b, c);
        a[bO] && a[bO].push(arguments)
    };
    a[bO] = [];
    a.view = bJ;
    a.getViews = function () {
        return H
    };
    return a
}(FM, window);
!function () {
    function e(a) {
        return "js_" + a.replace(/^\/?(.*)\.css\??.*$/i, "$1").replace(/\//g, "_")
    }

    function d(a) {
        var b;
        if (a && ((b = a.match(c("pl"))) || (b = a.match(c("trustPagelet")))))return b[1].replace(/\//g, ".")
    }

    function c(a) {
        return new RegExp("^.*?\\/(" + a + "\\/.*?)(_[a-z\\d]{16})?\\.js\\??.*$")
    }

    var a = $CONFIG, b = FM.view;
    FM.init({jsPath: a.jsPath, cssPath: a.cssPath, mJsPath: a.mJsPath});
    FM.view = function (a) {
        a = a || {};
        var c = a.js, f = "domid", g = "ns", h, i;
        c = c && [].concat(c);
        a[f] = a[f] || a.pid;
        a.js = c = c && c[0];
        g in a || (a[g] = d(c));
        a.css = h = [].concat(a.css || []);
        a.cssid = i = [].concat(a.cssid || []);
        for (var j = i.length, k = h.length; j < k; ++j)i[j] = e(h[j]);
        b(a)
    }
}()
< / script >
