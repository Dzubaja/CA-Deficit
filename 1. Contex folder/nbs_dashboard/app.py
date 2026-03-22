"""
Serbia External Sector Dashboard
─────────────────────────────────
Interactive dashboard built on NBS public data.
Run: streamlit run app.py
"""

import streamlit as st
from dashboard.data_loader import (
    get_ca_annual, get_ca_components_annual, get_ca_gdp_ratio,
    get_fa_components_annual, get_fdi_coverage, get_goods_trade_annual,
    get_fx_reserves, get_external_debt_total, get_external_debt_gdp_ratio,
    get_latest_kpis,
    get_component_ranking,
    get_fdi_by_country, get_fdi_by_sector, get_fdi_total_flows,
    get_fdi_concentration, get_fdi_yoy_growth, get_fdi_ca_coverage,
    get_fdi_net_bop,
)
from dashboard.charts import (
    ca_trend_chart, ca_components_stacked, ca_waterfall,
    trade_chart, fa_components_chart, fdi_coverage_chart,
    fx_reserves_chart, external_debt_chart,
    component_ranking_chart, yoy_change_chart, component_share_chart,
    fdi_total_flows_chart, fdi_by_country_chart, fdi_by_sector_chart,
    fdi_concentration_chart, fdi_yoy_growth_chart, fdi_ca_coverage_chart,
    fdi_sector_latest_chart,
    set_theme, COLORS,
)
from dashboard.styles import get_css, kpi_card

# ── Page config ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Serbia External Sector",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme toggle ──────────────────────────────────────────────────────
theme = "dark" if st.session_state.get("dark_mode", True) else "light"
set_theme(theme)
st.markdown(get_css(theme), unsafe_allow_html=True)


def _style_df(df, fmt="{:,.0f}"):
    """Apply theme-appropriate styling to a DataFrame."""
    s = df.style.format(fmt)
    if theme == "light":
        s = s.set_properties(**{
            "background-color": "#FFFFFF",
            "color": "#1E293B",
        }).set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#F1F5F9"),
                ("color", "#475569"),
                ("font-weight", "600"),
            ]},
        ])
    return s


# ── Load data (cached) ────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_all():
    return {
        "kpis": get_latest_kpis(),
        "ca": get_ca_annual(),
        "comp": get_ca_components_annual(),
        "ca_gdp": get_ca_gdp_ratio(),
        "fa": get_fa_components_annual(),
        "fdi_cov": get_fdi_coverage(),
        "trade": get_goods_trade_annual(),
        "fx": get_fx_reserves(),
        "debt": get_external_debt_total(),
        "debt_gdp": get_external_debt_gdp_ratio(),
        "ranking": get_component_ranking(),
        "fdi_flows": get_fdi_total_flows(),
        "fdi_sectors": get_fdi_by_sector(),
        "fdi_conc": get_fdi_concentration(),
        "fdi_growth": get_fdi_yoy_growth(),
        "fdi_ca_cov": get_fdi_ca_coverage(),
        "fdi_net_bop": get_fdi_net_bop(),
    }


data = load_all()
kpis = data["kpis"]


# ── Header ─────────────────────────────────────────────────────────────

col_title, col_toggle, col_info = st.columns([3, 0.5, 1])
with col_title:
    st.markdown(
        '<p class="dash-title">Serbia External Sector Dashboard</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="dash-subtitle">'
        'National Bank of Serbia &nbsp;&middot;&nbsp; '
        'Balance of Payments & External Position</p>',
        unsafe_allow_html=True,
    )
with col_toggle:
    st.toggle("Dark mode", value=True, key="dark_mode")
with col_info:
    accent = COLORS["cyan"]
    st.markdown(
        f'<p class="dash-subtitle" style="text-align:right; margin-top:8px;">'
        f'Latest data: <b style="color:{accent};">{kpis["year"]}</b><br>'
        f'Source: NBS (BPM6)</p>',
        unsafe_allow_html=True,
    )

st.markdown("---")


# ── Filters ────────────────────────────────────────────────────────────

