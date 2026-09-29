import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import re
import textwrap
import base64
from html import escape

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RYANOMAD",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SHEET_ID = "1L7w2G7Ze_9iMgOa1fcfY7nSTWLRrK4Dkm3GfEKqzBqg"

GIDS = {
    "trips": "0",
    "places": "527065857",
    "itinerary": "832949487",
    "transport": "1007910317",
    "expenses": "1741809247",
    "exchange_rates": "1170609156",
    "motor_rentals": "2023805153",
    "booking_tracker": "135820957",
}


# =========================================================
# HERO IMAGE
# =========================================================

with open("f1_hero.jpg", "rb") as f:
    hero_image_base64 = base64.b64encode(f.read()).decode()

hero_image_css = (
    "url(data:image/jpeg;base64,"
    + hero_image_base64
    + ")"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>
    :root {{
        --hero-image: {hero_image_css};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F4F7FB;
    color: #203A5F;
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* =====================================================
   HEADER
   ===================================================== */

.hero {
    background: linear-gradient(
        135deg,
        #17365D 0%,
        #244F7D 55%,
        #356C99 100%
    );
    border-radius: 24px;
    padding: 30px 34px;
    margin-bottom: 26px;
    box-shadow: 0 12px 30px rgba(24,55,90,.15);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #FFFFFF;
    margin: 0;
}

.hero-subtitle {
    margin-top: 7px;
    font-size: 16px;
    font-weight: 500;
    color: #DCEAF7;
}

/* =====================================================
   SECTION
   ===================================================== */

.section-title {
    font-size: 26px;
    font-weight: 800;
    color: #203A5F;
    margin: 30px 0 15px 0;
    letter-spacing: -.5px;
}

/* =====================================================
   KPI
   ===================================================== */

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 18px;
    padding: 20px;
    min-height: 118px;
    box-shadow: 0 7px 20px rgba(28,55,85,.07);
}

.kpi-label {
    font-size: 10px;
    font-weight: 700;

    letter-spacing: 1.25px;

    color: #718398;

    text-transform: uppercase;
}

.kpi-value {
    font-size: 28px;
    line-height: 1;

    font-weight: 800;

    letter-spacing: -0.9px;

    color: #17365D;
}

.kpi-accent {
    width: 38px;
    height: 4px;
    background: #4F6BED;
    border-radius: 5px;
    margin-top: 12px;
}

/* =====================================================
   ITINERARY EXPLORER
   ===================================================== */

.itinerary-toolbar {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 18px;
    padding: 18px 20px 8px 20px;
    margin: 8px 0 20px 0;
    box-shadow: 0 6px 18px rgba(28,55,85,.06);
}

.itinerary-toolbar-title {
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #637B94;
    margin-bottom: 6px;
}

.itinerary-day {
    margin: 24px 0 18px 0;
}

.itinerary-day-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    background: linear-gradient(
        135deg,
        #17365D 0%,
        #244F7D 100%
    );
    color: #FFFFFF;
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 7px 18px rgba(23,54,93,.14);
}

.itinerary-day-name {
    font-size: 17px;
    font-weight: 800;
    margin: 0;
}

.itinerary-day-meta {
    font-size: 12px;
    font-weight: 600;
    color: #DCEAF7;
    margin-top: 3px;
}

.itinerary-day-count {
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.22);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
}


/* -----------------------------------------------------
   TIMELINE
   ----------------------------------------------------- */

.itinerary-timeline {
    position: relative;
    margin-top: 8px;
    padding: 4px 0 4px 0;
}

.itinerary-timeline::before {
    content: "";
    position: absolute;
    left: 92px;
    top: 16px;
    bottom: 16px;
    width: 2px;
    background: #DCE5EF;
}

.itinerary-item {
    position: relative;
    display: grid;
    grid-template-columns: 78px 1fr;
    column-gap: 30px;
    margin-bottom: 15px;
}

.itinerary-time {
    text-align: right;
    padding-top: 19px;
    font-size: 13px;
    line-height: 1.35;
    font-weight: 800;
    color: #203A5F;
}

.itinerary-dot {
    position: absolute;
    left: 85px;
    top: 22px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #7EC0EE;
    border: 4px solid #F4F7FB;
    box-shadow: 0 0 0 2px #7EC0EE;
    z-index: 2;
}

.itinerary-card {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 17px;
    padding: 17px 19px;
    box-shadow: 0 5px 16px rgba(28,55,85,.055);
    transition: transform .15s ease, box-shadow .15s ease;
}

.itinerary-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 9px 22px rgba(28,55,85,.09);
}

.itinerary-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 7px;
}

.itinerary-type {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EEF5FB;
    color: #315B82;
    border-radius: 999px;
    padding: 5px 9px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .5px;
}

.itinerary-duration {
    color: #71869B;
    font-size: 12px;
    font-weight: 700;
}

.itinerary-title {
    color: #17365D;
    font-size: 18px;
    line-height: 1.35;
    font-weight: 800;
    margin: 0 0 7px 0;
}

.itinerary-place {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #4F6B86;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 7px;
}

.itinerary-mode {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #637B94;
    background: #F5F8FB;
    border-radius: 8px;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 7px;
}

.itinerary-note {
    color: #6C8095;
    font-size: 12.5px;
    line-height: 1.55;
    border-top: 1px solid #EDF1F5;
    padding-top: 8px;
    margin-top: 4px;
}

.itinerary-booking {
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid #EDF1F5;
}

.itinerary-booking a {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    background: #EEF5FB;
    color: #315B82;
    border: 1px solid #D7E5F2;
    border-radius: 9px;
    padding: 7px 11px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .3px;
    transition: all .15s ease;
}

.itinerary-booking a:hover {
    background: #E2EFF9;
    border-color: #BFD7EB;
    color: #17365D;
}

/* TRANSPORT KPI */

.transport-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
}

/* -----------------------------------------------------
   EMPTY STATE
   ----------------------------------------------------- */

.itinerary-empty {
    background: #FFFFFF;
    border: 1px dashed #C8D5E2;
    border-radius: 17px;
    padding: 35px 20px;
    text-align: center;
    color: #71869B;
}

.trip-kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 18px;
}

/* =====================================================
   BUDGET FINANCIAL CARD
   ===================================================== */

.budget-financial-card {
    position: relative;

    min-height: 190px;
    padding: 22px 22px 20px 22px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(126,192,238,0.16),
            transparent 38%
        ),
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F8FAFC 100%
        );

    border: 1px solid rgba(190,205,220,0.75);
    border-radius: 19px;

    box-shadow:
        0 8px 24px rgba(24,55,90,0.065),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}

.budget-financial-item {
    position: relative;
    z-index: 2;
}

.budget-financial-item + .budget-financial-divider {
    margin-top: 17px;
}

.budget-financial-divider {
    height: 1px;

    background:
        linear-gradient(
            90deg,
            #DCE5EF 0%,
            #EDF2F7 70%,
            transparent 100%
        );

    margin-bottom: 17px;
}

.budget-financial-card .kpi-value {
    margin-top: 8px;
    font-size: 28px;
}

.budget-financial-card .kpi-accent {
    position: absolute;

    left: 22px;
    bottom: 16px;

    width: 38px;
    height: 3px;

    margin: 0;

    background:
        linear-gradient(
            90deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );

    border-radius: 999px;

    box-shadow:
        0 0 8px rgba(79,107,237,0.20);
}

/* =====================================================
   BUDGET RACE CARD
   ===================================================== */

.budget-race-card {
    position: relative;

    min-height: 150px;
    padding: 20px 22px 18px 22px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(126,192,238,0.14),
            transparent 38%
        ),
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F8FAFC 100%
        );

    border: 1px solid rgba(190,205,220,0.75);
    border-radius: 19px;

    box-shadow:
        0 8px 24px rgba(24,55,90,0.065),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}

.budget-race-card .kpi-value {
    margin-top: 8px;
    font-size: 32px;
}

.budget-race {
    position: relative;

    height: 28px;

    margin-top: 12px;
}

.budget-race-line {
    position: absolute;

    left: 0;
    right: 0;
    top: 13px;

    height: 4px;

    background:
        repeating-linear-gradient(
            90deg,
            #B9C7D5 0px,
            #B9C7D5 7px,
            transparent 7px,
            transparent 11px
        );

    border-radius: 999px;
}

.budget-race-car {
    position: absolute;

    top: 0;

    z-index: 3;

    width: 26px;
    height: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    transform: translateY(-3px);

    filter:
        drop-shadow(
            0 2px 4px rgba(23,54,93,0.24)
        );
}

.race-car-body {
    position: relative;

    display: block;

    width: 25px;
    height: 11px;

    margin-top: 3px;

    background: #173D63;

    border-radius: 5px 8px 3px 3px;
}

.race-car-body::before {
    content: "";

    position: absolute;

    left: 6px;
    top: -5px;

    width: 11px;
    height: 7px;

    background: #7EC0EE;

    border-radius: 5px 5px 1px 1px;

    transform: skewX(-18deg);
}

.race-car-body::after {
    content: "";

    position: absolute;

    right: -3px;
    top: 5px;

    width: 5px;
    height: 3px;

    background: #4F6BED;

    border-radius: 0 3px 3px 0;
}

.race-car-cockpit {
    position: absolute;

    left: 9px;
    top: -3px;

    width: 6px;
    height: 4px;

    background: #102A47;

    border-radius: 50% 50% 1px 1px;

    z-index: 2;
}

.race-car-wheel {
    position: absolute;

    bottom: -4px;

    width: 7px;
    height: 7px;

    background: #102A47;

    border: 1px solid #DCEAF7;

    border-radius: 50%;
}

.race-wheel-front {
    right: 2px;
}

.race-wheel-rear {
    left: 3px;
}

.budget-race-car svg {
    width: 26px;
    height: auto;

    display: block;
}

.budget-finish {
    position: absolute;

    right: 0;
    top: -3px;

    z-index: 4;

    width: 18px;
    height: 27px;

    filter:
        drop-shadow(
            0 2px 3px rgba(23,54,93,0.16)
        );
}

.finish-flag {
    position: relative;

    display: block;

    width: 18px;
    height: 27px;
}

.flag-pole {
    position: absolute;

    left: 2px;
    top: 0;

    width: 2px;
    height: 27px;

    background: #173D63;

    border-radius: 999px;
}

.flag-cloth {
    position: absolute;

    left: 4px;
    top: 1px;

    width: 13px;
    height: 9px;

    background:
        conic-gradient(
            #173D63 25%,
            #FFFFFF 0 50%,
            #173D63 0 75%,
            #FFFFFF 0
        );

    background-size: 6px 6px;

    border-radius: 1px;

    box-shadow:
        0 1px 3px rgba(23,54,93,0.16);
}

.budget-finish svg {
    width: 18px;
    height: 24px;

    display: block;
}

.budget-race-meta {
    display: flex;

    justify-content: space-between;

    margin-top: 2px;

    color: #8797A8;

    font-size: 8px;
    font-weight: 700;

    letter-spacing: 0.9px;
}

/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .block-container {
        padding: .8rem .8rem 2rem .8rem;
    }

    .hero {
        position: relative;

        padding: 28px 21px 25px 21px;
        min-height: 125px;

        border-radius: 20px;

        background:
            linear-gradient(
                105deg,
                rgba(4, 17, 30, 0.98) 0%,
                rgba(7, 27, 47, 0.92) 38%,
                rgba(8, 35, 61, 0.62) 63%,
                rgba(18, 70, 105, 0.25) 100%
            ),
            var(--hero-image);

        background-size: cover;
        background-position: center right;

        border: 1px solid rgba(126,192,238,0.28);

        box-shadow:
            0 18px 38px rgba(8,31,53,0.28),
            0 0 0 1px rgba(255,255,255,0.04),
            inset 0 1px 0 rgba(255,255,255,0.12);

        overflow: hidden;
    }

    .hero::after {
        content: "";

        position: absolute;

        left: 0;
        right: 0;
        bottom: 0;

        height: 4px;

        background:
            linear-gradient(
                90deg,
                #4DA3E8 0%,
                #7EC0EE 35%,
                rgba(126,192,238,0.25) 75%,
                transparent 100%
            );

        box-shadow:
            0 0 12px rgba(77,163,232,0.45);

        pointer-events: none;
    }

    .hero-title {
        position: relative;
        z-index: 2;

        font-size: 31px;
        line-height: 1;

        letter-spacing: -1.5px;

        color: #FFFFFF;

        text-shadow:
            0 2px 12px rgba(0,0,0,0.28),
            0 0 24px rgba(126,192,238,0.08);
    }

    .hero-subtitle {
        position: relative;
        z-index: 2;

        margin-top: 9px;

        font-size: 14px;
        line-height: 1.4;

        color: #DCEAF7;

        letter-spacing: 0.15px;

        text-shadow:
            0 1px 6px rgba(0,0,0,0.20);
    }

    .section-title {
        font-size: 22px;
    }

    .kpi-card {
        position: relative;

        min-height: 104px;
        padding: 18px 19px 17px 19px;

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(126,192,238,0.12),
                transparent 38%
            ),
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F8FAFC 100%
            );

        border: 1px solid rgba(190,205,220,0.75);

        border-radius: 19px;

        box-shadow:
            0 8px 24px rgba(24,55,90,0.065),
            inset 0 1px 0 rgba(255,255,255,0.95);

        overflow: hidden;
    }

    .kpi-featured {
        background:
            radial-gradient(
                circle at 92% 12%,
                rgba(126,192,238,0.24),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #102A47 0%,
                #173D63 58%,
                #245A83 100%
            );

        border: 1px solid rgba(126,192,238,0.30);

        box-shadow:
            0 14px 30px rgba(18,52,82,0.20),
            inset 0 1px 0 rgba(255,255,255,0.10);

        min-height: 112px;
    }

    .kpi-featured .kpi-label {
        color: #BFD3E5;
    }

    .kpi-featured .kpi-value {
        font-size: 31px;
        letter-spacing: -1px;
        color: #FFFFFF;
    }

    .kpi-featured .kpi-accent {
        background:
            linear-gradient(
                90deg,
                #7EC0EE 0%,
                #FFFFFF 100%
            );

        box-shadow:
            0 0 10px rgba(126,192,238,0.30);
    }

    .kpi-card::before {
        content: "";

        position: absolute;

        width: 90px;
        height: 90px;

        right: -42px;
        top: -48px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(79,107,237,0.10) 0%,
                rgba(79,107,237,0.025) 55%,
                transparent 72%
            );

        pointer-events: none;
    }

    .kpi-label {
        position: relative;
        z-index: 2;

        color: #718398;

        font-size: 9.5px;
        font-weight: 700;

        letter-spacing: 1.35px;
        line-height: 1.2;

        text-transform: uppercase;
    }

    .kpi-value {
        position: relative;
        z-index: 2;

        margin-top: 9px;

        color: #17365D;

        font-size: 30px;
        line-height: 1;

        font-weight: 800;
        letter-spacing: -1px;
    }

    .kpi-accent {
        position: relative;
        z-index: 2;

        width: 34px;
        height: 3px;

        margin-top: 14px;

        background:
            linear-gradient(
                90deg,
                #4F6BED 0%,
                #7EC0EE 100%
            );

        border-radius: 999px;

        box-shadow:
            0 0 8px rgba(79,107,237,0.20);
    }

        .budget-financial-card {
        min-height: 190px;
        padding: 20px 19px 19px 19px;
        border-radius: 19px;
    }

    .budget-financial-card .kpi-value {
        font-size: 27px;
    }

    .budget-financial-card .kpi-accent {
        left: 19px;
        bottom: 15px;
    }

        .budget-race-card {
        min-height: 150px;
        padding: 19px 19px 17px 19px;
        border-radius: 19px;
    }

    .budget-race-card .kpi-value {
        font-size: 31px;
    }

    .budget-race {
        margin-top: 12px;
    }

    .budget-actual-wrap {
        position: relative;

        flex: 1;

        height: 100%;
    }

    .budget-actual-wrap .budget-lane-bar {
        position: relative;

        z-index: 2;
    }

    .budget-overflow {
        position: absolute;

        left: 100%;
        top: 0;

        height: 100%;

        background:
            repeating-linear-gradient(
                135deg,
                #D89A3D 0px,
                #D89A3D 4px,
                #F1D39B 4px,
                #F1D39B 8px
            );

        border-radius: 0 999px 999px 0;

        z-index: 3;
    }

    .budget-over-value {
        color: #B97821;

        font-size: 8px;
        font-weight: 800;

        white-space: nowrap;
    }

    .budget-under-value {
        color: #3D8A72;

        font-size: 8px;
        font-weight: 800;

        white-space: nowrap;
    }

    .budget-on-value {
        color: #718398;

        font-size: 8px;
        font-weight: 800;

        white-space: nowrap;
    }

    .trip-kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }

    .trip-kpi-grid .kpi-featured {
        grid-column: 1 / -1;
    }

    .itinerary-toolbar {
        padding: 14px 14px 5px 14px;
        border-radius: 15px;
    }

    .itinerary-day {
        margin-top: 0px;
    }

    .itinerary-day-header {
        padding: 12px 14px;
        border-radius: 14px;
    }

    .itinerary-day-name {
        font-size: 15px;
    }

    .itinerary-day-count {
        font-size: 11px;
        padding: 5px 8px;
    }

    .itinerary-timeline::before {
        left: 68px;
    }

    .itinerary-item {
        grid-template-columns: 56px 1fr;
        column-gap: 25px;
    }

    .itinerary-time {
        font-size: 11px;
        padding-top: 17px;
        word-break: normal;
    }

    .itinerary-dot {
        left: 61px;
        top: 20px;
        width: 14px;
        height: 14px;
    }

    .itinerary-card {
        padding: 14px;
        border-radius: 15px;
    }

    .itinerary-title {
        font-size: 16px;
    }

    .itinerary-place {
        font-size: 12.5px;
    }

    .itinerary-note {
        font-size: 12px;
    }

    .itinerary-duration {
        display: none;
    }
}

/* =========================================================
   BOOKINGS
========================================================= */

.booking-card {

    background: #FFFFFF;

    border: 1px solid #DCE5EF;

    border-radius: 18px;

    padding: 18px;

    margin-bottom: 14px;

    box-shadow:
        0 4px 14px
        rgba(32, 58, 95, 0.06);

}


.booking-card-top {

    display: flex;

    justify-content: space-between;

    align-items: center;

}


.booking-icon {

    font-size: 26px;

}


.booking-status {

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.7px;

    padding: 6px 10px;

    border-radius: 999px;

}


.booking-status.booked {

    background: #E7F5EC;

    color: #2E7D4F;

}


.booking-status.to-book {

    background: #FFF4D6;

    color: #9A6A00;

}


.booking-status.check-availability {

    background: #E8F0FA;

    color: #315A8B;

}


