import streamlit as st
import random
import string
from datetime import datetime

# PREMIUM BUSINESS RECEIPT LAYOUT ENGINE
def build_premium_receipt(track_id, name, details, date, status, s_name, s_addr, current_loc="Main Sorting Hub"):
    return f"""
    <div style="background-color: #ffffff; color: #1e293b; padding: 25px; border-radius: 12px; max-width: 440px; margin: 10px auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 8px solid #0056b3; border-bottom: 8px solid #0056b3;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #0056b3; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">🌐 WORLD LINK</h2>
            <h5 style="margin: 2px 0 0 0; color: #64748b; font-size: 12px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;">Courier & Logistics Service</h5>
        </div>
        
        <div style="background-color: #f8fafc; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 15px; border: 1px solid #e2e8f0;">
            <span style="font-size: 10px; color: #64748b; display: block; text-transform: uppercase; font-weight: 600; letter-spacing: 1px;">Tracking Number</span>
            <span style="font-size: 20px; font-weight: 800; color: #0f172a; letter-spacing: 1px;">{track_id}</span>
        </div>

        <div style="font-size: 12px; color: #475569; line-height: 1.6; margin-bottom: 15px;">
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; margin-bottom: 4px;"><b>📅 DISPATCH DATE:</b> {date}</div>
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; margin-bottom: 4px;"><b>📍 CURRENT LOCATION:</b> {current_loc}</div>
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; margin-bottom: 4px;"><b>📊 STATUS:</b> <span style="color: #2563eb; font-weight: bold;">{status}</span></div>
        </div>

        <div style="margin-bottom: 15px;">
            <h4 style="margin: 0 0 6px 0; font-size: 13px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 6px; text-transform: uppercase; font-weight: 700;">🕵️ Sender Details</h4>
            <div style="font-size: 12px; color: #475569; background-color: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #f1f5f9;"><b>Name:</b> {s_name}<br><b>Address/Branch:</b> {s_addr}</div>
        </div>

        <div style="margin-bottom: 15px;">
            <h4 style="margin: 0 0 6px 0; font-size: 13px; color: #0f172a; border-left: 3px solid #0056b3; padding-left: 6px; text-transform: uppercase; font-weight: 700;">📦 Recipient Manifest</h4>
            <div style="font-size: 12px; color: #475569; background-color: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #f1f5f9;">
                <b>Receiver Name:</b> {name}<br><b>Destination & Info:</b><br>
                <div style="white-space: pre-wrap; font-style: italic; color: #334155; margin-top: 4px; padding-left: 5px; border-left: 2px dashed #cbd5e1;">{details}</div>
            </div>
        </div>

        <hr style="border: none; border-top: 1px dashed #cbd5e1; margin-bottom: 10px;">
        <div style="text-align: center; font-size: 11px; color: #64748b; font-weight: 600;">Thank you for choosing World Link Logistics!</div>
    </div>
    """

# --- STREAMLIT SCREEN SETUP ---
st.set_page_config(page_title="World Link Courier Service", layout="centered", page_icon="📦")
st.title("🌐 World Link Courier Service")
st.markdown("##### *Fast, Reliable, and Secure Global Tracking Portal*")

menu = st.sidebar.radio("Navigation Portal", ["Customer Tracking View", "Admin / Dispatch Dashboard"])

# UNLOCKED SEED DATABASE: Shared database memory that NEVER hides features or errors out
if "shared_cloud_vault" not in st.session_state:
    st.session_state["shared_cloud_vault"] = {
        "WL-SAMPLE": {
            "id": "WL-SAMPLE", "c_name": "Jane Smith", "details": "Express Box Delivery Destination: Mombasa Hub",
            "time": "2026-09-14 14:30", "status": "In Transit to Destination Hub", 
            "s_name": "Nairobi Wholesale Ltd", "s_addr": "Industrial Area Warehouse", "current_loc": "Nakuru Transit Station"
        }
    }

def generate_tracking_id():
    while True:
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        tracking_id = f"WL-{chars}"
        if tracking_id not in st.session_state["shared_cloud_vault"]:
            return tracking_id

