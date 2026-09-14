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
            st.write(f"**Sender:** {str(result.iloc[0].get('sender_name', 'N/A'))} ({str(result.iloc[0].get('sender_address', 'N/A'))})")
            st.write(f"**Recipient:** {str(result.iloc[0]['customer_name'])}")
            st.write(f"**Description & Destination:** {str(result.iloc[0]['parcel_details'])}")
            st.write(f"**Dispatch Date:** {str(result.iloc[0]['date_created'])}")
        else:
            st.error("Tracking number not recognized by World Link. Please verify your number.")

# ----------------- ADMIN DASHBOARD (TOTAL FLAT MANAGEMENT) -----------------
if menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        st.markdown("### ➕ Register New Customer Parcel")
        
        # Completely flattened inputs out of form boxes to guarantee no indentation layers
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
            st.session_state["p_sname"] = s_name_in
            st.session_state["p_saddr"] = s_addr_in
            st.rerun()

        if "p_id" in st.session_state:
            st.markdown("### 🧾 Last Generated Tracking Receipt Layout Summary")
            st.write(f"**TRACKING NUMBER:** {st.session_state['p_id']}")
            st.write(f"**SENDER:** {st.session_state['p_sname']} ({st.session_state['p_saddr']})")
            st.write(f"**RECIPIENT:** {st.session_state['p_cname']}")
            st.write(f"**MANIFEST:** {st.session_state['p_info']}")
            st.write(f"**STATUS:** {st.session_state['p_status']}")
            st.write(f"**TIMESTAMP:** {st.session_state['p_time']}")
            if st.button("Clear Receipt Preview"):
                del st.session_state["p_id"]
                st.rerun()

        st.markdown("### 🔄 Update Live Parcel Location Pin & Status")
        all_parcels = fetch_local_data()
        if not all_parcels.empty:
            sel_track = st.selectbox("Select Tracking Number to Update Location/Status", all_parcels["tracking_number"].values)
            sel_row = all_parcels[all_parcels["tracking_number"] == sel_track]
            
            new_status = st.selectbox("Update Status To:", ["Manifest Created / Awaiting Dispatch", "Picked Up by Courier - In Transit to Hub", "Arrived at Distribution Facility Hub", "Out for Delivery with Transit Rider", "Delivered Successfully"])
            
            # Completely flat layout extraction fields
            up_loc_text = st.text_input("Edit Current Location Description", value=str(sel_row.iloc[0].get('current_location_text', 'Main Hub')), key="edit_loc_txt")
            up_lat = st.text_input("Edit Current Pin Latitude", value=str(sel_row.iloc[0]['latitude']), key="edit_lat_val")
            up_lon = st.text_input("Edit Current Pin Longitude", value=str(sel_row.iloc[0]['longitude']), key="edit_lon_val")
            
            if st.button("Commit Status & Location Update"):
                conn = sqlite3.connect("world_link_local.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE parcels SET status = ?, latitude = ?, longitude = ?, current_location_text = ? WHERE tracking_number = ?", (new_status, float(up_lat), float(up_lon), up_loc_text, sel_track))
                conn.commit()
                conn.close()
                st.success("Tracking information updated successfully!")
                st.rerun()
            st.dataframe(all_parcels, use_container_width=True, hide_index=True)
    elif admin_password != "":
        st.error("🔒 Incorrect Admin Password. Access Denied.")