.booking-category {

    margin-top: 14px;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;

    color: #8090A0;

    text-transform: uppercase;

}


.booking-item {

    margin-top: 4px;

    font-size: 18px;

    font-weight: 800;

    color: #203A5F;

}


.booking-date {

    margin-top: 10px;

    font-size: 13px;

    font-weight: 600;

    color: #506070;

}


.booking-provider {

    margin-top: 6px;

    font-size: 13px;

    color: #8090A0;

}


.booking-meta {

    display: flex;

    justify-content: space-between;

    gap: 10px;

    margin-top: 16px;

    padding-top: 14px;

    border-top:
        1px solid #EEF2F6;

}


.booking-meta span {

    display: block;

    font-size: 9px;

    font-weight: 700;

    letter-spacing: 0.8px;

    color: #8090A0;

}


.booking-meta strong {

    display: block;

    margin-top: 3px;

    font-size: 13px;

    color: #203A5F;

}


.booking-meta strong.high {

    color: #C84B4B;

}


.booking-notes {

    margin-top: 14px;

    font-size: 12px;

    line-height: 1.5;

    color: #607080;

}


.booking-link {

    display: block;

    margin-top: 16px;

    padding: 10px;

    border-radius: 10px;

    text-align: center;

    text-decoration: none;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 0.7px;

    color: #FFFFFF;

    background: #203A5F;

}


.booking-empty {

    padding: 30px;

    text-align: center;

    border-radius: 16px;

    background: #F6F8FA;

    color: #8090A0;

}

/* =========================================================
   BOOKING KPI
========================================================= */

.booking-kpi-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 18px;

    margin-top: 12px;
    margin-bottom: 18px;

}


.booking-kpi-card {

    background: #FFFFFF;

    border:
        1px solid #DCE5EF;

    border-radius: 18px;

    padding:
        18px 22px;

    min-height: 105px;

    display: flex;

    flex-direction: column;

    justify-content: center;

}


.booking-kpi-label {

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.8px;

    color: #7B8EA3;

}


.booking-kpi-value {

    margin-top: 8px;

    font-size: 30px;

    font-weight: 800;

    color: #203A5F;

}


@media (max-width: 768px) {

    .booking-kpi-grid {

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 10px;

        margin-top: -15;
        margin-bottom: -15;

    }


    .booking-kpi-card {

        min-height: 85px;

        padding:
            14px 16px;

    }


    .booking-kpi-value {

        font-size: 25px;

    }

}

/* =====================================================
   TRANSPORT
   ===================================================== */

.transport-toolbar {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 18px;
    padding: 16px 18px;
    margin: 8px 0 20px 0;
    box-shadow: 0 6px 18px rgba(28,55,85,.06);
}

.transport-card {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 17px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 5px 16px rgba(28,55,85,.055);
}

.transport-date {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .8px;
    color: #71869B;
    margin-bottom: 8px;
}

.transport-route {
    display: grid;
    grid-template-columns: minmax(0,1fr) 46px minmax(0,1fr);
    align-items: center;
    gap: 10px;
}

.transport-location {
    color: #17365D;
    font-size: 15px;
    line-height: 1.35;
    font-weight: 800;
}

.transport-arrow {
    text-align: center;
    color: #7EC0EE;
    font-size: 20px;
    font-weight: 800;
}

.transport-destination {
    text-align: right;
}

.transport-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 13px;
}

.transport-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #F5F8FB;
    color: #4F6B86;
    border-radius: 999px;
    padding: 6px 9px;
    font-size: 11px;
    font-weight: 700;
}

.transport-cost {
    color: #17365D;
    font-weight: 800;
}

.transport-note {
    margin-top: 11px;
    padding-top: 10px;
    border-top: 1px solid #EDF1F5;
    color: #71869B;
    font-size: 12px;
    line-height: 1.5;
}

.transport-empty {
    background: #FFFFFF;
    border: 1px dashed #C8D5E2;
    border-radius: 17px;
    padding: 35px 20px;
    text-align: center;
    color: #71869B;
}

@media (max-width: 768px) {

    .section-nav-wrap {
        margin-bottom: 20px;
        padding: 8px 0;
    }

    .section-pill {
        min-height: 36px;
        padding: 0 13px;
        font-size: 10px;
    }

    .transport-card {
        padding: 15px;
        border-radius: 15px;
    }

    .transport-route {
        grid-template-columns: minmax(0,1fr) 28px minmax(0,1fr);
    }

    .transport-location {
        font-size: 13px;
    }

    .transport-arrow {
        font-size: 16px;
    }
}

/* =====================================================
   DESTINATIONS — PREMIUM CARDS
   ===================================================== */

.destination-city {
    margin: 30px 0 13px 0;

    padding-bottom: 9px;

    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;

    color: #718398;

    border-bottom: 1px solid #DCE5EF;
}


/* -----------------------------------------------------
   CARD
   ----------------------------------------------------- */

.destination-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F9FBFD 100%
        );

    border: 1px solid #DCE5EF;
    border-radius: 18px;

    padding: 18px 19px 16px 19px;
    margin-bottom: 13px;

    box-shadow:
        0 8px 22px rgba(24,55,90,0.055),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}


/* subtle blue signature */

.destination-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    background:
        linear-gradient(
            180deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );

    opacity: 0.75;
}


/* -----------------------------------------------------
   TOP AREA
   ----------------------------------------------------- */

.destination-card-top {
    display: flex;

    align-items: flex-start;
    justify-content: space-between;

    gap: 16px;
}


/* -----------------------------------------------------
   NAME
   ----------------------------------------------------- */

.destination-name {
    color: #17365D;

    font-size: 17px;
    line-height: 1.3;

    font-weight: 800;
    letter-spacing: -0.25px;
}


.destination-location {
    margin-top: 5px;

    color: #7A8EA3;

    font-size: 11px;
    line-height: 1.4;

    font-weight: 600;
}


/* -----------------------------------------------------
   CATEGORY
   ----------------------------------------------------- */

.destination-tag {
    display: inline-flex;
    align-items: center;

    background: #F0F6FB;
    color: #315B82;

    border: 1px solid #DCEAF5;

    border-radius: 999px;

    padding: 5px 9px;

    font-size: 9px;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: .55px;

    white-space: nowrap;
}


/* -----------------------------------------------------
   DESCRIPTION
   ----------------------------------------------------- */

.destination-description {
    margin-top: 13px;

    color: #637B94;

    font-size: 12.5px;
    line-height: 1.58;

    max-width: 680px;
}


/* -----------------------------------------------------
   PHOTO SPOTS
   ----------------------------------------------------- */

.destination-photo {
    margin-top: 14px;

    padding: 11px 12px;

    background: #F7FAFC;

    border: 1px solid #E7EEF4;
    border-radius: 11px;

    color: #637B94;

    font-size: 11.5px;
    line-height: 1.5;
}


.destination-label {
    margin-bottom: 4px;

    color: #58748E;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .8px;
}


/* -----------------------------------------------------
   GOOGLE MAPS CTA
   ----------------------------------------------------- */

.destination-actions {
    margin-top: 13px;

    padding-top: 12px;

    border-top: 1px solid #E8EEF3;
}


.destination-actions a {
    display: inline-flex;
    align-items: center;

    text-decoration: none !important;

    background: #EEF5FB;
    color: #315B82;

    border: 1px solid #D7E5F2;

    border-radius: 10px;

    padding: 8px 12px;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .45px;

    transition:
        background .18s ease,
        border-color .18s ease,
        transform .18s ease;
}


.destination-actions a:hover {
    background: #E4F0F9;

    border-color: #BFD7EB;

    color: #17365D;

    transform: translateY(-1px);
}


/* -----------------------------------------------------
   EMPTY STATE
   ----------------------------------------------------- */

.destination-empty {
    background: #FFFFFF;

    border: 1px dashed #C8D5E2;
    border-radius: 17px;

    padding: 35px 20px;

    text-align: center;

    color: #71869B;
}


/* =====================================================
   DESTINATIONS — MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .destination-city {
        margin-top: 22px;
        margin-bottom: 10px;

        font-size: 11px;
        letter-spacing: 1.3px;
    }


    .destination-card {
        padding: 15px 15px 14px 15px;

        border-radius: 16px;

        margin-bottom: 11px;
    }


    .destination-card-top {
        gap: 9px;
    }


    .destination-name {
        font-size: 15px;
        line-height: 1.32;
    }


    .destination-location {
        margin-top: 4px;

        font-size: 10.5px;
    }


    .destination-tag {
        padding: 4px 7px;

        font-size: 8px;
        letter-spacing: .45px;
    }


    .destination-description {
        margin-top: 11px;

        font-size: 11.5px;
        line-height: 1.55;
    }


    .destination-photo {
        margin-top: 12px;

        padding: 10px 11px;

        border-radius: 10px;

        font-size: 11px;
    }


    .destination-label {
        font-size: 8.5px;
    }


    .destination-actions {
        margin-top: 11px;

        padding-top: 10px;
    }


    .destination-actions a {
        width: 100%;

        justify-content: center;

        padding: 8px 10px;

        font-size: 8.5px;
    }
}

/* =====================================================
   MOTOR RENTAL
   ===================================================== */

.rental-city {
    margin: 28px 0 12px 0;

    padding-bottom: 8px;

    border-bottom: 1px solid #DCE5EF;

    color: #637B94;

    font-size: 13px;
    font-weight: 800;

    letter-spacing: 1px;
}


.rental-card {
    background: #FFFFFF;

    border: 1px solid #DCE5EF;
    border-radius: 17px;

    padding: 18px 19px;
    margin-bottom: 13px;

    box-shadow:
        0 5px 16px rgba(28,55,85,.055);
}


.rental-name {
    color: #17365D;

    font-size: 17px;
    line-height: 1.35;

    font-weight: 800;
}


.rental-address {
    display: flex;
    align-items: flex-start;

    gap: 7px;

    margin-top: 10px;

    color: #637B94;

    font-size: 12px;
    line-height: 1.5;
}


.rental-icon {
    flex: 0 0 auto;
}


.rental-info-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 10px;

    margin-top: 16px;

    padding-top: 14px;

    border-top: 1px solid #EDF1F5;
}


.rental-info-item {
    min-width: 0;
}


.rental-info-label {
    margin-bottom: 4px;

    color: #8A9AAC;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .7px;
}


.rental-info-value {
    color: #315B82;

    font-size: 12px;
    font-weight: 700;

    line-height: 1.45;
}


.rental-price {
    color: #17365D;
}


.rental-price span {
    color: #8A9AAC;

    font-size: 10px;
    font-weight: 600;
}


.rental-notes {
    margin-top: 13px;

    padding: 10px 11px;

    background: #F7F9FB;

    border-radius: 9px;

    color: #637B94;

    font-size: 11px;
    line-height: 1.5;
}


.rental-actions {
    display: flex;
    flex-wrap: wrap;

    gap: 8px;

    margin-top: 15px;

    padding-top: 13px;

    border-top: 1px solid #EDF1F5;
}


.rental-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    padding: 7px 11px;

    border-radius: 9px;

    background: #EEF5FB;
    border: 1px solid #D7E5F2;

    color: #315B82 !important;

    text-decoration: none !important;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: .3px;
}


.rental-action:hover {
    background: #E2EFF9;

    border-color: #BFD7EB;

    color: #17365D !important;
}


.rental-empty {
    padding: 35px 20px;

    text-align: center;

    background: #FFFFFF;

    border: 1px dashed #C8D5E2;
    border-radius: 17px;

    color: #71869B;

    font-size: 12px;
}


/* =====================================================
   MOTOR RENTAL — MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .rental-city {
        margin-top: 22px;
        margin-bottom: 10px;

        font-size: 12px;
    }


    .rental-card {
        padding: 14px;

        border-radius: 15px;
    }


    .rental-name {
        font-size: 15px;
    }


    .rental-address {
        font-size: 11px;
    }


    .rental-info-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 12px;

        margin-top: 13px;
        padding-top: 12px;
    }


    .rental-info-label {
        font-size: 8px;
    }


    .rental-info-value {
        font-size: 11px;
    }


    .rental-actions {
        gap: 7px;
    }


    .rental-action {
        flex: 1 1 auto;

        font-size: 8.5px;

        padding: 7px 8px;
    }
}

/* ACTIVE NAVIGATION */

body:has(#budget-overview:target)
.ryanomad-nav a[href="#budget-overview"],

body:has(#time-pace:target)
.ryanomad-nav a[href="#time-pace"],

body:has(#destinations:target)
.ryanomad-nav a[href="#destinations"],

body:has(#itinerary:target)
.ryanomad-nav a[href="#itinerary"],

body:has(#bookings:target)
.ryanomad-nav a[href="#bookings"],

body:has(#transports:target)
.ryanomad-nav a[href="#transports"],

body:has(#motor-rental:target)
.ryanomad-nav a[href="#motor-rental"] {

    background: #29496d !important;
    color: #ffffff !important;

    border-radius: 999px;

}

/* =====================================================
   ITINERARY — PREMIUM TIMELINE OVERRIDE
   ===================================================== */

.itinerary-day {
    margin: 24px 0 22px 0;
}


/* -----------------------------------------------------
   DAY HEADER
   ----------------------------------------------------- */

.itinerary-day-header {
    position: relative;

    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 14px;

    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(126,192,238,0.24),
            transparent 42%
        ),
        linear-gradient(
            135deg,
            #102A47 0%,
            #173D63 58%,
            #245A83 100%
        );

    border: 1px solid rgba(126,192,238,0.25);

    border-radius: 17px;

    padding: 13px 16px;

    box-shadow:
        0 10px 24px rgba(18,52,82,0.16),
        inset 0 1px 0 rgba(255,255,255,0.10);
}


.itinerary-day-name {
    font-size: 16px;
    line-height: 1.25;

    font-weight: 800;

    letter-spacing: -0.2px;

    color: #FFFFFF;
}


.itinerary-day-meta {
    margin-top: 3px;

    font-size: 10px;

    font-weight: 600;

    letter-spacing: .15px;

    color: #BFD3E5;
}


.itinerary-day-count {
    flex-shrink: 0;

    background: rgba(255,255,255,0.10);

    border: 1px solid rgba(255,255,255,0.20);

    border-radius: 999px;

    padding: 5px 9px;

    font-size: 10px;

    font-weight: 800;

    color: #FFFFFF;

    white-space: nowrap;
}


/* -----------------------------------------------------
   TIMELINE
   ----------------------------------------------------- */

.itinerary-timeline {
    position: relative;

    margin-top: 11px;

    padding: 2px 0 3px 0;
}


.itinerary-timeline::before {
    left: 76px;

    top: 17px;
    bottom: 17px;

    width: 2px;

    background:
        linear-gradient(
            180deg,
            #BFD3E5 0%,
            #DCE5EF 100%
        );
}


/* -----------------------------------------------------
   ITEM
   ----------------------------------------------------- */

.itinerary-item {
    position: relative;

    display: grid;

    grid-template-columns: 62px minmax(0, 1fr);

    column-gap: 27px;

    margin-bottom: 11px;
}


/* -----------------------------------------------------
   TIME
   ----------------------------------------------------- */

.itinerary-time {
    text-align: right;

    padding-top: 16px;

    font-size: 10.5px;

    line-height: 1.35;

    font-weight: 800;

    color: #526A82;
}


/* -----------------------------------------------------
   DOT
   ----------------------------------------------------- */

.itinerary-dot {
    left: 69px;

    top: 20px;

    width: 14px;
    height: 14px;

    background: #7EC0EE;

    border: 4px solid #F4F7FB;

    box-shadow:
        0 0 0 2px #7EC0EE,
        0 2px 5px rgba(79,107,237,0.16);

    z-index: 2;
}


/* -----------------------------------------------------
   CARD
   ----------------------------------------------------- */

.itinerary-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F9FBFD 100%
        );

    border: 1px solid #DCE5EF;

    border-radius: 16px;

    padding: 14px 15px 13px 15px;

    box-shadow:
        0 7px 18px rgba(24,55,90,0.055),
        inset 0 1px 0 rgba(255,255,255,0.95);

    transition:
        transform .15s ease,
        box-shadow .15s ease;
}


.itinerary-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 12px;
    bottom: 12px;

    width: 3px;

    border-radius: 0 999px 999px 0;

    background:
        linear-gradient(
            180deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );

    opacity: .72;
}


/* -----------------------------------------------------
   CARD TOP
   ----------------------------------------------------- */

.itinerary-card-top {
    display: flex;

    align-items: center;
    justify-content: space-between;

    gap: 8px;

    margin-bottom: 8px;
}


.itinerary-type {
    background: #EEF5FB;

    color: #315B82;

    border: 1px solid #DCEAF5;

    border-radius: 999px;

    padding: 4px 8px;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: .5px;
}


.itinerary-duration {
    color: #8797A8;

    font-size: 9px;

    font-weight: 700;

    white-space: nowrap;
}


/* -----------------------------------------------------
   TITLE
   ----------------------------------------------------- */

.itinerary-title {
    color: #17365D;

    font-size: 16px;

    line-height: 1.35;

    font-weight: 800;

    letter-spacing: -.2px;

    margin: 0 0 6px 0;
}


/* -----------------------------------------------------
   PLACE
   ----------------------------------------------------- */

.itinerary-place {
    display: flex;

    align-items: center;

    gap: 5px;

    color: #4F6B86;

    font-size: 11.5px;

    font-weight: 700;

    margin-bottom: 6px;
}


/* -----------------------------------------------------
   TRANSPORT MODE
   ----------------------------------------------------- */

.itinerary-mode {
    display: inline-flex;

    align-items: center;

    gap: 4px;

    color: #637B94;

    background: #F5F8FB;

    border: 1px solid #E8EEF4;

    border-radius: 8px;

    padding: 4px 7px;

    font-size: 10px;

    font-weight: 600;

    margin-bottom: 5px;
}


/* -----------------------------------------------------
   NOTE
   ----------------------------------------------------- */

.itinerary-note {
    color: #6C8095;

    font-size: 11px;

    line-height: 1.5;

    border-top: 1px solid #EDF1F5;

    padding-top: 8px;

    margin-top: 5px;
}


/* -----------------------------------------------------
   BOOKING
   ----------------------------------------------------- */

.itinerary-booking {
    margin-top: 9px;

    padding-top: 9px;

    border-top: 1px solid #EDF1F5;
}


.itinerary-booking a {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    text-decoration: none;

    background: #EEF5FB;

    color: #315B82;

    border: 1px solid #D7E5F2;

    border-radius: 9px;

    padding: 6px 9px;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: .35px;
}


/* =====================================================
   ITINERARY — MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .itinerary-day {
        margin: 19px 0 18px 0;
    }


    .itinerary-day-header {
        border-radius: 15px;

        padding: 11px 13px;

        gap: 9px;
    }


    .itinerary-day-name {
        font-size: 15px;
    }


    .itinerary-day-meta {
        font-size: 9px;

        margin-top: 2px;
    }


    .itinerary-day-count {
        padding: 5px 8px;

        font-size: 9px;
    }


    .itinerary-timeline {
        margin-top: 9px;
    }


    .itinerary-timeline::before {
        left: 61px;

        top: 15px;
        bottom: 15px;
    }


    .itinerary-item {
        grid-template-columns: 50px minmax(0, 1fr);

        column-gap: 23px;

        margin-bottom: 9px;
    }


    .itinerary-time {
        padding-top: 15px;

        font-size: 10px;
    }


    .itinerary-dot {
        left: 54px;

        top: 19px;

        width: 13px;
        height: 13px;

        border-width: 4px;
    }


    .itinerary-card {
        border-radius: 15px;

        padding: 13px 13px 12px 13px;
    }


    .itinerary-card::before {
        top: 11px;
        bottom: 11px;
    }


    .itinerary-card-top {
        margin-bottom: 7px;
    }


    .itinerary-type {
        padding: 4px 7px;

        font-size: 8.5px;
    }


    .itinerary-title {
        font-size: 15.5px;

        line-height: 1.34;
    }


    .itinerary-place {
        font-size: 11px;

        margin-bottom: 5px;
    }


    .itinerary-mode {
        font-size: 9.5px;

        padding: 4px 7px;
    }


    .itinerary-note {
        font-size: 10.5px;
    }


    .itinerary-booking a {
        width: 100%;

        font-size: 8.5px;

        padding: 7px 9px;
    }
}

/* =====================================================
   BOOKINGS — PREMIUM TRAVEL CARDS
   ===================================================== */

.booking-kpi-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px;

    margin-top: 12px;
    margin-bottom: 18px;
}


.booking-kpi-card {
    position: relative;

    min-height: 102px;

    padding: 17px 18px;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F8FAFC 100%
        );

    border: 1px solid #DCE5EF;

    border-radius: 18px;

    box-shadow:
        0 7px 20px rgba(24,55,90,0.055),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}


.booking-kpi-card::after {
    content: "";

    position: absolute;

    left: 18px;
    bottom: 13px;

    width: 30px;
    height: 3px;

    border-radius: 999px;

    background:
        linear-gradient(
            90deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );
}


.booking-kpi-label {
    position: relative;
    z-index: 2;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 1.15px;

    color: #718398;
}


.booking-kpi-value {
    position: relative;
    z-index: 2;

    margin-top: 9px;

    font-size: 28px;

    line-height: 1;

    font-weight: 800;

    letter-spacing: -0.8px;

    color: #17365D;
}


/* -----------------------------------------------------
   BOOKING CARD
   ----------------------------------------------------- */

.booking-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F9FBFD 100%
        );

    border: 1px solid #DCE5EF;

    border-radius: 18px;

    padding: 17px 18px 16px 18px;

    margin-bottom: 13px;

    box-shadow:
        0 8px 22px rgba(24,55,90,0.055),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}