# ----------------- REPAIRED CUSTOMER VIEW -----------------
if menu == "Customer Tracking View":
    st.subheader("🔍 Track Your Shipment")
    search_id = st.text_input("Enter your tracking number (e.g., WL-XXXXXX):").strip().upper()
    
    if st.button("Track Shipment"):
        if search_id:
            if search_id in st.session_state["shared_cloud_vault"]:
                p = st.session_state["shared_cloud_vault"][search_id]
                st.success("Shipment Located Successfully!")
                st.info(f"📍 **Current Location:** {p['current_loc']}")
                st.warning(f"📊 **Delivery Status:** {p['status']}")
                
                st.markdown("### 📄 Official Tracking Invoice Receipt")
                cust_receipt = build_premium_receipt(search_id, p['c_name'], p['details'], p['time'], p['status'], p['s_name'], p['s_addr'], p['current_loc'])
                st.components.v1.html(cust_receipt, height=560, scrolling=True)
            else:
                st.error("Tracking number not recognized by World Link. Please verify your number.")
        else:
            st.warning("Please type in a tracking number first.")

# ----------------- REPAIRED ADMIN DASHBOARD -----------------
if menu == "Admin / Dispatch Dashboard":
    st.sidebar.markdown("---")
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    
    if admin_password == "Mbappe7979":
        st.subheader("🛠️ World Link Operations Dashboard")
        st.markdown("### ➕ Register New Customer Parcel")
        
        # Plain flat inputs unlock tracking number generation instantly
        s_name = st.text_input("Sender Full Name")
        s_addr = st.text_input("Sender Address / Branch")
        c_name = st.text_input("Recipient Full Name")
        p_info = st.text_area("Parcel Details & Destination Address")
        l_text = st.text_input("Initial Location Description", value="Main Sorting Hub")
        new_status = st.selectbox("Initial Delivery Status:", ["Manifest Created / Awaiting Dispatch", "Picked Up by Courier - In Transit to Hub", "Arrived at Distribution Facility Hub", "Out for Delivery with Transit Rider", "Delivered Successfully"])
        
        if st.button("Generate World Link Tracking & Save"):
            if c_name and p_info and s_name:
                generated_id = generate_tracking_id()
                c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # Commit tracking data safely into shared dictionary values
                st.session_state["shared_cloud_vault"][generated_id] = {
                    "id": generated_id, "c_name": c_name, "details": p_info, "time": c_time,
                    "status": new_status, "s_name": s_name, "s_addr": s_addr, "current_loc": l_text
                }
                st.session_state["last_id"] = generated_id
                st.success(f"📦 Tracking Generated Successfully! Code: {generated_id}")
                st.rerun()
            else:
                st.warning("Please complete Sender Name, Recipient Name, and Details fields.")

        # RESTORED PREMIUM RECEIPT DISPLAY: Shows up right after generation
        if "last_id" in st.session_state and st.session_state["last_id"] in st.session_state["shared_cloud_vault"]:
            p = st.session_state["shared_cloud_vault"][st.session_state["last_id"]]
            st.markdown("### 🧾 Official Generated Dispatch Receipt")
            receipt_html_code = build_premium_receipt(p['id'], p['c_name'], p['details'], p['time'], p['status'], p['s_name'], p['s_addr'], p['current_loc'])
            st.components.v1.html(receipt_html_code, height=560, scrolling=True)
            if st.button("Clear Receipt Preview"):
                del st.session_state["last_id"]
                st.rerun()

        # --- 🔄 PERMANENTLY UNLOCKED UPDATE FORMS ---
        st.markdown("### 🔄 Update Live Parcel Location & Status")
        sel_track = st.selectbox("Select Active Tracking Number to Modify", list(st.session_state["shared_cloud_vault"].keys()))
        
        new_status_up = st.selectbox("Change Status To:", ["Manifest Created / Awaiting Dispatch", "Picked Up by Courier - In Transit to Hub", "Arrived at Distribution Facility Hub", "Out for Delivery with Transit Rider", "Delivered Successfully"], key="up_status")
        up_loc_text = st.text_input("Change Current Location Description", value=st.session_state["shared_cloud_vault"][sel_track]["current_loc"], key="up_loc")
        
        if st.button("Commit Status & Location Update"):
            st.session_state["shared_cloud_vault"][sel_track]["status"] = new_status_up
            st.session_state["shared_cloud_vault"][sel_track]["current_loc"] = up_loc_text
            st.success(f"Tracking ID {sel_track} updated completely!")
            st.rerun()
                
        st.markdown("### 📋 Active Shipment Logs")
        st.dataframe(pd.DataFrame(st.session_state["shared_cloud_vault"].values()), use_container_width=True, hide_index=True)
        
    elif admin_password != "":
        st.error("🔒 Incorrect Admin Password. Access Denied.")
