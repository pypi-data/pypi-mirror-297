const {
  SvelteComponent: _a,
  assign: ca,
  create_slot: da,
  detach: ma,
  element: ha,
  get_all_dirty_from_scope: ga,
  get_slot_changes: ba,
  get_spread_update: wa,
  init: pa,
  insert: va,
  safe_not_equal: ka,
  set_dynamic_element_data: Rl,
  set_style: fe,
  toggle_class: Me,
  transition_in: go,
  transition_out: bo,
  update_slot_base: ya
} = window.__gradio__svelte__internal;
function Ca(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = da(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let r = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let a = 0; a < r.length; a += 1)
    f = ca(f, r[a]);
  return {
    c() {
      e = ha(
        /*tag*/
        l[14]
      ), o && o.c(), Rl(
        /*tag*/
        l[14]
      )(e, f), Me(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), Me(
        e,
        "padded",
        /*padding*/
        l[6]
      ), Me(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), Me(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), Me(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), fe(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), fe(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), fe(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), fe(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), fe(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), fe(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), fe(e, "border-width", "var(--block-border-width)");
    },
    m(a, s) {
      va(a, e, s), o && o.m(e, null), n = !0;
    },
    p(a, s) {
      o && o.p && (!n || s & /*$$scope*/
      131072) && ya(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? ba(
          i,
          /*$$scope*/
          a[17],
          s,
          null
        ) : ga(
          /*$$scope*/
          a[17]
        ),
        null
      ), Rl(
        /*tag*/
        a[14]
      )(e, f = wa(r, [
        (!n || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!n || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!n || s & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Me(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), Me(
        e,
        "padded",
        /*padding*/
        a[6]
      ), Me(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), Me(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), Me(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), s & /*height*/
      1 && fe(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), s & /*width*/
      2 && fe(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), s & /*variant*/
      16 && fe(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), s & /*allow_overflow*/
      2048 && fe(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && fe(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), s & /*min_width*/
      8192 && fe(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (go(o, a), n = !0);
    },
    o(a) {
      bo(o, a), n = !1;
    },
    d(a) {
      a && ma(e), o && o.d(a);
    }
  };
}
function qa(l) {
  let e, t = (
    /*tag*/
    l[14] && Ca(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (go(t, n), e = !0);
    },
    o(n) {
      bo(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function za(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: r = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: s = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: d = "normal" } = e, { test_id: c = void 0 } = e, { explicit_call: m = !1 } = e, { container: h = !0 } = e, { visible: p = !0 } = e, { allow_overflow: v = !0 } = e, { scale: g = null } = e, { min_width: w = 0 } = e, b = d === "fieldset" ? "fieldset" : "div";
  const L = (q) => {
    if (q !== void 0) {
      if (typeof q == "number")
        return q + "px";
      if (typeof q == "string")
        return q;
    }
  };
  return l.$$set = (q) => {
    "height" in q && t(0, o = q.height), "width" in q && t(1, r = q.width), "elem_id" in q && t(2, f = q.elem_id), "elem_classes" in q && t(3, a = q.elem_classes), "variant" in q && t(4, s = q.variant), "border_mode" in q && t(5, u = q.border_mode), "padding" in q && t(6, _ = q.padding), "type" in q && t(16, d = q.type), "test_id" in q && t(7, c = q.test_id), "explicit_call" in q && t(8, m = q.explicit_call), "container" in q && t(9, h = q.container), "visible" in q && t(10, p = q.visible), "allow_overflow" in q && t(11, v = q.allow_overflow), "scale" in q && t(12, g = q.scale), "min_width" in q && t(13, w = q.min_width), "$$scope" in q && t(17, i = q.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    m,
    h,
    p,
    v,
    g,
    w,
    b,
    L,
    d,
    i,
    n
  ];
}
class Sa extends _a {
  constructor(e) {
    super(), pa(this, e, za, qa, ka, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: La,
  append: Mn,
  attr: $t,
  create_component: Ea,
  destroy_component: ja,
  detach: Fa,
  element: Nl,
  init: Ia,
  insert: Da,
  mount_component: Aa,
  safe_not_equal: Ma,
  set_data: Ba,
  space: Ta,
  text: Ra,
  toggle_class: nt,
  transition_in: Na,
  transition_out: Ua
} = window.__gradio__svelte__internal;
function Va(l) {
  let e, t, n, i, o, r;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Nl("label"), t = Nl("span"), Ea(n.$$.fragment), i = Ta(), o = Ra(
        /*label*/
        l[0]
      ), $t(t, "class", "svelte-9gxdi0"), $t(e, "for", ""), $t(e, "data-testid", "block-label"), $t(e, "class", "svelte-9gxdi0"), nt(e, "hide", !/*show_label*/
      l[2]), nt(e, "sr-only", !/*show_label*/
      l[2]), nt(
        e,
        "float",
        /*float*/
        l[4]
      ), nt(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      Da(f, e, a), Mn(e, t), Aa(n, t, null), Mn(e, i), Mn(e, o), r = !0;
    },
    p(f, [a]) {
      (!r || a & /*label*/
      1) && Ba(
        o,
        /*label*/
        f[0]
      ), (!r || a & /*show_label*/
      4) && nt(e, "hide", !/*show_label*/
      f[2]), (!r || a & /*show_label*/
      4) && nt(e, "sr-only", !/*show_label*/
      f[2]), (!r || a & /*float*/
      16) && nt(
        e,
        "float",
        /*float*/
        f[4]
      ), (!r || a & /*disable*/
      8) && nt(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      r || (Na(n.$$.fragment, f), r = !0);
    },
    o(f) {
      Ua(n.$$.fragment, f), r = !1;
    },
    d(f) {
      f && Fa(e), ja(n);
    }
  };
}
function Oa(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, r = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, r, f];
}
let Pa = class extends La {
  constructor(e) {
    super(), Ia(this, e, Oa, Va, Ma, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
};
const {
  SvelteComponent: Za,
  append: rl,
  attr: Ye,
  bubble: Wa,
  create_component: Ha,
  destroy_component: Xa,
  detach: wo,
  element: fl,
  init: Ga,
  insert: po,
  listen: Ka,
  mount_component: Ya,
  safe_not_equal: Ja,
  set_data: Qa,
  set_style: Lt,
  space: xa,
  text: $a,
  toggle_class: le,
  transition_in: es,
  transition_out: ts
} = window.__gradio__svelte__internal;
function Ul(l) {
  let e, t;
  return {
    c() {
      e = fl("span"), t = $a(
        /*label*/
        l[1]
      ), Ye(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      po(n, e, i), rl(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Qa(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && wo(e);
    }
  };
}
function ns(l) {
  let e, t, n, i, o, r, f, a = (
    /*show_label*/
    l[2] && Ul(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = fl("button"), a && a.c(), t = xa(), n = fl("div"), Ha(i.$$.fragment), Ye(n, "class", "svelte-1lrphxw"), le(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), le(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), le(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Ye(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Ye(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Ye(
        e,
        "title",
        /*label*/
        l[1]
      ), Ye(e, "class", "svelte-1lrphxw"), le(
        e,
        "pending",
        /*pending*/
        l[3]
      ), le(
        e,
        "padded",
        /*padded*/
        l[5]
      ), le(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), le(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Lt(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Lt(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Lt(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(s, u) {
      po(s, e, u), a && a.m(e, null), rl(e, t), rl(e, n), Ya(i, n, null), o = !0, r || (f = Ka(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), r = !0);
    },
    p(s, [u]) {
      /*show_label*/
      s[2] ? a ? a.p(s, u) : (a = Ul(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && le(
        n,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || u & /*size*/
      16) && le(
        n,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || u & /*size*/
      16) && le(
        n,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || u & /*label*/
      2) && Ye(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || u & /*hasPopup*/
      256) && Ye(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || u & /*label*/
      2) && Ye(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || u & /*pending*/
      8) && le(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || u & /*padded*/
      32) && le(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || u & /*highlight*/
      64) && le(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || u & /*transparent*/
      512) && le(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), u & /*disabled, _color*/
      4224 && Lt(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Lt(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), u & /*offset*/
      2048 && Lt(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (es(i.$$.fragment, s), o = !0);
    },
    o(s) {
      ts(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && wo(e), a && a.d(), Xa(i), r = !1, f();
    }
  };
}
function ls(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: s = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: d = !1 } = e, { color: c = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: h = "var(--background-fill-primary)" } = e, { offset: p = 0 } = e;
  function v(g) {
    Wa.call(this, l, g);
  }
  return l.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, o = g.label), "show_label" in g && t(2, r = g.show_label), "pending" in g && t(3, f = g.pending), "size" in g && t(4, a = g.size), "padded" in g && t(5, s = g.padded), "highlight" in g && t(6, u = g.highlight), "disabled" in g && t(7, _ = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, c = g.color), "transparent" in g && t(9, m = g.transparent), "background" in g && t(10, h = g.background), "offset" in g && t(11, p = g.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : c);
  }, [
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    d,
    m,
    h,
    p,
    n,
    c,
    v
  ];
}
let St = class extends Za {
  constructor(e) {
    super(), Ga(this, e, ls, ns, Ja, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
};
const {
  SvelteComponent: is,
  append: os,
  attr: Bn,
  binding_callbacks: as,
  create_slot: ss,
  detach: rs,
  element: Vl,
  get_all_dirty_from_scope: fs,
  get_slot_changes: us,
  init: _s,
  insert: cs,
  safe_not_equal: ds,
  toggle_class: lt,
  transition_in: ms,
  transition_out: hs,
  update_slot_base: gs
} = window.__gradio__svelte__internal;
function bs(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = ss(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Vl("div"), t = Vl("div"), o && o.c(), Bn(t, "class", "icon svelte-3w3rth"), Bn(e, "class", "empty svelte-3w3rth"), Bn(e, "aria-label", "Empty value"), lt(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), lt(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), lt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), lt(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(r, f) {
      cs(r, e, f), os(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(r, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && gs(
        o,
        i,
        r,
        /*$$scope*/
        r[4],
        n ? us(
          i,
          /*$$scope*/
          r[4],
          f,
          null
        ) : fs(
          /*$$scope*/
          r[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && lt(
        e,
        "small",
        /*size*/
        r[0] === "small"
      ), (!n || f & /*size*/
      1) && lt(
        e,
        "large",
        /*size*/
        r[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && lt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        r[1]
      ), (!n || f & /*parent_height*/
      8) && lt(
        e,
        "small_parent",
        /*parent_height*/
        r[3]
      );
    },
    i(r) {
      n || (ms(o, r), n = !0);
    },
    o(r) {
      hs(o, r), n = !1;
    },
    d(r) {
      r && rs(e), o && o.d(r), l[6](null);
    }
  };
}
function ws(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: r = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function s(_) {
    var d;
    if (!_)
      return !1;
    const { height: c } = _.getBoundingClientRect(), { height: m } = ((d = _.parentElement) === null || d === void 0 ? void 0 : d.getBoundingClientRect()) || { height: c };
    return c > m + 2;
  }
  function u(_) {
    as[_ ? "unshift" : "push"](() => {
      a = _, t(2, a);
    });
  }
  return l.$$set = (_) => {
    "size" in _ && t(0, r = _.size), "unpadded_box" in _ && t(1, f = _.unpadded_box), "$$scope" in _ && t(4, o = _.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = s(a));
  }, [r, f, a, n, o, i, u];
}
class ps extends is {
  constructor(e) {
    super(), _s(this, e, ws, bs, ds, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: vs,
  append: Tn,
  attr: ze,
  detach: ks,
  init: ys,
  insert: Cs,
  noop: Rn,
  safe_not_equal: qs,
  set_style: Be,
  svg_element: en
} = window.__gradio__svelte__internal;
function zs(l) {
  let e, t, n, i;
  return {
    c() {
      e = en("svg"), t = en("g"), n = en("path"), i = en("path"), ze(n, "d", "M18,6L6.087,17.913"), Be(n, "fill", "none"), Be(n, "fill-rule", "nonzero"), Be(n, "stroke-width", "2px"), ze(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), ze(i, "d", "M4.364,4.364L19.636,19.636"), Be(i, "fill", "none"), Be(i, "fill-rule", "nonzero"), Be(i, "stroke-width", "2px"), ze(e, "width", "100%"), ze(e, "height", "100%"), ze(e, "viewBox", "0 0 24 24"), ze(e, "version", "1.1"), ze(e, "xmlns", "http://www.w3.org/2000/svg"), ze(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), ze(e, "xml:space", "preserve"), ze(e, "stroke", "currentColor"), Be(e, "fill-rule", "evenodd"), Be(e, "clip-rule", "evenodd"), Be(e, "stroke-linecap", "round"), Be(e, "stroke-linejoin", "round");
    },
    m(o, r) {
      Cs(o, e, r), Tn(e, t), Tn(t, n), Tn(e, i);
    },
    p: Rn,
    i: Rn,
    o: Rn,
    d(o) {
      o && ks(e);
    }
  };
}
class Ll extends vs {
  constructor(e) {
    super(), ys(this, e, null, zs, qs, {});
  }
}
const {
  SvelteComponent: Ss,
  append: Ls,
  attr: Tt,
  detach: Es,
  init: js,
  insert: Fs,
  noop: Nn,
  safe_not_equal: Is,
  svg_element: Ol
} = window.__gradio__svelte__internal;
function Ds(l) {
  let e, t;
  return {
    c() {
      e = Ol("svg"), t = Ol("path"), Tt(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), Tt(t, "fill", "currentColor"), Tt(e, "id", "icon"), Tt(e, "xmlns", "http://www.w3.org/2000/svg"), Tt(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      Fs(n, e, i), Ls(e, t);
    },
    p: Nn,
    i: Nn,
    o: Nn,
    d(n) {
      n && Es(e);
    }
  };
}
class As extends Ss {
  constructor(e) {
    super(), js(this, e, null, Ds, Is, {});
  }
}
const {
  SvelteComponent: Ms,
  append: Bs,
  attr: Et,
  detach: Ts,
  init: Rs,
  insert: Ns,
  noop: Un,
  safe_not_equal: Us,
  svg_element: Pl
} = window.__gradio__svelte__internal;
function Vs(l) {
  let e, t;
  return {
    c() {
      e = Pl("svg"), t = Pl("path"), Et(t, "fill", "currentColor"), Et(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Et(e, "xmlns", "http://www.w3.org/2000/svg"), Et(e, "width", "100%"), Et(e, "height", "100%"), Et(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      Ns(n, e, i), Bs(e, t);
    },
    p: Un,
    i: Un,
    o: Un,
    d(n) {
      n && Ts(e);
    }
  };
}
class El extends Ms {
  constructor(e) {
    super(), Rs(this, e, null, Vs, Us, {});
  }
}
const {
  SvelteComponent: Os,
  append: Ps,
  attr: Se,
  detach: Zs,
  init: Ws,
  insert: Hs,
  noop: Vn,
  safe_not_equal: Xs,
  svg_element: Zl
} = window.__gradio__svelte__internal;
function Gs(l) {
  let e, t;
  return {
    c() {
      e = Zl("svg"), t = Zl("path"), Se(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), Se(e, "xmlns", "http://www.w3.org/2000/svg"), Se(e, "width", "100%"), Se(e, "height", "100%"), Se(e, "viewBox", "0 0 24 24"), Se(e, "fill", "none"), Se(e, "stroke", "currentColor"), Se(e, "stroke-width", "1.5"), Se(e, "stroke-linecap", "round"), Se(e, "stroke-linejoin", "round"), Se(e, "class", "feather feather-edit-2");
    },
    m(n, i) {
      Hs(n, e, i), Ps(e, t);
    },
    p: Vn,
    i: Vn,
    o: Vn,
    d(n) {
      n && Zs(e);
    }
  };
}
class vo extends Os {
  constructor(e) {
    super(), Ws(this, e, null, Gs, Xs, {});
  }
}
const {
  SvelteComponent: Ks,
  append: Wl,
  attr: he,
  detach: Ys,
  init: Js,
  insert: Qs,
  noop: On,
  safe_not_equal: xs,
  svg_element: Pn
} = window.__gradio__svelte__internal;
function $s(l) {
  let e, t, n;
  return {
    c() {
      e = Pn("svg"), t = Pn("path"), n = Pn("polyline"), he(t, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), he(n, "points", "13 2 13 9 20 9"), he(e, "xmlns", "http://www.w3.org/2000/svg"), he(e, "width", "100%"), he(e, "height", "100%"), he(e, "viewBox", "0 0 24 24"), he(e, "fill", "none"), he(e, "stroke", "currentColor"), he(e, "stroke-width", "1.5"), he(e, "stroke-linecap", "round"), he(e, "stroke-linejoin", "round"), he(e, "class", "feather feather-file");
    },
    m(i, o) {
      Qs(i, e, o), Wl(e, t), Wl(e, n);
    },
    p: On,
    i: On,
    o: On,
    d(i) {
      i && Ys(e);
    }
  };
}
let er = class extends Ks {
  constructor(e) {
    super(), Js(this, e, null, $s, xs, {});
  }
};
const {
  SvelteComponent: tr,
  append: Zn,
  attr: Z,
  detach: nr,
  init: lr,
  insert: ir,
  noop: Wn,
  safe_not_equal: or,
  svg_element: tn
} = window.__gradio__svelte__internal;
function ar(l) {
  let e, t, n, i;
  return {
    c() {
      e = tn("svg"), t = tn("rect"), n = tn("circle"), i = tn("polyline"), Z(t, "x", "3"), Z(t, "y", "3"), Z(t, "width", "18"), Z(t, "height", "18"), Z(t, "rx", "2"), Z(t, "ry", "2"), Z(n, "cx", "8.5"), Z(n, "cy", "8.5"), Z(n, "r", "1.5"), Z(i, "points", "21 15 16 10 5 21"), Z(e, "xmlns", "http://www.w3.org/2000/svg"), Z(e, "width", "100%"), Z(e, "height", "100%"), Z(e, "viewBox", "0 0 24 24"), Z(e, "fill", "none"), Z(e, "stroke", "currentColor"), Z(e, "stroke-width", "1.5"), Z(e, "stroke-linecap", "round"), Z(e, "stroke-linejoin", "round"), Z(e, "class", "feather feather-image");
    },
    m(o, r) {
      ir(o, e, r), Zn(e, t), Zn(e, n), Zn(e, i);
    },
    p: Wn,
    i: Wn,
    o: Wn,
    d(o) {
      o && nr(e);
    }
  };
}
let ko = class extends tr {
  constructor(e) {
    super(), lr(this, e, null, ar, or, {});
  }
};
const {
  SvelteComponent: sr,
  append: rr,
  attr: nn,
  detach: fr,
  init: ur,
  insert: _r,
  noop: Hn,
  safe_not_equal: cr,
  svg_element: Hl
} = window.__gradio__svelte__internal;
function dr(l) {
  let e, t;
  return {
    c() {
      e = Hl("svg"), t = Hl("path"), nn(t, "fill", "currentColor"), nn(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), nn(e, "xmlns", "http://www.w3.org/2000/svg"), nn(e, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      _r(n, e, i), rr(e, t);
    },
    p: Hn,
    i: Hn,
    o: Hn,
    d(n) {
      n && fr(e);
    }
  };
}
class mr extends sr {
  constructor(e) {
    super(), ur(this, e, null, dr, cr, {});
  }
}
const {
  SvelteComponent: hr,
  append: Xl,
  attr: ge,
  detach: gr,
  init: br,
  insert: wr,
  noop: Xn,
  safe_not_equal: pr,
  svg_element: Gn
} = window.__gradio__svelte__internal;
function vr(l) {
  let e, t, n;
  return {
    c() {
      e = Gn("svg"), t = Gn("polyline"), n = Gn("path"), ge(t, "points", "1 4 1 10 7 10"), ge(n, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), ge(e, "xmlns", "http://www.w3.org/2000/svg"), ge(e, "width", "100%"), ge(e, "height", "100%"), ge(e, "viewBox", "0 0 24 24"), ge(e, "fill", "none"), ge(e, "stroke", "currentColor"), ge(e, "stroke-width", "2"), ge(e, "stroke-linecap", "round"), ge(e, "stroke-linejoin", "round"), ge(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      wr(i, e, o), Xl(e, t), Xl(e, n);
    },
    p: Xn,
    i: Xn,
    o: Xn,
    d(i) {
      i && gr(e);
    }
  };
}
class yo extends hr {
  constructor(e) {
    super(), br(this, e, null, vr, pr, {});
  }
}
const {
  SvelteComponent: kr,
  append: Kn,
  attr: x,
  detach: yr,
  init: Cr,
  insert: qr,
  noop: Yn,
  safe_not_equal: zr,
  svg_element: ln
} = window.__gradio__svelte__internal;
function Sr(l) {
  let e, t, n, i;
  return {
    c() {
      e = ln("svg"), t = ln("path"), n = ln("polyline"), i = ln("line"), x(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), x(n, "points", "17 8 12 3 7 8"), x(i, "x1", "12"), x(i, "y1", "3"), x(i, "x2", "12"), x(i, "y2", "15"), x(e, "xmlns", "http://www.w3.org/2000/svg"), x(e, "width", "90%"), x(e, "height", "90%"), x(e, "viewBox", "0 0 24 24"), x(e, "fill", "none"), x(e, "stroke", "currentColor"), x(e, "stroke-width", "2"), x(e, "stroke-linecap", "round"), x(e, "stroke-linejoin", "round"), x(e, "class", "feather feather-upload");
    },
    m(o, r) {
      qr(o, e, r), Kn(e, t), Kn(e, n), Kn(e, i);
    },
    p: Yn,
    i: Yn,
    o: Yn,
    d(o) {
      o && yr(e);
    }
  };
}
let Lr = class extends kr {
  constructor(e) {
    super(), Cr(this, e, null, Sr, zr, {});
  }
};
const Er = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Gl = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Er.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Gl[e][t],
      secondary: Gl[e][n]
    }
  }),
  {}
);
class jr extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Fr,
  create_component: Ir,
  destroy_component: Dr,
  init: Ar,
  mount_component: Mr,
  safe_not_equal: Br,
  transition_in: Tr,
  transition_out: Rr
} = window.__gradio__svelte__internal, { createEventDispatcher: Nr } = window.__gradio__svelte__internal;
function Ur(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: As,
      label: (
        /*i18n*/
        l[2]("common.share")
      ),
      pending: (
        /*pending*/
        l[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[5]
  ), {
    c() {
      Ir(e.$$.fragment);
    },
    m(n, i) {
      Mr(e, n, i), t = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      t || (Tr(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Rr(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dr(e, n);
    }
  };
}
function Vr(l, e, t) {
  const n = Nr();
  let { formatter: i } = e, { value: o } = e, { i18n: r } = e, f = !1;
  const a = async () => {
    try {
      t(3, f = !0);
      const s = await i(o);
      n("share", { description: s });
    } catch (s) {
      console.error(s);
      let u = s instanceof jr ? s.message : "Share failed.";
      n("error", u);
    } finally {
      t(3, f = !1);
    }
  };
  return l.$$set = (s) => {
    "formatter" in s && t(0, i = s.formatter), "value" in s && t(1, o = s.value), "i18n" in s && t(2, r = s.i18n);
  }, [i, o, r, f, n, a];
}
class Or extends Fr {
  constructor(e) {
    super(), Ar(this, e, Vr, Ur, Br, { formatter: 0, value: 1, i18n: 2 });
  }
}
const {
  SvelteComponent: Pr,
  append: bt,
  attr: ul,
  check_outros: Zr,
  create_component: Co,
  destroy_component: qo,
  detach: fn,
  element: _l,
  group_outros: Wr,
  init: Hr,
  insert: un,
  mount_component: zo,
  safe_not_equal: Xr,
  set_data: cl,
  space: dl,
  text: Rt,
  toggle_class: Kl,
  transition_in: dn,
  transition_out: mn
} = window.__gradio__svelte__internal;
function Gr(l) {
  let e, t;
  return e = new Lr({}), {
    c() {
      Co(e.$$.fragment);
    },
    m(n, i) {
      zo(e, n, i), t = !0;
    },
    i(n) {
      t || (dn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      mn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      qo(e, n);
    }
  };
}
function Kr(l) {
  let e, t;
  return e = new mr({}), {
    c() {
      Co(e.$$.fragment);
    },
    m(n, i) {
      zo(e, n, i), t = !0;
    },
    i(n) {
      t || (dn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      mn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      qo(e, n);
    }
  };
}
function Yl(l) {
  let e, t, n = (
    /*i18n*/
    l[1]("common.or") + ""
  ), i, o, r, f = (
    /*message*/
    (l[2] || /*i18n*/
    l[1]("upload_text.click_to_upload")) + ""
  ), a;
  return {
    c() {
      e = _l("span"), t = Rt("- "), i = Rt(n), o = Rt(" -"), r = dl(), a = Rt(f), ul(e, "class", "or svelte-kzcjhc");
    },
    m(s, u) {
      un(s, e, u), bt(e, t), bt(e, i), bt(e, o), un(s, r, u), un(s, a, u);
    },
    p(s, u) {
      u & /*i18n*/
      2 && n !== (n = /*i18n*/
      s[1]("common.or") + "") && cl(i, n), u & /*message, i18n*/
      6 && f !== (f = /*message*/
      (s[2] || /*i18n*/
      s[1]("upload_text.click_to_upload")) + "") && cl(a, f);
    },
    d(s) {
      s && (fn(e), fn(r), fn(a));
    }
  };
}
function Yr(l) {
  let e, t, n, i, o, r = (
    /*i18n*/
    l[1](
      /*defs*/
      l[5][
        /*type*/
        l[0]
      ] || /*defs*/
      l[5].file
    ) + ""
  ), f, a, s;
  const u = [Kr, Gr], _ = [];
  function d(m, h) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  n = d(l), i = _[n] = u[n](l);
  let c = (
    /*mode*/
    l[3] !== "short" && Yl(l)
  );
  return {
    c() {
      e = _l("div"), t = _l("span"), i.c(), o = dl(), f = Rt(r), a = dl(), c && c.c(), ul(t, "class", "icon-wrap svelte-kzcjhc"), Kl(
        t,
        "hovered",
        /*hovered*/
        l[4]
      ), ul(e, "class", "wrap svelte-kzcjhc");
    },
    m(m, h) {
      un(m, e, h), bt(e, t), _[n].m(t, null), bt(e, o), bt(e, f), bt(e, a), c && c.m(e, null), s = !0;
    },
    p(m, [h]) {
      let p = n;
      n = d(m), n !== p && (Wr(), mn(_[p], 1, 1, () => {
        _[p] = null;
      }), Zr(), i = _[n], i || (i = _[n] = u[n](m), i.c()), dn(i, 1), i.m(t, null)), (!s || h & /*hovered*/
      16) && Kl(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), (!s || h & /*i18n, type*/
      3) && r !== (r = /*i18n*/
      m[1](
        /*defs*/
        m[5][
          /*type*/
          m[0]
        ] || /*defs*/
        m[5].file
      ) + "") && cl(f, r), /*mode*/
      m[3] !== "short" ? c ? c.p(m, h) : (c = Yl(m), c.c(), c.m(e, null)) : c && (c.d(1), c = null);
    },
    i(m) {
      s || (dn(i), s = !0);
    },
    o(m) {
      mn(i), s = !1;
    },
    d(m) {
      m && fn(e), _[n].d(), c && c.d();
    }
  };
}
function Jr(l, e, t) {
  let { type: n = "file" } = e, { i18n: i } = e, { message: o = void 0 } = e, { mode: r = "full" } = e, { hovered: f = !1 } = e;
  const a = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return l.$$set = (s) => {
    "type" in s && t(0, n = s.type), "i18n" in s && t(1, i = s.i18n), "message" in s && t(2, o = s.message), "mode" in s && t(3, r = s.mode), "hovered" in s && t(4, f = s.hovered);
  }, [n, i, o, r, f, a];
}
class Qr extends Pr {
  constructor(e) {
    super(), Hr(this, e, Jr, Yr, Xr, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
new Intl.Collator(0, { numeric: 1 }).compare;
const { setContext: rd, getContext: xr } = window.__gradio__svelte__internal, $r = "WORKER_PROXY_CONTEXT_KEY";
function ef() {
  return xr($r);
}
function tf(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function nf(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function lf(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!tf(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: of,
  assign: hn,
  check_outros: So,
  compute_rest_props: Jl,
  create_slot: jl,
  detach: Ln,
  element: Lo,
  empty: Eo,
  exclude_internal_props: af,
  get_all_dirty_from_scope: Fl,
  get_slot_changes: Il,
  get_spread_update: jo,
  group_outros: Fo,
  init: sf,
  insert: En,
  listen: Io,
  prevent_default: rf,
  safe_not_equal: ff,
  set_attributes: gn,
  transition_in: Ct,
  transition_out: qt,
  update_slot_base: Dl
} = window.__gradio__svelte__internal, { createEventDispatcher: uf } = window.__gradio__svelte__internal;
function _f(l) {
  let e, t, n, i, o;
  const r = (
    /*#slots*/
    l[8].default
  ), f = jl(
    r,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let a = [
    { href: (
      /*href*/
      l[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      l[1]
    ) },
    /*$$restProps*/
    l[6]
  ], s = {};
  for (let u = 0; u < a.length; u += 1)
    s = hn(s, a[u]);
  return {
    c() {
      e = Lo("a"), f && f.c(), gn(e, s);
    },
    m(u, _) {
      En(u, e, _), f && f.m(e, null), n = !0, i || (o = Io(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(u, _) {
      f && f.p && (!n || _ & /*$$scope*/
      128) && Dl(
        f,
        r,
        u,
        /*$$scope*/
        u[7],
        n ? Il(
          r,
          /*$$scope*/
          u[7],
          _,
          null
        ) : Fl(
          /*$$scope*/
          u[7]
        ),
        null
      ), gn(e, s = jo(a, [
        (!n || _ & /*href*/
        1) && { href: (
          /*href*/
          u[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!n || _ & /*download*/
        2) && { download: (
          /*download*/
          u[1]
        ) },
        _ & /*$$restProps*/
        64 && /*$$restProps*/
        u[6]
      ]));
    },
    i(u) {
      n || (Ct(f, u), n = !0);
    },
    o(u) {
      qt(f, u), n = !1;
    },
    d(u) {
      u && Ln(e), f && f.d(u), i = !1, o();
    }
  };
}
function cf(l) {
  let e, t, n, i;
  const o = [mf, df], r = [];
  function f(a, s) {
    return (
      /*is_downloading*/
      a[2] ? 0 : 1
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = Eo();
    },
    m(a, s) {
      r[e].m(a, s), En(a, n, s), i = !0;
    },
    p(a, s) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (Fo(), qt(r[u], 1, 1, () => {
        r[u] = null;
      }), So(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), Ct(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (Ct(t), i = !0);
    },
    o(a) {
      qt(t), i = !1;
    },
    d(a) {
      a && Ln(n), r[e].d(a);
    }
  };
}
function df(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[8].default
  ), r = jl(
    o,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let f = [
    /*$$restProps*/
    l[6],
    { href: (
      /*href*/
      l[0]
    ) }
  ], a = {};
  for (let s = 0; s < f.length; s += 1)
    a = hn(a, f[s]);
  return {
    c() {
      e = Lo("a"), r && r.c(), gn(e, a);
    },
    m(s, u) {
      En(s, e, u), r && r.m(e, null), t = !0, n || (i = Io(e, "click", rf(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(s, u) {
      r && r.p && (!t || u & /*$$scope*/
      128) && Dl(
        r,
        o,
        s,
        /*$$scope*/
        s[7],
        t ? Il(
          o,
          /*$$scope*/
          s[7],
          u,
          null
        ) : Fl(
          /*$$scope*/
          s[7]
        ),
        null
      ), gn(e, a = jo(f, [
        u & /*$$restProps*/
        64 && /*$$restProps*/
        s[6],
        (!t || u & /*href*/
        1) && { href: (
          /*href*/
          s[0]
        ) }
      ]));
    },
    i(s) {
      t || (Ct(r, s), t = !0);
    },
    o(s) {
      qt(r, s), t = !1;
    },
    d(s) {
      s && Ln(e), r && r.d(s), n = !1, i();
    }
  };
}
function mf(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = jl(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      128) && Dl(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? Il(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : Fl(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (Ct(n, i), e = !0);
    },
    o(i) {
      qt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function hf(l) {
  let e, t, n, i, o;
  const r = [cf, _f], f = [];
  function a(s, u) {
    return u & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (s[4] && lf(
      /*href*/
      s[0]
    ))), e ? 0 : 1;
  }
  return t = a(l, -1), n = f[t] = r[t](l), {
    c() {
      n.c(), i = Eo();
    },
    m(s, u) {
      f[t].m(s, u), En(s, i, u), o = !0;
    },
    p(s, [u]) {
      let _ = t;
      t = a(s, u), t === _ ? f[t].p(s, u) : (Fo(), qt(f[_], 1, 1, () => {
        f[_] = null;
      }), So(), n = f[t], n ? n.p(s, u) : (n = f[t] = r[t](s), n.c()), Ct(n, 1), n.m(i.parentNode, i));
    },
    i(s) {
      o || (Ct(n), o = !0);
    },
    o(s) {
      qt(n), o = !1;
    },
    d(s) {
      s && Ln(i), f[t].d(s);
    }
  };
}
function gf(l, e, t) {
  const n = ["href", "download"];
  let i = Jl(e, n), { $$slots: o = {}, $$scope: r } = e;
  var f = this && this.__awaiter || function(m, h, p, v) {
    function g(w) {
      return w instanceof p ? w : new p(function(b) {
        b(w);
      });
    }
    return new (p || (p = Promise))(function(w, b) {
      function L(E) {
        try {
          z(v.next(E));
        } catch (F) {
          b(F);
        }
      }
      function q(E) {
        try {
          z(v.throw(E));
        } catch (F) {
          b(F);
        }
      }
      function z(E) {
        E.done ? w(E.value) : g(E.value).then(L, q);
      }
      z((v = v.apply(m, h || [])).next());
    });
  };
  let { href: a = void 0 } = e, { download: s } = e;
  const u = uf();
  let _ = !1;
  const d = ef();
  function c() {
    return f(this, void 0, void 0, function* () {
      if (_)
        return;
      if (u("click"), a == null)
        throw new Error("href is not defined.");
      if (d == null)
        throw new Error("Wasm worker proxy is not available.");
      const h = new URL(a, window.location.href).pathname;
      t(2, _ = !0), d.httpRequest({
        method: "GET",
        path: h,
        headers: {},
        query_string: ""
      }).then((p) => {
        if (p.status !== 200)
          throw new Error(`Failed to get file ${h} from the Wasm worker.`);
        const v = new Blob(
          [p.body],
          {
            type: nf(p.headers, "content-type")
          }
        ), g = URL.createObjectURL(v), w = document.createElement("a");
        w.href = g, w.download = s, w.click(), URL.revokeObjectURL(g);
      }).finally(() => {
        t(2, _ = !1);
      });
    });
  }
  return l.$$set = (m) => {
    e = hn(hn({}, e), af(m)), t(6, i = Jl(e, n)), "href" in m && t(0, a = m.href), "download" in m && t(1, s = m.download), "$$scope" in m && t(7, r = m.$$scope);
  }, [
    a,
    s,
    _,
    u,
    d,
    c,
    i,
    r,
    o
  ];
}
class Al extends of {
  constructor(e) {
    super(), sf(this, e, gf, hf, ff, { href: 0, download: 1 });
  }
}
const {
  SvelteComponent: bf,
  append: Jn,
  attr: wf,
  check_outros: Qn,
  create_component: Ot,
  destroy_component: Pt,
  detach: pf,
  element: vf,
  group_outros: xn,
  init: kf,
  insert: yf,
  mount_component: Zt,
  safe_not_equal: Cf,
  set_style: Ql,
  space: $n,
  toggle_class: xl,
  transition_in: oe,
  transition_out: je
} = window.__gradio__svelte__internal, { createEventDispatcher: qf } = window.__gradio__svelte__internal;
function $l(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: vo,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      Ot(e.$$.fragment);
    },
    m(n, i) {
      Zt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.edit")), e.$set(o);
    },
    i(n) {
      t || (oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Pt(e, n);
    }
  };
}
function ei(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: yo,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      Ot(e.$$.fragment);
    },
    m(n, i) {
      Zt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.undo")), e.$set(o);
    },
    i(n) {
      t || (oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Pt(e, n);
    }
  };
}
function ti(l) {
  let e, t;
  return e = new Al({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: { default: [zf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ot(e.$$.fragment);
    },
    m(n, i) {
      Zt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Pt(e, n);
    }
  };
}
function zf(l) {
  let e, t;
  return e = new St({
    props: {
      Icon: El,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      Ot(e.$$.fragment);
    },
    m(n, i) {
      Zt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.download")), e.$set(o);
    },
    i(n) {
      t || (oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Pt(e, n);
    }
  };
}
function Sf(l) {
  let e, t, n, i, o, r, f = (
    /*editable*/
    l[0] && $l(l)
  ), a = (
    /*undoable*/
    l[1] && ei(l)
  ), s = (
    /*download*/
    l[2] && ti(l)
  );
  return o = new St({
    props: {
      Icon: Ll,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = vf("div"), f && f.c(), t = $n(), a && a.c(), n = $n(), s && s.c(), i = $n(), Ot(o.$$.fragment), wf(e, "class", "svelte-1wj0ocy"), xl(e, "not-absolute", !/*absolute*/
      l[3]), Ql(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(u, _) {
      yf(u, e, _), f && f.m(e, null), Jn(e, t), a && a.m(e, null), Jn(e, n), s && s.m(e, null), Jn(e, i), Zt(o, e, null), r = !0;
    },
    p(u, [_]) {
      /*editable*/
      u[0] ? f ? (f.p(u, _), _ & /*editable*/
      1 && oe(f, 1)) : (f = $l(u), f.c(), oe(f, 1), f.m(e, t)) : f && (xn(), je(f, 1, 1, () => {
        f = null;
      }), Qn()), /*undoable*/
      u[1] ? a ? (a.p(u, _), _ & /*undoable*/
      2 && oe(a, 1)) : (a = ei(u), a.c(), oe(a, 1), a.m(e, n)) : a && (xn(), je(a, 1, 1, () => {
        a = null;
      }), Qn()), /*download*/
      u[2] ? s ? (s.p(u, _), _ & /*download*/
      4 && oe(s, 1)) : (s = ti(u), s.c(), oe(s, 1), s.m(e, i)) : s && (xn(), je(s, 1, 1, () => {
        s = null;
      }), Qn());
      const d = {};
      _ & /*i18n*/
      16 && (d.label = /*i18n*/
      u[4]("common.clear")), o.$set(d), (!r || _ & /*absolute*/
      8) && xl(e, "not-absolute", !/*absolute*/
      u[3]), _ & /*absolute*/
      8 && Ql(
        e,
        "position",
        /*absolute*/
        u[3] ? "absolute" : "static"
      );
    },
    i(u) {
      r || (oe(f), oe(a), oe(s), oe(o.$$.fragment, u), r = !0);
    },
    o(u) {
      je(f), je(a), je(s), je(o.$$.fragment, u), r = !1;
    },
    d(u) {
      u && pf(e), f && f.d(), a && a.d(), s && s.d(), Pt(o);
    }
  };
}
function Lf(l, e, t) {
  let { editable: n = !1 } = e, { undoable: i = !1 } = e, { download: o = null } = e, { absolute: r = !0 } = e, { i18n: f } = e;
  const a = qf(), s = () => a("edit"), u = () => a("undo"), _ = (d) => {
    a("clear"), d.stopPropagation();
  };
  return l.$$set = (d) => {
    "editable" in d && t(0, n = d.editable), "undoable" in d && t(1, i = d.undoable), "download" in d && t(2, o = d.download), "absolute" in d && t(3, r = d.absolute), "i18n" in d && t(4, f = d.i18n);
  }, [
    n,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _
  ];
}
let Do = class extends bf {
  constructor(e) {
    super(), kf(this, e, Lf, Sf, Cf, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
};
const {
  SvelteComponent: Ef,
  append: _n,
  attr: Qe,
  detach: Ml,
  element: bn,
  flush: ni,
  init: jf,
  insert: Bl,
  listen: Ao,
  noop: ml,
  safe_not_equal: Ff,
  set_data: If,
  space: li,
  src_url_equal: ii,
  text: Df
} = window.__gradio__svelte__internal, { createEventDispatcher: Af } = window.__gradio__svelte__internal;
function oi(l) {
  let e, t = (
    /*value*/
    l[1].caption + ""
  ), n;
  return {
    c() {
      e = bn("div"), n = Df(t), Qe(e, "class", "foot-label left-label svelte-1d4tgaw");
    },
    m(i, o) {
      Bl(i, e, o), _n(e, n);
    },
    p(i, o) {
      o & /*value*/
      2 && t !== (t = /*value*/
      i[1].caption + "") && If(n, t);
    },
    d(i) {
      i && Ml(e);
    }
  };
}
function ai(l) {
  let e, t, n;
  return {
    c() {
      e = bn("button"), e.innerHTML = '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="8" cy="8" r="8" fill="#FF6700"></circle><path d="M11.5797 10.6521C11.8406 10.913 11.8406 11.3188 11.5797 11.5797C11.4492 11.7101 11.2898 11.7681 11.1159 11.7681C10.942 11.7681 10.7826 11.7101 10.6521 11.5797L7.99997 8.92751L5.3478 11.5797C5.21736 11.7101 5.05794 11.7681 4.88403 11.7681C4.71012 11.7681 4.5507 11.7101 4.42026 11.5797C4.15939 11.3188 4.15939 10.913 4.42026 10.6521L7.07244 7.99997L4.42026 5.3478C4.15939 5.08693 4.15939 4.68113 4.42026 4.42026C4.68113 4.15939 5.08693 4.15939 5.3478 4.42026L7.99997 7.07244L10.6521 4.42026C10.913 4.15939 11.3188 4.15939 11.5797 4.42026C11.8406 4.68113 11.8406 5.08693 11.5797 5.3478L8.92751 7.99997L11.5797 10.6521Z" fill="#FFF4EA"></path></svg>', Qe(e, "class", "delete-button svelte-1d4tgaw");
    },
    m(i, o) {
      Bl(i, e, o), t || (n = Ao(
        e,
        "click",
        /*click_handler_1*/
        l[4]
      ), t = !0);
    },
    p: ml,
    d(i) {
      i && Ml(e), t = !1, n();
    }
  };
}
function Mf(l) {
  let e, t, n, i, o, r, f, a, s = (
    /*value*/
    l[1].caption && oi(l)
  ), u = (
    /*deletable*/
    l[0] && ai(l)
  );
  return {
    c() {
      e = bn("div"), t = bn("img"), o = li(), s && s.c(), r = li(), u && u.c(), Qe(t, "alt", n = /*value*/
      l[1].caption || ""), ii(t.src, i = /*value*/
      l[1].image.url) || Qe(t, "src", i), Qe(t, "class", "thumbnail-img svelte-1d4tgaw"), Qe(t, "loading", "lazy"), Qe(e, "class", "thumbnail-image-box svelte-1d4tgaw");
    },
    m(_, d) {
      Bl(_, e, d), _n(e, t), _n(e, o), s && s.m(e, null), _n(e, r), u && u.m(e, null), f || (a = Ao(
        t,
        "click",
        /*click_handler*/
        l[3]
      ), f = !0);
    },
    p(_, [d]) {
      d & /*value*/
      2 && n !== (n = /*value*/
      _[1].caption || "") && Qe(t, "alt", n), d & /*value*/
      2 && !ii(t.src, i = /*value*/
      _[1].image.url) && Qe(t, "src", i), /*value*/
      _[1].caption ? s ? s.p(_, d) : (s = oi(_), s.c(), s.m(e, r)) : s && (s.d(1), s = null), /*deletable*/
      _[0] ? u ? u.p(_, d) : (u = ai(_), u.c(), u.m(e, null)) : u && (u.d(1), u = null);
    },
    i: ml,
    o: ml,
    d(_) {
      _ && Ml(e), s && s.d(), u && u.d(), f = !1, a();
    }
  };
}
function Bf(l, e, t) {
  const n = Af();
  let { deletable: i } = e, { value: o } = e;
  const r = () => n("click"), f = () => {
    n("delete_image", o);
  };
  return l.$$set = (a) => {
    "deletable" in a && t(0, i = a.deletable), "value" in a && t(1, o = a.value);
  }, [i, o, n, r, f];
}
class Tl extends Ef {
  constructor(e) {
    super(), jf(this, e, Bf, Mf, Ff, { deletable: 0, value: 1 });
  }
  get deletable() {
    return this.$$.ctx[0];
  }
  set deletable(e) {
    this.$$set({ deletable: e }), ni();
  }
  get value() {
    return this.$$.ctx[1];
  }
  set value(e) {
    this.$$set({ value: e }), ni();
  }
}
var si = Object.prototype.hasOwnProperty;
function ri(l, e, t) {
  for (t of l.keys())
    if (Ut(t, e))
      return t;
}
function Ut(l, e) {
  var t, n, i;
  if (l === e)
    return !0;
  if (l && e && (t = l.constructor) === e.constructor) {
    if (t === Date)
      return l.getTime() === e.getTime();
    if (t === RegExp)
      return l.toString() === e.toString();
    if (t === Array) {
      if ((n = l.length) === e.length)
        for (; n-- && Ut(l[n], e[n]); )
          ;
      return n === -1;
    }
    if (t === Set) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n, i && typeof i == "object" && (i = ri(e, i), !i) || !e.has(i))
          return !1;
      return !0;
    }
    if (t === Map) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n[0], i && typeof i == "object" && (i = ri(e, i), !i) || !Ut(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      l = new Uint8Array(l), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l.getInt8(n) === e.getInt8(n); )
          ;
      return n === -1;
    }
    if (ArrayBuffer.isView(l)) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l[n] === e[n]; )
          ;
      return n === -1;
    }
    if (!t || typeof l == "object") {
      n = 0;
      for (t in l)
        if (si.call(l, t) && ++n && !si.call(e, t) || !(t in e) || !Ut(l[t], e[t]))
          return !1;
      return Object.keys(e).length === n;
    }
  }
  return l !== l && e !== e;
}
async function Tf(l) {
  return l ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(
    l.map((t) => !t.image || !t.image.url ? "" : t.image.url)
  )).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
const {
  SvelteComponent: Rf,
  add_render_callback: Nf,
  append: ee,
  attr: G,
  binding_callbacks: fi,
  bubble: ui,
  check_outros: ot,
  create_component: Ve,
  destroy_component: Oe,
  destroy_each: Mo,
  detach: ve,
  element: de,
  empty: Uf,
  ensure_array_like: wn,
  globals: Vf,
  group_outros: at,
  init: Of,
  insert: ke,
  listen: Vt,
  mount_component: Pe,
  run_all: Pf,
  safe_not_equal: Zf,
  set_data: Bo,
  set_style: Te,
  space: De,
  text: To,
  toggle_class: we,
  transition_in: M,
  transition_out: N
} = window.__gradio__svelte__internal, { window: Ro } = Vf, { createEventDispatcher: Wf } = window.__gradio__svelte__internal, { tick: Hf } = window.__gradio__svelte__internal;
function _i(l, e, t) {
  const n = l.slice();
  return n[51] = e[t], n[53] = t, n;
}
function ci(l, e, t) {
  const n = l.slice();
  return n[54] = e[t], n[55] = e, n[53] = t, n;
}
function di(l) {
  let e, t;
  return e = new Pa({
    props: {
      show_label: (
        /*show_label*/
        l[2]
      ),
      Icon: ko,
      label: (
        /*label*/
        l[3] || "Gallery"
      )
    }
  }), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Pe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      n[2]), i[0] & /*label*/
      8 && (o.label = /*label*/
      n[3] || "Gallery"), e.$set(o);
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      N(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Oe(e, n);
    }
  };
}
function Xf(l) {
  let e, t, n, i, o, r, f = (
    /*selected_image*/
    l[19] && /*allow_preview*/
    l[8] && mi(l)
  ), a = (
    /*interactive*/
    l[13] && wi(l)
  ), s = (
    /*show_share_button*/
    l[10] && pi(l)
  ), u = wn(
    /*resolved_value*/
    l[15]
  ), _ = [];
  for (let c = 0; c < u.length; c += 1)
    _[c] = ki(_i(l, u, c));
  const d = (c) => N(_[c], 1, 1, () => {
    _[c] = null;
  });
  return {
    c() {
      f && f.c(), e = De(), t = de("div"), n = de("div"), a && a.c(), i = De(), s && s.c(), o = De();
      for (let c = 0; c < _.length; c += 1)
        _[c].c();
      G(n, "class", "grid-container svelte-94ql7d"), Te(
        n,
        "--grid-cols",
        /*columns*/
        l[5]
      ), Te(
        n,
        "--grid-rows",
        /*rows*/
        l[6]
      ), Te(
        n,
        "--object-fit",
        /*object_fit*/
        l[9]
      ), Te(
        n,
        "height",
        /*height*/
        l[7]
      ), we(
        n,
        "pt-6",
        /*show_label*/
        l[2]
      ), G(t, "class", "grid-wrap svelte-94ql7d"), we(
        t,
        "minimal",
        /*mode*/
        l[14] === "minimal"
      ), we(
        t,
        "fixed-height",
        /*mode*/
        l[14] !== "minimal" && (!/*height*/
        l[7] || /*height*/
        l[7] == "auto")
      );
    },
    m(c, m) {
      f && f.m(c, m), ke(c, e, m), ke(c, t, m), ee(t, n), a && a.m(n, null), ee(n, i), s && s.m(n, null), ee(n, o);
      for (let h = 0; h < _.length; h += 1)
        _[h] && _[h].m(n, null);
      r = !0;
    },
    p(c, m) {
      if (/*selected_image*/
      c[19] && /*allow_preview*/
      c[8] ? f ? (f.p(c, m), m[0] & /*selected_image, allow_preview*/
      524544 && M(f, 1)) : (f = mi(c), f.c(), M(f, 1), f.m(e.parentNode, e)) : f && (at(), N(f, 1, 1, () => {
        f = null;
      }), ot()), /*interactive*/
      c[13] ? a ? (a.p(c, m), m[0] & /*interactive*/
      8192 && M(a, 1)) : (a = wi(c), a.c(), M(a, 1), a.m(n, i)) : a && (at(), N(a, 1, 1, () => {
        a = null;
      }), ot()), /*show_share_button*/
      c[10] ? s ? (s.p(c, m), m[0] & /*show_share_button*/
      1024 && M(s, 1)) : (s = pi(c), s.c(), M(s, 1), s.m(n, o)) : s && (at(), N(s, 1, 1, () => {
        s = null;
      }), ot()), m[0] & /*resolved_value, selected_index, deletable, handleDeleteImage*/
      2129938) {
        u = wn(
          /*resolved_value*/
          c[15]
        );
        let h;
        for (h = 0; h < u.length; h += 1) {
          const p = _i(c, u, h);
          _[h] ? (_[h].p(p, m), M(_[h], 1)) : (_[h] = ki(p), _[h].c(), M(_[h], 1), _[h].m(n, null));
        }
        for (at(), h = u.length; h < _.length; h += 1)
          d(h);
        ot();
      }
      (!r || m[0] & /*columns*/
      32) && Te(
        n,
        "--grid-cols",
        /*columns*/
        c[5]
      ), (!r || m[0] & /*rows*/
      64) && Te(
        n,
        "--grid-rows",
        /*rows*/
        c[6]
      ), (!r || m[0] & /*object_fit*/
      512) && Te(
        n,
        "--object-fit",
        /*object_fit*/
        c[9]
      ), (!r || m[0] & /*height*/
      128) && Te(
        n,
        "height",
        /*height*/
        c[7]
      ), (!r || m[0] & /*show_label*/
      4) && we(
        n,
        "pt-6",
        /*show_label*/
        c[2]
      ), (!r || m[0] & /*mode*/
      16384) && we(
        t,
        "minimal",
        /*mode*/
        c[14] === "minimal"
      ), (!r || m[0] & /*mode, height*/
      16512) && we(
        t,
        "fixed-height",
        /*mode*/
        c[14] !== "minimal" && (!/*height*/
        c[7] || /*height*/
        c[7] == "auto")
      );
    },
    i(c) {
      if (!r) {
        M(f), M(a), M(s);
        for (let m = 0; m < u.length; m += 1)
          M(_[m]);
        r = !0;
      }
    },
    o(c) {
      N(f), N(a), N(s), _ = _.filter(Boolean);
      for (let m = 0; m < _.length; m += 1)
        N(_[m]);
      r = !1;
    },
    d(c) {
      c && (ve(e), ve(t)), f && f.d(c), a && a.d(), s && s.d(), Mo(_, c);
    }
  };
}
function Gf(l) {
  let e, t;
  return e = new ps({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Kf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Pe(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      33554432 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      N(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Oe(e, n);
    }
  };
}
function mi(l) {
  var w;
  let e, t, n, i, o, r, f, a, s, u, _, d, c, m = (
    /*show_download_button*/
    l[11] && hi(l)
  );
  i = new Do({
    props: { i18n: (
      /*i18n*/
      l[12]
    ), absolute: !1 }
  }), i.$on(
    "clear",
    /*clear_handler*/
    l[34]
  ), f = new Tl({
    props: {
      "data-testid": "detailed-image",
      src: (
        /*selected_image*/
        l[19].image.url
      ),
      alt: (
        /*selected_image*/
        l[19].caption || ""
      ),
      title: (
        /*selected_image*/
        l[19].caption || null
      ),
      class: (
        /*selected_image*/
        l[19].caption && "with-caption"
      ),
      loading: "lazy"
    }
  });
  let h = (
    /*selected_image*/
    ((w = l[19]) == null ? void 0 : w.caption) && gi(l)
  ), p = wn(
    /*resolved_value*/
    l[15]
  ), v = [];
  for (let b = 0; b < p.length; b += 1)
    v[b] = bi(ci(l, p, b));
  const g = (b) => N(v[b], 1, 1, () => {
    v[b] = null;
  });
  return {
    c() {
      e = de("button"), t = de("div"), m && m.c(), n = De(), Ve(i.$$.fragment), o = De(), r = de("button"), Ve(f.$$.fragment), a = De(), h && h.c(), s = De(), u = de("div");
      for (let b = 0; b < v.length; b += 1)
        v[b].c();
      G(t, "class", "icon-buttons svelte-94ql7d"), G(r, "class", "image-button svelte-94ql7d"), Te(r, "height", "calc(100% - " + /*selected_image*/
      (l[19].caption ? "80px" : "60px") + ")"), G(r, "aria-label", "detailed view of selected image"), G(u, "class", "thumbnails scroll-hide svelte-94ql7d"), G(u, "data-testid", "container_el"), G(e, "class", "preview svelte-94ql7d"), we(
        e,
        "minimal",
        /*mode*/
        l[14] === "minimal"
      );
    },
    m(b, L) {
      ke(b, e, L), ee(e, t), m && m.m(t, null), ee(t, n), Pe(i, t, null), ee(e, o), ee(e, r), Pe(f, r, null), ee(e, a), h && h.m(e, null), ee(e, s), ee(e, u);
      for (let q = 0; q < v.length; q += 1)
        v[q] && v[q].m(u, null);
      l[39](u), _ = !0, d || (c = [
        Vt(
          r,
          "click",
          /*click_handler_1*/
          l[35]
        ),
        Vt(
          e,
          "keydown",
          /*on_keydown*/
          l[22]
        )
      ], d = !0);
    },
    p(b, L) {
      var E;
      /*show_download_button*/
      b[11] ? m ? (m.p(b, L), L[0] & /*show_download_button*/
      2048 && M(m, 1)) : (m = hi(b), m.c(), M(m, 1), m.m(t, n)) : m && (at(), N(m, 1, 1, () => {
        m = null;
      }), ot());
      const q = {};
      L[0] & /*i18n*/
      4096 && (q.i18n = /*i18n*/
      b[12]), i.$set(q);
      const z = {};
      if (L[0] & /*selected_image*/
      524288 && (z.src = /*selected_image*/
      b[19].image.url), L[0] & /*selected_image*/
      524288 && (z.alt = /*selected_image*/
      b[19].caption || ""), L[0] & /*selected_image*/
      524288 && (z.title = /*selected_image*/
      b[19].caption || null), L[0] & /*selected_image*/
      524288 && (z.class = /*selected_image*/
      b[19].caption && "with-caption"), f.$set(z), (!_ || L[0] & /*selected_image*/
      524288) && Te(r, "height", "calc(100% - " + /*selected_image*/
      (b[19].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (E = b[19]) != null && E.caption ? h ? h.p(b, L) : (h = gi(b), h.c(), h.m(e, s)) : h && (h.d(1), h = null), L[0] & /*resolved_value, el, selected_index, mode, deletable, handleDeleteImage*/
      2211858) {
        p = wn(
          /*resolved_value*/
          b[15]
        );
        let F;
        for (F = 0; F < p.length; F += 1) {
          const C = ci(b, p, F);
          v[F] ? (v[F].p(C, L), M(v[F], 1)) : (v[F] = bi(C), v[F].c(), M(v[F], 1), v[F].m(u, null));
        }
        for (at(), F = p.length; F < v.length; F += 1)
          g(F);
        ot();
      }
      (!_ || L[0] & /*mode*/
      16384) && we(
        e,
        "minimal",
        /*mode*/
        b[14] === "minimal"
      );
    },
    i(b) {
      if (!_) {
        M(m), M(i.$$.fragment, b), M(f.$$.fragment, b);
        for (let L = 0; L < p.length; L += 1)
          M(v[L]);
        _ = !0;
      }
    },
    o(b) {
      N(m), N(i.$$.fragment, b), N(f.$$.fragment, b), v = v.filter(Boolean);
      for (let L = 0; L < v.length; L += 1)
        N(v[L]);
      _ = !1;
    },
    d(b) {
      b && ve(e), m && m.d(), Oe(i), Oe(f), h && h.d(), Mo(v, b), l[39](null), d = !1, Pf(c);
    }
  };
}
function hi(l) {
  let e, t, n;
  return t = new St({
    props: {
      Icon: El,
      label: (
        /*i18n*/
        l[12]("common.download")
      )
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[33]
  ), {
    c() {
      e = de("div"), Ve(t.$$.fragment), G(e, "class", "download-button-container svelte-94ql7d");
    },
    m(i, o) {
      ke(i, e, o), Pe(t, e, null), n = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      4096 && (r.label = /*i18n*/
      i[12]("common.download")), t.$set(r);
    },
    i(i) {
      n || (M(t.$$.fragment, i), n = !0);
    },
    o(i) {
      N(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ve(e), Oe(t);
    }
  };
}
function gi(l) {
  let e, t = (
    /*selected_image*/
    l[19].caption + ""
  ), n;
  return {
    c() {
      e = de("caption"), n = To(t), G(e, "class", "caption svelte-94ql7d");
    },
    m(i, o) {
      ke(i, e, o), ee(e, n);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      524288 && t !== (t = /*selected_image*/
      i[19].caption + "") && Bo(n, t);
    },
    d(i) {
      i && ve(e);
    }
  };
}
function bi(l) {
  let e, t, n, i, o = (
    /*i*/
    l[53]
  ), r, f, a;
  t = new Tl({
    props: {
      deletable: (
        /*deletable*/
        l[4]
      ),
      src: (
        /*image*/
        l[54].image.url
      ),
      title: (
        /*image*/
        l[54].caption || null
      ),
      "data-testid": "thumbnail " + /*i*/
      (l[53] + 1),
      alt: "",
      loading: "lazy"
    }
  }), t.$on(
    "delete_image",
    /*delete_image_handler*/
    l[36]
  );
  const s = () => (
    /*button_binding*/
    l[37](e, o)
  ), u = () => (
    /*button_binding*/
    l[37](null, o)
  );
  function _() {
    return (
      /*click_handler_2*/
      l[38](
        /*i*/
        l[53]
      )
    );
  }
  return {
    c() {
      e = de("button"), Ve(t.$$.fragment), n = De(), G(e, "class", "thumbnail-item thumbnail-small svelte-94ql7d"), G(e, "aria-label", i = "Thumbnail " + /*i*/
      (l[53] + 1) + " of " + /*resolved_value*/
      l[15].length), we(
        e,
        "selected",
        /*selected_index*/
        l[1] === /*i*/
        l[53] && /*mode*/
        l[14] !== "minimal"
      );
    },
    m(d, c) {
      ke(d, e, c), Pe(t, e, null), ee(e, n), s(), r = !0, f || (a = Vt(e, "click", _), f = !0);
    },
    p(d, c) {
      l = d;
      const m = {};
      c[0] & /*deletable*/
      16 && (m.deletable = /*deletable*/
      l[4]), c[0] & /*resolved_value*/
      32768 && (m.src = /*image*/
      l[54].image.url), c[0] & /*resolved_value*/
      32768 && (m.title = /*image*/
      l[54].caption || null), t.$set(m), (!r || c[0] & /*resolved_value*/
      32768 && i !== (i = "Thumbnail " + /*i*/
      (l[53] + 1) + " of " + /*resolved_value*/
      l[15].length)) && G(e, "aria-label", i), o !== /*i*/
      l[53] && (u(), o = /*i*/
      l[53], s()), (!r || c[0] & /*selected_index, mode*/
      16386) && we(
        e,
        "selected",
        /*selected_index*/
        l[1] === /*i*/
        l[53] && /*mode*/
        l[14] !== "minimal"
      );
    },
    i(d) {
      r || (M(t.$$.fragment, d), r = !0);
    },
    o(d) {
      N(t.$$.fragment, d), r = !1;
    },
    d(d) {
      d && ve(e), Oe(t), u(), f = !1, a();
    }
  };
}
function wi(l) {
  let e, t, n;
  return t = new Do({
    props: { i18n: (
      /*i18n*/
      l[12]
    ), absolute: !1 }
  }), t.$on(
    "clear",
    /*clear_handler_1*/
    l[40]
  ), {
    c() {
      e = de("div"), Ve(t.$$.fragment), G(e, "class", "icon-button svelte-94ql7d");
    },
    m(i, o) {
      ke(i, e, o), Pe(t, e, null), n = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      4096 && (r.i18n = /*i18n*/
      i[12]), t.$set(r);
    },
    i(i) {
      n || (M(t.$$.fragment, i), n = !0);
    },
    o(i) {
      N(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ve(e), Oe(t);
    }
  };
}
function pi(l) {
  let e, t, n;
  return t = new Or({
    props: {
      i18n: (
        /*i18n*/
        l[12]
      ),
      value: (
        /*resolved_value*/
        l[15]
      ),
      formatter: Tf
    }
  }), t.$on(
    "share",
    /*share_handler*/
    l[41]
  ), t.$on(
    "error",
    /*error_handler*/
    l[42]
  ), {
    c() {
      e = de("div"), Ve(t.$$.fragment), G(e, "class", "icon-button svelte-94ql7d");
    },
    m(i, o) {
      ke(i, e, o), Pe(t, e, null), n = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      4096 && (r.i18n = /*i18n*/
      i[12]), o[0] & /*resolved_value*/
      32768 && (r.value = /*resolved_value*/
      i[15]), t.$set(r);
    },
    i(i) {
      n || (M(t.$$.fragment, i), n = !0);
    },
    o(i) {
      N(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ve(e), Oe(t);
    }
  };
}
function vi(l) {
  let e, t = (
    /*entry*/
    l[51].caption + ""
  ), n;
  return {
    c() {
      e = de("div"), n = To(t), G(e, "class", "caption-label svelte-94ql7d");
    },
    m(i, o) {
      ke(i, e, o), ee(e, n);
    },
    p(i, o) {
      o[0] & /*resolved_value*/
      32768 && t !== (t = /*entry*/
      i[51].caption + "") && Bo(n, t);
    },
    d(i) {
      i && ve(e);
    }
  };
}
function ki(l) {
  let e, t, n, i, o, r, f, a;
  function s() {
    return (
      /*click_handler_3*/
      l[43](
        /*i*/
        l[53]
      )
    );
  }
  t = new Tl({
    props: {
      deletable: (
        /*deletable*/
        l[4]
      ),
      value: (
        /*entry*/
        l[51]
      )
    }
  }), t.$on("click", s), t.$on(
    "delete_image",
    /*delete_image_handler_1*/
    l[44]
  );
  let u = (
    /*entry*/
    l[51].caption && vi(l)
  );
  function _() {
    return (
      /*click_handler_4*/
      l[45](
        /*i*/
        l[53]
      )
    );
  }
  return {
    c() {
      e = de("div"), Ve(t.$$.fragment), n = De(), u && u.c(), i = De(), G(e, "class", "thumbnail-item thumbnail-lg svelte-94ql7d"), G(e, "aria-label", o = "Thumbnail " + /*i*/
      (l[53] + 1) + " of " + /*resolved_value*/
      l[15].length), we(
        e,
        "selected",
        /*selected_index*/
        l[1] === /*i*/
        l[53]
      );
    },
    m(d, c) {
      ke(d, e, c), Pe(t, e, null), ee(e, n), u && u.m(e, null), ee(e, i), r = !0, f || (a = Vt(e, "click", _), f = !0);
    },
    p(d, c) {
      l = d;
      const m = {};
      c[0] & /*deletable*/
      16 && (m.deletable = /*deletable*/
      l[4]), c[0] & /*resolved_value*/
      32768 && (m.value = /*entry*/
      l[51]), t.$set(m), /*entry*/
      l[51].caption ? u ? u.p(l, c) : (u = vi(l), u.c(), u.m(e, i)) : u && (u.d(1), u = null), (!r || c[0] & /*resolved_value*/
      32768 && o !== (o = "Thumbnail " + /*i*/
      (l[53] + 1) + " of " + /*resolved_value*/
      l[15].length)) && G(e, "aria-label", o), (!r || c[0] & /*selected_index*/
      2) && we(
        e,
        "selected",
        /*selected_index*/
        l[1] === /*i*/
        l[53]
      );
    },
    i(d) {
      r || (M(t.$$.fragment, d), r = !0);
    },
    o(d) {
      N(t.$$.fragment, d), r = !1;
    },
    d(d) {
      d && ve(e), Oe(t), u && u.d(), f = !1, a();
    }
  };
}
function Kf(l) {
  let e, t;
  return e = new ko({}), {
    c() {
      Ve(e.$$.fragment);
    },
    m(n, i) {
      Pe(e, n, i), t = !0;
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      N(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Oe(e, n);
    }
  };
}
function Yf(l) {
  let e, t, n, i, o, r, f;
  Nf(
    /*onwindowresize*/
    l[32]
  );
  let a = (
    /*show_label*/
    l[2] && di(l)
  );
  const s = [Gf, Xf], u = [];
  function _(d, c) {
    return (
      /*value*/
      d[0] == null || /*resolved_value*/
      d[15] == null || /*resolved_value*/
      d[15].length === 0 ? 0 : 1
    );
  }
  return t = _(l), n = u[t] = s[t](l), {
    c() {
      a && a.c(), e = De(), n.c(), i = Uf();
    },
    m(d, c) {
      a && a.m(d, c), ke(d, e, c), u[t].m(d, c), ke(d, i, c), o = !0, r || (f = Vt(
        Ro,
        "resize",
        /*onwindowresize*/
        l[32]
      ), r = !0);
    },
    p(d, c) {
      /*show_label*/
      d[2] ? a ? (a.p(d, c), c[0] & /*show_label*/
      4 && M(a, 1)) : (a = di(d), a.c(), M(a, 1), a.m(e.parentNode, e)) : a && (at(), N(a, 1, 1, () => {
        a = null;
      }), ot());
      let m = t;
      t = _(d), t === m ? u[t].p(d, c) : (at(), N(u[m], 1, 1, () => {
        u[m] = null;
      }), ot(), n = u[t], n ? n.p(d, c) : (n = u[t] = s[t](d), n.c()), M(n, 1), n.m(i.parentNode, i));
    },
    i(d) {
      o || (M(a), M(n), o = !0);
    },
    o(d) {
      N(a), N(n), o = !1;
    },
    d(d) {
      d && (ve(e), ve(i)), a && a.d(d), u[t].d(d), r = !1, f();
    }
  };
}
function Jf(l, e, t) {
  let n, i, o;
  var r = this && this.__awaiter || function(k, ne, re, Ge) {
    function et(qe) {
      return qe instanceof re ? qe : new re(function(tt) {
        tt(qe);
      });
    }
    return new (re || (re = Promise))(function(qe, tt) {
      function xt(_t) {
        try {
          Dn(Ge.next(_t));
        } catch (An) {
          tt(An);
        }
      }
      function ua(_t) {
        try {
          Dn(Ge.throw(_t));
        } catch (An) {
          tt(An);
        }
      }
      function Dn(_t) {
        _t.done ? qe(_t.value) : et(_t.value).then(xt, ua);
      }
      Dn((Ge = Ge.apply(k, ne || [])).next());
    });
  }, f, a, s;
  let { show_label: u = !0 } = e, { label: _ } = e, { deletable: d } = e, { value: c = null } = e, { columns: m = [2] } = e, { rows: h = void 0 } = e, { height: p = "auto" } = e, { preview: v } = e, { allow_preview: g = !0 } = e, { object_fit: w = "cover" } = e, { show_share_button: b = !1 } = e, { show_download_button: L = !1 } = e, { i18n: q } = e, { selected_index: z = null } = e, { interactive: E } = e, { _fetch: F } = e, { mode: C = "normal" } = e;
  const T = Wf();
  let U = !0, R = null, Y = c;
  z == null && v && (c != null && c.length) && (z = 0);
  let W = z;
  function V(k) {
    const ne = k.target, re = k.offsetX, et = ne.offsetWidth / 2;
    re < et ? t(1, z = n) : t(1, z = i);
  }
  function me(k) {
    T("delete_image", k.detail.image.path);
  }
  function Ze(k) {
    switch (k.code) {
      case "Escape":
        k.preventDefault(), t(1, z = null);
        break;
      case "ArrowLeft":
        k.preventDefault(), t(1, z = n);
        break;
      case "ArrowRight":
        k.preventDefault(), t(1, z = i);
        break;
    }
  }
  let J = [], O;
  function te(k) {
    return r(this, void 0, void 0, function* () {
      var ne;
      if (typeof k != "number" || (yield Hf(), J[k] === void 0))
        return;
      (ne = J[k]) === null || ne === void 0 || ne.focus();
      const { left: re, width: Ge } = O.getBoundingClientRect(), { left: et, width: qe } = J[k].getBoundingClientRect(), xt = et - re + qe / 2 - Ge / 2 + O.scrollLeft;
      O && typeof O.scrollTo == "function" && O.scrollTo({
        left: xt < 0 ? 0 : xt,
        behavior: "smooth"
      });
    });
  }
  let S = 0;
  function xe(k, ne) {
    return r(this, void 0, void 0, function* () {
      let re;
      try {
        re = yield F(k);
      } catch (tt) {
        if (tt instanceof TypeError) {
          window.open(k, "_blank", "noreferrer");
          return;
        }
        throw tt;
      }
      const Ge = yield re.blob(), et = URL.createObjectURL(Ge), qe = document.createElement("a");
      qe.href = et, qe.download = ne, qe.click(), URL.revokeObjectURL(et);
    });
  }
  function ft() {
    t(18, S = Ro.innerHeight);
  }
  const j = () => {
    const k = o == null ? void 0 : o.image;
    if (k == null)
      return;
    const { url: ne, orig_name: re } = k;
    ne && xe(ne, re ?? "image");
  }, Bt = () => t(1, z = null), y = (k) => V(k), B = (k) => me(k);
  function H(k, ne) {
    fi[k ? "unshift" : "push"](() => {
      J[ne] = k, t(16, J);
    });
  }
  const X = (k) => t(1, z = k);
  function Q(k) {
    fi[k ? "unshift" : "push"](() => {
      O = k, t(17, O);
    });
  }
  const We = () => t(0, c = null);
  function $e(k) {
    ui.call(this, l, k);
  }
  function ut(k) {
    ui.call(this, l, k);
  }
  const Ce = (k) => t(1, z = k), He = (k) => me(k), Xe = (k) => t(1, z = k);
  return l.$$set = (k) => {
    "show_label" in k && t(2, u = k.show_label), "label" in k && t(3, _ = k.label), "deletable" in k && t(4, d = k.deletable), "value" in k && t(0, c = k.value), "columns" in k && t(5, m = k.columns), "rows" in k && t(6, h = k.rows), "height" in k && t(7, p = k.height), "preview" in k && t(24, v = k.preview), "allow_preview" in k && t(8, g = k.allow_preview), "object_fit" in k && t(9, w = k.object_fit), "show_share_button" in k && t(10, b = k.show_share_button), "show_download_button" in k && t(11, L = k.show_download_button), "i18n" in k && t(12, q = k.i18n), "selected_index" in k && t(1, z = k.selected_index), "interactive" in k && t(13, E = k.interactive), "_fetch" in k && t(25, F = k._fetch), "mode" in k && t(14, C = k.mode);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value, was_reset*/
    536870913 && t(29, U = c == null || c.length === 0 ? !0 : U), l.$$.dirty[0] & /*value*/
    1 && t(15, R = c == null ? null : c.map((k) => ({ image: k.image, caption: k.caption }))), l.$$.dirty[0] & /*prev_value, value, was_reset, preview, selected_index*/
    1627389955 && (Ut(Y, c) || (U ? (t(1, z = v && (c != null && c.length) ? 0 : null), t(29, U = !1)) : t(
      1,
      z = z != null && c != null && z < c.length ? z : null
    ), T("change"), t(30, Y = c))), l.$$.dirty[0] & /*selected_index, resolved_value, _a, _b*/
    201359362 && (n = ((z ?? 0) + (t(26, f = R == null ? void 0 : R.length) !== null && f !== void 0 ? f : 0) - 1) % (t(27, a = R == null ? void 0 : R.length) !== null && a !== void 0 ? a : 0)), l.$$.dirty[0] & /*selected_index, resolved_value, _c*/
    268468226 && (i = ((z ?? 0) + 1) % (t(28, s = R == null ? void 0 : R.length) !== null && s !== void 0 ? s : 0)), l.$$.dirty[0] & /*selected_index, resolved_value*/
    32770 | l.$$.dirty[1] & /*old_selected_index*/
    1 && z !== W && (t(31, W = z), z !== null && T("select", {
      index: z,
      value: R == null ? void 0 : R[z]
    })), l.$$.dirty[0] & /*allow_preview, selected_index*/
    258 && g && te(z), l.$$.dirty[0] & /*selected_index, resolved_value*/
    32770 && t(19, o = z != null && R != null ? R[z] : null);
  }, [
    c,
    z,
    u,
    _,
    d,
    m,
    h,
    p,
    g,
    w,
    b,
    L,
    q,
    E,
    C,
    R,
    J,
    O,
    S,
    o,
    V,
    me,
    Ze,
    xe,
    v,
    F,
    f,
    a,
    s,
    U,
    Y,
    W,
    ft,
    j,
    Bt,
    y,
    B,
    H,
    X,
    Q,
    We,
    $e,
    ut,
    Ce,
    He,
    Xe
  ];
}
class Qf extends Rf {
  constructor(e) {
    super(), Of(
      this,
      e,
      Jf,
      Yf,
      Zf,
      {
        show_label: 2,
        label: 3,
        deletable: 4,
        value: 0,
        columns: 5,
        rows: 6,
        height: 7,
        preview: 24,
        allow_preview: 8,
        object_fit: 9,
        show_share_button: 10,
        show_download_button: 11,
        i18n: 12,
        selected_index: 1,
        interactive: 13,
        _fetch: 25,
        mode: 14
      },
      null,
      [-1, -1]
    );
  }
}
function It(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function cn() {
}
function xf(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const No = typeof window < "u";
let yi = No ? () => window.performance.now() : () => Date.now(), Uo = No ? (l) => requestAnimationFrame(l) : cn;
const At = /* @__PURE__ */ new Set();
function Vo(l) {
  At.forEach((e) => {
    e.c(l) || (At.delete(e), e.f());
  }), At.size !== 0 && Uo(Vo);
}
function $f(l) {
  let e;
  return At.size === 0 && Uo(Vo), {
    promise: new Promise((t) => {
      At.add(e = { c: l, f: t });
    }),
    abort() {
      At.delete(e);
    }
  };
}
const jt = [];
function eu(l, e = cn) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (xf(l, f) && (l = f, t)) {
      const a = !jt.length;
      for (const s of n)
        s[1](), jt.push(s, l);
      if (a) {
        for (let s = 0; s < jt.length; s += 2)
          jt[s][0](jt[s + 1]);
        jt.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function r(f, a = cn) {
    const s = [f, a];
    return n.add(s), n.size === 1 && (t = e(i, o) || cn), f(l), () => {
      n.delete(s), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: r };
}
function Ci(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function hl(l, e, t, n) {
  if (typeof t == "number" || Ci(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), r = l.opts.stiffness * i, f = l.opts.damping * o, a = (r - f) * l.inv_mass, s = (o + a) * l.dt;
    return Math.abs(s) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Ci(t) ? new Date(t.getTime() + s) : t + s);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => hl(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = hl(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function qi(l, e = {}) {
  const t = eu(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let r, f, a, s = l, u = l, _ = 1, d = 0, c = !1;
  function m(p, v = {}) {
    u = p;
    const g = a = {};
    return l == null || v.hard || h.stiffness >= 1 && h.damping >= 1 ? (c = !0, r = yi(), s = p, t.set(l = u), Promise.resolve()) : (v.soft && (d = 1 / ((v.soft === !0 ? 0.5 : +v.soft) * 60), _ = 0), f || (r = yi(), c = !1, f = $f((w) => {
      if (c)
        return c = !1, f = null, !1;
      _ = Math.min(_ + d, 1);
      const b = {
        inv_mass: _,
        opts: h,
        settled: !0,
        dt: (w - r) * 60 / 1e3
      }, L = hl(b, s, l, u);
      return r = w, s = l, t.set(l = L), b.settled && (f = null), !b.settled;
    })), new Promise((w) => {
      f.promise.then(() => {
        g === a && w();
      });
    }));
  }
  const h = {
    set: m,
    update: (p, v) => m(p(u, l), v),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return h;
}
const {
  SvelteComponent: tu,
  append: Le,
  attr: A,
  component_subscribe: zi,
  detach: nu,
  element: lu,
  init: iu,
  insert: ou,
  noop: Si,
  safe_not_equal: au,
  set_style: on,
  svg_element: Ee,
  toggle_class: Li
} = window.__gradio__svelte__internal, { onMount: su } = window.__gradio__svelte__internal;
function ru(l) {
  let e, t, n, i, o, r, f, a, s, u, _, d;
  return {
    c() {
      e = lu("div"), t = Ee("svg"), n = Ee("g"), i = Ee("path"), o = Ee("path"), r = Ee("path"), f = Ee("path"), a = Ee("g"), s = Ee("path"), u = Ee("path"), _ = Ee("path"), d = Ee("path"), A(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), A(i, "fill", "#FF7C00"), A(i, "fill-opacity", "0.4"), A(i, "class", "svelte-43sxxs"), A(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), A(o, "fill", "#FF7C00"), A(o, "class", "svelte-43sxxs"), A(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), A(r, "fill", "#FF7C00"), A(r, "fill-opacity", "0.4"), A(r, "class", "svelte-43sxxs"), A(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), A(f, "fill", "#FF7C00"), A(f, "class", "svelte-43sxxs"), on(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), A(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), A(s, "fill", "#FF7C00"), A(s, "fill-opacity", "0.4"), A(s, "class", "svelte-43sxxs"), A(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), A(u, "fill", "#FF7C00"), A(u, "class", "svelte-43sxxs"), A(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), A(_, "fill", "#FF7C00"), A(_, "fill-opacity", "0.4"), A(_, "class", "svelte-43sxxs"), A(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), A(d, "fill", "#FF7C00"), A(d, "class", "svelte-43sxxs"), on(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), A(t, "viewBox", "-1200 -1200 3000 3000"), A(t, "fill", "none"), A(t, "xmlns", "http://www.w3.org/2000/svg"), A(t, "class", "svelte-43sxxs"), A(e, "class", "svelte-43sxxs"), Li(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(c, m) {
      ou(c, e, m), Le(e, t), Le(t, n), Le(n, i), Le(n, o), Le(n, r), Le(n, f), Le(t, a), Le(a, s), Le(a, u), Le(a, _), Le(a, d);
    },
    p(c, [m]) {
      m & /*$top*/
      2 && on(n, "transform", "translate(" + /*$top*/
      c[1][0] + "px, " + /*$top*/
      c[1][1] + "px)"), m & /*$bottom*/
      4 && on(a, "transform", "translate(" + /*$bottom*/
      c[2][0] + "px, " + /*$bottom*/
      c[2][1] + "px)"), m & /*margin*/
      1 && Li(
        e,
        "margin",
        /*margin*/
        c[0]
      );
    },
    i: Si,
    o: Si,
    d(c) {
      c && nu(e);
    }
  };
}
function fu(l, e, t) {
  let n, i;
  var o = this && this.__awaiter || function(c, m, h, p) {
    function v(g) {
      return g instanceof h ? g : new h(function(w) {
        w(g);
      });
    }
    return new (h || (h = Promise))(function(g, w) {
      function b(z) {
        try {
          q(p.next(z));
        } catch (E) {
          w(E);
        }
      }
      function L(z) {
        try {
          q(p.throw(z));
        } catch (E) {
          w(E);
        }
      }
      function q(z) {
        z.done ? g(z.value) : v(z.value).then(b, L);
      }
      q((p = p.apply(c, m || [])).next());
    });
  };
  let { margin: r = !0 } = e;
  const f = qi([0, 0]);
  zi(l, f, (c) => t(1, n = c));
  const a = qi([0, 0]);
  zi(l, a, (c) => t(2, i = c));
  let s;
  function u() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), a.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), a.set([125, -140])]), yield Promise.all([f.set([-125, 0]), a.set([125, -0])]), yield Promise.all([f.set([125, 0]), a.set([-125, 0])]);
    });
  }
  function _() {
    return o(this, void 0, void 0, function* () {
      yield u(), s || _();
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), a.set([-125, 0])]), _();
    });
  }
  return su(() => (d(), () => s = !0)), l.$$set = (c) => {
    "margin" in c && t(0, r = c.margin);
  }, [r, n, i, f, a];
}
class uu extends tu {
  constructor(e) {
    super(), iu(this, e, fu, ru, au, { margin: 0 });
  }
}
const {
  SvelteComponent: _u,
  append: wt,
  attr: Ae,
  binding_callbacks: Ei,
  check_outros: gl,
  create_component: Oo,
  create_slot: Po,
  destroy_component: Zo,
  destroy_each: Wo,
  detach: I,
  element: Ne,
  empty: Mt,
  ensure_array_like: pn,
  get_all_dirty_from_scope: Ho,
  get_slot_changes: Xo,
  group_outros: bl,
  init: cu,
  insert: D,
  mount_component: Go,
  noop: wl,
  safe_not_equal: du,
  set_data: ye,
  set_style: st,
  space: pe,
  text: P,
  toggle_class: be,
  transition_in: Ie,
  transition_out: Ue,
  update_slot_base: Ko
} = window.__gradio__svelte__internal, { tick: mu } = window.__gradio__svelte__internal, { onDestroy: hu } = window.__gradio__svelte__internal, { createEventDispatcher: gu } = window.__gradio__svelte__internal, bu = (l) => ({}), ji = (l) => ({}), wu = (l) => ({}), Fi = (l) => ({});
function Ii(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function Di(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function pu(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), r, f, a;
  t = new St({
    props: {
      Icon: Ll,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const s = (
    /*#slots*/
    l[30].error
  ), u = Po(
    s,
    l,
    /*$$scope*/
    l[29],
    ji
  );
  return {
    c() {
      e = Ne("div"), Oo(t.$$.fragment), n = pe(), i = Ne("span"), r = P(o), f = pe(), u && u.c(), Ae(e, "class", "clear-status svelte-vopvsi"), Ae(i, "class", "error svelte-vopvsi");
    },
    m(_, d) {
      D(_, e, d), Go(t, e, null), D(_, n, d), D(_, i, d), wt(i, r), D(_, f, d), u && u.m(_, d), a = !0;
    },
    p(_, d) {
      const c = {};
      d[0] & /*i18n*/
      2 && (c.label = /*i18n*/
      _[1]("common.clear")), t.$set(c), (!a || d[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      _[1]("common.error") + "") && ye(r, o), u && u.p && (!a || d[0] & /*$$scope*/
      536870912) && Ko(
        u,
        s,
        _,
        /*$$scope*/
        _[29],
        a ? Xo(
          s,
          /*$$scope*/
          _[29],
          d,
          bu
        ) : Ho(
          /*$$scope*/
          _[29]
        ),
        ji
      );
    },
    i(_) {
      a || (Ie(t.$$.fragment, _), Ie(u, _), a = !0);
    },
    o(_) {
      Ue(t.$$.fragment, _), Ue(u, _), a = !1;
    },
    d(_) {
      _ && (I(e), I(n), I(i), I(f)), Zo(t), u && u.d(_);
    }
  };
}
function vu(l) {
  let e, t, n, i, o, r, f, a, s, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Ai(l)
  );
  function _(w, b) {
    if (
      /*progress*/
      w[7]
    )
      return Cu;
    if (
      /*queue_position*/
      w[2] !== null && /*queue_size*/
      w[3] !== void 0 && /*queue_position*/
      w[2] >= 0
    )
      return yu;
    if (
      /*queue_position*/
      w[2] === 0
    )
      return ku;
  }
  let d = _(l), c = d && d(l), m = (
    /*timer*/
    l[5] && Ti(l)
  );
  const h = [Lu, Su], p = [];
  function v(w, b) {
    return (
      /*last_progress_level*/
      w[15] != null ? 0 : (
        /*show_progress*/
        w[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = v(l)) && (r = p[o] = h[o](l));
  let g = !/*timer*/
  l[5] && Zi(l);
  return {
    c() {
      u && u.c(), e = pe(), t = Ne("div"), c && c.c(), n = pe(), m && m.c(), i = pe(), r && r.c(), f = pe(), g && g.c(), a = Mt(), Ae(t, "class", "progress-text svelte-vopvsi"), be(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), be(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(w, b) {
      u && u.m(w, b), D(w, e, b), D(w, t, b), c && c.m(t, null), wt(t, n), m && m.m(t, null), D(w, i, b), ~o && p[o].m(w, b), D(w, f, b), g && g.m(w, b), D(w, a, b), s = !0;
    },
    p(w, b) {
      /*variant*/
      w[8] === "default" && /*show_eta_bar*/
      w[18] && /*show_progress*/
      w[6] === "full" ? u ? u.p(w, b) : (u = Ai(w), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), d === (d = _(w)) && c ? c.p(w, b) : (c && c.d(1), c = d && d(w), c && (c.c(), c.m(t, n))), /*timer*/
      w[5] ? m ? m.p(w, b) : (m = Ti(w), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!s || b[0] & /*variant*/
      256) && be(
        t,
        "meta-text-center",
        /*variant*/
        w[8] === "center"
      ), (!s || b[0] & /*variant*/
      256) && be(
        t,
        "meta-text",
        /*variant*/
        w[8] === "default"
      );
      let L = o;
      o = v(w), o === L ? ~o && p[o].p(w, b) : (r && (bl(), Ue(p[L], 1, 1, () => {
        p[L] = null;
      }), gl()), ~o ? (r = p[o], r ? r.p(w, b) : (r = p[o] = h[o](w), r.c()), Ie(r, 1), r.m(f.parentNode, f)) : r = null), /*timer*/
      w[5] ? g && (bl(), Ue(g, 1, 1, () => {
        g = null;
      }), gl()) : g ? (g.p(w, b), b[0] & /*timer*/
      32 && Ie(g, 1)) : (g = Zi(w), g.c(), Ie(g, 1), g.m(a.parentNode, a));
    },
    i(w) {
      s || (Ie(r), Ie(g), s = !0);
    },
    o(w) {
      Ue(r), Ue(g), s = !1;
    },
    d(w) {
      w && (I(e), I(t), I(i), I(f), I(a)), u && u.d(w), c && c.d(), m && m.d(), ~o && p[o].d(w), g && g.d(w);
    }
  };
}
function Ai(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Ne("div"), Ae(e, "class", "eta-bar svelte-vopvsi"), st(e, "transform", t);
    },
    m(n, i) {
      D(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && st(e, "transform", t);
    },
    d(n) {
      n && I(e);
    }
  };
}
function ku(l) {
  let e;
  return {
    c() {
      e = P("processing |");
    },
    m(t, n) {
      D(t, e, n);
    },
    p: wl,
    d(t) {
      t && I(e);
    }
  };
}
function yu(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, r;
  return {
    c() {
      e = P("queue: "), n = P(t), i = P("/"), o = P(
        /*queue_size*/
        l[3]
      ), r = P(" |");
    },
    m(f, a) {
      D(f, e, a), D(f, n, a), D(f, i, a), D(f, o, a), D(f, r, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && ye(n, t), a[0] & /*queue_size*/
      8 && ye(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (I(e), I(n), I(i), I(o), I(r));
    }
  };
}
function Cu(l) {
  let e, t = pn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Bi(Di(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Mt();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      D(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = pn(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Di(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = Bi(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && I(e), Wo(n, i);
    }
  };
}
function Mi(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, o = " ", r;
  function f(u, _) {
    return (
      /*p*/
      u[41].length != null ? zu : qu
    );
  }
  let a = f(l), s = a(l);
  return {
    c() {
      s.c(), e = pe(), n = P(t), i = P(" | "), r = P(o);
    },
    m(u, _) {
      s.m(u, _), D(u, e, _), D(u, n, _), D(u, i, _), D(u, r, _);
    },
    p(u, _) {
      a === (a = f(u)) && s ? s.p(u, _) : (s.d(1), s = a(u), s && (s.c(), s.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && ye(n, t);
    },
    d(u) {
      u && (I(e), I(n), I(i), I(r)), s.d(u);
    }
  };
}
function qu(l) {
  let e = It(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = P(e);
    },
    m(n, i) {
      D(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = It(
        /*p*/
        n[41].index || 0
      ) + "") && ye(t, e);
    },
    d(n) {
      n && I(t);
    }
  };
}
function zu(l) {
  let e = It(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = It(
    /*p*/
    l[41].length
  ) + "", o;
  return {
    c() {
      t = P(e), n = P("/"), o = P(i);
    },
    m(r, f) {
      D(r, t, f), D(r, n, f), D(r, o, f);
    },
    p(r, f) {
      f[0] & /*progress*/
      128 && e !== (e = It(
        /*p*/
        r[41].index || 0
      ) + "") && ye(t, e), f[0] & /*progress*/
      128 && i !== (i = It(
        /*p*/
        r[41].length
      ) + "") && ye(o, i);
    },
    d(r) {
      r && (I(t), I(n), I(o));
    }
  };
}
function Bi(l) {
  let e, t = (
    /*p*/
    l[41].index != null && Mi(l)
  );
  return {
    c() {
      t && t.c(), e = Mt();
    },
    m(n, i) {
      t && t.m(n, i), D(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = Mi(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && I(e), t && t.d(n);
    }
  };
}
function Ti(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = P(
        /*formatted_timer*/
        l[20]
      ), n = P(t), i = P("s");
    },
    m(o, r) {
      D(o, e, r), D(o, n, r), D(o, i, r);
    },
    p(o, r) {
      r[0] & /*formatted_timer*/
      1048576 && ye(
        e,
        /*formatted_timer*/
        o[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && ye(n, t);
    },
    d(o) {
      o && (I(e), I(n), I(i));
    }
  };
}
function Su(l) {
  let e, t;
  return e = new uu({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Oo(e.$$.fragment);
    },
    m(n, i) {
      Go(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (Ie(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ue(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Zo(e, n);
    }
  };
}
function Lu(l) {
  let e, t, n, i, o, r = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && Ri(l)
  );
  return {
    c() {
      e = Ne("div"), t = Ne("div"), f && f.c(), n = pe(), i = Ne("div"), o = Ne("div"), Ae(t, "class", "progress-level-inner svelte-vopvsi"), Ae(o, "class", "progress-bar svelte-vopvsi"), st(o, "width", r), Ae(i, "class", "progress-bar-wrap svelte-vopvsi"), Ae(e, "class", "progress-level svelte-vopvsi");
    },
    m(a, s) {
      D(a, e, s), wt(e, t), f && f.m(t, null), wt(e, n), wt(e, i), wt(i, o), l[31](o);
    },
    p(a, s) {
      /*progress*/
      a[7] != null ? f ? f.p(a, s) : (f = Ri(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), s[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      a[15] * 100}%`) && st(o, "width", r);
    },
    i: wl,
    o: wl,
    d(a) {
      a && I(e), f && f.d(), l[31](null);
    }
  };
}
function Ri(l) {
  let e, t = pn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Pi(Ii(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Mt();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      D(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = pn(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Ii(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = Pi(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && I(e), Wo(n, i);
    }
  };
}
function Ni(l) {
  let e, t, n, i, o = (
    /*i*/
    l[43] !== 0 && Eu()
  ), r = (
    /*p*/
    l[41].desc != null && Ui(l)
  ), f = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && Vi()
  ), a = (
    /*progress_level*/
    l[14] != null && Oi(l)
  );
  return {
    c() {
      o && o.c(), e = pe(), r && r.c(), t = pe(), f && f.c(), n = pe(), a && a.c(), i = Mt();
    },
    m(s, u) {
      o && o.m(s, u), D(s, e, u), r && r.m(s, u), D(s, t, u), f && f.m(s, u), D(s, n, u), a && a.m(s, u), D(s, i, u);
    },
    p(s, u) {
      /*p*/
      s[41].desc != null ? r ? r.p(s, u) : (r = Ui(s), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), /*p*/
      s[41].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[43]
      ] != null ? f || (f = Vi(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      s[14] != null ? a ? a.p(s, u) : (a = Oi(s), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(s) {
      s && (I(e), I(t), I(n), I(i)), o && o.d(s), r && r.d(s), f && f.d(s), a && a.d(s);
    }
  };
}
function Eu(l) {
  let e;
  return {
    c() {
      e = P(" /");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && I(e);
    }
  };
}
function Ui(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = P(e);
    },
    m(n, i) {
      D(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && ye(t, e);
    },
    d(n) {
      n && I(t);
    }
  };
}
function Vi(l) {
  let e;
  return {
    c() {
      e = P("-");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && I(e);
    }
  };
}
function Oi(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = P(e), n = P("%");
    },
    m(i, o) {
      D(i, t, o), D(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && ye(t, e);
    },
    d(i) {
      i && (I(t), I(n));
    }
  };
}
function Pi(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && Ni(l)
  );
  return {
    c() {
      t && t.c(), e = Mt();
    },
    m(n, i) {
      t && t.m(n, i), D(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = Ni(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && I(e), t && t.d(n);
    }
  };
}
function Zi(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), r = Po(
    o,
    l,
    /*$$scope*/
    l[29],
    Fi
  );
  return {
    c() {
      e = Ne("p"), t = P(
        /*loading_text*/
        l[9]
      ), n = pe(), r && r.c(), Ae(e, "class", "loading svelte-vopvsi");
    },
    m(f, a) {
      D(f, e, a), wt(e, t), D(f, n, a), r && r.m(f, a), i = !0;
    },
    p(f, a) {
      (!i || a[0] & /*loading_text*/
      512) && ye(
        t,
        /*loading_text*/
        f[9]
      ), r && r.p && (!i || a[0] & /*$$scope*/
      536870912) && Ko(
        r,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Xo(
          o,
          /*$$scope*/
          f[29],
          a,
          wu
        ) : Ho(
          /*$$scope*/
          f[29]
        ),
        Fi
      );
    },
    i(f) {
      i || (Ie(r, f), i = !0);
    },
    o(f) {
      Ue(r, f), i = !1;
    },
    d(f) {
      f && (I(e), I(n)), r && r.d(f);
    }
  };
}
function ju(l) {
  let e, t, n, i, o;
  const r = [vu, pu], f = [];
  function a(s, u) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = r[t](l)), {
    c() {
      e = Ne("div"), n && n.c(), Ae(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-vopvsi"), be(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), be(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), be(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), be(
        e,
        "border",
        /*border*/
        l[12]
      ), st(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), st(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, u) {
      D(s, e, u), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(s, u) {
      let _ = t;
      t = a(s), t === _ ? ~t && f[t].p(s, u) : (n && (bl(), Ue(f[_], 1, 1, () => {
        f[_] = null;
      }), gl()), ~t ? (n = f[t], n ? n.p(s, u) : (n = f[t] = r[t](s), n.c()), Ie(n, 1), n.m(e, null)) : n = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-vopvsi")) && Ae(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && be(e, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && be(
        e,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status*/
      336) && be(
        e,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && be(
        e,
        "border",
        /*border*/
        s[12]
      ), u[0] & /*absolute*/
      1024 && st(
        e,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && st(
        e,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      o || (Ie(n), o = !0);
    },
    o(s) {
      Ue(n), o = !1;
    },
    d(s) {
      s && I(e), ~t && f[t].d(), l[33](null);
    }
  };
}
var Fu = function(l, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(r) {
      r(o);
    });
  }
  return new (t || (t = Promise))(function(o, r) {
    function f(u) {
      try {
        s(n.next(u));
      } catch (_) {
        r(_);
      }
    }
    function a(u) {
      try {
        s(n.throw(u));
      } catch (_) {
        r(_);
      }
    }
    function s(u) {
      u.done ? o(u.value) : i(u.value).then(f, a);
    }
    s((n = n.apply(l, e || [])).next());
  });
};
let an = [], el = !1;
function Iu(l) {
  return Fu(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (an.push(e), !el)
        el = !0;
      else
        return;
      yield mu(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < an.length; i++) {
          const r = an[i].getBoundingClientRect();
          (i === 0 || r.top + window.scrollY <= n[0]) && (n[0] = r.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), el = !1, an = [];
      });
    }
  });
}
function Du(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  const r = gu();
  let { i18n: f } = e, { eta: a = null } = e, { queue_position: s } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: d = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: h = null } = e, { progress: p = null } = e, { variant: v = "default" } = e, { loading_text: g = "Loading..." } = e, { absolute: w = !0 } = e, { translucent: b = !1 } = e, { border: L = !1 } = e, { autoscroll: q } = e, z, E = !1, F = 0, C = 0, T = null, U = null, R = 0, Y = null, W, V = null, me = !0;
  const Ze = () => {
    t(0, a = t(27, T = t(19, te = null))), t(25, F = performance.now()), t(26, C = 0), E = !0, J();
  };
  function J() {
    requestAnimationFrame(() => {
      t(26, C = (performance.now() - F) / 1e3), E && J();
    });
  }
  function O() {
    t(26, C = 0), t(0, a = t(27, T = t(19, te = null))), E && (E = !1);
  }
  hu(() => {
    E && O();
  });
  let te = null;
  function S(j) {
    Ei[j ? "unshift" : "push"](() => {
      V = j, t(16, V), t(7, p), t(14, Y), t(15, W);
    });
  }
  const xe = () => {
    r("clear_status");
  };
  function ft(j) {
    Ei[j ? "unshift" : "push"](() => {
      z = j, t(13, z);
    });
  }
  return l.$$set = (j) => {
    "i18n" in j && t(1, f = j.i18n), "eta" in j && t(0, a = j.eta), "queue_position" in j && t(2, s = j.queue_position), "queue_size" in j && t(3, u = j.queue_size), "status" in j && t(4, _ = j.status), "scroll_to_output" in j && t(22, d = j.scroll_to_output), "timer" in j && t(5, c = j.timer), "show_progress" in j && t(6, m = j.show_progress), "message" in j && t(23, h = j.message), "progress" in j && t(7, p = j.progress), "variant" in j && t(8, v = j.variant), "loading_text" in j && t(9, g = j.loading_text), "absolute" in j && t(10, w = j.absolute), "translucent" in j && t(11, b = j.translucent), "border" in j && t(12, L = j.border), "autoscroll" in j && t(24, q = j.autoscroll), "$$scope" in j && t(29, o = j.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = T), a != null && T !== a && (t(28, U = (performance.now() - F) / 1e3 + a), t(19, te = U.toFixed(1)), t(27, T = a))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, R = U === null || U <= 0 || !C ? null : Math.min(C / U, 1)), l.$$.dirty[0] & /*progress*/
    128 && p != null && t(18, me = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (p != null ? t(14, Y = p.map((j) => {
      if (j.index != null && j.length != null)
        return j.index / j.length;
      if (j.progress != null)
        return j.progress;
    })) : t(14, Y = null), Y ? (t(15, W = Y[Y.length - 1]), V && (W === 0 ? t(16, V.style.transition = "0", V) : t(16, V.style.transition = "150ms", V))) : t(15, W = void 0)), l.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? Ze() : O()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && z && d && (_ === "pending" || _ === "complete") && Iu(z, q), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = C.toFixed(1));
  }, [
    a,
    f,
    s,
    u,
    _,
    c,
    m,
    p,
    v,
    g,
    w,
    b,
    L,
    z,
    Y,
    W,
    V,
    R,
    me,
    te,
    n,
    r,
    d,
    h,
    q,
    F,
    C,
    T,
    U,
    o,
    i,
    S,
    xe,
    ft
  ];
}
class Au extends _u {
  constructor(e) {
    super(), cu(
      this,
      e,
      Du,
      ju,
      du,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Mu,
  append: tl,
  attr: sn,
  create_component: Bu,
  destroy_component: Tu,
  detach: Ru,
  element: Wi,
  init: Nu,
  insert: Uu,
  mount_component: Vu,
  safe_not_equal: Ou,
  set_data: Pu,
  space: Zu,
  text: Wu,
  toggle_class: it,
  transition_in: Hu,
  transition_out: Xu
} = window.__gradio__svelte__internal;
function Gu(l) {
  let e, t, n, i, o, r;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Wi("label"), t = Wi("span"), Bu(n.$$.fragment), i = Zu(), o = Wu(
        /*label*/
        l[0]
      ), sn(t, "class", "svelte-9gxdi0"), sn(e, "for", ""), sn(e, "data-testid", "block-label"), sn(e, "class", "svelte-9gxdi0"), it(e, "hide", !/*show_label*/
      l[2]), it(e, "sr-only", !/*show_label*/
      l[2]), it(
        e,
        "float",
        /*float*/
        l[4]
      ), it(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      Uu(f, e, a), tl(e, t), Vu(n, t, null), tl(e, i), tl(e, o), r = !0;
    },
    p(f, [a]) {
      (!r || a & /*label*/
      1) && Pu(
        o,
        /*label*/
        f[0]
      ), (!r || a & /*show_label*/
      4) && it(e, "hide", !/*show_label*/
      f[2]), (!r || a & /*show_label*/
      4) && it(e, "sr-only", !/*show_label*/
      f[2]), (!r || a & /*float*/
      16) && it(
        e,
        "float",
        /*float*/
        f[4]
      ), (!r || a & /*disable*/
      8) && it(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      r || (Hu(n.$$.fragment, f), r = !0);
    },
    o(f) {
      Xu(n.$$.fragment, f), r = !1;
    },
    d(f) {
      f && Ru(e), Tu(n);
    }
  };
}
function Ku(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, r = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, r, f];
}
class Yu extends Mu {
  constructor(e) {
    super(), Nu(this, e, Ku, Gu, Ou, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Ju,
  append: pl,
  attr: Je,
  bubble: Qu,
  create_component: xu,
  destroy_component: $u,
  detach: Yo,
  element: vl,
  init: e_,
  insert: Jo,
  listen: t_,
  mount_component: n_,
  safe_not_equal: l_,
  set_data: i_,
  set_style: Ft,
  space: o_,
  text: a_,
  toggle_class: ie,
  transition_in: s_,
  transition_out: r_
} = window.__gradio__svelte__internal;
function Hi(l) {
  let e, t;
  return {
    c() {
      e = vl("span"), t = a_(
        /*label*/
        l[1]
      ), Je(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Jo(n, e, i), pl(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && i_(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Yo(e);
    }
  };
}
function f_(l) {
  let e, t, n, i, o, r, f, a = (
    /*show_label*/
    l[2] && Hi(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = vl("button"), a && a.c(), t = o_(), n = vl("div"), xu(i.$$.fragment), Je(n, "class", "svelte-1lrphxw"), ie(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), ie(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), ie(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Je(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Je(
        e,
        "title",
        /*label*/
        l[1]
      ), Je(e, "class", "svelte-1lrphxw"), ie(
        e,
        "pending",
        /*pending*/
        l[3]
      ), ie(
        e,
        "padded",
        /*padded*/
        l[5]
      ), ie(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), ie(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Ft(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Ft(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Ft(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(s, u) {
      Jo(s, e, u), a && a.m(e, null), pl(e, t), pl(e, n), n_(i, n, null), o = !0, r || (f = t_(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), r = !0);
    },
    p(s, [u]) {
      /*show_label*/
      s[2] ? a ? a.p(s, u) : (a = Hi(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && ie(
        n,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || u & /*size*/
      16) && ie(
        n,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || u & /*size*/
      16) && ie(
        n,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || u & /*label*/
      2) && Je(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || u & /*hasPopup*/
      256) && Je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || u & /*label*/
      2) && Je(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || u & /*pending*/
      8) && ie(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || u & /*padded*/
      32) && ie(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || u & /*highlight*/
      64) && ie(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || u & /*transparent*/
      512) && ie(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), u & /*disabled, _color*/
      4224 && Ft(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Ft(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), u & /*offset*/
      2048 && Ft(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (s_(i.$$.fragment, s), o = !0);
    },
    o(s) {
      r_(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && Yo(e), a && a.d(), $u(i), r = !1, f();
    }
  };
}
function u_(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: s = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: d = !1 } = e, { color: c = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: h = "var(--background-fill-primary)" } = e, { offset: p = 0 } = e;
  function v(g) {
    Qu.call(this, l, g);
  }
  return l.$$set = (g) => {
    "Icon" in g && t(0, i = g.Icon), "label" in g && t(1, o = g.label), "show_label" in g && t(2, r = g.show_label), "pending" in g && t(3, f = g.pending), "size" in g && t(4, a = g.size), "padded" in g && t(5, s = g.padded), "highlight" in g && t(6, u = g.highlight), "disabled" in g && t(7, _ = g.disabled), "hasPopup" in g && t(8, d = g.hasPopup), "color" in g && t(13, c = g.color), "transparent" in g && t(9, m = g.transparent), "background" in g && t(10, h = g.background), "offset" in g && t(11, p = g.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : c);
  }, [
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    d,
    m,
    h,
    p,
    n,
    c,
    v
  ];
}
class jn extends Ju {
  constructor(e) {
    super(), e_(this, e, u_, f_, l_, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const Xi = (l) => {
  let e = ["B", "KB", "MB", "GB", "PB"], t = 0;
  for (; l > 1024; )
    l /= 1024, t++;
  let n = e[t];
  return l.toFixed(1) + "&nbsp;" + n;
}, {
  HtmlTag: __,
  SvelteComponent: c_,
  append: _e,
  attr: ce,
  check_outros: Qo,
  create_component: d_,
  destroy_component: m_,
  detach: Wt,
  element: Re,
  ensure_array_like: Gi,
  group_outros: xo,
  init: h_,
  insert: Ht,
  listen: kl,
  mount_component: g_,
  noop: Ki,
  outro_and_destroy_block: b_,
  run_all: w_,
  safe_not_equal: p_,
  set_data: yl,
  set_style: Yi,
  space: rn,
  text: vn,
  toggle_class: Ji,
  transition_in: kn,
  transition_out: yn,
  update_keyed_each: v_
} = window.__gradio__svelte__internal, { createEventDispatcher: k_ } = window.__gradio__svelte__internal;
function Qi(l, e, t) {
  const n = l.slice();
  return n[11] = e[t], n[13] = t, n;
}
function y_(l) {
  let e = (
    /*i18n*/
    l[2]("file.uploading") + ""
  ), t;
  return {
    c() {
      t = vn(e);
    },
    m(n, i) {
      Ht(n, t, i);
    },
    p(n, i) {
      i & /*i18n*/
      4 && e !== (e = /*i18n*/
      n[2]("file.uploading") + "") && yl(t, e);
    },
    i: Ki,
    o: Ki,
    d(n) {
      n && Wt(t);
    }
  };
}
function C_(l) {
  let e, t;
  return e = new Al({
    props: {
      href: (
        /*file*/
        l[11].url
      ),
      download: window.__is_colab__ ? null : (
        /*file*/
        l[11].orig_name
      ),
      $$slots: { default: [q_] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      d_(e.$$.fragment);
    },
    m(n, i) {
      g_(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*normalized_files*/
      8 && (o.href = /*file*/
      n[11].url), i & /*normalized_files*/
      8 && (o.download = window.__is_colab__ ? null : (
        /*file*/
        n[11].orig_name
      )), i & /*$$scope, normalized_files*/
      16392 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (kn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      yn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      m_(e, n);
    }
  };
}
function q_(l) {
  let e, t = (
    /*file*/
    (l[11].size != null ? Xi(
      /*file*/
      l[11].size
    ) : "(size unknown)") + ""
  ), n;
  return {
    c() {
      e = new __(!1), n = vn(" ⇣"), e.a = n;
    },
    m(i, o) {
      e.m(t, i, o), Ht(i, n, o);
    },
    p(i, o) {
      o & /*normalized_files*/
      8 && t !== (t = /*file*/
      (i[11].size != null ? Xi(
        /*file*/
        i[11].size
      ) : "(size unknown)") + "") && e.p(t);
    },
    d(i) {
      i && (e.d(), Wt(n));
    }
  };
}
function xi(l) {
  let e, t, n, i;
  function o() {
    return (
      /*click_handler*/
      l[7](
        /*i*/
        l[13]
      )
    );
  }
  function r(...f) {
    return (
      /*keydown_handler*/
      l[8](
        /*i*/
        l[13],
        ...f
      )
    );
  }
  return {
    c() {
      e = Re("td"), t = Re("button"), t.textContent = "×", ce(t, "class", "label-clear-button svelte-1g4vug2"), ce(t, "aria-label", "Remove this file"), ce(e, "class", "svelte-1g4vug2");
    },
    m(f, a) {
      Ht(f, e, a), _e(e, t), n || (i = [
        kl(t, "click", o),
        kl(t, "keydown", r)
      ], n = !0);
    },
    p(f, a) {
      l = f;
    },
    d(f) {
      f && Wt(e), n = !1, w_(i);
    }
  };
}
function $i(l, e) {
  let t, n, i, o = (
    /*file*/
    e[11].filename_stem + ""
  ), r, f, a, s = (
    /*file*/
    e[11].filename_ext + ""
  ), u, _, d, c, m, h, p, v, g, w, b;
  const L = [C_, y_], q = [];
  function z(C, T) {
    return (
      /*file*/
      C[11].url ? 0 : 1
    );
  }
  m = z(e), h = q[m] = L[m](e);
  let E = (
    /*normalized_files*/
    e[3].length > 1 && xi(e)
  );
  function F(...C) {
    return (
      /*click_handler_1*/
      e[9](
        /*i*/
        e[13],
        ...C
      )
    );
  }
  return {
    key: l,
    first: null,
    c() {
      t = Re("tr"), n = Re("td"), i = Re("span"), r = vn(o), f = rn(), a = Re("span"), u = vn(s), d = rn(), c = Re("td"), h.c(), p = rn(), E && E.c(), v = rn(), ce(i, "class", "stem svelte-1g4vug2"), ce(a, "class", "ext svelte-1g4vug2"), ce(n, "class", "filename svelte-1g4vug2"), ce(n, "aria-label", _ = /*file*/
      e[11].orig_name), ce(c, "class", "download svelte-1g4vug2"), ce(t, "class", "file svelte-1g4vug2"), Ji(
        t,
        "selectable",
        /*selectable*/
        e[0]
      ), this.first = t;
    },
    m(C, T) {
      Ht(C, t, T), _e(t, n), _e(n, i), _e(i, r), _e(n, f), _e(n, a), _e(a, u), _e(t, d), _e(t, c), q[m].m(c, null), _e(t, p), E && E.m(t, null), _e(t, v), g = !0, w || (b = kl(t, "click", F), w = !0);
    },
    p(C, T) {
      e = C, (!g || T & /*normalized_files*/
      8) && o !== (o = /*file*/
      e[11].filename_stem + "") && yl(r, o), (!g || T & /*normalized_files*/
      8) && s !== (s = /*file*/
      e[11].filename_ext + "") && yl(u, s), (!g || T & /*normalized_files*/
      8 && _ !== (_ = /*file*/
      e[11].orig_name)) && ce(n, "aria-label", _);
      let U = m;
      m = z(e), m === U ? q[m].p(e, T) : (xo(), yn(q[U], 1, 1, () => {
        q[U] = null;
      }), Qo(), h = q[m], h ? h.p(e, T) : (h = q[m] = L[m](e), h.c()), kn(h, 1), h.m(c, null)), /*normalized_files*/
      e[3].length > 1 ? E ? E.p(e, T) : (E = xi(e), E.c(), E.m(t, v)) : E && (E.d(1), E = null), (!g || T & /*selectable*/
      1) && Ji(
        t,
        "selectable",
        /*selectable*/
        e[0]
      );
    },
    i(C) {
      g || (kn(h), g = !0);
    },
    o(C) {
      yn(h), g = !1;
    },
    d(C) {
      C && Wt(t), q[m].d(), E && E.d(), w = !1, b();
    }
  };
}
function z_(l) {
  let e, t, n, i = [], o = /* @__PURE__ */ new Map(), r, f = Gi(
    /*normalized_files*/
    l[3]
  );
  const a = (s) => (
    /*file*/
    s[11]
  );
  for (let s = 0; s < f.length; s += 1) {
    let u = Qi(l, f, s), _ = a(u);
    o.set(_, i[s] = $i(_, u));
  }
  return {
    c() {
      e = Re("div"), t = Re("table"), n = Re("tbody");
      for (let s = 0; s < i.length; s += 1)
        i[s].c();
      ce(n, "class", "svelte-1g4vug2"), ce(t, "class", "file-preview svelte-1g4vug2"), ce(e, "class", "file-preview-holder svelte-1g4vug2"), Yi(e, "max-height", typeof /*height*/
      l[1] === void 0 ? "auto" : (
        /*height*/
        l[1] + "px"
      ));
    },
    m(s, u) {
      Ht(s, e, u), _e(e, t), _e(t, n);
      for (let _ = 0; _ < i.length; _ += 1)
        i[_] && i[_].m(n, null);
      r = !0;
    },
    p(s, [u]) {
      u & /*selectable, handle_row_click, normalized_files, remove_file, window, i18n*/
      61 && (f = Gi(
        /*normalized_files*/
        s[3]
      ), xo(), i = v_(i, u, a, 1, s, f, o, n, b_, $i, null, Qi), Qo()), (!r || u & /*height*/
      2) && Yi(e, "max-height", typeof /*height*/
      s[1] === void 0 ? "auto" : (
        /*height*/
        s[1] + "px"
      ));
    },
    i(s) {
      if (!r) {
        for (let u = 0; u < f.length; u += 1)
          kn(i[u]);
        r = !0;
      }
    },
    o(s) {
      for (let u = 0; u < i.length; u += 1)
        yn(i[u]);
      r = !1;
    },
    d(s) {
      s && Wt(e);
      for (let u = 0; u < i.length; u += 1)
        i[u].d();
    }
  };
}
function S_(l) {
  const e = l.lastIndexOf(".");
  return e === -1 ? [l, ""] : [l.slice(0, e), l.slice(e)];
}
function L_(l, e, t) {
  let n;
  const i = k_();
  let { value: o } = e, { selectable: r = !1 } = e, { height: f = void 0 } = e, { i18n: a } = e;
  function s(m, h) {
    const p = m.currentTarget;
    (m.target === p || // Only select if the click is on the row itself
    m.composedPath().includes(p.firstElementChild)) && i("select", {
      value: n[h].orig_name,
      index: h
    });
  }
  function u(m) {
    n.splice(m, 1), t(3, n = [...n]), t(6, o = n), i("change", n);
  }
  const _ = (m) => {
    u(m);
  }, d = (m, h) => {
    h.key === "Enter" && u(m);
  }, c = (m, h) => {
    s(h, m);
  };
  return l.$$set = (m) => {
    "value" in m && t(6, o = m.value), "selectable" in m && t(0, r = m.selectable), "height" in m && t(1, f = m.height), "i18n" in m && t(2, a = m.i18n);
  }, l.$$.update = () => {
    l.$$.dirty & /*value*/
    64 && t(3, n = (Array.isArray(o) ? o : [o]).map((m) => {
      var h;
      const [p, v] = S_((h = m.orig_name) !== null && h !== void 0 ? h : "");
      return Object.assign(Object.assign({}, m), { filename_stem: p, filename_ext: v });
    }));
  }, [
    r,
    f,
    a,
    n,
    s,
    u,
    o,
    _,
    d,
    c
  ];
}
class E_ extends c_ {
  constructor(e) {
    super(), h_(this, e, L_, z_, p_, {
      value: 6,
      selectable: 0,
      height: 1,
      i18n: 2
    });
  }
}
var j_ = Object.defineProperty, F_ = (l, e, t) => e in l ? j_(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t, Ke = (l, e, t) => (F_(l, typeof e != "symbol" ? e + "" : e, t), t);
new Intl.Collator(0, { numeric: 1 }).compare;
async function I_(l, e) {
  return l.map(
    (t) => new D_({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class D_ {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: r,
    mime_type: f,
    alt_text: a
  }) {
    Ke(this, "path"), Ke(this, "url"), Ke(this, "orig_name"), Ke(this, "size"), Ke(this, "blob"), Ke(this, "is_stream"), Ke(this, "mime_type"), Ke(this, "alt_text"), Ke(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = r, this.mime_type = f, this.alt_text = a;
  }
}
const {
  SvelteComponent: A_,
  append: se,
  attr: ht,
  detach: $o,
  element: gt,
  init: M_,
  insert: ea,
  noop: eo,
  safe_not_equal: B_,
  set_data: Cn,
  set_style: nl,
  space: Cl,
  text: Dt,
  toggle_class: to
} = window.__gradio__svelte__internal, { onMount: T_, createEventDispatcher: R_, onDestroy: N_ } = window.__gradio__svelte__internal;
function no(l) {
  let e, t, n, i, o = Nt(
    /*file_to_display*/
    l[2]
  ) + "", r, f, a, s, u = (
    /*file_to_display*/
    l[2].orig_name + ""
  ), _;
  return {
    c() {
      e = gt("div"), t = gt("span"), n = gt("div"), i = gt("progress"), r = Dt(o), a = Cl(), s = gt("span"), _ = Dt(u), nl(i, "visibility", "hidden"), nl(i, "height", "0"), nl(i, "width", "0"), i.value = f = Nt(
        /*file_to_display*/
        l[2]
      ), ht(i, "max", "100"), ht(i, "class", "svelte-cr2edf"), ht(n, "class", "progress-bar svelte-cr2edf"), ht(s, "class", "file-name svelte-cr2edf"), ht(e, "class", "file svelte-cr2edf");
    },
    m(d, c) {
      ea(d, e, c), se(e, t), se(t, n), se(n, i), se(i, r), se(e, a), se(e, s), se(s, _);
    },
    p(d, c) {
      c & /*file_to_display*/
      4 && o !== (o = Nt(
        /*file_to_display*/
        d[2]
      ) + "") && Cn(r, o), c & /*file_to_display*/
      4 && f !== (f = Nt(
        /*file_to_display*/
        d[2]
      )) && (i.value = f), c & /*file_to_display*/
      4 && u !== (u = /*file_to_display*/
      d[2].orig_name + "") && Cn(_, u);
    },
    d(d) {
      d && $o(e);
    }
  };
}
function U_(l) {
  let e, t, n, i = (
    /*files_with_progress*/
    l[0].length + ""
  ), o, r, f = (
    /*files_with_progress*/
    l[0].length > 1 ? "files" : "file"
  ), a, s, u, _ = (
    /*file_to_display*/
    l[2] && no(l)
  );
  return {
    c() {
      e = gt("div"), t = gt("span"), n = Dt("Uploading "), o = Dt(i), r = Cl(), a = Dt(f), s = Dt("..."), u = Cl(), _ && _.c(), ht(t, "class", "uploading svelte-cr2edf"), ht(e, "class", "wrap svelte-cr2edf"), to(
        e,
        "progress",
        /*progress*/
        l[1]
      );
    },
    m(d, c) {
      ea(d, e, c), se(e, t), se(t, n), se(t, o), se(t, r), se(t, a), se(t, s), se(e, u), _ && _.m(e, null);
    },
    p(d, [c]) {
      c & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      d[0].length + "") && Cn(o, i), c & /*files_with_progress*/
      1 && f !== (f = /*files_with_progress*/
      d[0].length > 1 ? "files" : "file") && Cn(a, f), /*file_to_display*/
      d[2] ? _ ? _.p(d, c) : (_ = no(d), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null), c & /*progress*/
      2 && to(
        e,
        "progress",
        /*progress*/
        d[1]
      );
    },
    i: eo,
    o: eo,
    d(d) {
      d && $o(e), _ && _.d();
    }
  };
}
function Nt(l) {
  return l.progress * 100 / (l.size || 0) || 0;
}
function V_(l) {
  let e = 0;
  return l.forEach((t) => {
    e += Nt(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / l.length).toFixed(2) + "%"), e / l.length;
}
function O_(l, e, t) {
  var n = this && this.__awaiter || function(h, p, v, g) {
    function w(b) {
      return b instanceof v ? b : new v(function(L) {
        L(b);
      });
    }
    return new (v || (v = Promise))(function(b, L) {
      function q(F) {
        try {
          E(g.next(F));
        } catch (C) {
          L(C);
        }
      }
      function z(F) {
        try {
          E(g.throw(F));
        } catch (C) {
          L(C);
        }
      }
      function E(F) {
        F.done ? b(F.value) : w(F.value).then(q, z);
      }
      E((g = g.apply(h, p || [])).next());
    });
  };
  let { upload_id: i } = e, { root: o } = e, { files: r } = e, { stream_handler: f } = e, a, s = !1, u, _, d = r.map((h) => Object.assign(Object.assign({}, h), { progress: 0 }));
  const c = R_();
  function m(h, p) {
    t(0, d = d.map((v) => (v.orig_name === h && (v.progress += p), v)));
  }
  return T_(() => n(void 0, void 0, void 0, function* () {
    if (a = yield f(new URL(`${o}/upload_progress?upload_id=${i}`)), a == null)
      throw new Error("Event source is not defined");
    a.onmessage = function(h) {
      return n(this, void 0, void 0, function* () {
        const p = JSON.parse(h.data);
        s || t(1, s = !0), p.msg === "done" ? (a == null || a.close(), c("done")) : (t(7, u = p), m(p.orig_name, p.chunk_size));
      });
    };
  })), N_(() => {
    (a != null || a != null) && a.close();
  }), l.$$set = (h) => {
    "upload_id" in h && t(3, i = h.upload_id), "root" in h && t(4, o = h.root), "files" in h && t(5, r = h.files), "stream_handler" in h && t(6, f = h.stream_handler);
  }, l.$$.update = () => {
    l.$$.dirty & /*files_with_progress*/
    1 && V_(d), l.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, _ = u || d[0]);
  }, [
    d,
    s,
    _,
    i,
    o,
    r,
    f,
    u
  ];
}
class P_ extends A_ {
  constructor(e) {
    super(), M_(this, e, O_, U_, B_, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: Z_,
  append: lo,
  attr: $,
  binding_callbacks: W_,
  bubble: ct,
  check_outros: ta,
  create_component: H_,
  create_slot: na,
  destroy_component: X_,
  detach: Fn,
  element: ql,
  empty: la,
  get_all_dirty_from_scope: ia,
  get_slot_changes: oa,
  group_outros: aa,
  init: G_,
  insert: In,
  listen: ue,
  mount_component: K_,
  prevent_default: dt,
  run_all: Y_,
  safe_not_equal: J_,
  set_style: sa,
  space: Q_,
  stop_propagation: mt,
  toggle_class: K,
  transition_in: rt,
  transition_out: zt,
  update_slot_base: ra
} = window.__gradio__svelte__internal, { createEventDispatcher: x_, tick: $_ } = window.__gradio__svelte__internal;
function ec(l) {
  let e, t, n, i, o, r, f, a, s, u, _;
  const d = (
    /*#slots*/
    l[26].default
  ), c = na(
    d,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = ql("button"), c && c.c(), t = Q_(), n = ql("input"), $(n, "aria-label", "file upload"), $(n, "data-testid", "file-upload"), $(n, "type", "file"), $(n, "accept", i = /*accept_file_types*/
      l[16] || void 0), n.multiple = o = /*file_count*/
      l[6] === "multiple" || void 0, $(n, "webkitdirectory", r = /*file_count*/
      l[6] === "directory" || void 0), $(n, "mozdirectory", f = /*file_count*/
      l[6] === "directory" || void 0), $(n, "class", "svelte-1s26xmt"), $(e, "tabindex", a = /*hidden*/
      l[9] ? -1 : 0), $(e, "class", "svelte-1s26xmt"), K(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), K(
        e,
        "center",
        /*center*/
        l[4]
      ), K(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), K(
        e,
        "flex",
        /*flex*/
        l[5]
      ), K(
        e,
        "disable_click",
        /*disable_click*/
        l[7]
      ), sa(e, "height", "100%");
    },
    m(m, h) {
      In(m, e, h), c && c.m(e, null), lo(e, t), lo(e, n), l[34](n), s = !0, u || (_ = [
        ue(
          n,
          "change",
          /*load_files_from_upload*/
          l[18]
        ),
        ue(e, "drag", mt(dt(
          /*drag_handler*/
          l[27]
        ))),
        ue(e, "dragstart", mt(dt(
          /*dragstart_handler*/
          l[28]
        ))),
        ue(e, "dragend", mt(dt(
          /*dragend_handler*/
          l[29]
        ))),
        ue(e, "dragover", mt(dt(
          /*dragover_handler*/
          l[30]
        ))),
        ue(e, "dragenter", mt(dt(
          /*dragenter_handler*/
          l[31]
        ))),
        ue(e, "dragleave", mt(dt(
          /*dragleave_handler*/
          l[32]
        ))),
        ue(e, "drop", mt(dt(
          /*drop_handler*/
          l[33]
        ))),
        ue(
          e,
          "click",
          /*open_file_upload*/
          l[13]
        ),
        ue(
          e,
          "drop",
          /*loadFilesFromDrop*/
          l[19]
        ),
        ue(
          e,
          "dragenter",
          /*updateDragging*/
          l[17]
        ),
        ue(
          e,
          "dragleave",
          /*updateDragging*/
          l[17]
        )
      ], u = !0);
    },
    p(m, h) {
      c && c.p && (!s || h[0] & /*$$scope*/
      33554432) && ra(
        c,
        d,
        m,
        /*$$scope*/
        m[25],
        s ? oa(
          d,
          /*$$scope*/
          m[25],
          h,
          null
        ) : ia(
          /*$$scope*/
          m[25]
        ),
        null
      ), (!s || h[0] & /*accept_file_types*/
      65536 && i !== (i = /*accept_file_types*/
      m[16] || void 0)) && $(n, "accept", i), (!s || h[0] & /*file_count*/
      64 && o !== (o = /*file_count*/
      m[6] === "multiple" || void 0)) && (n.multiple = o), (!s || h[0] & /*file_count*/
      64 && r !== (r = /*file_count*/
      m[6] === "directory" || void 0)) && $(n, "webkitdirectory", r), (!s || h[0] & /*file_count*/
      64 && f !== (f = /*file_count*/
      m[6] === "directory" || void 0)) && $(n, "mozdirectory", f), (!s || h[0] & /*hidden*/
      512 && a !== (a = /*hidden*/
      m[9] ? -1 : 0)) && $(e, "tabindex", a), (!s || h[0] & /*hidden*/
      512) && K(
        e,
        "hidden",
        /*hidden*/
        m[9]
      ), (!s || h[0] & /*center*/
      16) && K(
        e,
        "center",
        /*center*/
        m[4]
      ), (!s || h[0] & /*boundedheight*/
      8) && K(
        e,
        "boundedheight",
        /*boundedheight*/
        m[3]
      ), (!s || h[0] & /*flex*/
      32) && K(
        e,
        "flex",
        /*flex*/
        m[5]
      ), (!s || h[0] & /*disable_click*/
      128) && K(
        e,
        "disable_click",
        /*disable_click*/
        m[7]
      );
    },
    i(m) {
      s || (rt(c, m), s = !0);
    },
    o(m) {
      zt(c, m), s = !1;
    },
    d(m) {
      m && Fn(e), c && c.d(m), l[34](null), u = !1, Y_(_);
    }
  };
}
function tc(l) {
  let e, t, n = !/*hidden*/
  l[9] && io(l);
  return {
    c() {
      n && n.c(), e = la();
    },
    m(i, o) {
      n && n.m(i, o), In(i, e, o), t = !0;
    },
    p(i, o) {
      /*hidden*/
      i[9] ? n && (aa(), zt(n, 1, 1, () => {
        n = null;
      }), ta()) : n ? (n.p(i, o), o[0] & /*hidden*/
      512 && rt(n, 1)) : (n = io(i), n.c(), rt(n, 1), n.m(e.parentNode, e));
    },
    i(i) {
      t || (rt(n), t = !0);
    },
    o(i) {
      zt(n), t = !1;
    },
    d(i) {
      i && Fn(e), n && n.d(i);
    }
  };
}
function nc(l) {
  let e, t, n, i, o;
  const r = (
    /*#slots*/
    l[26].default
  ), f = na(
    r,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = ql("button"), f && f.c(), $(e, "tabindex", t = /*hidden*/
      l[9] ? -1 : 0), $(e, "class", "svelte-1s26xmt"), K(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), K(
        e,
        "center",
        /*center*/
        l[4]
      ), K(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), K(
        e,
        "flex",
        /*flex*/
        l[5]
      ), sa(e, "height", "100%");
    },
    m(a, s) {
      In(a, e, s), f && f.m(e, null), n = !0, i || (o = ue(
        e,
        "click",
        /*paste_clipboard*/
        l[12]
      ), i = !0);
    },
    p(a, s) {
      f && f.p && (!n || s[0] & /*$$scope*/
      33554432) && ra(
        f,
        r,
        a,
        /*$$scope*/
        a[25],
        n ? oa(
          r,
          /*$$scope*/
          a[25],
          s,
          null
        ) : ia(
          /*$$scope*/
          a[25]
        ),
        null
      ), (!n || s[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      a[9] ? -1 : 0)) && $(e, "tabindex", t), (!n || s[0] & /*hidden*/
      512) && K(
        e,
        "hidden",
        /*hidden*/
        a[9]
      ), (!n || s[0] & /*center*/
      16) && K(
        e,
        "center",
        /*center*/
        a[4]
      ), (!n || s[0] & /*boundedheight*/
      8) && K(
        e,
        "boundedheight",
        /*boundedheight*/
        a[3]
      ), (!n || s[0] & /*flex*/
      32) && K(
        e,
        "flex",
        /*flex*/
        a[5]
      );
    },
    i(a) {
      n || (rt(f, a), n = !0);
    },
    o(a) {
      zt(f, a), n = !1;
    },
    d(a) {
      a && Fn(e), f && f.d(a), i = !1, o();
    }
  };
}
function io(l) {
  let e, t;
  return e = new P_({
    props: {
      root: (
        /*root*/
        l[8]
      ),
      upload_id: (
        /*upload_id*/
        l[14]
      ),
      files: (
        /*file_data*/
        l[15]
      ),
      stream_handler: (
        /*stream_handler*/
        l[11]
      )
    }
  }), {
    c() {
      H_(e.$$.fragment);
    },
    m(n, i) {
      K_(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      256 && (o.root = /*root*/
      n[8]), i[0] & /*upload_id*/
      16384 && (o.upload_id = /*upload_id*/
      n[14]), i[0] & /*file_data*/
      32768 && (o.files = /*file_data*/
      n[15]), i[0] & /*stream_handler*/
      2048 && (o.stream_handler = /*stream_handler*/
      n[11]), e.$set(o);
    },
    i(n) {
      t || (rt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      zt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      X_(e, n);
    }
  };
}
function lc(l) {
  let e, t, n, i;
  const o = [nc, tc, ec], r = [];
  function f(a, s) {
    return (
      /*filetype*/
      a[0] === "clipboard" ? 0 : (
        /*uploading*/
        a[1] && /*show_progress*/
        a[10] ? 1 : 2
      )
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = la();
    },
    m(a, s) {
      r[e].m(a, s), In(a, n, s), i = !0;
    },
    p(a, s) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (aa(), zt(r[u], 1, 1, () => {
        r[u] = null;
      }), ta(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), rt(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (rt(t), i = !0);
    },
    o(a) {
      zt(t), i = !1;
    },
    d(a) {
      a && Fn(n), r[e].d(a);
    }
  };
}
function ic(l, e, t) {
  if (!l || l === "*" || l === "file/*" || Array.isArray(l) && l.some((i) => i === "*" || i === "file/*"))
    return !0;
  let n;
  if (typeof l == "string")
    n = l.split(",").map((i) => i.trim());
  else if (Array.isArray(l))
    n = l;
  else
    return !1;
  return n.includes(e) || n.some((i) => {
    const [o] = i.split("/").map((r) => r.trim());
    return i.endsWith("/*") && t.startsWith(o + "/");
  });
}
function oc(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(y, B, H, X) {
    function Q(We) {
      return We instanceof H ? We : new H(function($e) {
        $e(We);
      });
    }
    return new (H || (H = Promise))(function(We, $e) {
      function ut(Xe) {
        try {
          He(X.next(Xe));
        } catch (k) {
          $e(k);
        }
      }
      function Ce(Xe) {
        try {
          He(X.throw(Xe));
        } catch (k) {
          $e(k);
        }
      }
      function He(Xe) {
        Xe.done ? We(Xe.value) : Q(Xe.value).then(ut, Ce);
      }
      He((X = X.apply(y, B || [])).next());
    });
  };
  let { filetype: r = null } = e, { dragging: f = !1 } = e, { boundedheight: a = !0 } = e, { center: s = !0 } = e, { flex: u = !0 } = e, { file_count: _ = "single" } = e, { disable_click: d = !1 } = e, { root: c } = e, { hidden: m = !1 } = e, { format: h = "file" } = e, { uploading: p = !1 } = e, { hidden_upload: v = null } = e, { show_progress: g = !0 } = e, { max_file_size: w = null } = e, { upload: b } = e, { stream_handler: L } = e, q, z, E;
  const F = x_(), C = ["image", "video", "audio", "text", "file"], T = (y) => y.startsWith(".") || y.endsWith("/*") ? y : C.includes(y) ? y + "/*" : "." + y;
  function U() {
    t(20, f = !f);
  }
  function R() {
    navigator.clipboard.read().then((y) => o(this, void 0, void 0, function* () {
      for (let B = 0; B < y.length; B++) {
        const H = y[B].types.find((X) => X.startsWith("image/"));
        if (H) {
          y[B].getType(H).then((X) => o(this, void 0, void 0, function* () {
            const Q = new File([X], `clipboard.${H.replace("image/", "")}`);
            yield V([Q]);
          }));
          break;
        }
      }
    }));
  }
  function Y() {
    d || v && (t(2, v.value = "", v), v.click());
  }
  function W(y) {
    return o(this, void 0, void 0, function* () {
      yield $_(), t(14, q = Math.random().toString(36).substring(2, 15)), t(1, p = !0);
      try {
        const B = yield b(y, c, q, w ?? 1 / 0);
        return F("load", _ === "single" ? B == null ? void 0 : B[0] : B), t(1, p = !1), B || [];
      } catch (B) {
        return F("error", B.message), t(1, p = !1), [];
      }
    });
  }
  function V(y) {
    return o(this, void 0, void 0, function* () {
      if (!y.length)
        return;
      let B = y.map((H) => new File([H], H instanceof File ? H.name : "file", { type: H.type }));
      return t(15, z = yield I_(B)), yield W(z);
    });
  }
  function me(y) {
    return o(this, void 0, void 0, function* () {
      const B = y.target;
      if (B.files)
        if (h != "blob")
          yield V(Array.from(B.files));
        else {
          if (_ === "single") {
            F("load", B.files[0]);
            return;
          }
          F("load", B.files);
        }
    });
  }
  function Ze(y) {
    return o(this, void 0, void 0, function* () {
      var B;
      if (t(20, f = !1), !(!((B = y.dataTransfer) === null || B === void 0) && B.files))
        return;
      const H = Array.from(y.dataTransfer.files).filter((X) => {
        const Q = "." + X.name.split(".").pop();
        return Q && ic(E, Q, X.type) || (Q && Array.isArray(r) ? r.includes(Q) : Q === r) ? !0 : (F("error", `Invalid file type only ${r} allowed.`), !1);
      });
      yield V(H);
    });
  }
  function J(y) {
    ct.call(this, l, y);
  }
  function O(y) {
    ct.call(this, l, y);
  }
  function te(y) {
    ct.call(this, l, y);
  }
  function S(y) {
    ct.call(this, l, y);
  }
  function xe(y) {
    ct.call(this, l, y);
  }
  function ft(y) {
    ct.call(this, l, y);
  }
  function j(y) {
    ct.call(this, l, y);
  }
  function Bt(y) {
    W_[y ? "unshift" : "push"](() => {
      v = y, t(2, v);
    });
  }
  return l.$$set = (y) => {
    "filetype" in y && t(0, r = y.filetype), "dragging" in y && t(20, f = y.dragging), "boundedheight" in y && t(3, a = y.boundedheight), "center" in y && t(4, s = y.center), "flex" in y && t(5, u = y.flex), "file_count" in y && t(6, _ = y.file_count), "disable_click" in y && t(7, d = y.disable_click), "root" in y && t(8, c = y.root), "hidden" in y && t(9, m = y.hidden), "format" in y && t(21, h = y.format), "uploading" in y && t(1, p = y.uploading), "hidden_upload" in y && t(2, v = y.hidden_upload), "show_progress" in y && t(10, g = y.show_progress), "max_file_size" in y && t(22, w = y.max_file_size), "upload" in y && t(23, b = y.upload), "stream_handler" in y && t(11, L = y.stream_handler), "$$scope" in y && t(25, i = y.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*filetype*/
    1 && (r == null ? t(16, E = null) : typeof r == "string" ? t(16, E = T(r)) : (t(0, r = r.map(T)), t(16, E = r.join(", "))));
  }, [
    r,
    p,
    v,
    a,
    s,
    u,
    _,
    d,
    c,
    m,
    g,
    L,
    R,
    Y,
    q,
    z,
    E,
    U,
    me,
    Ze,
    f,
    h,
    w,
    b,
    V,
    i,
    n,
    J,
    O,
    te,
    S,
    xe,
    ft,
    j,
    Bt
  ];
}
class ac extends Z_ {
  constructor(e) {
    super(), G_(
      this,
      e,
      oc,
      lc,
      J_,
      {
        filetype: 0,
        dragging: 20,
        boundedheight: 3,
        center: 4,
        flex: 5,
        file_count: 6,
        disable_click: 7,
        root: 8,
        hidden: 9,
        format: 21,
        uploading: 1,
        hidden_upload: 2,
        show_progress: 10,
        max_file_size: 22,
        upload: 23,
        stream_handler: 11,
        paste_clipboard: 12,
        open_file_upload: 13,
        load_files: 24
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[12];
  }
  get open_file_upload() {
    return this.$$.ctx[13];
  }
  get load_files() {
    return this.$$.ctx[24];
  }
}
const {
  SvelteComponent: sc,
  append: ll,
  attr: rc,
  check_outros: il,
  create_component: Xt,
  destroy_component: Gt,
  detach: fc,
  element: uc,
  group_outros: ol,
  init: _c,
  insert: cc,
  mount_component: Kt,
  safe_not_equal: dc,
  set_style: oo,
  space: al,
  toggle_class: ao,
  transition_in: ae,
  transition_out: Fe
} = window.__gradio__svelte__internal, { createEventDispatcher: mc } = window.__gradio__svelte__internal;
function so(l) {
  let e, t;
  return e = new jn({
    props: {
      Icon: vo,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      Xt(e.$$.fragment);
    },
    m(n, i) {
      Kt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.edit")), e.$set(o);
    },
    i(n) {
      t || (ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Gt(e, n);
    }
  };
}
function ro(l) {
  let e, t;
  return e = new jn({
    props: {
      Icon: yo,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      Xt(e.$$.fragment);
    },
    m(n, i) {
      Kt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.undo")), e.$set(o);
    },
    i(n) {
      t || (ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Gt(e, n);
    }
  };
}
function fo(l) {
  let e, t;
  return e = new Al({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: { default: [hc] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Xt(e.$$.fragment);
    },
    m(n, i) {
      Kt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Gt(e, n);
    }
  };
}
function hc(l) {
  let e, t;
  return e = new jn({
    props: {
      Icon: El,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      Xt(e.$$.fragment);
    },
    m(n, i) {
      Kt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.download")), e.$set(o);
    },
    i(n) {
      t || (ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Gt(e, n);
    }
  };
}
function gc(l) {
  let e, t, n, i, o, r, f = (
    /*editable*/
    l[0] && so(l)
  ), a = (
    /*undoable*/
    l[1] && ro(l)
  ), s = (
    /*download*/
    l[2] && fo(l)
  );
  return o = new jn({
    props: {
      Icon: Ll,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = uc("div"), f && f.c(), t = al(), a && a.c(), n = al(), s && s.c(), i = al(), Xt(o.$$.fragment), rc(e, "class", "svelte-1wj0ocy"), ao(e, "not-absolute", !/*absolute*/
      l[3]), oo(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(u, _) {
      cc(u, e, _), f && f.m(e, null), ll(e, t), a && a.m(e, null), ll(e, n), s && s.m(e, null), ll(e, i), Kt(o, e, null), r = !0;
    },
    p(u, [_]) {
      /*editable*/
      u[0] ? f ? (f.p(u, _), _ & /*editable*/
      1 && ae(f, 1)) : (f = so(u), f.c(), ae(f, 1), f.m(e, t)) : f && (ol(), Fe(f, 1, 1, () => {
        f = null;
      }), il()), /*undoable*/
      u[1] ? a ? (a.p(u, _), _ & /*undoable*/
      2 && ae(a, 1)) : (a = ro(u), a.c(), ae(a, 1), a.m(e, n)) : a && (ol(), Fe(a, 1, 1, () => {
        a = null;
      }), il()), /*download*/
      u[2] ? s ? (s.p(u, _), _ & /*download*/
      4 && ae(s, 1)) : (s = fo(u), s.c(), ae(s, 1), s.m(e, i)) : s && (ol(), Fe(s, 1, 1, () => {
        s = null;
      }), il());
      const d = {};
      _ & /*i18n*/
      16 && (d.label = /*i18n*/
      u[4]("common.clear")), o.$set(d), (!r || _ & /*absolute*/
      8) && ao(e, "not-absolute", !/*absolute*/
      u[3]), _ & /*absolute*/
      8 && oo(
        e,
        "position",
        /*absolute*/
        u[3] ? "absolute" : "static"
      );
    },
    i(u) {
      r || (ae(f), ae(a), ae(s), ae(o.$$.fragment, u), r = !0);
    },
    o(u) {
      Fe(f), Fe(a), Fe(s), Fe(o.$$.fragment, u), r = !1;
    },
    d(u) {
      u && fc(e), f && f.d(), a && a.d(), s && s.d(), Gt(o);
    }
  };
}
function bc(l, e, t) {
  let { editable: n = !1 } = e, { undoable: i = !1 } = e, { download: o = null } = e, { absolute: r = !0 } = e, { i18n: f } = e;
  const a = mc(), s = () => a("edit"), u = () => a("undo"), _ = (d) => {
    a("clear"), d.stopPropagation();
  };
  return l.$$set = (d) => {
    "editable" in d && t(0, n = d.editable), "undoable" in d && t(1, i = d.undoable), "download" in d && t(2, o = d.download), "absolute" in d && t(3, r = d.absolute), "i18n" in d && t(4, f = d.i18n);
  }, [
    n,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _
  ];
}
class wc extends sc {
  constructor(e) {
    super(), _c(this, e, bc, gc, dc, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
const {
  SvelteComponent: pc,
  add_flush_callback: vc,
  bind: kc,
  binding_callbacks: yc,
  bubble: sl,
  check_outros: Cc,
  create_component: qn,
  create_slot: qc,
  destroy_component: zn,
  detach: zl,
  empty: zc,
  get_all_dirty_from_scope: Sc,
  get_slot_changes: Lc,
  group_outros: Ec,
  init: jc,
  insert: Sl,
  mount_component: Sn,
  safe_not_equal: Fc,
  space: fa,
  transition_in: pt,
  transition_out: vt,
  update_slot_base: Ic
} = window.__gradio__svelte__internal, { createEventDispatcher: Dc, tick: Ac } = window.__gradio__svelte__internal;
function Mc(l) {
  let e, t, n;
  function i(r) {
    l[18](r);
  }
  let o = {
    filetype: (
      /*file_types*/
      l[4]
    ),
    file_count: (
      /*file_count*/
      l[3]
    ),
    max_file_size: (
      /*max_file_size*/
      l[9]
    ),
    root: (
      /*root*/
      l[6]
    ),
    stream_handler: (
      /*stream_handler*/
      l[11]
    ),
    upload: (
      /*upload*/
      l[10]
    ),
    $$slots: { default: [Tc] },
    $$scope: { ctx: l }
  };
  return (
    /*dragging*/
    l[12] !== void 0 && (o.dragging = /*dragging*/
    l[12]), e = new ac({ props: o }), yc.push(() => kc(e, "dragging", i)), e.$on(
      "load",
      /*handle_upload*/
      l[13]
    ), e.$on(
      "error",
      /*error_handler*/
      l[19]
    ), {
      c() {
        qn(e.$$.fragment);
      },
      m(r, f) {
        Sn(e, r, f), n = !0;
      },
      p(r, f) {
        const a = {};
        f & /*file_types*/
        16 && (a.filetype = /*file_types*/
        r[4]), f & /*file_count*/
        8 && (a.file_count = /*file_count*/
        r[3]), f & /*max_file_size*/
        512 && (a.max_file_size = /*max_file_size*/
        r[9]), f & /*root*/
        64 && (a.root = /*root*/
        r[6]), f & /*stream_handler*/
        2048 && (a.stream_handler = /*stream_handler*/
        r[11]), f & /*upload*/
        1024 && (a.upload = /*upload*/
        r[10]), f & /*$$scope*/
        1048576 && (a.$$scope = { dirty: f, ctx: r }), !t && f & /*dragging*/
        4096 && (t = !0, a.dragging = /*dragging*/
        r[12], vc(() => t = !1)), e.$set(a);
      },
      i(r) {
        n || (pt(e.$$.fragment, r), n = !0);
      },
      o(r) {
        vt(e.$$.fragment, r), n = !1;
      },
      d(r) {
        zn(e, r);
      }
    }
  );
}
function Bc(l) {
  let e, t, n, i;
  return e = new wc({
    props: { i18n: (
      /*i18n*/
      l[8]
    ), absolute: !0 }
  }), e.$on(
    "clear",
    /*handle_clear*/
    l[14]
  ), n = new E_({
    props: {
      i18n: (
        /*i18n*/
        l[8]
      ),
      selectable: (
        /*selectable*/
        l[5]
      ),
      value: (
        /*value*/
        l[0]
      ),
      height: (
        /*height*/
        l[7]
      )
    }
  }), n.$on(
    "select",
    /*select_handler*/
    l[16]
  ), n.$on(
    "change",
    /*change_handler*/
    l[17]
  ), {
    c() {
      qn(e.$$.fragment), t = fa(), qn(n.$$.fragment);
    },
    m(o, r) {
      Sn(e, o, r), Sl(o, t, r), Sn(n, o, r), i = !0;
    },
    p(o, r) {
      const f = {};
      r & /*i18n*/
      256 && (f.i18n = /*i18n*/
      o[8]), e.$set(f);
      const a = {};
      r & /*i18n*/
      256 && (a.i18n = /*i18n*/
      o[8]), r & /*selectable*/
      32 && (a.selectable = /*selectable*/
      o[5]), r & /*value*/
      1 && (a.value = /*value*/
      o[0]), r & /*height*/
      128 && (a.height = /*height*/
      o[7]), n.$set(a);
    },
    i(o) {
      i || (pt(e.$$.fragment, o), pt(n.$$.fragment, o), i = !0);
    },
    o(o) {
      vt(e.$$.fragment, o), vt(n.$$.fragment, o), i = !1;
    },
    d(o) {
      o && zl(t), zn(e, o), zn(n, o);
    }
  };
}
function Tc(l) {
  let e;
  const t = (
    /*#slots*/
    l[15].default
  ), n = qc(
    t,
    l,
    /*$$scope*/
    l[20],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      1048576) && Ic(
        n,
        t,
        i,
        /*$$scope*/
        i[20],
        e ? Lc(
          t,
          /*$$scope*/
          i[20],
          o,
          null
        ) : Sc(
          /*$$scope*/
          i[20]
        ),
        null
      );
    },
    i(i) {
      e || (pt(n, i), e = !0);
    },
    o(i) {
      vt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Rc(l) {
  let e, t, n, i, o, r, f;
  e = new Yu({
    props: {
      show_label: (
        /*show_label*/
        l[2]
      ),
      Icon: er,
      float: (
        /*value*/
        l[0] === null
      ),
      label: (
        /*label*/
        l[1] || "File"
      )
    }
  });
  const a = [Bc, Mc], s = [];
  function u(_, d) {
    return d & /*value*/
    1 && (n = null), n == null && (n = !!/*value*/
    (_[0] && (!Array.isArray(
      /*value*/
      _[0]
    ) || /*value*/
    _[0].length > 0))), n ? 0 : 1;
  }
  return i = u(l, -1), o = s[i] = a[i](l), {
    c() {
      qn(e.$$.fragment), t = fa(), o.c(), r = zc();
    },
    m(_, d) {
      Sn(e, _, d), Sl(_, t, d), s[i].m(_, d), Sl(_, r, d), f = !0;
    },
    p(_, [d]) {
      const c = {};
      d & /*show_label*/
      4 && (c.show_label = /*show_label*/
      _[2]), d & /*value*/
      1 && (c.float = /*value*/
      _[0] === null), d & /*label*/
      2 && (c.label = /*label*/
      _[1] || "File"), e.$set(c);
      let m = i;
      i = u(_, d), i === m ? s[i].p(_, d) : (Ec(), vt(s[m], 1, 1, () => {
        s[m] = null;
      }), Cc(), o = s[i], o ? o.p(_, d) : (o = s[i] = a[i](_), o.c()), pt(o, 1), o.m(r.parentNode, r));
    },
    i(_) {
      f || (pt(e.$$.fragment, _), pt(o), f = !0);
    },
    o(_) {
      vt(e.$$.fragment, _), vt(o), f = !1;
    },
    d(_) {
      _ && (zl(t), zl(r)), zn(e, _), s[i].d(_);
    }
  };
}
function Nc(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(C, T, U, R) {
    function Y(W) {
      return W instanceof U ? W : new U(function(V) {
        V(W);
      });
    }
    return new (U || (U = Promise))(function(W, V) {
      function me(O) {
        try {
          J(R.next(O));
        } catch (te) {
          V(te);
        }
      }
      function Ze(O) {
        try {
          J(R.throw(O));
        } catch (te) {
          V(te);
        }
      }
      function J(O) {
        O.done ? W(O.value) : Y(O.value).then(me, Ze);
      }
      J((R = R.apply(C, T || [])).next());
    });
  };
  let { value: r } = e, { label: f } = e, { show_label: a = !0 } = e, { file_count: s = "single" } = e, { file_types: u = null } = e, { selectable: _ = !1 } = e, { root: d } = e, { height: c = void 0 } = e, { i18n: m } = e, { max_file_size: h = null } = e, { upload: p } = e, { stream_handler: v } = e;
  function g(C) {
    return o(this, arguments, void 0, function* ({ detail: T }) {
      t(0, r = T), yield Ac(), b("change", r), b("upload", T);
    });
  }
  function w() {
    t(0, r = null), b("change", null), b("clear");
  }
  const b = Dc();
  let L = !1;
  function q(C) {
    sl.call(this, l, C);
  }
  function z(C) {
    sl.call(this, l, C);
  }
  function E(C) {
    L = C, t(12, L);
  }
  function F(C) {
    sl.call(this, l, C);
  }
  return l.$$set = (C) => {
    "value" in C && t(0, r = C.value), "label" in C && t(1, f = C.label), "show_label" in C && t(2, a = C.show_label), "file_count" in C && t(3, s = C.file_count), "file_types" in C && t(4, u = C.file_types), "selectable" in C && t(5, _ = C.selectable), "root" in C && t(6, d = C.root), "height" in C && t(7, c = C.height), "i18n" in C && t(8, m = C.i18n), "max_file_size" in C && t(9, h = C.max_file_size), "upload" in C && t(10, p = C.upload), "stream_handler" in C && t(11, v = C.stream_handler), "$$scope" in C && t(20, i = C.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*dragging*/
    4096 && b("drag", L);
  }, [
    r,
    f,
    a,
    s,
    u,
    _,
    d,
    c,
    m,
    h,
    p,
    v,
    L,
    g,
    w,
    n,
    q,
    z,
    E,
    F,
    i
  ];
}
class Uc extends pc {
  constructor(e) {
    super(), jc(this, e, Nc, Rc, Fc, {
      value: 0,
      label: 1,
      show_label: 2,
      file_count: 3,
      file_types: 4,
      selectable: 5,
      root: 6,
      height: 7,
      i18n: 8,
      max_file_size: 9,
      upload: 10,
      stream_handler: 11
    });
  }
}
const {
  SvelteComponent: Vc,
  add_flush_callback: uo,
  assign: Oc,
  bind: _o,
  binding_callbacks: co,
  check_outros: Pc,
  create_component: Yt,
  destroy_component: Jt,
  detach: mo,
  empty: Zc,
  get_spread_object: Wc,
  get_spread_update: Hc,
  group_outros: Xc,
  init: Gc,
  insert: ho,
  mount_component: Qt,
  safe_not_equal: Kc,
  space: Yc,
  transition_in: kt,
  transition_out: yt
} = window.__gradio__svelte__internal, { createEventDispatcher: Jc } = window.__gradio__svelte__internal;
function Qc(l) {
  let e, t, n, i;
  function o(a) {
    l[27](a);
  }
  function r(a) {
    l[28](a);
  }
  let f = {
    deletable: (
      /*deletable*/
      l[9]
    ),
    label: (
      /*label*/
      l[4]
    ),
    show_label: (
      /*show_label*/
      l[3]
    ),
    columns: (
      /*columns*/
      l[13]
    ),
    rows: (
      /*rows*/
      l[14]
    ),
    height: (
      /*height*/
      l[15]
    ),
    preview: (
      /*preview*/
      l[16]
    ),
    object_fit: (
      /*object_fit*/
      l[18]
    ),
    interactive: (
      /*interactive*/
      l[20]
    ),
    allow_preview: (
      /*allow_preview*/
      l[17]
    ),
    show_share_button: (
      /*show_share_button*/
      l[19]
    ),
    show_download_button: (
      /*show_download_button*/
      l[21]
    ),
    i18n: (
      /*gradio*/
      l[22].i18n
    ),
    _fetch: (
      /*gradio*/
      l[22].client.fetch
    )
  };
  return (
    /*selected_index*/
    l[1] !== void 0 && (f.selected_index = /*selected_index*/
    l[1]), /*value*/
    l[0] !== void 0 && (f.value = /*value*/
    l[0]), e = new Qf({ props: f }), co.push(() => _o(e, "selected_index", o)), co.push(() => _o(e, "value", r)), e.$on(
      "change",
      /*change_handler*/
      l[29]
    ), e.$on(
      "select",
      /*select_handler*/
      l[30]
    ), e.$on(
      "share",
      /*share_handler*/
      l[31]
    ), e.$on(
      "delete_image",
      /*delete_image_handler*/
      l[32]
    ), e.$on(
      "error",
      /*error_handler_1*/
      l[33]
    ), {
      c() {
        Yt(e.$$.fragment);
      },
      m(a, s) {
        Qt(e, a, s), i = !0;
      },
      p(a, s) {
        const u = {};
        s[0] & /*deletable*/
        512 && (u.deletable = /*deletable*/
        a[9]), s[0] & /*label*/
        16 && (u.label = /*label*/
        a[4]), s[0] & /*show_label*/
        8 && (u.show_label = /*show_label*/
        a[3]), s[0] & /*columns*/
        8192 && (u.columns = /*columns*/
        a[13]), s[0] & /*rows*/
        16384 && (u.rows = /*rows*/
        a[14]), s[0] & /*height*/
        32768 && (u.height = /*height*/
        a[15]), s[0] & /*preview*/
        65536 && (u.preview = /*preview*/
        a[16]), s[0] & /*object_fit*/
        262144 && (u.object_fit = /*object_fit*/
        a[18]), s[0] & /*interactive*/
        1048576 && (u.interactive = /*interactive*/
        a[20]), s[0] & /*allow_preview*/
        131072 && (u.allow_preview = /*allow_preview*/
        a[17]), s[0] & /*show_share_button*/
        524288 && (u.show_share_button = /*show_share_button*/
        a[19]), s[0] & /*show_download_button*/
        2097152 && (u.show_download_button = /*show_download_button*/
        a[21]), s[0] & /*gradio*/
        4194304 && (u.i18n = /*gradio*/
        a[22].i18n), s[0] & /*gradio*/
        4194304 && (u._fetch = /*gradio*/
        a[22].client.fetch), !t && s[0] & /*selected_index*/
        2 && (t = !0, u.selected_index = /*selected_index*/
        a[1], uo(() => t = !1)), !n && s[0] & /*value*/
        1 && (n = !0, u.value = /*value*/
        a[0], uo(() => n = !1)), e.$set(u);
      },
      i(a) {
        i || (kt(e.$$.fragment, a), i = !0);
      },
      o(a) {
        yt(e.$$.fragment, a), i = !1;
      },
      d(a) {
        Jt(e, a);
      }
    }
  );
}
function xc(l) {
  let e, t;
  return e = new Uc({
    props: {
      value: null,
      root: (
        /*root*/
        l[5]
      ),
      label: (
        /*label*/
        l[4]
      ),
      max_file_size: (
        /*gradio*/
        l[22].max_file_size
      ),
      file_count: "multiple",
      file_types: ["image"],
      i18n: (
        /*gradio*/
        l[22].i18n
      ),
      upload: (
        /*gradio*/
        l[22].client.upload
      ),
      stream_handler: (
        /*gradio*/
        l[22].client.stream
      ),
      $$slots: { default: [$c] },
      $$scope: { ctx: l }
    }
  }), e.$on(
    "upload",
    /*upload_handler*/
    l[25]
  ), e.$on(
    "error",
    /*error_handler*/
    l[26]
  ), {
    c() {
      Yt(e.$$.fragment);
    },
    m(n, i) {
      Qt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      32 && (o.root = /*root*/
      n[5]), i[0] & /*label*/
      16 && (o.label = /*label*/
      n[4]), i[0] & /*gradio*/
      4194304 && (o.max_file_size = /*gradio*/
      n[22].max_file_size), i[0] & /*gradio*/
      4194304 && (o.i18n = /*gradio*/
      n[22].i18n), i[0] & /*gradio*/
      4194304 && (o.upload = /*gradio*/
      n[22].client.upload), i[0] & /*gradio*/
      4194304 && (o.stream_handler = /*gradio*/
      n[22].client.stream), i[0] & /*gradio*/
      4194304 | i[1] & /*$$scope*/
      16 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (kt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      yt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Jt(e, n);
    }
  };
}
function $c(l) {
  let e, t;
  return e = new Qr({
    props: {
      i18n: (
        /*gradio*/
        l[22].i18n
      ),
      type: "gallery"
    }
  }), {
    c() {
      Yt(e.$$.fragment);
    },
    m(n, i) {
      Qt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*gradio*/
      4194304 && (o.i18n = /*gradio*/
      n[22].i18n), e.$set(o);
    },
    i(n) {
      t || (kt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      yt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Jt(e, n);
    }
  };
}
function ed(l) {
  let e, t, n, i, o, r;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        l[22].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[22].i18n
    ) },
    /*loading_status*/
    l[2]
  ];
  let a = {};
  for (let d = 0; d < f.length; d += 1)
    a = Oc(a, f[d]);
  e = new Au({ props: a }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[24]
  );
  const s = [xc, Qc], u = [];
  function _(d, c) {
    return (
      /*interactive*/
      d[20] && /*no_value*/
      d[23] ? 0 : 1
    );
  }
  return n = _(l), i = u[n] = s[n](l), {
    c() {
      Yt(e.$$.fragment), t = Yc(), i.c(), o = Zc();
    },
    m(d, c) {
      Qt(e, d, c), ho(d, t, c), u[n].m(d, c), ho(d, o, c), r = !0;
    },
    p(d, c) {
      const m = c[0] & /*gradio, loading_status*/
      4194308 ? Hc(f, [
        c[0] & /*gradio*/
        4194304 && {
          autoscroll: (
            /*gradio*/
            d[22].autoscroll
          )
        },
        c[0] & /*gradio*/
        4194304 && { i18n: (
          /*gradio*/
          d[22].i18n
        ) },
        c[0] & /*loading_status*/
        4 && Wc(
          /*loading_status*/
          d[2]
        )
      ]) : {};
      e.$set(m);
      let h = n;
      n = _(d), n === h ? u[n].p(d, c) : (Xc(), yt(u[h], 1, 1, () => {
        u[h] = null;
      }), Pc(), i = u[n], i ? i.p(d, c) : (i = u[n] = s[n](d), i.c()), kt(i, 1), i.m(o.parentNode, o));
    },
    i(d) {
      r || (kt(e.$$.fragment, d), kt(i), r = !0);
    },
    o(d) {
      yt(e.$$.fragment, d), yt(i), r = !1;
    },
    d(d) {
      d && (mo(t), mo(o)), Jt(e, d), u[n].d(d);
    }
  };
}
function td(l) {
  let e, t;
  return e = new Sa({
    props: {
      visible: (
        /*visible*/
        l[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[6]
      ),
      elem_classes: (
        /*elem_classes*/
        l[7]
      ),
      container: (
        /*container*/
        l[10]
      ),
      scale: (
        /*scale*/
        l[11]
      ),
      min_width: (
        /*min_width*/
        l[12]
      ),
      allow_overflow: !1,
      height: typeof /*height*/
      l[15] == "number" ? (
        /*height*/
        l[15]
      ) : void 0,
      $$slots: { default: [ed] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Yt(e.$$.fragment);
    },
    m(n, i) {
      Qt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      n[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      n[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      n[7]), i[0] & /*container*/
      1024 && (o.container = /*container*/
      n[10]), i[0] & /*scale*/
      2048 && (o.scale = /*scale*/
      n[11]), i[0] & /*min_width*/
      4096 && (o.min_width = /*min_width*/
      n[12]), i[0] & /*height*/
      32768 && (o.height = typeof /*height*/
      n[15] == "number" ? (
        /*height*/
        n[15]
      ) : void 0), i[0] & /*root, label, gradio, value, loading_status, interactive, no_value, deletable, show_label, columns, rows, height, preview, object_fit, allow_preview, show_share_button, show_download_button, selected_index*/
      16769599 | i[1] & /*$$scope*/
      16 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (kt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      yt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Jt(e, n);
    }
  };
}
function nd(l, e, t) {
  let n, { loading_status: i } = e, { show_label: o } = e, { label: r } = e, { root: f } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: u = !0 } = e, { value: _ = null } = e, { deletable: d } = e, { container: c = !0 } = e, { scale: m = null } = e, { min_width: h = void 0 } = e, { columns: p = [2] } = e, { rows: v = void 0 } = e, { height: g = "auto" } = e, { preview: w } = e, { allow_preview: b = !0 } = e, { selected_index: L = null } = e, { object_fit: q = "cover" } = e, { show_share_button: z = !1 } = e, { interactive: E } = e, { show_download_button: F = !1 } = e, { gradio: C } = e;
  const T = Jc(), U = () => C.dispatch("clear_status", i), R = (S) => {
    const xe = Array.isArray(S.detail) ? S.detail : [S.detail];
    t(0, _ = xe.map((ft) => ({ image: ft, caption: null }))), C.dispatch("upload", _);
  }, Y = ({ detail: S }) => {
    t(2, i = i || {}), t(2, i.status = "error", i), C.dispatch("error", S);
  };
  function W(S) {
    L = S, t(1, L);
  }
  function V(S) {
    _ = S, t(0, _);
  }
  const me = () => C.dispatch("change", _), Ze = (S) => C.dispatch("select", S.detail), J = (S) => C.dispatch("share", S.detail), O = (S) => C.dispatch("delete_image", S.detail), te = (S) => C.dispatch("error", S.detail);
  return l.$$set = (S) => {
    "loading_status" in S && t(2, i = S.loading_status), "show_label" in S && t(3, o = S.show_label), "label" in S && t(4, r = S.label), "root" in S && t(5, f = S.root), "elem_id" in S && t(6, a = S.elem_id), "elem_classes" in S && t(7, s = S.elem_classes), "visible" in S && t(8, u = S.visible), "value" in S && t(0, _ = S.value), "deletable" in S && t(9, d = S.deletable), "container" in S && t(10, c = S.container), "scale" in S && t(11, m = S.scale), "min_width" in S && t(12, h = S.min_width), "columns" in S && t(13, p = S.columns), "rows" in S && t(14, v = S.rows), "height" in S && t(15, g = S.height), "preview" in S && t(16, w = S.preview), "allow_preview" in S && t(17, b = S.allow_preview), "selected_index" in S && t(1, L = S.selected_index), "object_fit" in S && t(18, q = S.object_fit), "show_share_button" in S && t(19, z = S.show_share_button), "interactive" in S && t(20, E = S.interactive), "show_download_button" in S && t(21, F = S.show_download_button), "gradio" in S && t(22, C = S.gradio);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1 && t(23, n = Array.isArray(_) ? _.length === 0 : !_), l.$$.dirty[0] & /*selected_index*/
    2 && T("prop_change", { selected_index: L });
  }, [
    _,
    L,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    d,
    c,
    m,
    h,
    p,
    v,
    g,
    w,
    b,
    q,
    z,
    E,
    F,
    C,
    n,
    U,
    R,
    Y,
    W,
    V,
    me,
    Ze,
    J,
    O,
    te
  ];
}
class ud extends Vc {
  constructor(e) {
    super(), Gc(
      this,
      e,
      nd,
      td,
      Kc,
      {
        loading_status: 2,
        show_label: 3,
        label: 4,
        root: 5,
        elem_id: 6,
        elem_classes: 7,
        visible: 8,
        value: 0,
        deletable: 9,
        container: 10,
        scale: 11,
        min_width: 12,
        columns: 13,
        rows: 14,
        height: 15,
        preview: 16,
        allow_preview: 17,
        selected_index: 1,
        object_fit: 18,
        show_share_button: 19,
        interactive: 20,
        show_download_button: 21,
        gradio: 22
      },
      null,
      [-1, -1]
    );
  }
}
export {
  Qf as BaseGallery,
  ud as default
};