/* blue signature line */

.booking-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    background:
        linear-gradient(
            180deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );

    opacity: .72;
}


/* -----------------------------------------------------
   TOP
   ----------------------------------------------------- */

.booking-card-top {
    display: flex;

    align-items: center;
    justify-content: space-between;

    gap: 12px;
}


.booking-icon {
    display: flex;

    align-items: center;
    justify-content: center;

    width: 34px;
    height: 34px;

    background: #F1F6FA;

    border: 1px solid #E1EAF1;

    border-radius: 10px;

    font-size: 18px;
}


/* -----------------------------------------------------
   STATUS
   ----------------------------------------------------- */

.booking-status {
    display: inline-flex;

    align-items: center;

    padding: 5px 9px;

    border-radius: 999px;

    font-size: 8.5px;

    font-weight: 800;

    letter-spacing: .6px;

    white-space: nowrap;
}


.booking-status.booked {
    background: #EAF5EF;

    border: 1px solid #D4E9DC;

    color: #397A57;
}


.booking-status.to-book {
    background: #FFF4D8;

    border: 1px solid #F1E1B5;

    color: #9A6A00;
}


.booking-status.check-availability {
    background: #EEF5FB;

    border: 1px solid #D9E7F3;

    color: #315B82;
}


/* -----------------------------------------------------
   CATEGORY
   ----------------------------------------------------- */

.booking-category {
    margin-top: 13px;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 1.05px;

    color: #8192A3;

    text-transform: uppercase;
}


/* -----------------------------------------------------
   ITEM
   ----------------------------------------------------- */

.booking-item {
    margin-top: 4px;

    font-size: 17px;

    line-height: 1.32;

    font-weight: 800;

    letter-spacing: -.25px;

    color: #17365D;
}


/* -----------------------------------------------------
   DATE
   ----------------------------------------------------- */

.booking-date {
    margin-top: 9px;

    font-size: 11.5px;

    font-weight: 700;

    color: #526A82;
}


/* -----------------------------------------------------
   PROVIDER
   ----------------------------------------------------- */

.booking-provider {
    margin-top: 4px;

    font-size: 11.5px;

    color: #7A8EA3;
}


/* -----------------------------------------------------
   META
   ----------------------------------------------------- */

.booking-meta {
    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 12px;

    margin-top: 14px;

    padding-top: 12px;

    border-top: 1px solid #E8EEF3;
}


.booking-meta span {
    display: block;

    font-size: 8px;

    font-weight: 800;

    letter-spacing: .8px;

    color: #8A9AAC;
}


.booking-meta strong {
    display: block;

    margin-top: 4px;

    font-size: 12px;

    color: #315B82;
}


.booking-meta strong.high {
    color: #B97821;
}


/* -----------------------------------------------------
   NOTES
   ----------------------------------------------------- */

.booking-notes {
    margin-top: 11px;

    padding: 9px 10px;

    background: #F7FAFC;

    border: 1px solid #E7EEF4;

    border-radius: 9px;

    font-size: 10.5px;

    line-height: 1.5;

    color: #637B94;
}


/* -----------------------------------------------------
   BOOKING LINK
   ----------------------------------------------------- */

.booking-link {
    display: flex;

    align-items: center;
    justify-content: center;

    margin-top: 11px;

    padding: 8px 10px;

    border-radius: 9px;

    text-align: center;

    text-decoration: none !important;

    font-size: 8.5px;

    font-weight: 800;

    letter-spacing: .55px;

    color: #315B82 !important;

    background: #EEF5FB;

    border: 1px solid #D7E5F2;
}


.booking-link:hover {
    background: #E4F0F9;

    border-color: #BFD7EB;
}


/* =====================================================
   BOOKINGS — MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .booking-kpi-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 10px;

        margin-top: 12px;
        margin-bottom: 17px;
    }


    .booking-kpi-card {
        min-height: 88px;

        padding: 14px 15px;

        border-radius: 17px;
    }


    .booking-kpi-label {
        font-size: 8.5px;

        letter-spacing: 1px;
    }


    .booking-kpi-value {
        margin-top: 8px;

        font-size: 25px;
    }


    .booking-kpi-card::after {
        left: 15px;
        bottom: 11px;

        width: 28px;
        height: 3px;
    }


    .booking-card {
        padding: 15px 15px 14px 15px;

        border-radius: 16px;

        margin-bottom: 11px;
    }


    .booking-icon {
        width: 32px;
        height: 32px;

        border-radius: 9px;

        font-size: 17px;
    }


    .booking-status {
        padding: 5px 8px;

        font-size: 8px;
    }


    .booking-category {
        margin-top: 11px;

        font-size: 8.5px;
    }


    .booking-item {
        font-size: 16px;
    }


    .booking-date {
        font-size: 11px;
    }


    .booking-provider {
        font-size: 11px;
    }


    .booking-meta {
        margin-top: 12px;

        padding-top: 11px;

        gap: 10px;
    }


    .booking-meta span {
        font-size: 7.5px;
    }


    .booking-meta strong {
        font-size: 11.5px;
    }


    .booking-notes {
        font-size: 10px;

        padding: 8px 9px;
    }


    .booking-link {
        margin-top: 10px;

        padding: 8px;

        font-size: 8px;
    }
}

/* =====================================================
   TRANSPORT — PREMIUM JOURNEY CARDS
   ===================================================== */

.transport-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F9FBFD 100%
        );

    border: 1px solid #DCE5EF;

    border-radius: 18px;

    padding: 17px 18px 15px 18px;

    margin-bottom: 12px;

    box-shadow:
        0 8px 22px rgba(24,55,90,0.055),
        inset 0 1px 0 rgba(255,255,255,0.95);

    overflow: hidden;
}


/* blue signature */

.transport-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    background:
        linear-gradient(
            180deg,
            #4F6BED 0%,
            #7EC0EE 100%
        );

    opacity: .72;
}


/* -----------------------------------------------------
   DATE
   ----------------------------------------------------- */

.transport-date {
    margin-bottom: 12px;

    color: #718398;

    font-size: 9.5px;

    font-weight: 800;

    letter-spacing: 1px;

    text-transform: uppercase;
}


/* -----------------------------------------------------
   ROUTE
   ----------------------------------------------------- */

.transport-route {
    display: grid;

    grid-template-columns:
        minmax(0,1fr)
        34px
        minmax(0,1fr);

    align-items: center;

    gap: 8px;
}


.transport-location {
    color: #17365D;

    font-size: 15px;

    line-height: 1.3;

    font-weight: 800;

    letter-spacing: -.15px;
}


.transport-destination {
    text-align: right;
}


.transport-arrow {
    display: flex;

    align-items: center;
    justify-content: center;

    color: #7EC0EE;

    font-size: 17px;

    font-weight: 800;
}


/* -----------------------------------------------------
   META BADGES
   ----------------------------------------------------- */

.transport-meta {
    display: flex;

    flex-wrap: wrap;

    gap: 6px;

    margin-top: 13px;
}


.transport-badge {
    display: inline-flex;

    align-items: center;

    gap: 4px;

    background: #F4F8FB;

    border: 1px solid #E6EDF3;

    color: #526A82;

    border-radius: 999px;

    padding: 5px 8px;

    font-size: 10px;

    font-weight: 700;
}


.transport-cost {
    color: #315B82;

    font-weight: 800;
}


/* -----------------------------------------------------
   COUNTRY / NOTE
   ----------------------------------------------------- */

.transport-note {
    margin-top: 11px;

    padding-top: 10px;

    border-top: 1px solid #E8EEF3;

    color: #718398;

    font-size: 11px;

    line-height: 1.45;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {

    .transport-card {
        padding: 15px 15px 14px 15px;

        border-radius: 16px;

        margin-bottom: 11px;
    }


    .transport-date {
        margin-bottom: 11px;

        font-size: 9px;
    }


    .transport-route {
        grid-template-columns:
            minmax(0,1fr)
            28px
            minmax(0,1fr);

        gap: 7px;
    }


    .transport-location {
        font-size: 13.5px;

        line-height: 1.35;
    }


    .transport-arrow {
        font-size: 15px;
    }


    .transport-meta {
        gap: 5px;

        margin-top: 11px;
    }


    .transport-badge {
        padding: 5px 7px;

        font-size: 9.5px;
    }


    .transport-note {
        margin-top: 10px;

        padding-top: 9px;

        font-size: 10.5px;
    }
}

/* =====================================================
   TRANSPORT KPI — COMPACT
   ===================================================== */

.transport-kpi-grid .kpi-value {
    font-size: 24px;
    letter-spacing: -0.7px;
    white-space: nowrap;
}

@media (max-width: 768px) {

    .transport-kpi-grid .kpi-value {
        font-size: 22px;
        letter-spacing: -0.6px;
        white-space: nowrap;
    }

}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# GOOGLE SHEETS
# =========================================================

def sheet_url(gid):
    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
    )


@st.cache_data(ttl=300, show_spinner=False)
def load_sheet(gid):

    url = sheet_url(gid)

    try:
        response = requests.get(
            url,
            timeout=(5, 15),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/csv",
            },
        )

        response.raise_for_status()

        from io import StringIO

        df = pd.read_csv(
            StringIO(response.text)
        )

        df.columns = [
            str(c)
            .strip()
            .lower()
            .replace(" ", "_")
            for c in df.columns
        ]

        return df

    except requests.exceptions.Timeout:

        st.error(
            f"Google Sheets timeout untuk GID `{gid}`."
        )

        return pd.DataFrame()

    except requests.exceptions.RequestException as e:

        st.error(
            f"Gagal mengambil Google Sheets "
            f"(GID `{gid}`): {e}"
        )

        return pd.DataFrame()

# =========================================================
# HELPERS
# =========================================================

def clean(x):

    if pd.isna(x):
        return ""

    return str(x).strip()


def find_col(df, candidates):

    cols = {
        str(c).lower().strip(): c
        for c in df.columns
    }

    for candidate in candidates:

        candidate = candidate.lower().strip()

        if candidate in cols:
            return cols[candidate]

    for candidate in candidates:

        candidate = candidate.lower().strip()

        for col in cols:

            if candidate in col:
                return cols[col]

    return None


def number(x):

    if pd.isna(x):
        return 0.0

    if isinstance(
        x,
        (int, float, np.integer, np.floating)
    ):
        return float(x)

    s = str(x).strip()

    if not s:
        return 0.0

    s = re.sub(
        r"[^\d,.\-]",
        "",
        s
    )

    if "," in s and "." in s:

        if s.rfind(",") > s.rfind("."):

            s = (
                s.replace(".", "")
                .replace(",", ".")
            )

        else:

            s = s.replace(",", "")

    elif "," in s:

        parts = s.split(",")

        if len(parts[-1]) == 3:
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")

    elif "." in s:

        parts = s.split(".")

        if len(parts) > 2:
            s = s.replace(".", "")

        elif len(parts[-1]) == 3:
            s = s.replace(".", "")

    try:
        return float(s)

    except Exception:
        return 0.0


def duration_to_hours(value):

    if pd.isna(value):
        return 0.0

    if isinstance(
        value,
        (int, float, np.integer, np.floating)
    ):
        return max(float(value), 0)

    s = str(value).strip().lower()

    if not s:
        return 0.0

    # 02:30
    match = re.match(
        r"^(\d+):(\d{1,2})$",
        s
    )

    if match:

        h = float(match.group(1))
        m = float(match.group(2))

        return h + m / 60

    # 2h 30m
    h = re.search(
        r"(\d+(?:\.\d+)?)\s*h",
        s
    )

    m = re.search(
        r"(\d+(?:\.\d+)?)\s*m",
        s
    )

    if h or m:

        hours = (
            float(h.group(1))
            if h else 0
        )

        minutes = (
            float(m.group(1))
            if m else 0
        )

        return hours + minutes / 60

    # 2 hours
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*hour",
        s
    )

    if match:
        return float(match.group(1))

    # 90 min
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*min",
        s
    )

    if match:
        return float(match.group(1)) / 60

    try:
        return float(s)

    except Exception:
        return 0.0



def normalize_activity_category(value):
    """
    Classify an itinerary item based primarily on its activity/title.

    Category priority:
    Rest
    Personal
    Transport
    Food
    Event
    Accommodation
    Culture
    Nature
    Explore
    Other

    The activity/title is the main source of truth.
    Other fields are only used when the title itself is empty.
    """

    s = clean(value).strip().lower()

    if not s:
        return "Other"

    # =====================================================
    # 1. REST
    # =====================================================

    rest_patterns = [
        r"\bovernight\b",
        r"\bsleep\b",
        r"\bsleeping\b",
        r"\bsleep/rest\b",
        r"\brest\b",
        r"\bnap\b",
        r"\bdowntime\b",
        r"\bfree time\b",
        r"\bleisure\b",
        r"\bsleep at\b",
        r"\bsleep on\b",
        r"\bsleeper\b",
    ]

    if any(re.search(pattern, s) for pattern in rest_patterns):
        return "Rest"

    # =====================================================
    # 2. PERSONAL
    # =====================================================

    personal_patterns = [
        r"\bwake up\b",
        r"\bwakeup\b",
        r"\bwake-up\b",
        r"\bget ready\b",
        r"\bgetting ready\b",
        r"\bprepare\b",
        r"\bpreparation\b",
        r"\bshower\b",
        r"\bfreshen up\b",
        r"\bpack\b",
        r"\bunpack\b",
        r"\bpersonal time\b",
        r"\bchange clothes\b",
        r"\bget dressed\b",
    ]

    if any(re.search(pattern, s) for pattern in personal_patterns):
        return "Personal"

    # =====================================================
    # 3. TRANSPORT
    # =====================================================

    transport_patterns = [
        r"\btrain\b",
        r"\bsleeper train\b",
        r"\bbus\b",
        r"\bflight\b",
        r"\bplane\b",
        r"\bairport transfer\b",
        r"\btaxi\b",
        r"\bgrab\b",
        r"\bbolt\b",
        r"\bferry\b",
        r"\bboat\b",
        r"\btransfer\b",
        r"\bjourney\b",
        r"\btravel\b",
        r"\bdeparture\b",
        r"\bdepart\b",
        r"\barrival\b",
        r"\barrive\b",
        r"\btransport\b",
        r"\bboarding\b",
        r"\btransit\b",
        r"\bcommute\b",
        r"\bmrt\b",
        r"\blrt\b",
        r"\bmonorail\b",
        r"\bktm\b",
        r"\brental\b",
        r"\bmotorbike\b",
        r"\bmotorcycle\b",
        r"\bcar rental\b",
    ]

    # Route notation such as:
    # PODs → KL Sentral
    # KL Sentral → Bandar Tasik Selatan
    # KLIA → Sepang
    has_route_arrow = "→" in s or "->" in s

    if (
        has_route_arrow
        or any(re.search(pattern, s) for pattern in transport_patterns)
    ):
        return "Transport"

    # Waiting / boarding at a transport terminal
    transport_wait_patterns = [
        r"\bwait at tbs\b",
        r"\bwait at klia\b",
        r"\bwait at airport\b",
        r"\bwait for bus\b",
        r"\bwait for train\b",
        r"\bboarding\b",
        r"\bcheck-in.*boarding\b",
        r"\bboarding.*check-in\b",
    ]

    if any(
        re.search(pattern, s)
        for pattern in transport_wait_patterns
    ):
        return "Transport"

    # =====================================================
    # 4. FOOD
    # =====================================================

    food_patterns = [
        r"\bbreakfast\b",
        r"\blunch\b",
        r"\bdinner\b",
        r"\bmeal\b",
        r"\brestaurant\b",
        r"\bcafe\b",
        r"\bcoffee\b",
        r"\bfood\b",
        r"\beat\b",
        r"\beating\b",
        r"\bdining\b",
        r"\bbrunch\b",
        r"\bsupper\b",
    ]

    if any(re.search(pattern, s) for pattern in food_patterns):
        return "Food"

    # =====================================================
    # 5. EVENT
    # =====================================================

    event_patterns = [
        r"\bf1\b",
        r"\bformula 1\b",
        r"\bformula one\b",
        r"\brace\b",
        r"\bqualifying\b",
        r"\bgrand prix\b",
        r"\bfree practice\b",
        r"\bpractice session\b",
        r"\bsprint\b",
    ]

    if any(re.search(pattern, s) for pattern in event_patterns):
        return "Event"

    # =====================================================
    # 6. ACCOMMODATION
    # =====================================================

    accommodation_patterns = [
        r"\bhotel\b",
        r"\bhostel\b",
        r"\baccommodation\b",
        r"\bcheck-in at hotel\b",
        r"\bcheck in at hotel\b",
        r"\bcheck-out at hotel\b",
        r"\bcheck out at hotel\b",
        r"\bhotel check-in\b",
        r"\bhotel check out\b",
        r"\bstay at\b",
        r"\bovernight stay\b",
    ]

    if any(
        re.search(pattern, s)
        for pattern in accommodation_patterns
    ):
        return "Accommodation"

    # IMPORTANT:
    # Generic "check-in" is NOT automatically accommodation.
    # Example:
    # "Check-in + boarding / wait at TBS"
    # = Transport, already caught above.

    # =====================================================
    # 7. CULTURE
    # =====================================================

    culture_patterns = [
        r"\bculture\b",
        r"\bcultural\b",
        r"\barchitecture\b",
        r"\btemple\b",
        r"\bmuseum\b",
        r"\bheritage\b",
        r"\bhistorical\b",
        r"\bhistoric\b",
        r"\bpalace\b",
        r"\bmosque\b",
        r"\bchurch\b",
        r"\bmarket\b",
        r"\bshrine\b",
        r"\bfort\b",
        r"\bcastle\b",
    ]

    if any(re.search(pattern, s) for pattern in culture_patterns):
        return "Culture"

    # =====================================================
    # 8. NATURE
    # =====================================================

    nature_patterns = [
        r"\bnature\b",
        r"\bviewpoint\b",
        r"\bmountain\b",
        r"\bbeach\b",
        r"\blake\b",
        r"\bwaterfall\b",
        r"\bpark\b",
        r"\bhiking\b",
        r"\bhike\b",
        r"\btrek\b",
        r"\bisland\b",
        r"\bsunset\b",
        r"\bsunrise\b",
        r"\bforest\b",
        r"\bvalley\b",
        r"\btrail\b",
    ]

    if any(re.search(pattern, s) for pattern in nature_patterns):
        return "Nature"

    # =====================================================
    # 9. EXPLORE
    # =====================================================

    explore_patterns = [
        r"\bsightseeing\b",
        r"\bexplore\b",
        r"\bexploration\b",
        r"\bwander\b",
        r"\bwalking tour\b",
        r"\bsightseeing tour\b",
        r"\bvisit\b",
        r"\bshopping\b",
    ]

    if any(re.search(pattern, s) for pattern in explore_patterns):
        return "Explore"

    return "Other"

