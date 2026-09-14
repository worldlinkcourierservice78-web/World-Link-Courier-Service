import streamlit as st
import random
import string
import urllib.parse
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

# --- STREAMLIT UI DESIGN ---
st.set_page_config(page_title="World Link Courier Service", layout="centered", page_icon="📦")
st.title("🌐 World Link Courier Service")
st.markdown("##### *Fast, Reliable, and Secure Global Tracking Portal*")

# READ UNIQUE INCOMING LINK LINK CONFIGURATION
query_params = st.query_params

if "track" in query_params:
    # ----------------- SMART AUTOMATED LINK TRACKING VIEW -----------------
    st.subheader("🔍 Automated Shipment Tracking")
    
    # Decodes incoming variables packed inside the text string links instantly
    t_id = query_params.get("track", "WL-UNKNOWN").upper()
    t_cust = query_params.get("name", "Valued Client")
    t_details = query_params.get("desc", "In Transit")
    t_status = query_params.get("status", "Manifest Created")
    t_loc = query_params.get("loc", "MainSorting Hub")
    t_sname = query_params.get("sname", "World Link Branch")
    t_saddr = query_params.get("saddr", "Logistics Office")
    t_date = query_params.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    st.success("Shipment Located via Cloud Link Link!")
    st.info(f"📍 **Current Location:** {t_loc}")
    st.warning(f"📊 **Delivery Status:** {t_status}")
    
    st.markdown("### 📄 Official Tracking Invoice Receipt")
    receipt_code = build_premium_receipt(t_id, t_cust, t_details, t_date, t_status, t_sname, t_saddr, t_loc)
    st.components.v1.html(receipt_code, height=560, scrolling=True)
    
    if st.button("⬅️ Return to Manual Tracking Portal"):
        st.query_params.clear()
        st.rerun()

else:
    # ----------------- REGULAR DASHBOARD VIEW -----------------
    menu = st.sidebar.radio("Navigation Portal", ["Customer Manual Search", "Admin Dashboard Portal"])

    if menu == "Customer Manual Search":
        st.subheader("🔍 Track Your Shipment")
        search_id = st.text_input("Enter your tracking number (e.g., WL-XXXXXX):").strip().upper()
        st.info("💡 Note: To avoid database lag, use the smart direct link generated by your admin agent to view live updates instantly.")
        if st.button("Search System Memory"):
            st.error("Manual local cache cleared. Please contact World Link Dispatch to receive your package's active Live tracking link link.")

    elif menu == "Admin Dashboard Portal":
        st.sidebar.markdown("---")
        admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
        if admin_password == "Mbappe7979":
            st.subheader("🛠️ World Link Operations Dashboard")
            st.markdown("### ➕ Register New Customer Parcel")
            
            s_name = st.text_input("Sender Full Name")
            s_addr = st.text_input("Sender Address / Branch")
            c_name = st.text_input("Recipient Full Name")
            p_info = st.text_area("Parcel Details & Destination Address")
            l_text = st.text_input("Current Location Description", value="Main Sorting Hub")
            new_status = st.selectbox("Current Delivery Status:", ["Manifest Created / Awaiting Dispatch", "Picked Up by Courier - In Transit to Hub", "Arrived at Distribution Facility Hub", "Out for Delivery with Transit Rider", "Delivered Successfully"])
            
            if st.button("Generate World Link Tracking Card & Link"):
                if c_name and p_info and s_name:
                    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    generated_id = f"WL-{chars}"
                    c_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    # Generate the smart direct web link parameters safely
                    base_url = "https://streamlit.app"
                    params = {
                        "track": generated_id, "name": c_name, "desc": p_info,
                        "status": new_status, "loc": l_text, "sname": s_name,
                        "saddr": s_addr, "date": c_time
                    }
                    encoded_link = f"{base_url}?{urllib.parse.urlencode(params)}"
                    
                    st.session_state["out_id"] = generated_id
                    st.session_state["out_html"] = build_premium_receipt(generated_id, c_name, p_info, c_time, new_status, s_name, s_addr, l_text)
                    st.session_state["out_link"] = encoded_link
                    st.rerun()
                else:
                    st.warning("Please complete Sender Name, Recipient Name, and Details fields.")

            if "out_id" in st.session_state:
                st.markdown("---")
                st.success(f"📦 Tracking Generated Successfully! Code: {st.session_state['out_id']}")
                
                st.markdown("### 🔗 Smart Client Tracking Link")
                st.info("Copy this exact link below and send it to your customer via WhatsApp or SMS. Clicking it lets them view their live tracking map and invoice instantly!")
                st.code(st.session_state["out_link"])
                
                st.markdown("### 🧾 Official Generated Dispatch Receipt")
                st.components.v1.html(st.session_state["out_html"], height=560, scrolling=True)
                
                if st.button("Clear Dashboard Registration Preview"):
                    del st.session_state["out_id"]
                    st.rerun()
        elif admin_password != "":
            st.error("🔒 Incorrect Admin Password. Access Denied.")
