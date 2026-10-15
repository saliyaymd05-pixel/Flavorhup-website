import streamlit as st
import pandas as pd
from datetime import datetime, date
from food_data import MENU_ITEMS

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="FlavorHub – Modern Restaurant & Online Food Ordering",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM STYLING (THEME & PALETTE)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .font-serif {
        font-family: 'Playfair Display', serif;
    }
    
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        background-color: #DC2626;
        color: white;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #7F1D1D;
        color: white;
    }
    
    .announcement-bar {
        background-color: #7F1D1D;
        color: white;
        padding: 10px;
        text-align: center;
        font-weight: 500;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border: 1px solid #FEE2E2;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'reservations' not in st.session_state:
    st.session_state.reservations = []
if 'reviews' not in st.session_state:
    st.session_state.reviews = [
        {"name": "Rahul Sharma", "rating": 5, "date": "October 12, 2026", "text": "The Butter Chicken and Garlic Naan were exceptionally authentic! The delivery was lightning fast."},
        {"name": "Priya Menon", "rating": 5, "date": "October 10, 2026", "text": "FlavorHub is our family's favorite weekend spot. Their Chocolate Lava Cake is a must-try!"},
        {"name": "David Miller", "rating": 4, "date": "October 05, 2026", "text": "Great vegetarian options! The Paneer Tikka Pizza was full of flavor."}
    ]
if 'user' not in st.session_state:
    st.session_state.user = None
if 'applied_coupon' not in st.session_state:
    st.session_state.applied_coupon = None

menu_df = pd.DataFrame(MENU_ITEMS)

# ==========================================
# SIDEBAR NAVIGATION & CART
# ==========================================
st.sidebar.markdown("## 🍽️ FlavorHub")
st.sidebar.markdown("Fine Dining & Cafe Portal")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation", 
    [
        "Home", "Menu & Order Online", "Combo Builder", "Smart Recommender", 
        "Table Reservations", "About Us", "Gallery", "Reviews", 
        "Offers & Events", "My Profile", "Contact"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛒 Shopping Cart Summary")
cart_subtotal = sum([item['price'] * item['qty'] for item in st.session_state.cart])
cart_count = sum([item['qty'] for item in st.session_state.cart])
st.sidebar.metric("Items in Cart", cart_count, f"₹{cart_subtotal}")

if st.sidebar.button("🛍️ View Cart & Checkout", use_container_width=True):
    page = "Cart & Checkout"

# Top Announcement Bar
st.markdown("""
<div class="announcement-bar">
    🔥 Free Delivery on Orders Over ₹500! Use Coupon Code <strong>FLAVOR10</strong> for 10% Off!
</div>
""", unsafe_allow_html=True)


# ==========================================
# 1. HOME PAGE
# ==========================================
if page == "Home":
    col1, col2 = st.columns([7, 5])
    with col1:
        st.markdown('<span style="background-color: #FEE2E2; color: #DC2626; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 12px;">🏆 FRESHLY PREPARED EVERY DAY</span>', unsafe_allow_html=True)
        st.markdown("# Every Bite Tells a <br><span style='color: #DC2626; font-style: italic;'>Delicious Story.</span>", unsafe_allow_html=True)
        st.write("Discover extraordinary flavors, freshly prepared favorites, and unforgettable dining experiences at FlavorHub.")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Order Now", use_container_width=True):
                st.switch_page = "Menu & Order Online"
        with b2:
            if st.button("Explore Menu", use_container_width=True):
                pass
        with b3:
            if st.button("Book a Table", use_container_width=True):
                pass
                
        st.markdown("---")
        st.markdown("⭐ **4.8 / 5.0** (1,420+ Reviews) | 🚚 Fast 30-Min Delivery")

    with col2:
        st.image("https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&q=80&w=800", use_container_width=True, caption="Signature Gourmet Platter")

    st.markdown("---")
    st.markdown("## Featured Categories")
    cat_cols = st.columns(5)
    categories = ["Starters and Appetizers", "Indian Vegetarian", "Pizza", "Burgers and Sandwiches", "Desserts"]
    icons = ["🍲", "🌱", "🍕", "🍔", "🍨"]
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            st.info(f"{icons[i]} **{cat}**")

    st.markdown("---")
    st.markdown("## Today's Chef Specials")
    specials = menu_df[menu_df['featured'] == True].sample(3)
    spec_cols = st.columns(3)
    for idx, (_, row) in enumerate(specials.iterrows()):
        with spec_cols[idx]:
            st.image(row['image'], use_container_width=True)
            st.markdown(f"#### {row['name']}")
            st.write(row['description'])
            st.markdown(f"**₹{row['price']}**")

# ==========================================
# 2. MENU & ORDER ONLINE
# ==========================================
elif page == "Menu & Order Online":
    st.markdown("## 📜 Masterpiece Menu Marketplace")
    st.write("Browse our selection of 70+ handcrafted culinary items.")

    search_query = st.text_input("🔍 Search dishes (e.g. Biryani, Pizza, Burger)...", "")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_cat = st.selectbox("Category", ["All"] + list(menu_df['category'].unique()))
    with col2:
        sort_by = st.selectbox("Sort By", ["Featured", "Price: Low to High", "Price: High to Low", "Highest Rated"])
    with col3:
        diet_filter = st.selectbox("Dietary", ["All", "Veg", "Non-Veg", "Vegan", "Gluten-Free"])
    with col4:
        max_price = st.slider("Max Price (₹)", 50, 500, 500)

    filtered_df = menu_df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False) | filtered_df['description'].str.contains(search_query, case=False)]
    if selected_cat != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_cat]
    if diet_filter != "All":
        filtered_df = filtered_df[filtered_df['dietary'].apply(lambda x: diet_filter in x)]
    
    filtered_df = filtered_df[filtered_df['price'] <= max_price]

    if sort_by == "Price: Low to High":
        filtered_df = filtered_df.sort_values(by="price", ascending=True)
    elif sort_by == "Price: High to Low":
        filtered_df = filtered_df.sort_values(by="price", ascending=False)
    elif sort_by == "Highest Rated":
        filtered_df = filtered_df.sort_values(by="rating", ascending=False)

    st.markdown(f"**Showing {len(filtered_df)} items**")

    cols = st.columns(3)
    for index, row in filtered_df.reset_index().iterrows():
        col = cols[index % 3]
        with col:
            st.image(row['image'], use_container_width=True)
            st.markdown(f"#### {row['name']}")
            st.caption(f"{row['category']} • ⭐ {row['rating']}")
            st.write(row['description'])
            st.markdown(f"**₹{row['price']}**")
            
            notes = st.text_input(f"Notes for {row['name']}", key=f"note_{row['id']}", placeholder="e.g. Less spicy")
            if st.button("➕ Add to Cart", key=f"add_{row['id']}"):
                existing = next((item for item in st.session_state.cart if item['id'] == row['id'] and item['notes'] == notes), None)
                if existing:
                    existing['qty'] += 1
                else:
                    st.session_state.cart.append({**row.to_dict(), "qty": 1, "notes": notes})
                st.success(f"Added {row['name']} to cart!")
            st.markdown("---")