def parse_time_to_minutes(value):
    """Parse HH:MM into minutes after midnight."""
    if pd.isna(value):
        return None

    match = re.search(r"(\d{1,2}):(\d{2})", str(value).strip())
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2))

    if hour > 23 or minute > 59:
        return None

    return hour * 60 + minute


def merge_intervals(intervals):
    """Merge overlapping intervals so the same clock time is not double-counted."""
    intervals = sorted(
        [
            (start, end)
            for start, end in intervals
            if start is not None and end is not None and end > start
        ],
        key=lambda x: x[0]
    )

    if not intervals:
        return 0.0

    merged = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))

    return sum(end - start for start, end in merged) / 60


# =========================================================
# DAILY ACTIVITY CALCULATION
# =========================================================

TRAVEL_KEYWORDS = [
    "train",
    "sleeper",
    "overnight train",
    "bus",
    "flight",
    "plane",
    "airport transfer",
    "taxi",
    "grab",
    "bolt",
    "ferry",
    "boat transfer",
    "transfer",
    "motor rental",
    "motorbike rental",
    "rental",
    "car rental",
    "transport",
    "journey",
    "travel",
]

REST_KEYWORDS = [
    "sleep",
    "sleeping",
    "rest",
    "free time",
    "downtime",
    "leisure",
    "nap",
    "hotel stay",
    "overnight",
]

# Things that ARE real activities.
ACTIVE_KEYWORDS = [
    # food
    "breakfast",
    "lunch",
    "dinner",
    "meal",
    "restaurant",
    "cafe",
    "coffee",
    "food",
    "eat",

    # sightseeing / culture
    "sightseeing",
    "visit",
    "museum",
    "temple",
    "mosque",
    "church",
    "palace",
    "heritage",
    "architecture",
    "historical",
    "market",
    "shopping",
    "culture",

    # nature
    "nature",
    "viewpoint",
    "mountain",
    "beach",
    "lake",
    "waterfall",
    "park",
    "hiking",
    "trek",
    "island",
    "sunset",
    "sunrise",

    # event
    "f1",
    "formula 1",
    "race",
    "event",

    # walking / exploration
    "walking",
    "walk",
    "explore",
    "exploration",
]


def row_text(row):
    """
    Combine all useful itinerary text fields into one searchable string.
    This makes the activity filter robust even when the Google Sheet
    uses different column names.
    """
    values = []

    for col in itinerary.columns:
        try:
            value = row[col]

            if pd.notna(value):
                values.append(str(value))

        except Exception:
            pass

    return " ".join(values).lower()


def is_real_activity(row):
    """
    Return True only for activities that represent
    actual active time.

    Included:
    - Food
    - Event
    - Culture
    - Nature
    - Explore
    - Personal

    Excluded:
    - Rest
    - Transport
    - Accommodation
    - Other
    """

    category = clean(
        row.get("_category", "")
    )

    ACTIVE_CATEGORIES = {
        "Food",
        "Event",
        "Culture",
        "Nature",
        "Explore",
        "Personal",
    }

    return category in ACTIVE_CATEGORIES


def calculate_daily_activity_hours(day_df):
    """
    Calculate genuine active hours only.

    Rules:
    - Uses the same canonical category as the itinerary UI.
    - Excludes Rest.
    - Excludes Transport, including sleeper trains.
    - Excludes Accommodation.
    - Requires both start and end time.
    - Does not use duration as fallback.
    - Merges overlapping intervals.
    """

    intervals = []

    for _, row in day_df.iterrows():

        # -------------------------------------------------
        # ONLY genuine active categories
        # -------------------------------------------------

        if not is_real_activity(row):
            continue

        # -------------------------------------------------
        # Require BOTH start and end
        # -------------------------------------------------

        start_min = (
            parse_time_to_minutes(
                row[start_col]
            )
            if start_col
            else None
        )

        end_min = (
            parse_time_to_minutes(
                row[end_col]
            )
            if end_col
            else None
        )

        if start_min is None or end_min is None:
            continue

        # -------------------------------------------------
        # Handle crossing midnight
        # -------------------------------------------------

        if end_min < start_min:
            end_min += 24 * 60

        if end_min <= start_min:
            continue

        intervals.append(
            (start_min, end_min)
        )

    return merge_intervals(intervals)


def parse_date(value):

    if pd.isna(value):
        return pd.NaT

    return pd.to_datetime(
        value,
        errors="coerce"
    )


def rupiah(value):

    return (
        f"{int(round(value)):,}"
        .replace(",", ".")
    )


def hours(value):

    return f"{value:.1f} h"

def format_hours_short(value):
    value = float(value or 0)

    if value >= 1:
        return f"{value:.1f} h"

    return f"{int(round(value * 60))} min"


def format_distance(value):
    value = float(value or 0)

    if value >= 1000:
        return f"{value / 1000:.1f}k km"

    if value == int(value):
        return f"{int(value)} km"

    return f"{value:.1f} km"


def clean_mode(value):
    mode = clean(value)

    if not mode:
        return "Other"

    if "grab" in mode.lower():
        return "Grab"

    return mode.title()


def safe_date_label(value):
    if pd.isna(value):
        return ""

    try:
        return pd.to_datetime(value).strftime("%d %b")
    except Exception:
        return str(value)
        
# =========================================================
# LOAD ALL DATA
# =========================================================

try:

    trips = load_sheet(
        GIDS["trips"]
    )

    places = load_sheet(
        GIDS["places"]
    )

    itinerary = load_sheet(
        GIDS["itinerary"]
    )

    transport = load_sheet(
        GIDS["transport"]
    )

    expenses = load_sheet(
        GIDS["expenses"]
    )

    exchange_rates = load_sheet(
        GIDS["exchange_rates"]
    )

    motor_rentals = load_sheet(
        GIDS["motor_rentals"]
    )

    booking_tracker = load_sheet(
        GIDS["booking_tracker"]
    )

except Exception as e:

    st.error(
        "Gagal mengambil data dari Google Sheets."
    )

    st.code(str(e))

    st.stop()


# =========================================================
# EXPENSES
# =========================================================

# PLANNED / ESTIMATED COST
expense_estimated_col = find_col(
    expenses,
    [
        "estimated_cost_idr",
        "estimated_cost",
        "estimated_price",
        "planned_cost",
        "planned_price",
        "budget",
        "amount",
        "cost",
        "price",
    ],
)

# ACTUAL / REAL EXPENSE
expense_actual_col = find_col(
    expenses,
    [
        "actual_cost_idr",
        "actual_cost",
        "actual_price",
        "actual_expense",
        "real_expense",
        "spent",
        "paid_cost",
        "paid_amount",
    ],
)

expense_category_col = find_col(
    expenses,
    [
        "category",
        "expense_category",
        "type",
    ],
)

expense_date_col = find_col(
    expenses,
    [
        "date",
        "expense_date",
        "start_date",
    ],
)

expense_currency_col = find_col(
    expenses,
    [
        "currency",
        "currency_code",
    ],
)


# ---------------------------------------------------------
# RAW AMOUNTS
# ---------------------------------------------------------

expenses["_planned_amount"] = (
    expenses[expense_estimated_col].apply(number)
    if expense_estimated_col
    else 0
)

expenses["_actual_amount"] = (
    expenses[expense_actual_col].apply(number)
    if expense_actual_col
    else 0
)

expenses["_category"] = (
    expenses[expense_category_col]
    .astype(str)
    .str.strip()
    if expense_category_col
    else "Other"
)

expenses["_currency"] = (
    expenses[expense_currency_col]
    .astype(str)
    .str.upper()
    .str.strip()
    if expense_currency_col
    else "IDR"
)

# =========================================================
# EXPENSE CONVERSION + BUDGET TOTALS
# =========================================================

# Build exchange-rate dictionary from Google Sheets.
# Expected exchange-rate sheet structure:
# currency | rate
exchange_currency_col = find_col(
    exchange_rates,
    [
        "currency",
        "currency_code",
    ],
)

exchange_rate_col = find_col(
    exchange_rates,
    [
        "rate",
        "exchange_rate",
        "rate_to_idr",
        "idr_rate",
        "value",
    ],
)

rates = {}

if (
    not exchange_rates.empty
    and exchange_currency_col
    and exchange_rate_col
):
    for _, fx_row in exchange_rates.iterrows():

        currency = clean(
            fx_row[exchange_currency_col]
        ).upper()

        rate = number(
            fx_row[exchange_rate_col]
        )

        if currency:
            rates[currency] = rate

# IDR is always 1:1
rates["IDR"] = 1.0


def convert_to_idr(amount, currency):
    amount = number(amount)
    currency = clean(currency).upper()

    if not currency:
        currency = "IDR"

    rate = rates.get(currency)

    if rate is None or rate <= 0:
        return amount

    return amount * rate


# Planned / estimated amount in IDR
expenses["_idr"] = expenses.apply(
    lambda row: convert_to_idr(
        row["_planned_amount"],
        row["_currency"],
    ),
    axis=1,
)


# Actual / real expense in IDR
expenses["_actual_idr"] = expenses.apply(
    lambda row: convert_to_idr(
        row["_actual_amount"],
        row["_currency"],
    ),
    axis=1,
)


# =========================================================
# BUDGET TOTALS
# =========================================================

total_budget = expenses["_idr"].sum()

total_actual = expenses["_actual_idr"].sum()

total_remaining = (
    total_budget
    - total_actual
)

budget_used_pct = (
    (total_actual / total_budget) * 100
    if total_budget > 0
    else 0
)

# =========================================================
# ITINERARY COLUMNS
# =========================================================

date_col = find_col(
    itinerary,
    [
        "date",
        "itinerary_date",
        "start_date",
        "datetime",
    ],
)

# Optional columns used specifically to calculate multi-day accommodation stays.
end_date_col = find_col(
    itinerary,
    [
        "end_date",
        "checkout_date",
        "check_out_date",
        "stay_end_date",
    ],
)

nights_col = find_col(
    itinerary,
    [
        "nights",
        "number_of_nights",
        "stay_nights",
        "accommodation_nights",
    ],
)

start_col = find_col(
    itinerary,
    [
        "start_time",
        "time_start",
        "departure_time",
        "start",
    ],
)

end_col = find_col(
    itinerary,
    [
        "end_time",
        "time_end",
        "arrival_time",
        "end",
    ],
)

activity_col = find_col(
    itinerary,
    [
        "activity",
        "title",
        "activity_name",
        "name",
    ],
)

place_col = find_col(
    itinerary,
    [
        "place",
        "place_name",
        "location",
    ],
)

notes_col = find_col(
    itinerary,
    [
        "notes",
        "note",
        "description",
    ],
)

duration_col = find_col(
    itinerary,
    [
        "duration_hours",
        "duration",
        "hours",
        "planned_hours",
    ],
)

group_col = find_col(
    itinerary,
    [
        "activity_group",
        "group",
        "category",
        "type",
    ],
)

transport_mode_col = find_col(
    itinerary,
    [
        "from_previous",
        "transport",
        "mode",
        "travel_mode",
    ],
)

booking_url_col = find_col(
    itinerary,
    [
        "booking_url",
        "booking_link",
        "reservation_url",
        "reservation_link",
        "ticket_url",
        "ticket_link",
        "voucher_url",
        "confirmation_url",
    ],
)

# =========================================================
# DATES
# =========================================================

if date_col:

    itinerary["_date"] = (
        itinerary[date_col]
        .apply(parse_date)
    )

else:

    itinerary["_date"] = pd.NaT


# =========================================================
# HOURS
# =========================================================

def calculate_row_hours(row):

    # Prefer explicit duration
    if duration_col:

        value = duration_to_hours(
            row[duration_col]
        )

        if value > 0:
            return value

    # Otherwise calculate from start/end
    if start_col and end_col:

        start = pd.to_datetime(
            str(row[start_col]),
            errors="coerce"
        )

        end = pd.to_datetime(
            str(row[end_col]),
            errors="coerce"
        )

        if (
            pd.notna(start)
            and pd.notna(end)
        ):

            diff = (
                end - start
            ).total_seconds() / 3600

            if diff < 0:
                diff += 24

            return max(
                diff,
                0
            )

    return 0.0


itinerary["_hours"] = itinerary.apply(
    calculate_row_hours,
    axis=1
)

itinerary["_hours"] = (
    itinerary["_hours"]
    .fillna(0)
    .clip(lower=0)
)

# Total planned hours across all itinerary items
total_planned_hours = itinerary["_hours"].sum()

# Consolidated dashboard category for Time Allocation.
# IMPORTANT: classify from the actual activity/title, NOT from the sheet
# group/category column. The group is only a fallback when the title is empty.
# =========================================================
# UNIFIED ITINERARY CATEGORY
# =========================================================

def classify_row_category(row):
    """
    Assign ONE canonical category to each itinerary row.

    The activity/title is authoritative.
    Other fields are only consulted when the activity/title
    is genuinely empty.
    """

    activity = clean(
        row[activity_col]
    ) if activity_col else ""

    # -----------------------------------------------------
    # Activity/title is the source of truth
    # -----------------------------------------------------

    if activity:
        return normalize_activity_category(activity)

    # -----------------------------------------------------
    # Only when activity/title is empty:
    # inspect other useful fields
    # -----------------------------------------------------

    place = clean(
        row[place_col]
    ) if place_col else ""

    note = clean(
        row[notes_col]
    ) if notes_col else ""

    mode = clean(
        row[transport_mode_col]
    ) if transport_mode_col else ""

    group = clean(
        row[group_col]
    ) if group_col else ""

    fallback_text = " ".join(
        x for x in [
            place,
            note,
            mode,
            group,
        ]
        if x
    )

    if fallback_text:
        return normalize_activity_category(
            fallback_text
        )

    return "Other"


