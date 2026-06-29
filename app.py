import streamlit as st
from datetime import date, datetime, timedelta
from bazi_calc import (
    NATAL, WUXING_STEM, WUXING_BRANCH, ZANGGAN,
    get_day_ganzhi, get_month_ganzhi, get_year_ganzhi,
    get_current_dayun, get_shishen, day_recommendation,
    get_week_preview, get_shichen_guide,
)

st.set_page_config(page_title="安琪·命理日历", page_icon="☯", layout="wide",
                   initial_sidebar_state="collapsed")

# Global CSS — only place that needs st.markdown
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Noto Serif SC', serif; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
div[data-testid="stTabs"] button {
    font-family: 'Noto Serif SC', serif; font-size: 14px;
    letter-spacing: 2px; color: #667788;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #d4a843; border-bottom: 2px solid #d4a843;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
WX_COLORS = {'木': '#52B788', '火': '#E05C5C', '土': '#C9A84C', '金': '#A8B8C8', '水': '#4A90D9'}

def sp(h):  # spacer
    st.html(f"<div style='height:{h};'></div>")

def card(inner, title=""):
    hdr = ""
    if title:
        hdr = f"<div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #1e2d40;'>{title}</div>"
    st.html(f"<div style='background:#0d1321;border:1px solid #1e2d40;border-radius:16px;padding:22px 20px;'>{hdr}{inner}</div>")

def dots(filled, total, fill_color, empty_color="#1e2d40"):
    return (f"<span style='color:{fill_color};'>" + "●" * filled + "</span>"
            + f"<span style='color:{empty_color};'>" + "●" * (total - filled) + "</span>")

# ── Data ───────────────────────────────────────────────────────────────────────
today        = date.today()
yr_s, yr_b   = get_year_ganzhi(today.year)
mo_s, mo_b   = get_month_ganzhi(today)
day_s, day_b = get_day_ganzhi(today)
rec          = day_recommendation(day_s, day_b)
dayun        = get_current_dayun(today)
week         = get_week_preview(today)
shichen      = get_shichen_guide()
age_now      = (today - NATAL['birthday']).days / 365.25
day_ss       = get_shishen(NATAL['day_master'], day_s)
wx_color     = rec['color']

# ── Header ─────────────────────────────────────────────────────────────────────
st.html(f"""
<div style='text-align:center;padding:6px 0 22px;font-family:Noto Serif SC,serif;'>
  <div style='color:#d4a843;font-size:11px;letter-spacing:6px;margin-bottom:6px;'>命 理 日 历</div>
  <div style='color:#e8e8e8;font-size:26px;font-weight:700;letter-spacing:6px;margin-bottom:4px;'>安 琪</div>
  <div style='color:#445566;font-size:13px;letter-spacing:2px;'>
    {today.strftime('%Y年%m月%d日')} &nbsp;·&nbsp; {yr_s}{yr_b}年 {mo_s}{mo_b}月 {day_s}{day_b}日
  </div>
</div>
""")

tab1, tab2, tab3 = st.tabs(["✦ 今日运势", "✦ 命盘八字", "✦ 大运流年"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.html(f"""
    <div style='background:linear-gradient(135deg,#0d1321,#111827,#0d1829);
                border:1px solid #1e2d40;border-radius:20px;padding:28px 32px;
                margin-bottom:8px;display:flex;align-items:center;gap:36px;flex-wrap:wrap;
                font-family:Noto Serif SC,serif;'>
      <div style='min-width:120px;'>
        <div style='color:#445566;font-size:11px;letter-spacing:3px;margin-bottom:8px;'>TODAY</div>
        <div style='color:{wx_color};font-size:56px;font-weight:900;line-height:1;'>{day_s}</div>
        <div style='color:{wx_color};opacity:0.5;font-size:56px;font-weight:900;line-height:1;margin-top:-4px;'>{day_b}</div>
        <div style='color:#445566;font-size:12px;margin-top:10px;'>{WUXING_STEM[day_s]} · {day_ss}</div>
      </div>
      <div style='flex:1;min-width:200px;'>
        <div style='font-size:34px;margin-bottom:6px;'>{rec["emoji"]}</div>
        <div style='color:{wx_color};font-size:20px;font-weight:700;letter-spacing:2px;margin-bottom:10px;'>{rec["title"]}</div>
        <div style='color:#7a8a9a;font-size:13px;line-height:1.85;max-width:460px;'>{rec["summary"]}</div>
      </div>
      <div style='text-align:center;min-width:90px;'>
        <div style='color:#445566;font-size:11px;letter-spacing:2px;margin-bottom:10px;'>能量指数</div>
        <div style='font-size:24px;letter-spacing:5px;'>{dots(rec["score"], 5, wx_color)}</div>
        <div style='color:#445566;font-size:12px;margin-top:8px;'>{rec["score"]} / 5</div>
      </div>
    </div>
    """)

    # ── Three columns ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1.05, 0.85, 1.1], gap="medium")

    # LEFT — Recommendations
    with col1:
        interaction = {
            '水': '水克火、润戊土之燥。今日财星当令，思维敏锐流动，适合主动出击与决策。',
            '木': '木克土，官杀逢令，压力背后藏机遇。主动争取，有望晋升或获认可。',
            '金': '土生金，食伤泄秀，才华输出顺畅。表达、创作、汇报皆有灵感涌现。',
            '火': '火生土，偏印当令，命局火已偏旺。今日再旺，宜静不宜动，养心为要。',
            '土': '土旺同类，比劫并肩，格局略显壅滞。低调稳健，专注本职，慎防竞争。',
        }
        action_rows = ""
        for a in rec['actions']:
            action_rows += (
                f"<div style='display:flex;align-items:flex-start;padding:9px 0;"
                f"border-bottom:1px solid #141c28;gap:10px;'>"
                f"<span style='color:#d4a843;flex-shrink:0;'>▸</span>"
                f"<span style='color:#c8d8e8;font-size:13px;line-height:1.5;'>{a}</span></div>"
            )
        card(f"""
        <div style='color:#445566;font-size:11px;letter-spacing:2px;margin-bottom:6px;'>今日宜</div>
        {action_rows}
        <div style='background:rgba(201,107,107,0.08);border-left:3px solid #c96b6b;
                    border-radius:0 8px 8px 0;padding:11px 14px;margin-top:12px;'>
          <span style='color:#c96b6b;font-size:11px;letter-spacing:1px;'>注意 · </span>
          <span style='color:#c8a0a0;font-size:12px;'>{rec["caution"]}</span>
        </div>
        <div style='margin-top:14px;padding:14px;background:rgba(255,255,255,0.02);
                    border-radius:10px;border:1px solid #1e2d40;'>
          <div style='color:#d4a843;font-size:11px;letter-spacing:2px;margin-bottom:8px;'>五行交互</div>
          <div style='color:#7a8a9a;font-size:12px;line-height:1.9;'>{interaction[WUXING_STEM[day_s]]}</div>
        </div>
        """, "今日指引")

    # CENTER — Shichen guide
    with col2:
        current_hour = datetime.now().hour
        branch_list  = list('子丑寅卯辰巳午未申酉戌亥')
        hour_starts  = [23,1,3,5,7,9,11,13,15,17,19,21]
        rows_html = ""
        for entry in shichen:
            idx     = branch_list.index(entry['branch'])
            h_start = hour_starts[idx]
            is_now  = (current_hour == h_start or
                       (h_start == 23 and current_hour == 0) or
                       (h_start < current_hour < h_start + 2))
            q       = entry['quality']
            dot_c   = {'good': '#52B788', 'neutral': '#445566', 'bad': '#c96b6b'}[q]
            row_bg  = {'good': 'rgba(82,183,136,0.1)',
                       'neutral': 'rgba(255,255,255,0.02)',
                       'bad': 'rgba(224,92,92,0.07)'}[q]
            now_mark = "<span style='color:#d4a843;font-size:10px;margin-left:4px;'>◀</span>" if is_now else ""
            border   = "border:1px solid #d4a84355;" if is_now else "border:1px solid transparent;"
            rows_html += (
                f"<div style='display:flex;align-items:center;gap:8px;padding:7px 8px;"
                f"border-radius:8px;margin-bottom:3px;background:{row_bg};{border}'>"
                f"<div style='color:#556677;font-size:10px;width:34px;flex-shrink:0;'>{entry['time']}</div>"
                f"<div style='color:{dot_c};font-size:14px;font-weight:700;width:16px;flex-shrink:0;'>{entry['branch']}</div>"
                f"<div style='color:#445566;font-size:11px;flex:1;'>{entry['name']}</div>"
                f"<div style='color:{dot_c};font-size:10px;'>{dots(entry['stars'], 3, dot_c)}</div>"
                f"{now_mark}</div>"
            )
        card(f"""
        {rows_html}
        <div style='margin-top:12px;text-align:center;color:#2a3a4a;font-size:11px;'>
          ●●● 吉 &nbsp;·&nbsp; ●●○ 平 &nbsp;·&nbsp; ●○○ 慎
        </div>
        """, "时辰吉凶")

    # RIGHT — Week preview
    with col3:
        day_names  = ['一', '二', '三', '四', '五', '六', '日']
        week_cells = ""
        for i, w in enumerate(week):
            is_today = (i == 0)
            border   = "border:2px solid #d4a843;" if is_today else "border:1px solid #1e2d40;"
            bg       = "background:rgba(212,168,67,0.06);" if is_today else "background:#0d1321;"
            bar      = "─" * w['score'] + "·" * (5 - w['score'])
            dn       = day_names[w['date'].weekday()]
            week_cells += (
                f"<div style='{border}{bg}border-radius:10px;padding:8px 4px;text-align:center;'>"
                f"<div style='color:#445566;font-size:10px;'>{dn}</div>"
                f"<div style='color:#556677;font-size:10px;'>{w['date'].strftime('%-d')}</div>"
                f"<div style='font-size:18px;margin:3px 0;'>{w['emoji']}</div>"
                f"<div style='color:{w['color']};font-size:11px;font-weight:700;'>{w['stem']}{w['branch']}</div>"
                f"<div style='color:{w['color']};font-size:9px;'>{bar}</div>"
                f"</div>"
            )
        detail_rows = ""
        for w in week[1:]:
            stars  = "★" * w['score'] + "☆" * (5 - w['score'])
            bg     = ('rgba(82,183,136,0.06)' if w['score'] >= 4
                      else 'rgba(201,107,107,0.06)' if w['score'] <= 2
                      else 'rgba(255,255,255,0.02)')
            detail_rows += (
                f"<div style='background:{bg};border:1px solid #1a2535;border-radius:8px;"
                f"padding:7px 12px;margin-bottom:4px;display:flex;align-items:center;gap:10px;'>"
                f"<span style='color:#445566;font-size:11px;width:34px;'>{w['date'].strftime('%-m/%-d')}</span>"
                f"<span style='color:{w['color']};font-size:15px;font-weight:700;width:30px;'>{w['stem']}{w['branch']}</span>"
                f"<span style='color:#445566;font-size:11px;flex:1;'>{w['wx']} · {w['shishen']}</span>"
                f"<span style='color:{w['color']};font-size:10px;'>{stars}</span>"
                f"</div>"
            )
        card(f"""
        <div style='display:grid;grid-template-columns:repeat(8,1fr);gap:3px;margin-bottom:14px;'>
          {week_cells}
        </div>
        <div style='color:#445566;font-size:11px;letter-spacing:2px;margin-bottom:8px;'>未来7天</div>
        {detail_rows}
        """, "本周一览")

    # ── Date lookup ────────────────────────────────────────────────────────────
    sp("12px")
    with st.expander("🔍 查询任意日期", expanded=False):
        qc1, qc2 = st.columns([1, 2])
        with qc1:
            qdate = st.date_input("选择日期", value=today, key="qdate",
                                  min_value=date(1950,1,1), max_value=date(2099,12,31))
        qs, qb = get_day_ganzhi(qdate)
        qrec   = day_recommendation(qs, qb)
        qss    = get_shishen(NATAL['day_master'], qs)
        qstars = "★" * qrec['score'] + "☆" * (5 - qrec['score'])
        with qc2:
            st.html(f"""
            <div style='background:#0d1321;border:1px solid #1e2d40;border-radius:12px;
                        padding:16px 20px;margin-top:6px;font-family:Noto Serif SC,serif;'>
              <div style='display:flex;align-items:center;gap:14px;'>
                <span style='font-size:30px;'>{qrec["emoji"]}</span>
                <div>
                  <div style='color:{qrec["color"]};font-size:17px;font-weight:700;'>
                    {qs}{qb}日 · {qrec["title"]}</div>
                  <div style='color:#667788;font-size:12px;margin-top:3px;'>
                    {qdate.strftime("%Y年%m月%d日")} · {WUXING_STEM[qs]} · {qss} · {qstars}</div>
                </div>
              </div>
              <div style='color:#7a8a9a;font-size:13px;margin-top:11px;line-height:1.8;'>
                {qrec["summary"]}</div>
            </div>
            """)

    # ── Current Period Analysis ─────────────────────────────────────────────────
    sp("10px")
    st.html("<div style='color:#d4a843;font-size:13px;font-weight:600;letter-spacing:3px;padding-bottom:10px;border-bottom:1px solid #1e2d40;font-family:Noto Serif SC,serif;'>当前时期综合分析</div>")
    sp("14px")

    pc1, pc2 = st.columns([1, 1.4], gap="large")

    with pc1:
        if dayun:
            ds, db, da, dy = dayun
            ds_wx  = WUXING_STEM[ds]
            ds_ss  = get_shishen(NATAL['day_master'], ds)
            yr_ss  = get_shishen(NATAL['day_master'], yr_s)
            yr_wx  = WUXING_STEM[yr_s]
            mo_ss  = get_shishen(NATAL['day_master'], mo_s)
            mo_wx  = WUXING_STEM[mo_s]

            def prow(label, gz, wx, ss, sub):
                c = WX_COLORS[wx]
                return (
                    f"<div style='display:flex;align-items:center;gap:14px;padding:12px 0;"
                    f"border-bottom:1px solid #1a2535;'>"
                    f"<div style='color:#445566;font-size:11px;letter-spacing:2px;width:52px;flex-shrink:0;'>{label}</div>"
                    f"<div style='color:{c};font-size:20px;font-weight:700;width:48px;flex-shrink:0;'>{gz}</div>"
                    f"<div><div style='color:#8899aa;font-size:12px;'>{wx}（{ss}）</div>"
                    f"<div style='color:#445566;font-size:11px;margin-top:2px;'>{sub}</div></div>"
                    f"</div>"
                )

            rows = (prow("大运", ds+db, ds_wx, ds_ss, f"{da}–{da+10}岁 · {dy}–{dy+10}年") +
                    prow("流年", yr_s+yr_b, yr_wx, yr_ss, f"{today.year}年 · 年度引动") +
                    prow("流月", mo_s+mo_b, mo_wx, mo_ss, "当月节令 · 近期节奏"))

            st.html(f"""
            <div style='background:linear-gradient(135deg,#0a1520,#0d1f35);
                        border:1px solid #1e3a55;border-radius:16px;padding:20px 22px;
                        font-family:Noto Serif SC,serif;'>
              <div style='color:#667788;font-size:11px;letter-spacing:3px;margin-bottom:4px;'>时间层叠</div>
              {rows}
            </div>
            """)

    with pc2:
        rgba_map = {"#4A90D9":"74,144,217","#52B788":"82,183,136","#c96b6b":"201,107,107","#A8B8C8":"168,184,200"}
        domain_cards = [("#4A90D9","事业","精进专业<br>慎换环境"),
                        ("#52B788","财运","稳健为主<br>忌激进投资"),
                        ("#c96b6b","感情","偏印旺盛<br>需主动沟通"),
                        ("#A8B8C8","健康","火旺伤心<br>注意作息")]
        cards_html = ""
        for c, lbl, txt in domain_cards:
            cards_html += (
                f"<div style='background:rgba({rgba_map[c]},0.1);border:1px solid {c};"
                f"border-radius:8px;padding:10px 14px;flex:1;min-width:110px;'>"
                f"<div style='color:{c};font-size:11px;letter-spacing:1px;margin-bottom:4px;'>{lbl}</div>"
                f"<div style='color:#c8d8e8;font-size:12px;line-height:1.7;'>{txt}</div></div>"
            )
        st.html(f"""
        <div style='font-family:Noto Serif SC,serif;'>
          <div style='color:#d4a843;font-size:14px;font-weight:700;margin-bottom:12px;'>
            丙申大运 × 丙午流年 · 当下解读</div>
          <div style='background:rgba(212,168,67,0.04);border-left:3px solid #d4a843;
                      border-radius:0 10px 10px 0;padding:14px 16px;
                      color:#b8c8d8;font-size:13px;line-height:1.95;'>
            <strong style='color:#d4a843;'>大运格局（2025–2035）：</strong>
            丙火忌神掌天干，申金喜神坐地支，外压内秀之象。
            前半程（2025–2030）偏印旺盛，需防思虑过度；
            后半程（2030–2035）申金食伤发力，才华财运将迎来厚积薄发的收获期。
            <br><br>
            <strong style='color:#d4a843;'>流年叠加（2026 丙午）：</strong>
            丙火流年与大运天干同气相聚，偏印力量为近年最强。
            宜深耕专业，投资自身教育，回报最高。甲午流月火势最旺，
            <strong style='color:#52B788;'>静中求变，厚积薄发。</strong>
            <br><br>
            <strong style='color:#A8B8C8;'>✦ 核心策略：</strong>
            这是积累期，不是爆发期。2028–2030年流年入喜运时，收获将远超当下付出。
          </div>
          <div style='display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;'>{cards_html}</div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sp("8px")
    p = NATAL['pillars']
    cols4 = st.columns(4, gap="medium")
    for i, col_name in enumerate(['时柱', '日柱', '月柱', '年柱']):
        s, b    = p[col_name]
        ss      = get_shishen(NATAL['day_master'], s) if col_name != '日柱' else '日主'
        s_wx    = WUXING_STEM[s]
        b_wx    = WUXING_BRANCH[b]
        sc      = WX_COLORS[s_wx]
        bc      = WX_COLORS[b_wx]
        is_good = s_wx in NATAL['xiyong']
        is_bad  = s_wx in NATAL['ji']
        bdr     = '#52B788' if is_good else ('#c96b6b' if is_bad else '#1e2d40')
        zg      = ZANGGAN[b]
        zg_html = " · ".join(
            f"<span style='color:{WX_COLORS[WUXING_STEM[z]]};'>{z}</span>"
            f"<span style='color:#2a3a4a;'>({n[0]})</span>"
            for z, n in zg
        )
        with cols4[i]:
            st.html(f"""
            <div style='background:linear-gradient(180deg,#0f1726,#0b1220);
                        border:1px solid {bdr};border-radius:14px;padding:20px 12px;
                        text-align:center;font-family:Noto Serif SC,serif;'>
              <div style='color:#334455;font-size:11px;letter-spacing:3px;margin-bottom:12px;'>{col_name}</div>
              <div style='color:{sc};font-size:54px;font-weight:900;line-height:1;'>{s}</div>
              <div style='width:1px;height:18px;background:#1e2d40;margin:4px auto;'></div>
              <div style='color:{bc};font-size:54px;font-weight:900;line-height:1;'>{b}</div>
              <div style='margin-top:14px;padding-top:12px;border-top:1px solid #1a2535;'>
                <div style='color:#d4a843;font-size:13px;margin-bottom:6px;'>{ss}</div>
                <div style='color:#334455;font-size:11px;line-height:1.8;'>{zg_html}</div>
                <div style='color:#1e2d3a;font-size:11px;margin-top:4px;'>{s_wx} · {b_wx}</div>
              </div>
            </div>
            """)

    sp("22px")
    c1, c2, c3 = st.columns([1.1, 0.9, 1], gap="medium")

    with c1:
        st.html(f"""
        <div style='background:#0d1321;border:1px solid #1e2d40;border-radius:16px;
                    padding:22px 20px;font-family:Noto Serif SC,serif;'>
          <div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;
                      margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #1e2d40;'>命局解读</div>
          <div style='color:#334455;font-size:11px;letter-spacing:2px;margin-bottom:6px;'>日主</div>
          <div style='color:#C9A84C;font-size:22px;font-weight:700;margin-bottom:6px;'>戊土 · 阳土</div>
          <div style='color:#7a8a9a;font-size:13px;line-height:1.85;margin-bottom:16px;'>
            生于巳月，火旺土相，临官之地，<span style='color:#52B788;'>身旺</span>。<br>
            双巳火生扶，印星有力；庚申食神泄秀；<br>月干癸水正财透干，财星根深。
          </div>
          <div style='border-top:1px solid #1e2d40;padding-top:14px;margin-bottom:14px;'>
            <div style='color:#334455;font-size:11px;letter-spacing:2px;margin-bottom:6px;'>格局</div>
            <div style='color:#e8e8e8;font-size:14px;font-weight:600;margin-bottom:8px;'>正财格 · 食神生财</div>
            <div style='color:#7a8a9a;font-size:12px;line-height:1.85;'>
              月干癸水透干，坐日支子水，财星有力。<br>庚金食神生癸水，格局清纯。<br>
              <span style='color:#445566;font-size:11px;'>《子平真诠》：食神生财，清秀富贵之格。</span>
            </div>
          </div>
          <div style='border-top:1px solid #1e2d40;padding-top:14px;'>
            <div style='color:#52B788;font-size:12px;margin-bottom:5px;'>▲ 喜用神 · 水 &gt; 木 &gt; 金</div>
            <div style='color:#c96b6b;font-size:12px;'>▼ 忌神 · 火（偏印过旺）· 土（比劫壅滞）</div>
          </div>
        </div>
        """)

    with c2:
        wx_bars = ""
        wx_count = {'木': 0, '火': 3, '土': 3, '金': 4, '水': 3}
        total    = sum(wx_count.values())
        for wx, cnt in wx_count.items():
            pct = cnt / total * 100
            c   = WX_COLORS[wx]
            tag = (" <span style='color:#52B788;font-size:10px;'>喜</span>" if wx in NATAL['xiyong']
                   else " <span style='color:#c96b6b;font-size:10px;'>忌</span>" if wx in NATAL['ji']
                   else "")
            wx_bars += (
                f"<div style='margin-bottom:14px;'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>"
                f"<span style='color:#8899aa;font-size:13px;'>{wx}{tag}</span>"
                f"<span style='color:{c};font-size:12px;font-weight:600;'>{pct:.0f}%</span></div>"
                f"<div style='background:#111827;border-radius:4px;height:6px;overflow:hidden;'>"
                f"<div style='background:linear-gradient(90deg,{c}88,{c});height:6px;"
                f"border-radius:4px;width:{pct:.0f}%;'></div></div></div>"
            )
        st.html(f"""
        <div style='background:#0d1321;border:1px solid #1e2d40;border-radius:16px;
                    padding:22px 20px;font-family:Noto Serif SC,serif;'>
          <div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;
                      margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #1e2d40;'>五行分布</div>
          {wx_bars}
          <div style='background:rgba(82,183,136,0.06);border:1px solid #1e3a2e;
                      border-radius:10px;padding:12px;margin-top:6px;'>
            <div style='color:#52B788;font-size:11px;letter-spacing:1px;margin-bottom:5px;'>《穷通宝典》调候</div>
            <div style='color:#667788;font-size:12px;line-height:1.85;'>
              戊土生巳月，火炎土燥，<br>调候首需壬癸水润土。<br>癸子同柱，调候到位，格局清贵。
            </div>
          </div>
        </div>
        """)

    with c3:
        shensha = [('天乙贵人','丑·未','#d4a843','戊日贵人在丑未，逢凶化吉，关键时刻常有贵人出现。'),
                   ('文昌贵人','申','#4A90D9','时支坐文昌，学习力强，深造进修，知识改变命运。'),
                   ('驿马','寅','#52B788','申子辰驿马在寅，动中求财，异地发展对运势有益。'),
                   ('桃花','酉','#E05C5C','申子辰桃花在酉，异性缘旺，才艺出众，社交活跃。')]
        ss_cards = ""
        for nm, vl, cl, dc in shensha:
            ss_cards += (
                f"<div style='border:1px solid #1e2d40;border-radius:10px;padding:11px 14px;"
                f"margin-bottom:8px;display:flex;gap:14px;align-items:center;'>"
                f"<div style='text-align:center;min-width:48px;'>"
                f"<div style='color:#334455;font-size:10px;margin-bottom:2px;'>{nm}</div>"
                f"<div style='color:{cl};font-size:19px;font-weight:700;'>{vl}</div></div>"
                f"<div style='color:#667788;font-size:12px;line-height:1.7;"
                f"border-left:1px solid #1e2d40;padding-left:12px;'>{dc}</div></div>"
            )
        st.html(f"""
        <div style='background:#0d1321;border:1px solid #1e2d40;border-radius:16px;
                    padding:22px 20px;font-family:Noto Serif SC,serif;'>
          <div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;
                      margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid #1e2d40;'>神煞 · 特质</div>
          {ss_cards}
          <div style='padding:12px 14px;background:rgba(168,184,200,0.05);
                      border-radius:10px;border:1px solid #1e2d40;'>
            <div style='color:#A8B8C8;font-size:11px;letter-spacing:1px;margin-bottom:5px;'>性格特质</div>
            <div style='color:#667788;font-size:12px;line-height:1.85;'>
              戊土厚重踏实，食神才华横溢，正财脚踏实地。<br>
              待人真诚，擅长执行与落实，有天生财务敏感度。<br>
              双巳印旺，直觉敏锐，学习吸收能力强。
            </div>
          </div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    sp("8px")
    cy1, cy2 = st.columns([1, 1.3], gap="large")

    with cy1:
        st.html(f"""
        <div style='font-family:Noto Serif SC,serif;'>
          <div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;
                      padding-bottom:10px;border-bottom:1px solid #1e2d40;margin-bottom:16px;'>大运 · 人生周期</div>
          <div style='background:#0d1321;border:1px solid #1e2d40;border-radius:10px;
                      padding:12px 16px;margin-bottom:14px;'>
            <div style='color:#445566;font-size:11px;'>起运方式</div>
            <div style='color:#d4a843;font-size:16px;font-weight:700;margin:4px 0;'>4岁起运 · 2005年</div>
            <div style='color:#2a3a4a;font-size:12px;'>阴年女命顺排 · 出生距芒种12天 ÷ 3 = 4岁</div>
          </div>
        </div>
        """)

        for s, b, start_age, start_year in NATAL['dayun']:
            end_age   = start_age + 10
            is_active = start_age <= age_now < end_age
            ss        = get_shishen(NATAL['day_master'], s)
            wx        = WUXING_STEM[s]
            color     = WX_COLORS[wx]
            is_good   = wx in NATAL['xiyong']
            is_bad    = wx in NATAL['ji']
            trend     = '↑' if is_good else ('↓' if is_bad else '→')
            tc        = '#52B788' if is_good else ('#c96b6b' if is_bad else '#778899')
            bg        = 'linear-gradient(135deg,#0f2318,#0a1a12)' if is_active else '#0d1321'
            bdr       = f'2px solid {color}' if is_active else '1px solid #1e2d40'
            now_tag   = (f"<span style='background:{color}22;color:{color};font-size:10px;"
                         f"padding:2px 7px;border-radius:8px;margin-left:8px;'>NOW</span>"
                         if is_active else "")
            pct       = max(0, min(100, int((age_now - start_age) / 10 * 100))) if is_active else 0
            bar       = (f"<div style='background:#111827;border-radius:3px;height:3px;"
                         f"overflow:hidden;margin-top:6px;'>"
                         f"<div style='background:{color};height:3px;width:{pct}%;'></div></div>"
                         if is_active else "")
            st.html(f"""
            <div style='background:{bg};border:{bdr};border-radius:12px;
                        padding:13px 16px;margin-bottom:8px;font-family:Noto Serif SC,serif;'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>
                <div>
                  <span style='color:{color};font-size:22px;font-weight:700;'>{s}{b}</span>
                  <span style='color:{tc};font-size:14px;margin-left:8px;'>{trend}</span>
                  {now_tag}
                </div>
                <div style='color:#2a3a4a;font-size:11px;text-align:right;'>
                  {start_age}–{end_age}岁<br>{start_year}–{start_year+10}
                </div>
              </div>
              <div style='color:#2a3a4a;font-size:11px;'>{wx} · {ss}</div>
              {bar}
            </div>
            """)

    with cy2:
        st.html("""
        <div style='color:#d4a843;font-size:12px;font-weight:600;letter-spacing:3px;
                    padding-bottom:10px;border-bottom:1px solid #1e2d40;margin-bottom:16px;
                    font-family:Noto Serif SC,serif;'>流年 · 年度运势</div>
        """)

        if dayun:
            ds, db, da, dy = dayun
            ds_color = WX_COLORS[WUXING_STEM[ds]]
            st.html(f"""
            <div style='background:linear-gradient(135deg,#0a1829,#0d1f38);
                        border:1px solid #1e3a55;border-radius:14px;
                        padding:18px 20px;margin-bottom:16px;font-family:Noto Serif SC,serif;'>
              <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px;'>
                <span style='color:{ds_color};font-size:26px;font-weight:700;'>{ds}{db}</span>
                <div>
                  <div style='color:#667788;font-size:11px;letter-spacing:2px;'>当前大运</div>
                  <div style='color:#445566;font-size:12px;'>{da}–{da+10}岁 · {dy}–{dy+10}年</div>
                </div>
              </div>
              <div style='color:#b8c8d8;font-size:13px;line-height:1.9;'>
                <strong style='color:{ds_color};'>丙火（偏印）</strong>掌天干，思虑过多、贵人关系波动，
                天干管前五年（2025–2030），需防内耗。<br>
                <strong style='color:#A8B8C8;'>申金（食伤）</strong>坐地支，地支管后五年（2030–2035），
                才华财运迎来厚积薄发的收获期。
              </div>
            </div>
            """)

        liunian = [
            (2024,'甲辰','木·偏官','#52B788','事业有压力，考验执行力，主动争取为上。',False),
            (2025,'乙巳','木·正官','#52B788','官星入局，升职机会浮现，需做好准备。',False),
            (2026,'丙午','火·偏印','#E05C5C','偏印叠加大运丙火，深造蓄力年，忌冒进。',True),
            (2027,'丁未','火·正印','#E05C5C','正印入局，学业进步，贵人相助，防依赖。',False),
            (2028,'戊申','土·比肩','#C9A84C','比肩入申，竞争加剧，独立发展优先。',False),
            (2029,'己酉','土·劫财','#C9A84C','劫财年，财务需谨慎，防小人，慎重合伙。',False),
            (2030,'庚戌','金·食神','#A8B8C8','食神得力，才华大放异彩，财运渐入佳境！',False),
            (2031,'辛亥','金·伤官','#A8B8C8','伤官发力，创新思维爆发，适合转型创业。',False),
            (2032,'壬子','水·偏财','#4A90D9','偏财入局，意外之财，投资机会，大年！',False),
            (2033,'癸丑','水·正财','#4A90D9','正财稳进，财运持续，事业稳步上升。',False),
        ]
        for yr, gz, detail, color, desc, is_now in liunian:
            bg      = 'rgba(212,168,67,0.06)' if is_now else 'rgba(255,255,255,0.01)'
            bdr     = '1px solid #d4a84355' if is_now else '1px solid #1a2535'
            now_tag = ("<span style='color:#d4a843;font-size:10px;margin-left:6px;"
                       "padding:1px 6px;border:1px solid #d4a84355;border-radius:6px;'>今年</span>"
                       if is_now else "")
            st.html(f"""
            <div style='background:{bg};border:{bdr};border-radius:10px;
                        padding:10px 16px;margin-bottom:5px;display:flex;align-items:center;
                        gap:12px;font-family:Noto Serif SC,serif;'>
              <div style='color:#334455;font-size:12px;width:32px;flex-shrink:0;'>{yr}</div>
              <div style='color:{color};font-size:16px;font-weight:700;width:34px;flex-shrink:0;'>{gz}</div>
              <div style='flex:1;'>
                <div style='color:#7a8a9a;font-size:11px;'>{detail} {now_tag}</div>
                <div style='color:#445566;font-size:11px;margin-top:2px;line-height:1.5;'>{desc}</div>
              </div>
            </div>
            """)

st.html("""
<div style='text-align:center;padding:28px 0 12px;color:#1e2d3a;font-size:11px;
            letter-spacing:2px;font-family:Noto Serif SC,serif;'>
  命理分析仅供文化参考 · 人生在于自身努力与选择 · ☯
</div>
""")