# ==========================================
# 3. COMBO BUILDER
# ==========================================
elif page == "Combo Builder":
    st.markdown("## 🍔 Custom Combo Meal Builder")
    st.write("Pick your favorite main, side, beverage, and dessert to create a personalized meal at a 15% bundle discount.")

    mains = menu_df[menu_df['category'].isin(['Indian Non-Vegetarian', 'Indian Vegetarian', 'Pizza'])]
    sides = menu_df[menu_df['category'] == 'Starters and Appetizers']
    beverages = menu_df[menu_df['category'] == 'Beverages']
    desserts = menu_df[menu_df['category'] == 'Desserts']

    col1, col2 = st.columns(2)
    with col1:
        selected_main = st.selectbox("1. Select Main Dish", mains['name'].tolist())
        selected_side = st.selectbox("2. Select Side Dish", sides['name'].tolist())
    with col2:
        selected_bev = st.selectbox("3. Select Beverage", beverages['name'].tolist())
        selected_dessert = st.selectbox("4. Select Dessert (Optional)", ["-- No Dessert --"] + desserts['name'].tolist())

    main_item = menu_df[menu_df['name'] == selected_main].iloc[0]
    side_item = menu_df[menu_df['name'] == selected_side].iloc[0]
    bev_item = menu_df[menu_df['name'] == selected_bev].iloc[0]
    
    orig_total = main_item['price'] + side_item['price'] + bev_item['price']
    dessert_item = None
    if selected_dessert != "-- No Dessert --":
        dessert_item = menu_df[menu_df['name'] == selected_dessert].iloc[0]
        orig_total += dessert_item['price']

    discount = int(orig_total * 0.15)
    final_price = orig_total - discount

    st.markdown("---")
    st.markdown("### Your Custom Combo Summary")
    st.write(f"- **Main:** {main_item['name']} (₹{main_item['price']})")
    st.write(f"- **Side:** {side_item['name']} (₹{side_item['price']})")
    st.write(f"- **Beverage:** {bev_item['name']} (₹{bev_item['price']})")
    if dessert_item is not None:
        st.write(f"- **Dessert:** {dessert_item['name']} (₹{dessert_item['price']})")
    
    st.markdown(f"~~Regular Total: ₹{orig_total}~~")
    st.markdown(f"**Bundle Discount (15% OFF): -₹{discount}**")
    st.markdown(f"### **Combo Price: ₹{final_price}**")

    if st.button("🛒 Add Custom Combo to Cart", use_container_width=True):
        combo_name = f"Custom Combo ({main_item['name']} + {side_item['name']} + {bev_item['name']})"
        st.session_state.cart.append({
            "id": 9999 + len(st.session_state.cart),
            "name": combo_name,
            "category": "Custom Combo",
            "price": final_price,
            "image": main_item['image'],
            "qty": 1,
            "notes": "Custom Bundle Meal (15% OFF)"
        })
        st.success("Custom combo successfully added to cart!")