itinerary["_category"] = itinerary.apply(
    classify_row_category,
    axis=1
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">RYAN.LOG</div>
    <div class="hero-subtitle">
        F1 Sepang + Thailand 2026
    </div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# RYANOMAD SECTION NAVIGATION
# =========================================================

nav_html = """
<style>

.ryanomad-nav {
    position: fixed;
    top: 82px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 999999;

    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;

    width: fit-content;
    max-width: calc(100vw - 40px);

    padding: 5px;

    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #DCE5EF;
    border-radius: 999px;

    box-shadow: 0 6px 18px rgba(32, 58, 95, 0.14);

    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.ryanomad-nav a {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    height: 34px;
    padding: 0 15px;

    flex: 0 0 auto;

    border-radius: 999px;

    color: #637B94;
    background: transparent;

    text-decoration: none !important;

    font-family: Inter, sans-serif;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.4px;

    white-space: nowrap;

    transition: all 0.18s ease;
}

.ryanomad-nav a:hover {
    background: #EEF4F9;
    color: #203A5F;
}

.ryanomad-nav a.active {
    background: #203A5F;
    color: #FFFFFF;

    box-shadow: 0 3px 9px rgba(32, 58, 95, 0.18);
}

.ryanomad-nav a.top-button {
    margin-left: 4px;

    background: #F2F6FA;
    border: 1px solid #DCE5EF;
    color: #637B94;
}

.ryanomad-nav a.top-button:hover {
    background: #E8F0F7;
    color: #203A5F;
}

.ryanomad-nav-spacer {
    height: 72px;
}

.dashboard-section {
    scroll-margin-top: 80px;
}


/* MOBILE */

@media (max-width: 768px) {

    .ryanomad-nav {
        top: 10px;
        left: 12px;
        right: 12px;
        transform: none;

        width: auto;
        max-width: none;

        justify-content: flex-start;

        padding: 5px;

        background:
            linear-gradient(
                135deg,
                rgba(12, 31, 52, 0.96),
                rgba(19, 52, 82, 0.92)
            );

        border: 1px solid rgba(126,192,238,0.22);

        border-radius: 18px;

        box-shadow:
            0 8px 22px rgba(8,28,48,0.22),
            inset 0 1px 0 rgba(255,255,255,0.08);

        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);

        overflow-x: auto;
        scrollbar-width: none;
    }

    .ryanomad-nav-spacer {
        height: 0;
    }

    .hero {
        position: relative;
        top: 10px;
        margin-bottom: 0;
    }

    .stButton {
        margin-top: -30px;
    }

    .stButton > button {
        background: rgba(255,255,255,0.72) !important;
        color: #526A82 !important;

        border: 1px solid #D8E3ED !important;
        border-radius: 14px !important;

        box-shadow:
            0 5px 14px rgba(28,55,85,0.06),
            inset 0 1px 0 rgba(255,255,255,0.9);

        font-family: Inter, sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;

        letter-spacing: 0.1px;

        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        background: #FFFFFF !important;
        border-color: #BFD0DF !important;
        color: #203A5F !important;

        box-shadow:
            0 7px 18px rgba(28,55,85,0.09);
    }

    .section-title {
        position: relative;

        padding-left: 13px;

        font-size: 22px;
        line-height: 1.15;

        font-weight: 800;

        color: #203A5F;

        letter-spacing: -0.45px;

        margin-top: 18px;
        margin-bottom: 16px;
    }

    .section-title::before {
        content: "";

        position: absolute;

        left: 0;
        top: 3px;

        width: 4px;
        height: calc(100% - 6px);

        border-radius: 999px;

        background:
            linear-gradient(
                180deg,
                #4F6BED 0%,
                #7EC0EE 100%
            );

        box-shadow:
            0 0 8px rgba(79,107,237,0.22);
    }

    .ryanomad-nav::-webkit-scrollbar {
        display: none;
    }

    .ryanomad-nav a {
        height: 32px;
        padding: 0 13px;

        color: #B8C9D9;

        font-size: 9px;
        font-weight: 700;

        letter-spacing: 0.55px;
    }

    .ryanomad-nav a:hover {
        background: rgba(126,192,238,0.10);
        color: #FFFFFF;
    }

    .ryanomad-nav a.active {
        background:
            linear-gradient(
                135deg,
                #3D82B5,
                #245A83
            );

        color: #FFFFFF;

        box-shadow:
            0 3px 10px rgba(43,96,144,0.35),
            inset 0 1px 0 rgba(255,255,255,0.12);
    }

    .ryanomad-nav a.top-button {
        padding: 0 11px;
    }

    /* BOOKING FILTERS — MOBILE ONLY */
    .st-key-booking_category_filter [data-testid="stWidgetLabel"],
    .st-key-booking_status_filter [data-testid="stWidgetLabel"] {
        display: none;
    }

    .st-key-booking_category_filter,
    .st-key-booking_status_filter {
        margin-top: 0px;
        margin-bottom: 0px;
    }

    .transport-kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    }
}

</style>


<div id="ryanomad-top"></div>

<nav class="ryanomad-nav">

    <a href="#budget-overview">
        BUDGET
    </a>

    <a href="#time-pace">
        TIME
    </a>

    <a href="#destinations">
        DESTINATIONS
    </a>

    <a href="#itinerary">
        ITINERARY
    </a>

    <a href="#bookings">
        BOOKINGS
    </a>

    <a href="#transports">
        TRANSPORT
    </a>

    <a href="#motor-rental">
        RENTAL
    </a>

    <a href="#ryanomad-top" class="top-button">
        ↑ TOP
    </a>

</nav>

<script>

(function () {

    const nav =
        document.querySelector(".ryanomad-nav");

    if (!nav) return;

    const navLinks =
        nav.querySelectorAll(
            "a:not(.top-button)"
        );


    function updateActiveNav(hash) {

        navLinks.forEach(function (link) {

            if (
                link.getAttribute("href")
                === hash
            ) {

                link.classList.add("active");

            } else {

                link.classList.remove("active");

            }

        });

    }


    navLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    !targetId.startsWith("#")
                ) {
                    return;
                }

                const target =
                    document.querySelector(
                        targetId
                    );

                if (!target) {
                    return;
                }

                event.preventDefault();


                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

                updateActiveNav(
                    targetId
                );

            }
        );

    });


    updateActiveNav(
        window.location.hash
        || "#budget-overview"
    );

})();

</script>
"""

st.html(nav_html)

st.markdown(
    '<div class="ryanomad-nav-spacer"></div>',
    unsafe_allow_html=True
)

# =========================================================
# REFRESH DATA
# =========================================================

refresh_left, refresh_right = st.columns(
    [5, 1],
    vertical_alignment="center"
)

with refresh_right:

    if st.button(
    "🔄 Refresh Data",
    use_container_width=True,
    type="primary"
    ):
        st.cache_data.clear()
        st.rerun()

# =========================================================
# KPI
# =========================================================

st.markdown(
    '<div class="section-title">TRIP OVERVIEW</div>',
    unsafe_allow_html=True
)

st.html(
    f"""
    <div class="trip-kpi-grid">

        <div class="kpi-card kpi-featured">
            <div class="kpi-label">Total Budget</div>
            <div class="kpi-value">{rupiah(total_budget)}</div>
            <div class="kpi-accent"></div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Places</div>
            <div class="kpi-value">{len(places)}</div>
            <div class="kpi-accent"></div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Itinerary Items</div>
            <div class="kpi-value">{len(itinerary)}</div>
            <div class="kpi-accent"></div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Transport</div>
            <div class="kpi-value">{len(transport)}</div>
            <div class="kpi-accent"></div>
        </div>

        <div class="kpi-card">
            <div class="kpi-label">Planned Hours</div>
            <div class="kpi-value">{hours(total_planned_hours)}</div>
            <div class="kpi-accent"></div>
        </div>

    </div>
    """
)


# =========================================================
# BUDGET OVERVIEW
# =========================================================

st.markdown(
    """
    <div id="budget-overview" class="dashboard-section">
        <div class="section-title">BUDGET OVERVIEW</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# BUDGET STATUS
# =========================================================

b1, b2, b3 = st.columns(3)


with b1:

    remaining_label = (
        f"Rp {rupiah(total_remaining)}"
        if total_remaining >= 0
        else f"-Rp {rupiah(abs(total_remaining))}"
    )

    st.html(
        f"""
        <div class="budget-financial-card">

            <div class="budget-financial-item">

                <div class="kpi-label">
                    Real Expense
                </div>

                <div class="kpi-value">
                    Rp {rupiah(total_actual)}
                </div>

            </div>

            <div class="budget-financial-divider"></div>

            <div class="budget-financial-item">

                <div class="kpi-label">
                    Remaining
                </div>

                <div class="kpi-value">
                    {remaining_label}
                </div>

            </div>

            <div class="kpi-accent"></div>

        </div>
        """
    )


with b3:

    progress_position = min(
        max(budget_used_pct, 0),
        100
    )

    st.html(
        f"""
        <div class="budget-race-card">

            <div class="kpi-label">
                Budget Used
            </div>

            <div class="kpi-value">
                {budget_used_pct:.1f}%
            </div>

            <div class="budget-race">

                <div class="budget-race-line"></div>

                <div
                    class="budget-race-car"
                    style="left: calc({progress_position:.1f}% - 13px);"
                >
                    <span class="race-car-body">
                        <span class="race-car-cockpit"></span>
                        <span class="race-car-wheel race-wheel-front"></span>
                        <span class="race-car-wheel race-wheel-rear"></span>
                    </span>
                </div>

                <div class="budget-finish">
                    <span class="finish-flag">
                        <span class="flag-pole"></span>
                        <span class="flag-cloth"></span>
                    </span>
                </div>

            </div>

            <div class="budget-race-meta">
                <span>START</span>
                <span>FINISH</span>
            </div>

        </div>
        """
    )

# =========================================================
# BUDGET BY CATEGORY
# =========================================================

budget_category = (
    expenses
    .groupby("_category")[
        ["_idr", "_actual_idr"]
    ]
    .sum()
    .reset_index()
)

budget_category.columns = [
    "Category",
    "Planned",
    "Actual"
]

budget_category["Category"] = (
    budget_category["Category"]
    .astype(str)
    .str.strip()
)

# ---------------------------------------------------------
# DISPLAY ORDER
# ---------------------------------------------------------

budget_category = (
    budget_category
    .sort_values(
        "Planned",
        ascending=False
    )
    .reset_index(drop=True)
)

budget_lanes_html = ""

for _, row in budget_category.iterrows():

    category = escape(
        str(row["Category"])
    )

    planned = float(row["Planned"])
    actual = float(row["Actual"])

    planned_width = 100

    if planned > 0:
        actual_ratio = (
            actual / planned
        )

        actual_width = min(
            actual_ratio * 100,
            100
        )

        overflow_width = max(
            (actual_ratio - 1) * 100,
            0
        )
    else:
        actual_ratio = 0
        actual_width = 0
        overflow_width = 0

    planned_label = (
        f"Rp {rupiah(planned)}"
    )

    actual_label = (
        f"Rp {rupiah(actual)}"
    )

    if planned > 0:

        variance_pct = (
            (actual - planned)
            / planned
        ) * 100

        if variance_pct > 0:

            variance_html = f"""
                <span class="budget-over-value">
                    +{variance_pct:.1f}%
                </span>
            """

        elif variance_pct < 0:

            variance_html = f"""
                <span class="budget-under-value">
                    {variance_pct:.1f}%
                </span>
            """

        else:

            variance_html = """
                <span class="budget-on-value">
                    0.0%
                </span>
            """

    else:

        variance_html = ""

    budget_lanes_html += f"""
        <div class="budget-lane">

            <div class="budget-lane-header">

                <div class="budget-lane-category">
                    {category}
                </div>

                <div class="budget-lane-values">
                    <span class="budget-planned-value">
                        {planned_label}
                    </span>

                   <span class="budget-actual-value">
                        {actual_label}
                    </span>

                    {variance_html}
                </div>

            </div>

            <div class="budget-lane-bars">

                <div class="budget-lane-row">

                    <div class="budget-lane-tag">
                        P
                    </div>

                    <div class="budget-lane-track">

                        <div
                            class="budget-lane-bar budget-planned"
                            style="width:{planned_width:.1f}%"
                        ></div>

                    </div>

                </div>

                <div class="budget-lane-row">

                    <div class="budget-lane-tag budget-tag-actual">
                        A
                    </div>

                    <div class="budget-lane-track">

                        <div class="budget-actual-wrap">

                            <div
                                class="budget-lane-bar budget-actual"
                                style="width:{actual_width:.1f}%"
                            ></div>

                            {
                                f'''
                                <div
                                    class="budget-overflow"
                                    style="width:{min(overflow_width, 25):.1f}%"
                                ></div>
                                '''
                                if overflow_width > 0
                                else ""
                            }

                        </div>

                    </div>

                </div>

            </div>

        </div>
    """


st.html(
    f"""
    <style>

    /* =====================================================
       BUDGET LANES
       ===================================================== */

    .budget-lanes-card {{
        position: relative;

        width: 100%;

        padding: 22px 22px 24px 22px;

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(126,192,238,0.11),
                transparent 32%
            ),
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F8FAFC 100%
            );

        border: 1px solid rgba(190,205,220,0.75);

        border-radius: 20px;

        box-shadow:
            0 8px 24px rgba(24,55,90,0.065),
            inset 0 1px 0 rgba(255,255,255,0.95);

        overflow: hidden;
    }}

    .budget-lanes-title {{
        color: #203A5F;

        font-size: 20px;
        line-height: 1.15;

        font-weight: 800;

        letter-spacing: -0.45px;

        margin-bottom: 13px;
    }}

    .budget-lanes-legend {{
        display: flex;

        align-items: center;

        gap: 16px;

        margin-bottom: 22px;
    }}

    .budget-legend-item {{
        display: flex;

        align-items: center;

        gap: 6px;

        color: #718398;

        font-size: 9px;
        font-weight: 700;

        letter-spacing: 0.8px;

        text-transform: uppercase;
    }}

    .budget-legend-dot {{
        width: 8px;
        height: 8px;

        border-radius: 3px;
    }}

    .budget-legend-planned {{
        background: #7BC0EE;
    }}

    .budget-legend-actual {{
        background: #1468B3;
    }}

    .budget-lane {{
        padding: 0 0 17px 0;

        margin-bottom: 17px;

        border-bottom:
            1px solid #E8EEF4;
    }}

    .budget-lane:last-child {{
        padding-bottom: 0;
        margin-bottom: 0;

        border-bottom: none;
    }}

    .budget-lane-header {{
        display: flex;

        align-items: baseline;

        justify-content: space-between;

        gap: 10px;

        margin-bottom: 8px;
    }}

    .budget-lane-category {{
        color: #526A82;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 0.75px;

        text-transform: uppercase;

        white-space: nowrap;
    }}

    .budget-lane-values {{
        display: flex;

        gap: 8px;

        align-items: baseline;

        white-space: nowrap;
    }}

    .budget-planned-value {{
        color: #8BA0B3;

        font-size: 8px;
        font-weight: 600;
    }}

    .budget-actual-value {{
        color: #203A5F;

        font-size: 9px;
        font-weight: 800;
    }}

    .budget-lane-bars {{
        display: flex;

        flex-direction: column;

        gap: 5px;
    }}

    .budget-lane-row {{
        display: flex;

        align-items: center;

        gap: 7px;
    }}

    .budget-lane-tag {{
        width: 12px;

        color: #8BA0B3;

        font-size: 7px;
        font-weight: 800;

        text-align: center;

        letter-spacing: 0.3px;
    }}

    .budget-tag-actual {{
        color: #1468B3;
    }}

    .budget-lane-track {{
        flex: 1;

        height: 6px;

        background: #EDF2F6;

        border-radius: 999px;

        overflow: hidden;
    }}

    .budget-lane-bar {{
        height: 100%;

        min-width: 2px;

        border-radius: 999px;
    }}

    .budget-planned {{
        background:
            linear-gradient(
                90deg,
                #7BC0EE 0%,
                #A8D8F5 100%
            );
    }}

    .budget-actual {{
        background:
            linear-gradient(
                90deg,
                #1468B3 0%,
                #4F8FC5 100%
            );

        box-shadow:
            0 0 7px rgba(20,104,179,0.16);
    }}

    @media (max-width: 768px) {{

        .budget-lanes-card {{
            padding: 20px 19px 21px 19px;

            border-radius: 19px;
        }}

        .budget-lanes-title {{
            font-size: 20px;
        }}

        .budget-lanes-legend {{
            margin-bottom: 20px;
        }}

        .budget-lane {{
            padding-bottom: 16px;
            margin-bottom: 16px;
        }}

        .budget-lane-category {{
            font-size: 10px;
        }}

        .budget-lane-values {{
            gap: 5px;
        }}

        .budget-planned-value {{
            font-size: 7px;
        }}

        .budget-actual-value {{
            font-size: 8px;
        }}

        .budget-lane-track {{
            height: 7px;
        }}

    }}

    </style>

    <div class="budget-lanes-card">

        <div class="budget-lanes-title">
            Budget by Category
        </div>

        <div class="budget-lanes-legend">

            <div class="budget-legend-item">
                <span class="budget-legend-dot budget-legend-planned"></span>
                Planned
            </div>

            <div class="budget-legend-item">
                <span class="budget-legend-dot budget-legend-actual"></span>
                Actual
            </div>

        </div>

        {budget_lanes_html}

    </div>
    """
)

# =========================================================
# TIME & PACE
# =========================================================

st.markdown(
    """
    <div id="time-pace" class="dashboard-section">
        <div class="section-title">TIME & PACE</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TIME ALLOCATION HOURS
# ---------------------------------------------------------
#
# Time Allocation represents the FULL trip timeline.
#
# Rules:
#
# 1. Every explicit itinerary item keeps its own category
#    and duration.
#
# 2. Any unallocated gap between explicit itinerary items
#    is treated as REST.
#
# 3. Accommodation rows themselves are NOT counted using
#    their short check-in/check-out duration.
#
# 4. Accommodation is merged into REST.
#
# 5. Sleeper trains / flights / buses remain TRANSPORT if
#    they exist as explicit transport itinerary rows.
#
# 6. Same categories are consolidated into ONE row.
#
# 7. Categories are sorted from largest -> smallest.
#
# Example:
#
#   Dinner       19:00 - 21:00   Food
#   [NO ROW]     21:00 - 07:00   Rest
#   Breakfast    07:00 - 07:30   Food
#
# => Rest = 10.0 h
#
# ---------------------------------------------------------


# =========================================================
# HELPERS
# =========================================================

def _ta_text(row):

    values = []

    for col in [
        activity_col,
        place_col,
        notes_col,
        group_col,
    ]:

        if not col:
            continue

        try:

            value = clean(
                row[col]
            )

            if value:
                values.append(value)

        except Exception:
            pass

    return " ".join(
        values
    ).strip().lower()


def _ta_datetime(
    row,
    date_column,
    time_column=None,
):

    if not date_column:
        return pd.NaT

    try:

        date_value = parse_date(
            row[date_column]
        )

    except Exception:

        return pd.NaT

    if pd.isna(date_value):
        return pd.NaT

    base_date = (
        pd.Timestamp(
            date_value
        ).normalize()
    )

    if not time_column:
        return base_date

    try:

        time_value = clean(
            row[time_column]
        )

    except Exception:

        time_value = ""

    match = re.search(
        r"(\d{1,2}):(\d{2})",
        time_value,
    )

    if not match:
        return base_date

    try:

        hour = int(
            match.group(1)
        )

        minute = int(
            match.group(2)
        )

        return (
            base_date
            + pd.Timedelta(
                hours=hour,
                minutes=minute,
            )
        )

    except Exception:

        return base_date


def _ta_interval(row):

    start_dt = _ta_datetime(
        row,
        date_col,
        start_col,
    )

    if pd.isna(start_dt):
        return pd.NaT, pd.NaT

    end_dt = _ta_datetime(
        row,
        date_col,
        end_col,
    )

    # If there is no end time, use the calculated row duration.
    if pd.isna(end_dt):

        row_hours = pd.to_numeric(
            row.get(
                "_hours",
                0,
            ),
            errors="coerce",
        )

        if (
            pd.notna(row_hours)
            and row_hours > 0
        ):

            end_dt = (
                start_dt
                + pd.Timedelta(
                    hours=float(
                        row_hours
                    )
                )
            )

        else:

            end_dt = start_dt


    # Handle overnight activities.
    if end_dt <= start_dt:

        end_dt = (
            end_dt
            + pd.Timedelta(
                days=1
            )
        )

    return (
        start_dt,
        end_dt,
    )


def _ta_category(row):

    category = clean(
        row.get(
            "_category",
            "",
        )
    )

    if not category:
        return "Other"

    # Accommodation is conceptually rest
    # for Time Allocation.
    if category.lower() == "accommodation":
        return "Rest"

    return category