fcol1, _, _ = st.columns([1, 1, 2])
with fcol1:
    year_min = int(data["ca"]["year"].min())
    year_max = int(data["ca"]["year"].max())
    year_range = st.slider(
        "Year range", year_min, year_max, (year_min, year_max),
        key="year_range"
    )

# Apply year filter to all datasets
mask_ca = (data["ca"]["year"] >= year_range[0]) & (data["ca"]["year"] <= year_range[1])
mask_comp = (data["comp"]["year"] >= year_range[0]) & (data["comp"]["year"] <= year_range[1])

ca_f = data["ca"][mask_ca]
comp_f = data["comp"][mask_comp]
ca_gdp_f = data["ca_gdp"][
    (data["ca_gdp"]["year"] >= year_range[0]) & (data["ca_gdp"]["year"] <= year_range[1])
]
fa_f = data["fa"][(data["fa"]["year"] >= year_range[0]) & (data["fa"]["year"] <= year_range[1])]
trade_f = data["trade"][(data["trade"]["year"] >= year_range[0]) & (data["trade"]["year"] <= year_range[1])]
cov_f = data["fdi_cov"][(data["fdi_cov"]["year"] >= year_range[0]) & (data["fdi_cov"]["year"] <= year_range[1])]


# ── KPI Cards ──────────────────────────────────────────────────────────

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(kpi_card(
        "Current Account", kpis["ca"],
        css_class="kpi-negative" if kpis["ca"] < 0 else "kpi-positive",
        sub_text=str(kpis["year"]),
        change=kpis.get("ca_change"), change_pct=kpis.get("ca_pct"),
    ), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card(
        "Trade Balance", kpis["goods"],
        css_class="kpi-negative" if kpis["goods"] < 0 else "kpi-positive",
        sub_text=str(kpis["year"]),
        change=kpis.get("goods_change"), change_pct=kpis.get("goods_pct"),
    ), unsafe_allow_html=True)
with k3:
    st.markdown(kpi_card(
        "Services Surplus", kpis["services"],
        css_class="kpi-positive" if kpis["services"] > 0 else "kpi-negative",
        sub_text=str(kpis["year"]),
        change=kpis.get("services_change"), change_pct=kpis.get("services_pct"),
    ), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card(
        "FDI Net Inflow", kpis["fdi"],
        css_class="kpi-neutral",
        sub_text=str(kpis["year"]),
        change=kpis.get("fdi_change"), change_pct=kpis.get("fdi_pct"),
    ), unsafe_allow_html=True)
with k5:
    fx_sub = str(kpis.get("fx_year", "latest"))
    st.markdown(kpi_card(
        "NBS FX Reserves", kpis["fx_reserves"],
        css_class="kpi-neutral",
        sub_text=fx_sub,
        change=kpis.get("fx_change"), change_pct=kpis.get("fx_pct"),
    ), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 0.8rem'></div>", unsafe_allow_html=True)


# ── Tabs ───────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Current Account  ",
    "  Trade & Financing  ",
    "  External Position  ",
    "  Component Rankings  ",
    "  FDI Deep Dive  ",
])


