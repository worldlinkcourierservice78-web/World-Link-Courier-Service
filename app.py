import streamlit as st
import pandas as pd
import random
import string
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect("world_link_local.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS parcels (tracking_number TEXT PRIMARY KEY, customer_name TEXT, parcel_details TEXT, status TEXT, date_created TEXT, latitude REAL, longitude REAL, current_location_text TEXT, sender_name TEXT, sender_address TEXT)")
conn.commit()
conn.close()

def fetch_local_data():
    conn = sqlite3.connect("world_link_local.db")
    df = pd.read_sql_query("SELECT * FROM parcels", conn)
    conn.close()
    return df

def generate_tracking_id():
    df = fetch_local_data()
    existing_ids = df["tracking_number"].values if not df.empty else []
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in existing_ids:
            return tracking_id

# BEAUTIFUL, PROFESSIONALLY DESIGNED HTML RECEIPT LAYOUT
def build_premium_receipt(track_id, name, details, date, status, s_name, s_addr):
    return f"""
    <div style="background-color: #ffffff; color: #1e293b; padding: 30px; border-radius: 12px; max-width: 480px; margin: 20px auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 8px solid #0056b3; border-bottom: 8px solid #0056b3;">
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="margin: 0; color: #0056b3; font-size: 26px; font-weight: 800; letter-spacing: 0.5px;">🌐 WORLD LINK</h2>
            <h5 style="margin: 3px 0 0 0; color: #64748b; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;">Courier & Logistics Service</h5>
            <p style="margin: 8px 0 0 0; font-size: 11px; color: #94a3b8; font-style: italic;">Fast, Reliable & Secure Global Delivery Network</p>
        </div>
        
        <div style="background-color: #f8fafc; padding: 12px; border-radius: 6px; text-align: center; margin-bottom: 20px; border: 1px solid #e2e8f0;">
            <span style="font-size: 11px; color: #64748b; display: block; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Tracking Number</span>
            <span style="font-size: 22px; font-weight: 800; color: #0f172a; letter-spacing: 1px;">{track_id}</span>
        </div>

        <div style="font-size: 13px; color: #475569; line-height: 1.8; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; margin-bottom: 6px;">
                <span style="font-weight: 600; color: #334155;">📅 DISPATCH DATE:</span>
                <span>{date}</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; margin-bottom: 6px;">
                <span style="font-weight: 600; color: #334155;">📊 CURRENT STATUS:</span>
                <span style="color: #2563eb; font-weight: bold;">{status}</span>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <h4 style="margin: 0 0 8px 0; font-size: 14px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 8px; text-transform: uppercase; font-weight: 700;">🕵️ Sender Details</h4>
            <div style="font-size: 13px; color: #475569; background-color: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid #f1f5f9;">
                <b>Name:</b> {s_name}<br>
                <b>Address/Branch:</b> {s_addr}
            </div>
        </div>

        <div style="margin-bottom: 25px;">
            <h4 style="margin: 0 0 8px 0; font-size: 14px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 8px; text-transform: uppercase; font-weight: 700;">📦 Recipient Manifest</h4>
            <div style="font-size: 13px; color: #475569; background-color: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid #f1f5f9;">
                <b>Receiver Name:</b> {name}<br>
                <b>Destination & Info:</b><br>
                <div style="white-space: pre-wrap; font-style: italic; color: #334155; margin-top: 4px; padding-left: 5px; border-left: 2px dashed #cbd5e1;">{details}</div>
            </div>
        </div>

        <hr style="border: none; border-top: 1px dashed #cbd5e1; margin-bottom: 15px;">
        
        <div style="text-align: center; font-size: 11px; color: #64748b; font-weight: 600;">
            Thank you for choosing World Link Logistics!<br>
            <span style="color: #0056b3; font-size: 12px; display: block; margin-top: 4px;">Track live anytime via World Link Portal</span>
        </div>
    </div>
    """

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="World Link Courier Service", layout="centered", page_icon="📦")
st.title("🌐 World Link Courier Service")
st.markdown("##### *Fast, Reliable, and Secure Global Tracking Portal*")

menu = st.sidebar.radio("Navigation Portal", ["Customer Tracking View", "Admin / Dispatch Dashboard"])