# ==========================================
# 4. SMART RECOMMENDER
# ==========================================
elif page == "Smart Recommender":
    st.markdown("## 🪄 Find Your Perfect Bite")
    st.write("Tell us what you're craving, and our recommendation tool will suggest matching dishes.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rec_diet = st.selectbox("Dietary Preference", ["All", "Veg", "Non-Veg", "Vegan"])
    with col2:
        rec_spice = st.selectbox("Spice Tolerance", ["All", "Mild (0-1)", "Spicy (2-3)"])
    with col3:
        rec_budget = st.selectbox("Maximum Budget", [9999, 199, 300, 500])
    with col4:
        rec_cat = st.selectbox("Meal Category", ["All"] + list(menu_df['category'].unique()))

    if st.button("Get Recommendations"):
        rec_df = menu_df.copy()
        if rec_diet != "All":
            rec_df = rec_df[rec_df['dietary'].apply(lambda x: rec_diet in x)]
        if rec_spice == "Mild (0-1)":
            rec_df = rec_df[rec_df['spice'] <= 1]
        elif rec_spice == "Spicy (2-3)":
            rec_df = rec_df[rec_df['spice'] >= 2]
        rec_df = rec_df[rec_df['price'] <= rec_budget]
        if rec_cat != "All":
            rec_df = rec_df[rec_df['category'] == rec_cat]
            
        rec_df = rec_df.sample(min(3, len(rec_df))) if len(rec_df) > 0 else rec_df
        
        if len(rec_df) == 0:
            st.warning("No dishes match your specific preferences. Try broadening your criteria!")
        else:
            st.markdown("### Top Recommendations For You:")
            for _, row in rec_df.iterrows():
                st.info(f"**{row['name']}** ({row['category']}) - ₹{row['price']} | ⭐ {row['rating']}\n\n_{row['description']}_")

# ==========================================
# 5. TABLE RESERVATIONS
# ==========================================
elif page == "Table Reservations":
    st.markdown("## 📅 Reserve Your Table Online")
    st.write("Experience exceptional dining at FlavorHub. Book a table for family gatherings, romantic dinners, or celebrations.")

    with st.form("reservation_form"):
        col1, col2 = st.columns(2)
        with col1:
            res_name = st.text_input("Full Name *")
            res_email = st.text_input("Email Address *")
            res_phone = st.text_input("Mobile Number *")
        with col2:
            res_guests = st.selectbox("Party Size *", ["1 Person", "2 People (Couple)", "4 People (Family)", "6 People", "8+ People"])
            res_date = st.date_input("Reservation Date *", min_value=date.today())
            res_time = st.selectbox("Time Slot *", ["12:00 PM (Lunch)", "01:30 PM (Lunch)", "07:00 PM (Dinner)", "08:30 PM (Dinner)", "09:45 PM"])
        
        res_seating = st.selectbox("Seating Area Preference", ["Indoor Dining Room (AC)", "Garden Open-Air Patio", "Rooftop View"])
        res_notes = st.text_area("Special Requests (Optional)", placeholder="Anniversary setup, high chair needed...")

        submitted = st.form_submit_button("Confirm Table Reservation")
        if submitted:
            if not res_name or not res_email or not res_phone:
                st.error("Please fill in all required fields.")
            else:
                res_id = f"RES-{int(datetime.now().timestamp())}"
                st.session_state.reservations.append({
                    "id": res_id, "name": res_name, "date": str(res_date), "time": res_time, "guests": res_guests, "seating": res_seating
                })
                st.success(f"Table successfully reserved! Reference ID: **{res_id}**")

# ==========================================
# 6. ABOUT US
# ==========================================
elif page == "About Us":
    st.markdown("## 📖 About FlavorHub")
    st.write("Founded in 2021, FlavorHub started with a simple belief: that extraordinary food brings people together.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800", use_container_width=True)
    with col2:
        st.markdown("### Our Core Values")
        st.write("- **100% Fresh Produce:** Sourced directly from certified local organic farms.")
        st.write("- **Award-Winning Chefs:** Decades of culinary mastery crafting authentic recipes.")
        st.write("- **Uncompromising Hygiene:** Rigorous quality standards and pristine kitchen environments.")

# ==========================================
# 7. GALLERY
# ==========================================
elif page == "Gallery":
    st.markdown("## 📸 Photo Gallery")
    st.write("A visual feast of our signature dishes, cozy ambience, and delightful customer moments.")
    
    gallery_images = [
        "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=800"
    ]
    
    g_cols = st.columns(3)
    for idx, img_url in enumerate(gallery_images):
        with g_cols[idx % 3]:
            st.image(img_url, use_container_width=True)

# ==========================================
# 8. REVIEWS
# ==========================================
elif page == "Reviews":
    st.markdown("## ⭐ Customer Reviews & Ratings")
    
    with st.expander("Write a Review"):
        with st.form("review_form"):
            rev_name = st.text_input("Your Name")
            rev_rating = st.slider("Rating", 1, 5, 5)
            rev_text = st.text_area("Your Review")
            if st.form_submit_button("Submit Review"):
                st.session_state.reviews.insert(0, {
                    "name": rev_name, "rating": rev_rating, "date": datetime.today().strftime('%B %d, %Y'), "text": rev_text
                })
                st.success("Thank you! Your review has been published.")

    for rev in st.session_state.reviews:
        st.markdown(f"**{rev['name']}** - {'⭐' * rev['rating']} ({rev['date']})")
        st.write(f"_{rev['text']}_")
        st.markdown("---")

# ==========================================
# 9. OFFERS & EVENTS
# ==========================================
elif page == "Offers & Events":
    st.markdown("## 🎁 Offers & Promotions")
    st.write("Take advantage of our limited-time combo deals and discount voucher codes.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("### Pizza Party Combo\n\nBuy any 2 Large Pizzas & get Garlic Bread and a 1.5L Beverage free.\n\n**Code: FLAVOR20**")
    with col2:
        st.info("### Welcome Flat ₹50 Off\n\nGet ₹50 discount on your very first online order above ₹300.\n\n**Code: WELCOME50**")
    with col3:
        st.success("### Royal Biryani Fest\n\nSpecial Hyderabadi Dum Biryani family bucket with raita & desserts.\n\n**Code: FLAVOR10**")

# ==========================================
# 10. MY PROFILE
# ==========================================
elif page == "My Profile":
    st.markdown("## 👤 Customer Portal & History")
    
    if st.session_state.user is None:
        with st.form("auth_form"):
            st.markdown("### Login / Register")
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Mobile Number")
            if st.form_submit_button("Continue to Account"):
                st.session_state.user = {"name": name, "email": email, "phone": phone}
                st.success(f"Welcome, {name}!")
                st.rerun()
    else:
        user = st.session_state.user
        st.write(f"**Name:** {user['name']} | **Email:** {user['email']} | **Phone:** {user['phone']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
            
        st.markdown("### Your Past Orders")
        if len(st.session_state.orders) == 0:
            st.info("No orders placed yet.")
        else:
            for ord in st.session_state.orders:
                st.write(f"**Order ID:** {ord['id']} | **Total:** ₹{ord['total']} | **Status:** {ord['status']}")

# ==========================================
# 11. CONTACT
# ==========================================
elif page == "Contact":
    st.markdown("## 📞 Get In Touch")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Location:** Swaraj Round South, Thrissur, Kerala 680001, India")
        st.write("**Phone:** +91 98765 43210")
        st.write("**Email:** support@flavorhub.demo")
        st.write("**Hours:** Mon - Sun: 11:00 AM – 11:00 PM")
    with col2:
        with st.form("contact_form"):
            st.markdown("### Send a Message")
            st.text_input("Your Name")
            st.text_input("Email Address")
            st.text_area("Message")
            if st.form_submit_button("Send Message"):
                st.success("Message sent successfully!")

# ==========================================
# 12. CART & CHECKOUT PAGE
# ==========================================
elif page == "Cart & Checkout":
    st.markdown("## 🛒 Your Shopping Cart & Checkout")
    
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty. Browse our menu to add items.")
    else:
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([4, 2, 1])
            col1.write(f"**{item['name']}** (x{item['qty']})")
            col2.write(f"₹{item['price'] * item['qty']}")
            if col3.button("❌", key=id):
                st.session_state.cart.pop(i)
                st.rerun()

        coupon = st.text_input("Coupon Code", placeholder="FLAVOR10")
        if st.button("Apply Coupon"):
            if coupon in ["FLAVOR10", "WELCOME50", "FLAVOR20"]:
                st.session_state.applied_coupon = coupon
                st.success(f"Coupon {coupon} applied successfully!")
            else:
                st.error("Invalid coupon code.")

        discount = 0
        if st.session_state.applied_coupon == "FLAVOR10":
            discount = int(cart_subtotal * 0.10)
        elif st.session_state.applied_coupon == "WELCOME50":
            discount = 50
        elif st.session_state.applied_coupon == "FLAVOR20":
            discount = int(cart_subtotal * 0.20)

        tax = int(cart_subtotal * 0.05)
        delivery = 0 if cart_subtotal >= 500 or cart_subtotal == 0 else 40
        final_total = max(0, cart_subtotal - discount + tax + delivery)

        st.write(f"Subtotal: ₹{cart_subtotal}")
        if discount > 0:
            st.write(f"Discount: -₹{discount}")
        st.write(f"Taxes (5%): ₹{tax}")
        st.write(f"Delivery: ₹{delivery}")
        st.markdown(f"### **Final Payable Amount: ₹{final_total}**")

        with st.form("checkout_form"):
            st.markdown("### Checkout Details")
            chk_name = st.text_input("Full Name *", value=st.session_state.user['name'] if st.session_state.user else "")
            chk_phone = st.text_input("Mobile Number *", value=st.session_state.user['phone'] if st.session_state.user else "")
            chk_type = st.selectbox("Order Type", ["Home Delivery", "Store Pickup"])
            chk_address = st.text_area("Delivery Address *")
            chk_payment = st.selectbox("Payment Mode", ["Cash on Delivery", "UPI / Google Pay", "Credit/Debit Card"])
            
            if st.form_submit_button("Place Demo Order Now"):
                order_id = f"#FH-{int(datetime.now().timestamp())}"
                st.session_state.orders.insert(0, {
                    "id": order_id, "items": st.session_state.cart, "total": final_total, "status": "Preparing & Confirmed"
                })
                st.session_state.cart = []
                st.success(f"Order placed successfully! Order ID: {order_id}")