# ── Tab 1: Current Account ────────────────────────────────────────────

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig_ca = ca_trend_chart(ca_f, ca_gdp_f)
        st.plotly_chart(fig_ca, use_container_width=True)
    with c2:
        fig_stack = ca_components_stacked(comp_f)
        st.plotly_chart(fig_stack, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig_water = ca_waterfall(comp_f)
        st.plotly_chart(fig_water, use_container_width=True)
    with c4:
        fig_area = component_share_chart(comp_f)
        st.plotly_chart(fig_area, use_container_width=True)


# ── Tab 2: Trade & Financing ──────────────────────────────────────────

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig_trade = trade_chart(trade_f)
        st.plotly_chart(fig_trade, use_container_width=True)
    with c2:
        fig_cov = fdi_coverage_chart(cov_f)
        st.plotly_chart(fig_cov, use_container_width=True)

    st.markdown('<div class="section-header">Financial Account Breakdown</div>',
                unsafe_allow_html=True)
    fig_fa = fa_components_chart(fa_f)
    st.plotly_chart(fig_fa, use_container_width=True)


# ── Tab 3: External Position ──────────────────────────────────────────

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        if data["fx"] is not None and not data["fx"].empty:
            fig_fx = fx_reserves_chart(data["fx"])
            st.plotly_chart(fig_fx, use_container_width=True)
        else:
            st.info("FX reserves data not available")
    with c2:
        fig_debt = external_debt_chart(data["debt"], data["debt_gdp"])
        st.plotly_chart(fig_debt, use_container_width=True)

    # Key ratios
    st.markdown('<div class="section-header">Key Vulnerability Indicators</div>',
                unsafe_allow_html=True)

    if not ca_gdp_f.empty:
        latest = ca_gdp_f.iloc[-1]
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("CA / GDP", f"{latest['ca_gdp_pct']:.1f}%")
        with r2:
            fx_latest = data["fx"]
            if fx_latest is not None and "Total (1 to 4)" in fx_latest.columns:
                val = fx_latest["Total (1 to 4)"].iloc[-1]
                st.metric("NBS Reserves", f"{val:,.0f} EUR mn")
        with r3:
            debt_latest = data["debt"]
            if debt_latest is not None and not debt_latest.empty:
                val = debt_latest["value"].iloc[-1]
                st.metric("Total Ext. Debt", f"{val:,.0f} EUR mn")
        with r4:
            cov_latest = data["fdi_cov"]
            if not cov_latest.empty:
                val = cov_latest["coverage"].iloc[-1]
                st.metric("FDI Coverage", f"{val:.0f}%")


# ── Tab 4: Component Rankings ─────────────────────────────────────────

with tab4:
    ranking = data["ranking"]
    if not ranking.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig_rank = component_ranking_chart(ranking)
            st.plotly_chart(fig_rank, use_container_width=True)
        with c2:
            fig_yoy = yoy_change_chart(ranking)
            st.plotly_chart(fig_yoy, use_container_width=True)

    # Historical comparison table
    st.markdown('<div class="section-header">Component Values Over Time (EUR mn)</div>',
                unsafe_allow_html=True)
    display_df = comp_f[["year", "Current Account", "Goods", "Services",
                          "Primary Income", "Secondary Income"]].copy()
    display_df = display_df.set_index("year").sort_index(ascending=False)
    display_df = display_df.round(0)
    st.dataframe(_style_df(display_df), use_container_width=True, height=400)


# ── Tab 5: FDI Deep Dive ─────────────────────────────────────────────

with tab5:
    st.markdown('<div class="section-header">FDI Overview</div>',
                unsafe_allow_html=True)

    # FDI KPI cards
    fdi_flows = data["fdi_flows"]
    fdi_net_bop = data["fdi_net_bop"]
    if not fdi_flows.empty:
        latest_fdi = fdi_flows.iloc[-1]
        prev_fdi = fdi_flows.iloc[-2] if len(fdi_flows) >= 2 else None
        fdi_year = int(latest_fdi["year"])

        def _yoy(curr, prev):
            if curr is None or prev is None or prev == 0:
                return None, None
            c = round(curr - prev, 1)
            return c, round(c / abs(prev) * 100, 1)

        in_chg, in_pct = _yoy(
            latest_fdi.get("Inflows"), prev_fdi.get("Inflows") if prev_fdi is not None else None
        )
        out_chg, out_pct = _yoy(
            latest_fdi.get("Outflows"), prev_fdi.get("Outflows") if prev_fdi is not None else None
        )

        # Net FDI & Coverage: use BOP 2025 if available, else clean_fdi
        bop_max = int(fdi_net_bop["year"].max()) if not fdi_net_bop.empty else 0
        if bop_max > fdi_year:
            bop_latest = fdi_net_bop[fdi_net_bop["year"] == bop_max].iloc[0]
            bop_prev = fdi_net_bop[fdi_net_bop["year"] == bop_max - 1]
            net_curr = abs(bop_latest["value"])
            net_prev_val = abs(bop_prev["value"].iloc[0]) if not bop_prev.empty else None
            net_year = bop_max
        else:
            net_curr = abs(latest_fdi.get("Net FDI", 0))
            net_prev_val = abs(prev_fdi.get("Net FDI", 0)) if prev_fdi is not None else None
            net_year = fdi_year
        net_chg, net_pct = _yoy(net_curr, net_prev_val)

        # CA coverage using BOP net FDI
        ca_data = data["ca"]
        ca_for_cov = ca_data[ca_data["year"] == net_year]
        if not ca_for_cov.empty and ca_for_cov["value"].iloc[0] != 0:
            cov_val = round(net_curr / abs(ca_for_cov["value"].iloc[0]) * 100, 1)
            ca_prev_cov = ca_data[ca_data["year"] == net_year - 1]
            if not ca_prev_cov.empty and net_prev_val is not None:
                cov_prev = round(net_prev_val / abs(ca_prev_cov["value"].iloc[0]) * 100, 1)
            else:
                cov_prev = None
        else:
            fdi_ca = data["fdi_ca_cov"]
            cov_val = fdi_ca.iloc[-1]["coverage"] if not fdi_ca.empty else None
            cov_prev = fdi_ca.iloc[-2]["coverage"] if not fdi_ca.empty and len(fdi_ca) >= 2 else None

        cov_chg = round(cov_val - cov_prev, 1) if cov_val is not None and cov_prev is not None else None

        fk1, fk2, fk3, fk4 = st.columns(4)
        with fk1:
            st.markdown(kpi_card(
                "FDI Inflows", latest_fdi.get("Inflows", 0),
                css_class="kpi-positive", sub_text=str(fdi_year),
                change=in_chg, change_pct=in_pct,
            ), unsafe_allow_html=True)
        with fk2:
            st.markdown(kpi_card(
                "FDI Outflows", latest_fdi.get("Outflows", 0),
                css_class="kpi-negative", sub_text=str(fdi_year),
                change=out_chg, change_pct=out_pct,
            ), unsafe_allow_html=True)
        with fk3:
            st.markdown(kpi_card(
                "Net FDI", net_curr,
                css_class="kpi-neutral", sub_text=str(net_year),
                change=net_chg, change_pct=net_pct,
            ), unsafe_allow_html=True)
        with fk4:
            if cov_val is not None:
                st.markdown(kpi_card(
                    "CA Coverage", cov_val, unit="%",
                    css_class="kpi-positive" if cov_val >= 100 else "kpi-negative",
                    sub_text=str(net_year),
                    change=cov_chg,
                ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.8rem'></div>", unsafe_allow_html=True)

    # ── Sub-tabs for FDI views ──────────────────────────────────────
    fdi_tab1, fdi_tab2, fdi_tab3 = st.tabs([
        "  By Country  ",
        "  By Sector  ",
        "  Analytics  ",
    ])

    # ── FDI by Country ──────────────────────────────────────────────
    with fdi_tab1:
        # Filters
        fc1, fc2 = st.columns([1, 3])
        with fc1:
            top_n = st.selectbox(
                "Show top N countries",
                [5, 10, 15, 20],
                index=1,
                key="fdi_top_n",
            )

        fdi_country = get_fdi_by_country(top_n=top_n)

        # Year filter
        if not fdi_country.empty:
            fdi_country = fdi_country[
                (fdi_country["year"] >= year_range[0]) &
                (fdi_country["year"] <= year_range[1])
            ]

        c1, c2 = st.columns([2, 1])
        with c1:
            fig = fdi_by_country_chart(fdi_country)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig_conc = fdi_concentration_chart(data["fdi_conc"])
            st.plotly_chart(fig_conc, use_container_width=True)

        # Country table — all countries, no top_n grouping
        st.markdown('<div class="section-header">FDI Inflows by Country (EUR mn)</div>',
                    unsafe_allow_html=True)
        fdi_country_all = get_fdi_by_country(top_n=999)
        if not fdi_country_all.empty:
            fdi_country_all = fdi_country_all[
                (fdi_country_all["year"] >= year_range[0]) &
                (fdi_country_all["year"] <= year_range[1])
            ]
            pivot = fdi_country_all.pivot_table(
                index="country", columns="year", values="value", aggfunc="sum"
            ).round(0)
            pivot["Total"] = pivot.sum(axis=1)
            pivot = pivot[pivot["Total"].abs() > 0]
            pivot = pivot.sort_values("Total", ascending=False)
            st.dataframe(_style_df(pivot), use_container_width=True, height=450)

    # ── FDI by Sector ───────────────────────────────────────────────
    with fdi_tab2:
        sector_df = data["fdi_sectors"]

        # Year filter
        if not sector_df.empty:
            sector_f = sector_df[
                (sector_df["year"] >= year_range[0]) &
                (sector_df["year"] <= year_range[1])
            ]
        else:
            sector_f = sector_df

        c1, c2 = st.columns(2)
        with c1:
            fig = fdi_by_sector_chart(sector_f)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = fdi_sector_latest_chart(sector_f)
            st.plotly_chart(fig, use_container_width=True)

        # Sector table
        st.markdown('<div class="section-header">FDI by Sector Over Time (EUR mn)</div>',
                    unsafe_allow_html=True)
        if not sector_f.empty:
            pivot = sector_f.pivot_table(
                index="sector_short", columns="year", values="value", aggfunc="sum"
            ).round(0)
            pivot["Total"] = pivot.sum(axis=1)
            pivot = pivot.sort_values("Total", ascending=False)
            st.dataframe(_style_df(pivot), use_container_width=True, height=400)

    # ── FDI Analytics ───────────────────────────────────────────────
    with fdi_tab3:
        c1, c2 = st.columns(2)
        with c1:
            fig = fdi_total_flows_chart(data["fdi_flows"])
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = fdi_yoy_growth_chart(data["fdi_growth"])
            st.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            fig = fdi_ca_coverage_chart(data["fdi_ca_cov"])
            st.plotly_chart(fig, use_container_width=True)
        with c4:
            # Cumulative FDI inflows
            if not fdi_flows.empty and "Inflows" in fdi_flows.columns:
                import plotly.graph_objects as go
                from dashboard.charts import _base_layout
                cum = fdi_flows[["year", "Inflows"]].copy()
                cum["Cumulative"] = cum["Inflows"].cumsum()
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=cum["year"], y=cum["Cumulative"],
                    name="Cumulative FDI", mode="lines+markers",
                    line=dict(color=COLORS["cyan"], width=2.5, shape="spline"),
                    fill="tozeroy",
                    fillcolor="rgba(0, 212, 255, 0.08)",
                    marker=dict(size=5, color=COLORS["cyan"],
                                line=dict(width=2, color=COLORS["bg"])),
                    hovertemplate="%{x}: <b>%{y:,.0f}</b> EUR mn<extra></extra>",
                ))
                fig.update_layout(**_base_layout("Cumulative FDI Inflows", height=400))
                fig.update_layout(yaxis_title=dict(text="EUR millions",
                                  font=dict(size=12, color=COLORS["dim"])))
                st.plotly_chart(fig, use_container_width=True)

        # Key insights
        st.markdown('<div class="section-header">Key FDI Metrics</div>',
                    unsafe_allow_html=True)

        if not fdi_flows.empty and not data["fdi_growth"].empty:
            growth = data["fdi_growth"]
            conc = data["fdi_conc"]

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                avg_inflow = fdi_flows["Inflows"].mean()
                st.metric("Avg Annual Inflow", f"{avg_inflow:,.0f} EUR mn")
            with m2:
                latest_growth = growth.iloc[-1]
                delta = f"{latest_growth['growth_pct']:+.1f}%"
                st.metric("Latest YoY Growth", delta)
            with m3:
                if not conc.empty:
                    st.metric("Top 5 Concentration", f"{conc.iloc[-1]['top_share_pct']:.0f}%")
            with m4:
                total_cum = fdi_flows["Inflows"].sum()
                fdi_min_yr = int(fdi_flows["year"].min())
                fdi_max_yr = int(fdi_flows["year"].max())
                st.metric(f"Total FDI ({fdi_min_yr}-{fdi_max_yr})", f"{total_cum:,.0f} EUR mn")