# =========================================================
# BUILD EXPLICIT TIMELINE
# =========================================================

timeline = itinerary.copy()

timeline[
    "_ta_start"
] = timeline.apply(
    lambda row: _ta_interval(row)[0],
    axis=1,
)

timeline[
    "_ta_end"
] = timeline.apply(
    lambda row: _ta_interval(row)[1],
    axis=1,
)


timeline = timeline[
    timeline["_ta_start"].notna()
    &
    timeline["_ta_end"].notna()
].copy()


timeline = timeline[
    timeline["_ta_end"]
    >
    timeline["_ta_start"]
].copy()


timeline = timeline.sort_values(
    "_ta_start"
).reset_index(
    drop=False
)


# =========================================================
# EXPLICIT ACTIVITY ALLOCATION
# =========================================================
#
# Keep the actual duration of every explicit activity.
#
# Accommodation rows are excluded here because:
#
#   Hotel check-in 20:00-20:20
#
# is NOT 0.3 h of "Accommodation".
#
# Its surrounding empty time will become Rest.
# =========================================================

timeline[
    "_ta_hours"
] = (
    timeline[
        "_ta_end"
    ]
    - timeline[
        "_ta_start"
    ]
).dt.total_seconds() / 3600


timeline[
    "_ta_category"
] = timeline.apply(
    _ta_category,
    axis=1,
)


# =========================================================
# REMOVE ACCOMMODATION ROW DURATION
# =========================================================

accommodation_mask_ta = (
    timeline[
        "_category"
    ]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("accommodation")
)


timeline.loc[
    accommodation_mask_ta,
    "_ta_hours"
] = 0.0


# =========================================================
# MERGE OVERLAPPING EXPLICIT ACTIVITIES
# =========================================================
#
# This prevents double counting when two rows overlap.
#
# Example:
#
# 10:00-11:00 Event
# 10:30-11:30 Other
#
# Occupied time = 1.5 h
# NOT 2.0 h.
# =========================================================

occupied_intervals = []

for _, row in timeline.iterrows():

    start_dt = row[
        "_ta_start"
    ]

    end_dt = row[
        "_ta_end"
    ]

    if end_dt > start_dt:

        occupied_intervals.append(
            (
                start_dt,
                end_dt,
            )
        )


occupied_intervals = sorted(
    occupied_intervals,
    key=lambda x: x[0],
)


merged_occupied = []

for start_dt, end_dt in occupied_intervals:

    if (
        not merged_occupied
        or
        start_dt
        >
        merged_occupied[-1][1]
    ):

        merged_occupied.append(
            [
                start_dt,
                end_dt,
            ]
        )

    else:

        merged_occupied[-1][1] = max(
            merged_occupied[-1][1],
            end_dt,
        )


# =========================================================
# FIND ALL UNALLOCATED GAPS
# =========================================================
#
# Every gap between explicit activities becomes Rest.
#
# This is the key change.
# =========================================================

rest_intervals = []


for i in range(
    len(merged_occupied) - 1
):

    current_end = (
        merged_occupied[i][1]
    )

    next_start = (
        merged_occupied[i + 1][0]
    )

    if next_start > current_end:

        rest_intervals.append(
            (
                current_end,
                next_start,
            )
        )


# =========================================================
# REST HOURS
# =========================================================

rest_hours = sum(
    (
        end_dt - start_dt
    ).total_seconds()
    / 3600
    for start_dt, end_dt
    in rest_intervals
)


# =========================================================
# EXPLICIT CATEGORY HOURS
# =========================================================

explicit_hours = (
    timeline[
        timeline[
            "_ta_hours"
        ] > 0
    ]
    .groupby(
        "_ta_category"
    )[
        "_ta_hours"
    ]
    .sum()
    .to_dict()
)


# =========================================================
# ADD REST
# =========================================================

explicit_hours["Rest"] = (
    explicit_hours.get(
        "Rest",
        0.0,
    )
    + rest_hours
)


# =========================================================
# CREATE FINAL TABLE
# =========================================================

time_group = pd.DataFrame(
    [
        {
            "Activity": category,
            "Hours": hours,
        }

        for category, hours
        in explicit_hours.items()

        if hours > 0
    ]
)


# =========================================================
# CONSOLIDATE CATEGORY ALIASES
# =========================================================
#
# This prevents visually different labels representing the
# same concept from becoming separate bars.
# =========================================================

category_merge = {

    "accommodation": "Rest",

    "rest / sleep": "Rest",

    "sleep": "Rest",

    "sleep / rest": "Rest",

}


time_group[
    "Activity"
] = (
    time_group[
        "Activity"
    ]
    .astype(str)
    .str.strip()
    .map(
        lambda x:
            category_merge.get(
                x.lower(),
                x,
            )
    )
)


# Re-group after category aliases.
time_group = (
    time_group
    .groupby(
        "Activity",
        as_index=False,
    )[
        "Hours"
    ]
    .sum()
)


# =========================================================
# CLEAN NUMBERS
# =========================================================

time_group[
    "Hours"
] = pd.to_numeric(
    time_group[
        "Hours"
    ],
    errors="coerce",
).fillna(0.0)


time_group = time_group[
    time_group[
        "Hours"
    ] > 0
].copy()


# =========================================================
# SORT LARGEST -> SMALLEST
# =========================================================

time_group = (
    time_group
    .sort_values(
        "Hours",
        ascending=False,
        kind="stable",
    )
    .reset_index(
        drop=True
    )
)


# =========================================================
# TIME ALLOCATION
# =========================================================

time_group = (
    itinerary
    .groupby("_category")["_hours"]
    .sum()
    .reset_index()
)

time_group.columns = [
    "Activity",
    "Hours"
]

time_group["Activity"] = (
    time_group["Activity"]
    .astype(str)
    .str.strip()
)

time_group["Hours"] = pd.to_numeric(
    time_group["Hours"],
    errors="coerce"
).fillna(0)

time_group = (
    time_group[
        time_group["Hours"] > 0
    ]
    .sort_values(
        "Hours",
        ascending=False
    )
    .reset_index(drop=True)
)


total_time_hours = (
    time_group["Hours"].sum()
    if not time_group.empty
    else 0
)

max_time_hours = (
    time_group["Hours"].max()
    if not time_group.empty
    else 1
)


time_lanes_html = ""

for _, row in time_group.iterrows():

    activity = escape(
        str(row["Activity"])
    )

    activity_hours = float(
        row["Hours"]
    )

    bar_width = (
        activity_hours
        / max_time_hours
    ) * 100

    share = (
        activity_hours
        / total_time_hours
        * 100
        if total_time_hours > 0
        else 0
    )

    time_lanes_html += f"""
        <div class="time-lane">

            <div class="time-lane-header">

                <div class="time-lane-name">
                    {activity}
                </div>

                <div class="time-lane-value">
                    {activity_hours:.1f} h
                    <span>
                        {share:.1f}%
                    </span>
                </div>

            </div>

            <div class="time-lane-track">

                <div
                    class="time-lane-bar"
                    style="width:{bar_width:.1f}%"
                ></div>

            </div>

        </div>
    """


st.html(
    f"""
    <style>

    .time-profile-card {{
        position: relative;
        width: 100%;

        padding: 22px 22px 24px 22px;

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(126,192,238,0.11),
                transparent 32%
            ),
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F8FAFC 100%
            );

        border: 1px solid rgba(190,205,220,0.75);
        border-radius: 20px;

        box-shadow:
            0 8px 24px rgba(24,55,90,0.065),
            inset 0 1px 0 rgba(255,255,255,0.95);

        overflow: hidden;
    }}

    .time-profile-title {{
        color: #203A5F;

        font-size: 20px;
        line-height: 1.15;

        font-weight: 800;
        letter-spacing: -0.45px;

        margin-bottom: 16px;
    }}

    .time-profile-summary {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;

        padding-bottom: 16px;
        margin-bottom: 4px;

        border-bottom: 1px solid #E8EEF4;
    }}

    .time-profile-summary-label {{
        color: #718398;

        font-size: 9px;
        font-weight: 700;

        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .time-profile-summary-value {{
        color: #17365D;

        font-size: 18px;
        font-weight: 800;

        letter-spacing: -0.4px;
    }}

    .time-lane {{
        padding: 14px 0 15px 0;

        border-bottom: 1px solid #E8EEF4;
    }}

    .time-lane:last-child {{
        border-bottom: none;
        padding-bottom: 2px;
    }}

    .time-lane-header {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;

        gap: 10px;
        margin-bottom: 7px;
    }}

    .time-lane-name {{
        color: #526A82;

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 0.8px;
        text-transform: uppercase;
    }}

    .time-lane-value {{
        color: #203A5F;

        font-size: 10px;
        font-weight: 800;

        white-space: nowrap;
    }}

    .time-lane-value span {{
        color: #8BA0B3;

        font-size: 8px;
        font-weight: 700;

        margin-left: 5px;
    }}

    .time-lane-track {{
        width: 100%;
        height: 7px;

        background: #EDF2F6;

        border-radius: 999px;
        overflow: hidden;
    }}

    .time-lane-bar {{
        height: 100%;
        min-width: 2px;

        background:
            linear-gradient(
                90deg,
                #4F6BED 0%,
                #7EC0EE 100%
            );

        border-radius: 999px;

        box-shadow:
            0 0 8px rgba(79,107,237,0.15);
    }}

    @media (max-width: 768px) {{

        .time-profile-card {{
            padding: 20px 19px 21px 19px;
            border-radius: 19px;
        }}

        .time-profile-title {{
            font-size: 20px;
        }}

        .time-profile-summary {{
            padding-bottom: 14px;
        }}

        .time-profile-summary-value {{
            font-size: 17px;
        }}

        .time-lane {{
            padding: 13px 0 14px 0;
        }}

        .time-lane-name {{
            font-size: 10px;
        }}

        .time-lane-value {{
            font-size: 9px;
        }}

        .time-lane-track {{
            height: 7px;
        }}

    }}

    </style>

    <div class="time-profile-card">

        <div class="time-profile-title">
            Time Allocation
        </div>

        <div class="time-profile-summary">

            <div class="time-profile-summary-label">
                Trip Time Mix
            </div>

            <div class="time-profile-summary-value">
                {total_time_hours:.1f} h
            </div>

        </div>

        {time_lanes_html}

    </div>
    """
)

# =========================================================

daily_records = []

dated_itinerary = itinerary.dropna(
    subset=["_date"]
).copy()

for current_date, day_df in dated_itinerary.groupby(
    dated_itinerary["_date"].dt.date
):

    activity_hours = calculate_daily_activity_hours(
        day_df
    )

    daily_records.append({
        "_date": pd.Timestamp(current_date),
        "_hours": activity_hours,
    })


daily_hours = pd.DataFrame(
    daily_records
)


# ---------------------------------------------------------
# Sort by date
# ---------------------------------------------------------

if not daily_hours.empty:

    daily_hours = daily_hours.sort_values(
        "_date"
    )

    daily_hours["Label"] = daily_hours[
        "_date"
    ].apply(
        lambda x: f"{x.strftime('%b')} {x.day}"
    )

# =========================================================
# DAILY ACTIVITY HOURS — ACTIVITY RHYTHM
# =========================================================

max_daily_hours = (
    daily_hours["_hours"].max()
    if not daily_hours.empty
    else 1
)

daily_rhythm_html = ""

for _, row in daily_hours.iterrows():

    day_label = escape(
        str(row["Label"])
    )

    hours_value = float(
        row["_hours"]
    )

    bar_width = (
        hours_value
        / max_daily_hours
        * 100
        if max_daily_hours > 0
        else 0
    )

    if hours_value >= 8:
        pace_class = "pace-high"
        pace_label = "FULL"
    elif hours_value >= 5:
        pace_class = "pace-medium"
        pace_label = "ACTIVE"
    elif hours_value > 0:
        pace_class = "pace-light"
        pace_label = "LIGHT"
    else:
        pace_class = "pace-empty"
        pace_label = "REST"

    daily_rhythm_html += f"""
        <div class="rhythm-day {pace_class}">

            <div class="rhythm-day-top">

                <div class="rhythm-day-label">
                    {day_label}
                </div>

                <div class="rhythm-day-hours">
                    {hours_value:.1f}h
                </div>

            </div>

            <div class="rhythm-track">

                <div
                    class="rhythm-bar"
                    style="width:{bar_width:.1f}%"
                ></div>

            </div>

            <div class="rhythm-status">
                {pace_label}
            </div>

        </div>
    """


st.html(
    f"""
    <style>

    /* =====================================================
       DAILY ACTIVITY — ACTIVITY RHYTHM
       ===================================================== */

    .activity-rhythm-card {{
        position: relative;

        width: 100%;

        padding: 22px 22px 24px 22px;

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(126,192,238,0.12),
                transparent 34%
            ),
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F8FAFC 100%
            );

        border: 1px solid rgba(190,205,220,0.75);

        border-radius: 20px;

        box-shadow:
            0 8px 24px rgba(24,55,90,0.065),
            inset 0 1px 0 rgba(255,255,255,0.95);

        overflow: hidden;
    }}

    .rhythm-header {{
        display: flex;

        align-items: flex-end;
        justify-content: space-between;

        margin-bottom: 17px;
    }}

    .rhythm-title {{
        color: #203A5F;

        font-size: 20px;
        line-height: 1.1;

        font-weight: 800;

        letter-spacing: -0.45px;
    }}

    .rhythm-reference {{
        color: #8BA0B3;

        font-size: 8px;
        font-weight: 700;

        letter-spacing: 0.8px;

        text-transform: uppercase;

        white-space: nowrap;
    }}

    .rhythm-reference strong {{
        color: #637B94;

        font-weight: 800;
    }}

    .rhythm-grid {{
        display: grid;

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 9px;
    }}

    .rhythm-day {{
        position: relative;

        padding: 11px 11px 10px 11px;

        background:
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F7FAFC 100%
            );

        border:
            1px solid #E1E9F0;

        border-radius: 13px;

        min-width: 0;

        overflow: hidden;
    }}

    .rhythm-day-top {{
        display: flex;

        align-items: center;
        justify-content: space-between;

        gap: 6px;

        margin-bottom: 8px;
    }}

    .rhythm-day-label {{
        color: #526A82;

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.7px;

        text-transform: uppercase;
    }}

    .rhythm-day-hours {{
        color: #203A5F;

        font-size: 11px;
        font-weight: 800;

        white-space: nowrap;
    }}

    .rhythm-track {{
        width: 100%;

        height: 5px;

        background: #EAF0F4;

        border-radius: 999px;

        overflow: hidden;
    }}

    .rhythm-bar {{
        height: 100%;

        min-width: 0;

        background:
            linear-gradient(
                90deg,
                #4F6BED 0%,
                #7EC0EE 100%
            );

        border-radius: 999px;

        box-shadow:
            0 0 7px rgba(79,107,237,0.16);
    }}

    .rhythm-status {{
        margin-top: 6px;

        color: #9AAABA;

        font-size: 7px;
        font-weight: 800;

        letter-spacing: 0.75px;

        text-transform: uppercase;
    }}

    .pace-high {{
        border-color:
            rgba(79,107,237,0.24);

        background:
            radial-gradient(
                circle at 100% 0%,
                rgba(126,192,238,0.10),
                transparent 45%
            ),
            #FFFFFF;
    }}

    .pace-high .rhythm-status {{
        color: #4F6BED;
    }}

    .pace-medium .rhythm-status {{
        color: #637B94;
    }}

    .pace-light .rhythm-status {{
        color: #9AAABA;
    }}

    .pace-empty {{
        opacity: 0.65;
    }}

    .pace-empty .rhythm-bar {{
        min-width: 2px;
    }}

    @media (max-width: 768px) {{

        .activity-rhythm-card {{
            padding: 20px 18px 21px 18px;

            border-radius: 19px;
        }}

        .rhythm-title {{
            font-size: 20px;
        }}

        .rhythm-reference {{
            font-size: 7px;
        }}

        .rhythm-grid {{
            gap: 8px;
        }}

        .rhythm-day {{
            padding: 10px 10px 9px 10px;

            border-radius: 12px;
        }}

        .rhythm-day-label {{
            font-size: 8px;
        }}

        .rhythm-day-hours {{
            font-size: 10px;
        }}

        .rhythm-track {{
            height: 5px;
        }}

        .rhythm-status {{
            font-size: 6.5px;
        }}

    }}

    </style>

    <div class="activity-rhythm-card">

        <div class="rhythm-header">

            <div class="rhythm-title">
                Daily Activity
            </div>

            <div class="rhythm-reference">
                Pace · <strong>{max_daily_hours:.1f}h peak</strong>
            </div>

        </div>

        <div class="rhythm-grid">

            {daily_rhythm_html}

        </div>

    </div>
    """
)

# =========================================================
# DESTINATIONS
# =========================================================