# ----------------- CUSTOMER VIEW -----------------
if menu == "Customer Tracking View":
    st.subheader("🔍 Track Your Shipment")
    search_id = st.text_input("Enter your tracking number (e.g., WL-XXXXXX):").strip().upper()
    if st.button("Track Shipment"):
        df = fetch_local_data()
        result = df[df["tracking_number"] == search_id] if not df.empty else pd.DataFrame()
        if not result.empty:
            st.success("Shipment Located!")
            st.info(f"📍 Current Location: {str(result.iloc[0].get('current_location_text', 'Main Hub'))}")
            st.warning(f"📊 Delivery Status: {str(result.iloc[0]['status'])}")
            lat_val = result.iloc[0]['latitude']
            lon_val = result.iloc[0]['longitude']
            if pd.notna(lat_val) and pd.notna(lon_val) and lat_val != 0.0 and lon_val != 0.0:
                st.map(pd.DataFrame({"latitude": [float(lat_val)], "longitude": [float(lon_val)]}), zoom=14)
            
            # Display Premium Receipt view for customer copies
            st.markdown("### 📄 Official Tracking Invoice Receipt")
            premium_html = build_premium_receipt(
                search_id, 
                str(result.iloc[0]['customer_name']), 
                str(result.iloc[0]['parcel_details']), 
                str(result.iloc[0]['date_created']), 
                str(result.iloc[0]['status']),
                str(result.iloc[0].get('sender_name', 'N/A')),
                str(result.iloc[0].get('sender_address', 'N/A'))
            )
            st.components.v1.html(premium_html, height=560, scrolling=True)
        else:
            st.error("Tracking number not recognized by World Link. Please verify your number.")

# ----------------- ADMIN DASHBOARD -----------------
if menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        st.markdown("### ➕ Register New Customer Parcel")
        
        s_name_in = st.text_input("Sender Full Name")
        s_addr_in = st.text_input("Sender Address / Branch")
        c_name_in = st.text_input("Recipient Full Name")
        p_info_in = st.text_area("Parcel Details & Destination Address")
        l_text_in = st.text_input("Initial Location Name", value="Main Sorting Hub")
        lat_in = st.text_input("Initial Latitude", value="-1.2841")
        lon_in = st.text_input("Initial Longitude", value="36.8155")
        
        if st.button("Generate World Link Tracking & Save"):
            new_id = generate_tracking_id()
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            init_status = "Manifest Created / Awaiting Dispatch"
            conn = sqlite3.connect("world_link_local.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO parcels VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_id, c_name_in, p_info_in, init_status, c_time, float(lat_in), float(lon_in), l_text_in, s_name_in, s_addr_in))
            conn.commit()
            conn.close()
            st.success(f"📦 Tracking Generated Successfully! Code: {new_id}")
            st.session_state["p_id"] = new_id
            st.session_state["p_cname"] = c_name_in
            st.session_state["p_info"] = p_info_in
            st.session_state["p_time"] = c_time
            st.session_state["p_status"] = init_status
            st.session_state["p_name"] = s_name_in
            st.session_state["p_addr"] = s_addr_in
            st.rerun()

        if "p_id" in st.session_state:
            st.markdown("### 🧾 Official Generated Dispatch Receipt")
            admin_receipt = build_premium_receipt(
                st.session_state['p_id'],
                st.session_state['p_cname'],
                st.session_state['p_info'],
                st.session_state['p_time'],
                st.session_state['p_status'],
                st.session_state['p_name'],
                st.session_state['p_addr']
            )
            st.components.v1.html(admin_receipt, height=560, scrolling=True)
            st.caption("💡 *To save or print this receipt card, simply right-click inside the box and select **Print**, or take a clean snippet snapshot.*")
            if st.button("Clear Receipt Preview"):
                del st.session_state["p_id"]
                st.rerun()

        st.markdown("### 🔄 Update Live Parcel Location Pin & Status")
        all_parcels = fetch_local_data()
        if not all_parcels.empty:
            sel_track = st.selectbox("Select Tracking Number to Update Location/Status", all_parcels["tracking_number"].values)
            sel_row = all_parcels[all_parcels["tracking_number"] == sel_track]
            