st.markdown(
    """
    <div id="destinations" class="dashboard-section">
        <div class="section-title">DESTINATIONS</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DESTINATION COLUMNS
# =========================================================

place_name_col = find_col(
    places,
    [
        "place_name",
        "name",
        "place"
    ]
)

city_col = find_col(
    places,
    [
        "city"
    ]
)

country_col = find_col(
    places,
    [
        "country"
    ]
)

category_col = find_col(
    places,
    [
        "category",
        "type",
        "place_type"
    ]
)

description_col = find_col(
    places,
    [
        "description",
        "info",
        "about",
        "notes",
        "note"
    ]
)

photo_spots_col = find_col(
    places,
    [
        "photo_spots",
        "photography_spots",
        "photo_spot",
        "best_photo_spots"
    ]
)

maps_url_col = find_col(
    places,
    [
        "maps_url",
        "google_maps",
        "google_maps_url",
        "maps_link",
        "google_maps_link"
    ]
)

# =========================================================
# DESTINATION DISPLAY EXCLUSIONS
# =========================================================

EXCLUDED_DESTINATION_CITIES = {
    "bandung",
    "tangerang",
    "singapore",
}

EXCLUDED_DESTINATION_CATEGORIES = {
    "transport hub",
    "motorbike rental",
    "ferry pier",
    "event",
}

# =========================================================
# CITY FILTER
# =========================================================

if city_col and not places.empty:

    destination_cities = (
        places[city_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    destination_cities = sorted(
        [
            city
            for city in destination_cities.unique()
            if (
                city
                and city.casefold()
                not in EXCLUDED_DESTINATION_CITIES
            )
        ]
    )

else:
    destination_cities = []

city_options = ["ALL"] + destination_cities

selected_city = st.selectbox(
    "Filter destinations",
    city_options,
    format_func=lambda x:
        "All Cities"
        if x == "ALL"
        else x.upper(),
    label_visibility="collapsed",
    key="destination_city_filter"
)


# =========================================================
# CATEGORY FILTER
# =========================================================

if category_col and not places.empty:

    destination_categories = (
        places[category_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    destination_categories = sorted(
        [
            category
            for category in destination_categories.unique()
            if (
                category
                and category.casefold()
                not in EXCLUDED_DESTINATION_CATEGORIES
            )
        ]
    )

else:
    destination_categories = []


category_options = ["ALL"] + destination_categories

selected_category = st.selectbox(
    "Filter destination category",
    category_options,
    format_func=lambda x:
        "All Categories"
        if x == "ALL"
        else x.upper(),
    label_visibility="collapsed",
    key="destination_category_filter"
)


# =========================================================
# FILTER DATA
# =========================================================

destination_view = places.copy()


# Remove non-destination cities
if city_col:
    destination_view = destination_view[
        ~destination_view[city_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        .isin(EXCLUDED_DESTINATION_CITIES)
    ].copy()


# Remove non-destination categories
if category_col:
    destination_view = destination_view[
        ~destination_view[category_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        .isin(EXCLUDED_DESTINATION_CATEGORIES)
    ].copy()

if (
    selected_city != "ALL"
    and city_col
):
    destination_view = destination_view[
        destination_view[city_col]
        .astype(str)
        .str.strip()
        == selected_city
    ].copy()


if (
    selected_category != "ALL"
    and category_col
):
    destination_view = destination_view[
        destination_view[category_col]
        .astype(str)
        .str.strip()
        == selected_category
    ].copy()


# =========================================================
# DESTINATION CARDS
# =========================================================

if destination_view.empty:

    st.html(
        """
        <div class="destination-empty">
            No destinations found for this city.
        </div>
        """
    )

else:

    # Sort by city, then place name
    sort_columns = []

    if city_col:
        sort_columns.append(city_col)

    if place_name_col:
        sort_columns.append(place_name_col)

    if sort_columns:
        destination_view = destination_view.sort_values(
            sort_columns,
            kind="stable"
        )

    current_city = None

    for _, row in destination_view.iterrows():

        city = (
            clean(row[city_col])
            if city_col
            else ""
        )

        # -------------------------------------------------
        # CITY HEADER
        # -------------------------------------------------

        if city != current_city:

            current_city = city

            st.html(
                f"""
                <div class="destination-city">
                    {escape(city.upper())}
                </div>
                """
            )

        # -------------------------------------------------
        # BASIC INFO
        # -------------------------------------------------

        place_name = (
            clean(row[place_name_col])
            if place_name_col
            else "Destination"
        )

        country = (
            clean(row[country_col])
            if country_col
            else ""
        )

        category = (
            clean(row[category_col])
            if category_col
            else ""
        )

        description = (
            clean(row[description_col])
            if description_col
            else ""
        )

        photo_spots = (
            clean(row[photo_spots_col])
            if photo_spots_col
            else ""
        )

        maps_url = (
            clean(row[maps_url_col])
            if maps_url_col
            else ""
        )

        # -------------------------------------------------
        # OPTIONAL CONTENT
        # -------------------------------------------------

        category_html = ""

        if category:
            category_html = (
                f'<span class="destination-tag">'
                f'{escape(category)}'
                f'</span>'
            )

        description_html = ""

        if description:
            description_html = (
                f'<div class="destination-description">'
                f'{escape(description)}'
                f'</div>'
            )

        photo_html = ""

        if photo_spots:
            photo_html = (
                '<div class="destination-photo">'
                '<div class="destination-label">'
                '📷 PHOTO SPOTS'
                '</div>'
                f'<div>{escape(photo_spots)}</div>'
                '</div>'
            )

        maps_html = ""

        if maps_url:
            maps_html = (
                '<div class="destination-actions">'
                f'<a href="{escape(maps_url)}" '
                'target="_blank" '
                'rel="noopener noreferrer">'
                '📍 OPEN IN GOOGLE MAPS'
                '</a>'
                '</div>'
            )

        # -------------------------------------------------
        # CARD
        # -------------------------------------------------

        st.html(
            f"""
            <div class="destination-card">

                <div class="destination-card-top">

                    <div>
                        <div class="destination-name">
                            📍 {escape(place_name)}
                        </div>

                        <div class="destination-location">
                            {escape(country)}
                        </div>
                    </div>

                    <div>
                        {category_html}
                    </div>

                </div>

                {description_html}

                {photo_html}

                {maps_html}

            </div>
            """
        )

# =========================================================
# TRIP EXPLORER
# =========================================================

st.markdown(
    """
    <div id="itinerary" class="dashboard-section">
        <div class="section-title">ITINERARY</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATE FILTER
# =========================================================

if (
    date_col
    and itinerary["_date"].notna().any()
):

    dates = sorted(
        itinerary["_date"]
        .dropna()
        .dt.date
        .unique()
    )

    options = ["ALL"] + list(dates)

    selected = st.selectbox(
        "Filter itinerary",
        options,
        format_func=lambda x:
            "All Dates"
            if x == "ALL"
            else x.strftime(
                "%a, %d %b %Y"
            ),
        label_visibility="collapsed",
        key="itinerary_date_filter"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if selected == "ALL":

        filtered_itinerary = (
            itinerary.copy()
        )

    else:

        filtered_itinerary = (
            itinerary[
                itinerary["_date"].dt.date
                == selected
            ].copy()
        )

else:

    filtered_itinerary = (
        itinerary.copy()
    )

# =========================================================
# ITINERARY PLACE NAME MAP
# =========================================================

place_id_map = {}

if not places.empty:

    places_id_col = find_col(
        places,
        [
            "place_id",
            "location_id",
            "id",
        ]
    )

    places_name_col = find_col(
        places,
        [
            "place_name",
            "name",
            "location_name",
        ]
    )

    if (
        places_id_col
        and places_name_col
    ):

        for _, place_row in places.iterrows():

            place_id = clean(
                place_row[places_id_col]
            )

            place_name = clean(
                place_row[places_name_col]
            )

            if place_id and place_name:

                place_id_map[
                    place_id.casefold()
                ] = place_name

# =========================================================
# ITINERARY DISPLAY
# =========================================================

if len(filtered_itinerary) == 0:
    st.html(
        '<div class="itinerary-empty">'
        '<div style="font-size:28px;">🗓️</div>'
        '<div style="font-size:15px;font-weight:700;margin-top:8px;">'
        'No itinerary for this date'
        '</div>'
        '</div>'
    )

else:
    # Keep each day's timeline chronological.
    filtered_itinerary["_sort_minutes"] = filtered_itinerary[start_col].apply(
        parse_time_to_minutes
    ) if start_col else 0

    filtered_itinerary = filtered_itinerary.sort_values(
        ["_date", "_sort_minutes"],
        na_position="last",
        kind="stable"
    )

    for current_date, day_df in filtered_itinerary.groupby(
        filtered_itinerary["_date"].dt.date,
        dropna=False
    ):

        if pd.isna(current_date):
            date_label = "Undated"
        else:
            date_label = current_date.strftime("%a, %d %b %Y")

        item_count = len(day_df)
        item_word = "item" if item_count == 1 else "items"

        # Build the COMPLETE day's HTML in one string.
        # st.html() is deliberately used instead of st.markdown()
        # so Streamlit never interprets the HTML as a Markdown code block.
        day_html = (
            '<div class="itinerary-day">'
            '<div class="itinerary-day-header">'
            '<div>'
            '<div class="itinerary-day-name">'
            + escape(date_label) +
            '</div>'
            '</div>'
            '<div class="itinerary-day-count">'
            + str(item_count) + ' ' + item_word +
            '</div>'
            '</div>'
            '<div class="itinerary-timeline">'
        )

        for _, row in day_df.iterrows():

            start_time = clean(row[start_col]) if start_col else ""
            end_time = clean(row[end_col]) if end_col else ""

            if start_time and end_time:
                time_text = (
                    escape(start_time) + '<br>–<br>' + escape(end_time)
                )
            elif start_time:
                time_text = escape(start_time)
            else:
                row_hours = pd.to_numeric(
                    row["_hours"], errors="coerce"
                )
                time_text = (
                    f"{row_hours:.1f} h"
                    if pd.notna(row_hours) and row_hours > 0
                    else "—"
                )

            activity = (
                clean(row[activity_col])
                if activity_col
                else "Activity"
            )

            place = (
                clean(row[place_col])
                if place_col
                else ""
            )

            place_display = (
                place_id_map.get(
                    place.casefold(),
                    place
                )
            )
            note = clean(row[notes_col]) if notes_col else ""
            mode = clean(row[transport_mode_col]) if transport_mode_col else ""
            group = clean(row[group_col]) if group_col else ""

            booking_url = (
                clean(row[booking_url_col])
                 if booking_url_col
                 else ""
            )

            # =====================================================
            # CATEGORY
            # =====================================================

            # Always use the SAME canonical category calculated
            # earlier for the dataframe.
            classified = row.get(
                "_category",
                "Other"
            )

            type_map = {
                "Rest": ("😴", "Rest"),
                "Personal": ("🧳", "Personal"),
                "Transport": ("🚆", "Transport"),
                "Event": ("🏁", "Event"),
                "Food": ("🍜", "Food"),
                "Accommodation": ("🛏️", "Accommodation"),
                "Nature": ("🌿", "Nature"),
                "Culture": ("🏛️", "Culture"),
                "Explore": ("🚶", "Explore"),
                "Other": ("📍", "Activity"),
            }

            icon, type_label = type_map.get(
                classified,
                ("📍", "Activity")
            )

            row_hours = pd.to_numeric(row["_hours"], errors="coerce")
            duration_html = ""
            if pd.notna(row_hours) and row_hours > 0 and start_time and end_time:
                duration_html = (
                    '<div class="itinerary-duration">'
                    + f"{row_hours:.1f} h"
                    + '</div>'
                )

            place_html = ""

            place_text = (
                place_display
                if "place_display" in locals()
                else place
            )

            if (
                place_text
                and classified != "Transport"
            ):
                place_html = (
                    '<div class="itinerary-place">📍 '
                    + escape(place_text) +
                    '</div>'
                )

            mode_html = ""
            if mode:
                mode_html = (
                    '<div class="itinerary-mode">🚆 '
                    + escape(mode) +
                    '</div>'
                )

            note_html = ""
            if note:
                note_html = (
                    '<div class="itinerary-note">'
                    + escape(note) +
                    '</div>'
                )
            
            booking_html = ""

            if booking_url:
                if re.match(r"^https?://", booking_url, re.IGNORECASE):
                    booking_html = (
                        '<div class="itinerary-booking">'
                        '<a href="' + escape(booking_url, quote=True) + '" '
                        'target="_blank" rel="noopener noreferrer">'
                        '↗ OPEN BOOKING'
                        '</a>'
                        '</div>'
                    )

            day_html += (
                '<div class="itinerary-item">'
                '<div class="itinerary-time">'
                + time_text +
                '</div>'
                '<div class="itinerary-dot"></div>'
                '<div class="itinerary-card">'
                '<div class="itinerary-card-top">'
                '<div class="itinerary-type">'
                + icon + ' ' + escape(type_label) +
                '</div>'
                + duration_html +
                '</div>'
                '<div class="itinerary-title">'
                + escape(activity) +
                '</div>'
                + place_html
                + mode_html
                + note_html
                + booking_html
                + '</div>'
                '</div>'
            )

        day_html += '</div></div>'
        st.html(day_html)

# =========================================================
# BOOKINGS
# =========================================================

st.markdown(
    """
    <div id="bookings" class="dashboard-section">
        <div class="section-title">BOOKINGS</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# BOOKING TRACKER COLUMN DETECTION
# =========================================================

booking = booking_tracker.copy()

booking.columns = (
    booking.columns
    .astype(str)
    .str.strip()
)

booking_id_col = find_col(
    booking,
    ["booking_id"]
)

booking_category_col = find_col(
    booking,
    ["category"]
)

booking_item_col = find_col(
    booking,
    ["item"]
)

booking_provider_col = find_col(
    booking,
    ["provider"]
)

booking_start_col = find_col(
    booking,
    ["date_start"]
)

booking_end_col = find_col(
    booking,
    ["date_end"]
)

booking_priority_col = find_col(
    booking,
    ["priority"]
)

booking_status_col = find_col(
    booking,
    ["booking_status"]
)

booking_cost_col = find_col(
    booking,
    ["estimated_cost"]
)

booking_currency_col = find_col(
    booking,
    ["currency"]
)

booking_url_col = find_col(
    booking,
    ["booking_url"]
)

booking_confirmation_col = find_col(
    booking,
    ["confirmation_number"]
)

booking_notes_col = find_col(
    booking,
    ["notes"]
)

# =========================================================
# BOOKING KPI
# =========================================================

booking_total = len(booking)

booking_status = (
    booking[booking_status_col]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
    if booking_status_col
    else pd.Series(dtype=str)
)

booking_priority = (
    booking[booking_priority_col]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
    if booking_priority_col
    else pd.Series(dtype=str)
)

booked_count = (
    (booking_status == "booked").sum()
)

to_book_count = (
    (booking_status == "to book").sum()
)

high_priority_count = (
    (booking_priority == "high").sum()
)

st.html(
    f"""
    <div class="booking-kpi-grid">

        <div class="booking-kpi-card">
            <div class="booking-kpi-label">
                TOTAL BOOKINGS
            </div>

            <div class="booking-kpi-value">
                {booking_total}
            </div>
        </div>


        <div class="booking-kpi-card">
            <div class="booking-kpi-label">
                BOOKED
            </div>

            <div class="booking-kpi-value">
                {booked_count}
            </div>
        </div>


        <div class="booking-kpi-card">
            <div class="booking-kpi-label">
                TO BOOK
            </div>

            <div class="booking-kpi-value">
                {to_book_count}
            </div>
        </div>


        <div class="booking-kpi-card">
            <div class="booking-kpi-label">
                HIGH PRIORITY
            </div>

            <div class="booking-kpi-value">
                {high_priority_count}
            </div>
        </div>

    </div>
    """
)

# =========================================================
# BOOKING FILTERS
# =========================================================

# ---------------------------------------------------------
# CATEGORY OPTIONS
# ---------------------------------------------------------

if booking_category_col:

    booking_categories = sorted(
        booking[
            booking_category_col
        ]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

else:

    booking_categories = []


# ---------------------------------------------------------
# STATUS OPTIONS
# ---------------------------------------------------------

if booking_status_col:

    booking_statuses = sorted(
        booking[
            booking_status_col
        ]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

else:

    booking_statuses = []


# ---------------------------------------------------------
# FILTER UI
# ---------------------------------------------------------

filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    selected_booking_category = st.selectbox(

        "CATEGORY",

        ["ALL"] + booking_categories,

        format_func=lambda x:
        "All Categories"
        if x == "ALL"
        else x.upper(),

        key="booking_category_filter"

    )


with filter_col2:

    selected_booking_status = st.selectbox(

        "STATUS",

        ["ALL"] + booking_statuses,

        format_func=lambda x:
        "All Statuses"
        if x == "ALL"
        else x.upper(),

        key="booking_status_filter"

    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_booking = booking.copy()


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

if (

    selected_booking_category != "ALL"

    and booking_category_col

):

    filtered_booking = filtered_booking[

        filtered_booking[
            booking_category_col
        ]
        .fillna("")
        .astype(str)
        .str.strip()

        == selected_booking_category

    ]


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

if (

    selected_booking_status != "ALL"

    and booking_status_col

):

    filtered_booking = filtered_booking[

        filtered_booking[
            booking_status_col
        ]
        .fillna("")
        .astype(str)
        .str.strip()

        == selected_booking_status

    ]

# =========================================================
# BOOKING DISPLAY
# =========================================================

if len(filtered_booking) == 0:

    st.html(
        """
        <div class="booking-empty">
            <div style="font-size:30px;">📋</div>
            <div>No bookings found</div>
        </div>
        """
    )

else:

    for _, row in filtered_booking.iterrows():

        category = (
            clean(row[booking_category_col])
            if booking_category_col
            else "Booking"
        )

        item = (
            clean(row[booking_item_col])
            if booking_item_col
            else "Booking"
        )

        provider = (
            clean(row[booking_provider_col])
            if booking_provider_col
            else ""
        )

        status = (
            clean(row[booking_status_col])
            if booking_status_col
            else ""
        )

        priority = (
            clean(row[booking_priority_col])
            if booking_priority_col
            else ""
        )

        notes = (
            clean(row[booking_notes_col])
            if booking_notes_col
            else ""
        )

        booking_url = (
            clean(row[booking_url_col])
            if booking_url_col
            else ""
        )

        start_date = (
            parse_date(row[booking_start_col])
            if booking_start_col
            else pd.NaT
        )

        end_date = (
            parse_date(row[booking_end_col])
            if booking_end_col
            else pd.NaT
        )

        cost = (
            pd.to_numeric(
                row[booking_cost_col],
                errors="coerce"
            )
            if booking_cost_col
            else None
        )

        currency = (
            clean(row[booking_currency_col])
            if booking_currency_col
            else ""
        )

        # -----------------------------
        # ICON
        # -----------------------------

        category_icons = {

            "Accommodation": "🏨",
            "Flight": "✈️",
            "Transport": "🚆",
            "Motor Rental": "🛵",
            "Attraction": "🎟️",

        }

        icon = category_icons.get(
            category,
            "📋"
        )

        # -----------------------------
        # DATE LABEL
        # -----------------------------

        if (
            pd.notna(start_date)
            and pd.notna(end_date)
        ):

            if start_date.date() == end_date.date():

                date_label = (
                    start_date.strftime(
                        "%d %b %Y"
                    )
                )

            else:

                date_label = (
                    start_date.strftime("%d %b")
                    + " – "
                    + end_date.strftime(
                        "%d %b %Y"
                    )
                )

        else:

            date_label = "Date TBD"

        # -----------------------------
        # COST
        # -----------------------------

        if (
            pd.notna(cost)
            and cost > 0
        ):

            cost_label = (
                f"{currency} {cost:,.0f}"
            )

        else:

            cost_label = "TBD"

        # -----------------------------
        # STATUS CLASS
        # -----------------------------

        status_class = (
            status
            .lower()
            .replace(" ", "-")
        )

        priority_class = (
            priority
            .lower()
            .replace(" ", "-")
        )

        # -----------------------------
        # BOOKING CARD
        # -----------------------------

        card_html = f"""
        <div class="booking-card">

            <div class="booking-card-top">

                <div class="booking-icon">
                    {icon}
                </div>

                <div class="booking-status {status_class}">
                    {escape(status.upper())}
                </div>

            </div>

            <div class="booking-category">
                {escape(category)}
            </div>

            <div class="booking-item">
                {escape(item)}
            </div>

            <div class="booking-date">
                📅 {escape(date_label)}
            </div>

            <div class="booking-provider">
                {escape(provider)}
            </div>

            <div class="booking-meta">

                <div>
                    <span>PRIORITY</span>
                    <strong class="{priority_class}">
                        {escape(priority)}
                    </strong>
                </div>

                <div>
                    <span>ESTIMATED</span>
                    <strong>
                        {escape(cost_label)}
                    </strong>
                </div>

            </div>
        """

        if notes:

            card_html += f"""
            <div class="booking-notes">
                {escape(notes)}
            </div>
            """

        if booking_url:

            card_html += f"""

            <a
                href="{escape(booking_url)}"
                target="_blank"
                class="booking-link"
            >
                OPEN BOOKING ↗
            </a>
            """

        card_html += """
        </div>
        """

        st.html(card_html)

# =========================================================
# TRANSPORTS
# =========================================================

st.markdown(
    """
    <div id="transports" class="dashboard-section">
        <div class="section-title">TRANSPORTS</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TRANSPORT COLUMNS
# =========================================================

transport_date_col = find_col(
    transport,
    [
        "date",
        "transport_date",
        "start_date",
    ]
)

transport_origin_col = find_col(
    transport,
    [
        "origin",
        "from",
        "departure",
    ]
)

transport_destination_col = find_col(
    transport,
    [
        "destination",
        "to",
        "arrival",
    ]
)

transport_country_col = find_col(
    transport,
    [
        "country",
    ]
)

transport_mode_col = find_col(
    transport,
    [
        "mode",
        "transport_mode",
        "type",
    ]
)

transport_distance_col = find_col(
    transport,
    [
        "distance_km",
        "distance",
        "km",
    ]
)

transport_duration_col = find_col(
    transport,
    [
        "duration_min",
        "duration",
        "minutes",
    ]
)

transport_estimated_cost_col = find_col(
    transport,
    [
        "estimated_cost",
        "estimated_price",
        "planned_cost",
    ]
)

transport_actual_cost_col = find_col(
    transport,
    [
        "actual_cost",
        "actual_price",
        "paid_cost",
    ]
)

transport_currency_col = find_col(
    transport,
    [
        "currency",
        "currency_code",
    ]
)

transport_notes_col = find_col(
    transport,
    [
        "notes",
        "note",
        "description",
    ]
)


# =========================================================
# PREPARE TRANSPORT DATA
# =========================================================

transport_view = transport.copy()

if transport_date_col:
    transport_view["_transport_date"] = (
        transport_view[transport_date_col]
        .apply(parse_date)
    )
else:
    transport_view["_transport_date"] = pd.NaT


transport_view = transport_view.sort_values(
    "_transport_date",
    kind="stable"
)

# =========================================================
# NORMALIZE TRANSPORT MODES
# =========================================================

def normalize_transport_mode(value):
    """
    Canonical transport mode for the dashboard.

    Rules:
    - Grab/Walking -> Grab
    - Walking / Walk -> excluded
    - Motor / Motorbike / Motor Rental -> excluded
    - Other valid modes remain unchanged
    """

    mode = clean(value).strip().lower()

    if not mode:
        return ""

    # Grab + walking is treated as GRAB
    if "grab" in mode:
        return "Grab"

    # Walking is not a transport mode
    if mode in {
        "walking",
        "walk",
        "walking tour",
    }:
        return ""

    # Motor rental belongs to the future Motor Rental section
    if (
        "motor" in mode
        or "motorbike" in mode
        or "motorcycle" in mode
    ):
        return ""

    if mode == "flight":
        return "Flight"

    if mode == "train":
        return "Train"

    if mode == "bus":
        return "Bus"

    if mode == "ferry":
        return "Ferry"

    if mode == "travel":
        return "Travel"

    if mode == "car":
        return "Car"

    if mode == "taxi":
        return "Taxi"

    return clean(value).strip().title()


# Canonical mode used throughout the Transport section
if transport_mode_col:
    transport_view["_mode"] = (
        transport_view[transport_mode_col]
        .apply(normalize_transport_mode)
    )
else:
    transport_view["_mode"] = ""

# Remove walking and motor-rental rows from Transport section
transport_view = transport_view[
    transport_view["_mode"] != ""
].copy()

# =========================================================
# TRANSPORT SUMMARY
# =========================================================

total_transport = len(transport_view)

total_distance = (
    transport_view[transport_distance_col]
    .apply(number)
    .sum()
    if transport_distance_col
    else 0
)

total_duration_min = (
    transport_view[transport_duration_col]
    .apply(number)
    .sum()
    if transport_duration_col
    else 0
)

total_duration_hours = total_duration_min / 60


# Count canonical transport modes
mode_counts = (
    transport_view["_mode"]
    .value_counts()
    if not transport_view.empty
    else pd.Series(dtype=int)
)


# =========================================================
# TRANSPORT KPI
# =========================================================

st.html(
    f"""
    <div class="transport-kpi-grid">

        <div class="kpi-card">
            <div class="kpi-label">
                Journeys
            </div>

            <div class="kpi-value">
                {total_transport}
            </div>

            <div class="kpi-accent"></div>
        </div>


        <div class="kpi-card">
            <div class="kpi-label">
                Distance
            </div>

            <div class="kpi-value">
                {total_distance:,.1f} km
            </div>

            <div class="kpi-accent"></div>
        </div>


        <div class="kpi-card">
            <div class="kpi-label">
                Travel Time
            </div>

            <div class="kpi-value">
                {total_duration_hours:.1f} h
            </div>

            <div class="kpi-accent"></div>
        </div>


        <div class="kpi-card">
            <div class="kpi-label">
                Modes
            </div>

            <div class="kpi-value">
                {len(mode_counts)}
            </div>

            <div class="kpi-accent"></div>
        </div>

    </div>
    """
)

# =========================================================
# TRANSPORT FILTER
# =========================================================

# Keep dashboard order instead of alphabetical order
TRANSPORT_MODE_ORDER = [
    "Bus",
    "Ferry",
    "Flight",
    "Grab",
    "Train",
    "Travel",
]

transport_modes = (
    ["ALL"] +
    [
        mode
        for mode in TRANSPORT_MODE_ORDER
        if mode in mode_counts.index
    ]
)

# Extra spacing between KPI cards and filter
st.markdown(
    '<div style="height:28px;"></div>',
    unsafe_allow_html=True
)

selected_transport_mode = st.selectbox(
    "Filter transport",
    transport_modes,
    format_func=lambda x:
        "All Modes" if x == "ALL" else x.upper(),
    label_visibility="collapsed",
    key="transport_mode_filter"
)

if selected_transport_mode != "ALL":
    transport_view = transport_view[
        transport_view["_mode"]
        == selected_transport_mode
    ].copy()

# =========================================================
# TRANSPORT CARDS
# =========================================================

if transport_view.empty:

    st.html(
        """
        <div class="transport-empty">
            <div style="font-size:28px;">🚆</div>
            <div style="
                font-size:15px;
                font-weight:700;
                margin-top:8px;
            ">
                No transport found
            </div>
        </div>
        """
    )

else:

    for _, row in transport_view.iterrows():

        date_value = (
            row["_transport_date"]
            if pd.notna(row["_transport_date"])
            else None
        )

        if date_value is not None:
            date_label = date_value.strftime(
                "%a, %d %b %Y"
            )
        else:
            date_label = "Undated"


        origin = (
            clean(row[transport_origin_col])
            if transport_origin_col
            else ""
        )

        destination = (
            clean(row[transport_destination_col])
            if transport_destination_col
            else ""
        )

        mode = (
            clean(row["_mode"])
            if row.get("_mode", "")
            else "Transport"
        )

        country = (
            clean(row[transport_country_col])
            if transport_country_col
            else ""
        )

        distance = (
            number(row[transport_distance_col])
            if transport_distance_col
            else 0
        )

        duration_min = (
            number(row[transport_duration_col])
            if transport_duration_col
            else 0
        )

        estimated_cost = (
            number(row[transport_estimated_cost_col])
            if transport_estimated_cost_col
            else 0
        )

        actual_cost = (
            number(row[transport_actual_cost_col])
            if transport_actual_cost_col
            else 0
        )

        currency = (
            clean(row[transport_currency_col]).upper()
            if transport_currency_col
            else ""
        )

        notes = (
            clean(row[transport_notes_col])
            if transport_notes_col
            else ""
        )


        # ---------------------------------------------
        # MODE ICON
        # ---------------------------------------------

        mode_icons = {
            "flight": "✈️",
            "train": "🚆",
            "bus": "🚌",
            "ferry": "⛴️",
            "grab": "🚕",
            "travel": "🚗",
        }

        icon = mode_icons.get(
            mode.lower(),
            "🚆"
        )


        # ---------------------------------------------
        # DURATION
        # ---------------------------------------------

        if duration_min > 0:

            duration_h = int(duration_min // 60)
            duration_m = int(duration_min % 60)

            if duration_h > 0 and duration_m > 0:
                duration_label = (
                    f"{duration_h}h {duration_m}m"
                )
            elif duration_h > 0:
                duration_label = (
                    f"{duration_h}h"
                )
            else:
                duration_label = (
                    f"{duration_m}m"
                )

        else:
            duration_label = "—"


        # ---------------------------------------------
        # COST
        # ---------------------------------------------

        cost = (
            actual_cost
            if actual_cost > 0
            else estimated_cost
        )

        if cost > 0:

            if currency == "IDR":
                cost_label = (
                    f"Rp {rupiah(cost)}"
                )
            else:
                cost_label = (
                    f"{currency} {cost:,.0f}"
                )

        else:
            cost_label = "—"


        # ---------------------------------------------
        # HTML
        # ---------------------------------------------

        card_html = (
            '<div class="transport-card">'

            '<div class="transport-date">'
            + escape(date_label)
            + '</div>'

            '<div class="transport-route">'

            '<div class="transport-location">'
            + escape(origin or "—")
            + '</div>'

            '<div class="transport-arrow">'
            '→'
            '</div>'

            '<div class="transport-location transport-destination">'
            + escape(destination or "—")
            + '</div>'

            '</div>'

            '<div class="transport-meta">'

            '<div class="transport-badge">'
            + icon + ' '
            + escape(mode)
            + '</div>'

            '<div class="transport-badge">'
            '⏱️ '
            + escape(duration_label)
            + '</div>'

            '<div class="transport-badge">'
            '📏 '
            + f"{distance:,.1f} km"
            + '</div>'

            '<div class="transport-badge transport-cost">'
            '💰 '
            + escape(cost_label)
            + '</div>'

            '</div>'
        )


        if country:
            card_html += (
                '<div class="transport-note">'
                '🌏 '
                + escape(country)
                + '</div>'
            )


        if notes:
            card_html += (
                '<div class="transport-note">'
                + escape(notes)
                + '</div>'
            )


        card_html += '</div>'

        st.html(card_html)

# =========================================================
# MOTOR RENTAL
# =========================================================

st.markdown(
    """
    <div id="motor-rental" class="dashboard-section">
        <div class="section-title">MOTOR RENTAL</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MOTOR RENTAL COLUMNS
# =========================================================

rental_id_col = find_col(
    motor_rentals,
    ["rental_id"]
)

rental_city_col = find_col(
    motor_rentals,
    ["city"]
)

rental_name_col = find_col(
    motor_rentals,
    [
        "rental_name",
        "name"
    ]
)

rental_address_col = find_col(
    motor_rentals,
    ["address"]
)

rental_whatsapp_col = find_col(
    motor_rentals,
    ["whatsapp"]
)

rental_price_col = find_col(
    motor_rentals,
    [
        "price_per_day",
        "daily_price"
    ]
)

rental_deposit_col = find_col(
    motor_rentals,
    ["deposit"]
)

rental_currency_col = find_col(
    motor_rentals,
    ["currency"]
)

rental_motor_type_col = find_col(
    motor_rentals,
    [
        "motor_type",
        "motor"
    ]
)

rental_opening_col = find_col(
    motor_rentals,
    [
        "opening_hours",
        "opening_time"
    ]
)

rental_closing_col = find_col(
    motor_rentals,
    [
        "closing_hours",
        "closing_time"
    ]
)

rental_maps_col = find_col(
    motor_rentals,
    [
        "maps_url",
        "google_maps",
        "google_maps_url"
    ]
)

rental_notes_col = find_col(
    motor_rentals,
    [
        "notes",
        "note"
    ]
)


# =========================================================
# CITY FILTER
# =========================================================

if (
    not motor_rentals.empty
    and rental_city_col
):

    rental_cities = (
        motor_rentals[rental_city_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    rental_cities = sorted(
        [
            city
            for city in rental_cities.unique()
            if city
        ]
    )

else:
    rental_cities = []


rental_city_options = (
    ["ALL"] + rental_cities
)


selected_rental_city = st.selectbox(
    "Filter motor rental",
    rental_city_options,
    format_func=lambda x:
        "All Cities"
        if x == "ALL"
        else x.upper(),
    label_visibility="collapsed",
    key="motor_rental_city_filter"
)


# =========================================================
# FILTER RENTALS
# =========================================================

rental_view = motor_rentals.copy()

if (
    selected_rental_city != "ALL"
    and rental_city_col
):

    rental_view = rental_view[
        rental_view[rental_city_col]
        .astype(str)
        .str.strip()
        == selected_rental_city
    ].copy()


# =========================================================
# EMPTY STATE
# =========================================================

if rental_view.empty:

    st.html(
        """
        <div class="rental-empty">
            No motor rental information available.
        </div>
        """
    )


else:

    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    sort_columns = []

    if rental_city_col:
        sort_columns.append(
            rental_city_col
        )

    if rental_name_col:
        sort_columns.append(
            rental_name_col
        )

    if sort_columns:

        rental_view = rental_view.sort_values(
            sort_columns,
            kind="stable"
        )


    # -----------------------------------------------------
    # CITY GROUPING
    # -----------------------------------------------------

    current_rental_city = None


    for _, row in rental_view.iterrows():

        city = (
            clean(row[rental_city_col])
            if rental_city_col
            else ""
        )


        # -------------------------------------------------
        # CITY HEADER
        # -------------------------------------------------

        if city != current_rental_city:

            current_rental_city = city

            st.html(
                f"""
                <div class="rental-city">
                    {escape(city.upper())}
                </div>
                """
            )


        # -------------------------------------------------
        # BASIC DATA
        # -------------------------------------------------

        rental_name = (
            clean(row[rental_name_col])
            if rental_name_col
            else "Motor Rental"
        )

        address = (
            clean(row[rental_address_col])
            if rental_address_col
            else ""
        )

        whatsapp = (
            clean(row[rental_whatsapp_col])
            if rental_whatsapp_col
            else ""
        )

        price = (
            clean(row[rental_price_col])
            if rental_price_col
            else ""
        )

        deposit = (
            clean(row[rental_deposit_col])
            if rental_deposit_col
            else ""
        )

        currency = (
            clean(row[rental_currency_col])
            if rental_currency_col
            else ""
        )

        motor_type = (
            clean(row[rental_motor_type_col])
            if rental_motor_type_col
            else ""
        )

        opening = (
            clean(row[rental_opening_col])
            if rental_opening_col
            else ""
        )

        closing = (
            clean(row[rental_closing_col])
            if rental_closing_col
            else ""
        )

        maps_url = (
            clean(row[rental_maps_col])
            if rental_maps_col
            else ""
        )

        notes = (
            clean(row[rental_notes_col])
            if rental_notes_col
            else ""
        )


        # -------------------------------------------------
        # PRICE
        # -------------------------------------------------

        price_html = ""

        if price:

            price_html = f"""
            <div class="rental-info-item">
                <div class="rental-info-label">
                    PRICE
                </div>

                <div class="rental-info-value rental-price">
                    {escape(currency)} {escape(price)}
                    <span>/ day</span>
                </div>
            </div>
            """


        # -------------------------------------------------
        # DEPOSIT
        # -------------------------------------------------

        deposit_html = ""

        if deposit:

            deposit_html = f"""
            <div class="rental-info-item">
                <div class="rental-info-label">
                    DEPOSIT
                </div>

                <div class="rental-info-value">
                    {escape(currency)} {escape(deposit)}
                </div>
            </div>
            """


        # -------------------------------------------------
        # MOTOR TYPE
        # -------------------------------------------------

        motor_html = ""

        if motor_type:

            motor_html = f"""
            <div class="rental-info-item">
                <div class="rental-info-label">
                    MOTOR
                </div>

                <div class="rental-info-value">
                    🛵 {escape(motor_type)}
                </div>
            </div>
            """


        # -------------------------------------------------
        # OPENING HOURS
        # -------------------------------------------------

        hours_html = ""

        if opening or closing:

            if opening and closing:
                hours = (
                    f"{escape(opening)} – "
                    f"{escape(closing)}"
                )

            elif opening:
                hours = escape(opening)

            else:
                hours = escape(closing)

            hours_html = f"""
            <div class="rental-info-item">
                <div class="rental-info-label">
                    HOURS
                </div>

                <div class="rental-info-value">
                    🕐 {hours}
                </div>
            </div>
            """


        # -------------------------------------------------
        # NOTES
        # -------------------------------------------------

        notes_html = ""

        if notes:

            notes_html = f"""
            <div class="rental-notes">
                {escape(notes)}
            </div>
            """


        # -------------------------------------------------
        # WHATSAPP
        # -------------------------------------------------

        whatsapp_html = ""

        if whatsapp:

            whatsapp_clean = (
                whatsapp
                .replace("+", "")
                .replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )

            whatsapp_url = (
                f"https://wa.me/{whatsapp_clean}"
            )

            whatsapp_html = f"""
            <a
                href="{escape(whatsapp_url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="rental-action whatsapp"
            >
                💬 WHATSAPP
            </a>
            """


        # -------------------------------------------------
        # GOOGLE MAPS
        # -------------------------------------------------

        maps_html = ""

        if maps_url:

            maps_html = f"""
            <a
                href="{escape(maps_url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="rental-action maps"
            >
                📍 GOOGLE MAPS
            </a>
            """


        # -------------------------------------------------
        # CARD
        # -------------------------------------------------

        st.html(
            f"""
            <div class="rental-card">

                <div class="rental-header">

                    <div class="rental-name">
                        🛵 {escape(rental_name)}
                    </div>

                </div>


                <div class="rental-address">

                    <span class="rental-icon">
                        📍
                    </span>

                    <span>
                        {escape(address)}
                    </span>

                </div>


                <div class="rental-info-grid">

                    {price_html}

                    {deposit_html}

                    {motor_html}

                    {hours_html}

                </div>


                {notes_html}


                <div class="rental-actions">

                    {maps_html}

                    {whatsapp_html}

                </div>

            </div>
            """
        )

# FOOTER
# =========================================================

st.markdown(
    """
<div style="
    text-align:center;
    color:#8193A8;
    font-size:12px;
    padding:35px 0 10px 0;
">
    RYANOMAD
</div>
""",
    unsafe_allow_html=True
)