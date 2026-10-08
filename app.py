import streamlit as st
from datetime import datetime
import pandas as pd
import html

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Milk Tea POS",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    /* Nền */
    .stApp {
        background-color: #fff7fa;
    }

    /* Tiêu đề */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #d63384;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    /* Card */
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #f0dce5;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }

    /* Tổng tiền */
    .total-price {
        font-size: 30px;
        font-weight: 800;
        color: #d63384;
    }

    /* Bill */
    .bill {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #ddd;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }

    .bill-title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: #d63384;
    }

    .bill-center {
        text-align: center;
    }

    .bill-total {
        text-align: right;
        font-size: 25px;
        font-weight: bold;
        color: #d63384;
    }

    /* Button */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. DỮ LIỆU MENU
# =========================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa caramel": 35000,
    "Trà sữa trân châu đường đen": 38000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Matcha đá xay": 40000,
    "Socola đá xay": 40000
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding": 7000,
    "Kem cheese": 10000,
    "Trân châu hoàng kim": 7000,
    "Thạch phô mai": 7000
}

SUGAR_LEVEL = [
    "100% đường",
    "70% đường",
    "50% đường",
    "30% đường",
    "0% đường"
]

ICE_LEVEL = [
    "100% đá",
    "70% đá",
    "50% đá",
    "30% đá",
    "Không đá"
]


# =========================================================
# 4. SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "bill_number" not in st.session_state:
    st.session_state.bill_number = ""

if "payment_time" not in st.session_state:
    st.session_state.payment_time = None


# =========================================================
# 5. HÀM TIỆN ÍCH
# =========================================================

def money(value):
    return f"{value:,.0f} VNĐ"


def calculate_unit_price(drink, size, topping):
    return (
        MENU[drink]
        + SIZE_PRICE[size]
        + TOPPING_PRICE[topping]
    )


def calculate_total():
    return sum(
        item["total"]
        for item in st.session_state.cart
    )


def add_to_cart(
    drink,
    size,
    topping,
    sugar,
    ice,
    quantity
):

    unit_price = calculate_unit_price(
        drink,
        size,
        topping
    )

    total = unit_price * quantity

    item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": total
    }

    st.session_state.cart.append(item)


# =========================================================
# 6. TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">🧋 MILK TEA POS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'HỆ THỐNG TÍNH TIỀN & QUẢN LÝ HÓA ĐƠN TRÀ SỮA'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 7. THÔNG TIN KHÁCH HÀNG
# =========================================================

st.markdown("## 👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Ví dụ: Nguyễn Hoàng Anh",
    disabled=st.session_state.paid
)


# =========================================================
# 8. CHỌN MÓN
# =========================================================

st.markdown("## 🧋 Thêm món vào hóa đơn")

col1, col2, col3 = st.columns([2.2, 1, 1])

with col1:
    drink = st.selectbox(
        "Loại trà sữa",
        list(MENU.keys()),
        disabled=st.session_state.paid
    )

with col2:
    size = st.selectbox(
        "Size",
        list(SIZE_PRICE.keys()),
        disabled=st.session_state.paid
    )

with col3:
    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1,
        disabled=st.session_state.paid
    )


col4, col5, col6 = st.columns(3)

with col4:
    topping = st.selectbox(
        "Loại topping",
        list(TOPPING_PRICE.keys()),
        disabled=st.session_state.paid
    )

with col5:
    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVEL,
        disabled=st.session_state.paid
    )

with col6:
    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVEL,
        disabled=st.session_state.paid
    )


# =========================================================
# 9. HIỂN THỊ GIÁ MÓN
# =========================================================

unit_price = calculate_unit_price(
    drink,
    size,
    topping
)

st.info(
    f"💰 Đơn giá: **{money(unit_price)}**  |  "
    f"Thành tiền: **{money(unit_price * quantity)}**"
)


# =========================================================
# 10. NÚT THÊM MÓN
# =========================================================

if not st.session_state.paid:

    if st.button(
        "➕ THÊM MÓN",
        use_container_width=True
    ):

        add_to_cart(
            drink,
            size,
            topping,
            sugar,
            ice,
            quantity
        )

        st.success(
            f"Đã thêm {quantity} × {drink} vào hóa đơn!"
        )

        st.rerun()


# =========================================================
# 11. GIỎ HÀNG
# =========================================================

st.markdown("## 🛒 Danh sách món")

if len(st.session_state.cart) == 0:

    st.warning(
        "Hóa đơn đang trống. "
        "Hãy chọn món và bấm 'THÊM MÓN'."
    )

else:

    for index, item in enumerate(
        st.session_state.cart
    ):

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(
            [3, 2, 2, 1]
        )

        with c1:

            st.markdown(
                f"### 🧋 {item['drink']}"
            )

            st.write(
                f"Size: **{item['size']}**"
            )

            st.write(
                f"Topping: **{item['topping']}**"
            )

            st.write(
                f"Đường: **{item['sugar']}**"
            )

            st.write(
                f"Đá: **{item['ice']}**"
            )

        with c2:

            st.write(
                f"Số lượng: **{item['quantity']}**"
            )

            st.write(
                f"Đơn giá: **{money(item['unit_price'])}**"
            )

        with c3:

            st.write("Thành tiền")

            st.markdown(
                f'<div class="total-price">'
                f'{money(item["total"])}'
                f'</div>',
                unsafe_allow_html=True
            )

        with c4:

            if not st.session_state.paid:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                ):

                    st.session_state.cart.pop(index)

                    st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# 12. TỔNG TIỀN
# =========================================================

if len(st.session_state.cart) > 0:

    total_items = sum(
        item["quantity"]
        for item in st.session_state.cart
    )

    subtotal = calculate_total()

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Số loại nước",
            len(st.session_state.cart)
        )

    with c2:
        st.metric(
            "Tổng số ly",
            total_items
        )

    with c3:
        st.metric(
            "Tổng tiền",
            money(subtotal)
        )


# =========================================================
# 13. THANH TOÁN
# =========================================================

st.divider()

st.markdown("## 💳 Thanh toán")

if not st.session_state.paid:

    if len(st.session_state.cart) == 0:

        st.button(
            "💳 THANH TOÁN",
            disabled=True,
            use_container_width=True
        )

    else:

        if st.button(
            "💳 THANH TOÁN",
            use_container_width=True
        ):

            st.session_state.paid = True

            st.session_state.payment_time = datetime.now()

            st.session_state.bill_number = (
                "HD"
                + st.session_state.payment_time.strftime(
                    "%Y%m%d%H%M%S"
                )
            )

            st.rerun()


# =========================================================
# 14. TẠO HÓA ĐƠN
# =========================================================

if (
    st.session_state.paid
    and len(st.session_state.cart) > 0
):

    payment_time = (
        st.session_state.payment_time
    )

    bill_number = (
        st.session_state.bill_number
    )

    customer = (
        customer_name.strip()
        if customer_name.strip()
        else "Khách lẻ"
    )

    subtotal = calculate_total()

    st.divider()

    st.markdown("## 🧾 HÓA ĐƠN THANH TOÁN")

    # =====================================================
    # HTML BILL
    # =====================================================

    bill_html = f"""
    <div class="bill">

        <div class="bill-title">
            🧋 MILK TEA SHOP
        </div>

        <div class="bill-center">
            <b>HÓA ĐƠN THANH TOÁN</b>
        </div>

        <hr>

        <b>Mã hóa đơn:</b> {html.escape(bill_number)}<br>
        <b>Khách hàng:</b> {html.escape(customer)}<br>
        <b>Thời gian:</b>
        {payment_time.strftime("%d/%m/%Y %H:%M:%S")}

        <hr>
    """

    for i, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        bill_html += f"""
        <p>
            <b>{i}. {html.escape(item["drink"])}</b><br>

            Size: {html.escape(item["size"])}<br>

            Topping:
            {html.escape(item["topping"])}<br>

            Đường:
            {html.escape(item["sugar"])}<br>

            Đá:
            {html.escape(item["ice"])}<br>

            Số lượng:
            {item["quantity"]}<br>

            Đơn giá:
            {money(item["unit_price"])}<br>

            Thành tiền:
            <b>{money(item["total"])}</b>
        </p>

        <hr>
        """

    bill_html += f"""
        <div class="bill-total">
            TỔNG CỘNG: {money(subtotal)}
        </div>

        <br>

        <div class="bill-center">
            ❤️ Cảm ơn quý khách!
        </div>

    </div>
    """

    st.markdown(
        bill_html,
        unsafe_allow_html=True
    )


    # =====================================================
    # 15. TẠO FILE TXT
    # =====================================================

    bill_text = ""

    bill_text += "=" * 55 + "\n"
    bill_text += "                 MILK TEA SHOP\n"
    bill_text += "                 HÓA ĐƠN THANH TOÁN\n"
    bill_text += "=" * 55 + "\n\n"

    bill_text += f"Mã hóa đơn: {bill_number}\n"
    bill_text += f"Khách hàng: {customer}\n"
    bill_text += (
        "Thời gian: "
        + payment_time.strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        + "\n"
    )

    bill_text += "\n"
    bill_text += "-" * 55 + "\n"

    for i, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        bill_text += (
            f"{i}. {item['drink']}\n"
        )

        bill_text += (
            f"   Size: {item['size']}\n"
        )

        bill_text += (
            f"   Topping: {item['topping']}\n"
        )

        bill_text += (
            f"   Đường: {item['sugar']}\n"
        )

        bill_text += (
            f"   Đá: {item['ice']}\n"
        )

        bill_text += (
            f"   Số lượng: {item['quantity']}\n"
        )

        bill_text += (
            f"   Đơn giá: "
            f"{money(item['unit_price'])}\n"
        )

        bill_text += (
            f"   Thành tiền: "
            f"{money(item['total'])}\n"
        )

        bill_text += "\n"

    bill_text += "-" * 55 + "\n"

    bill_text += (
        f"TỔNG CỘNG: {money(subtotal)}\n"
    )

    bill_text += "=" * 55 + "\n"
    bill_text += "             CẢM ƠN QUÝ KHÁCH!\n"
    bill_text += "=" * 55


    # =====================================================
    # 16. TẠO FILE CSV
    # =====================================================

    csv_rows = []

    for item in st.session_state.cart:

        csv_rows.append({
            "Món": item["drink"],
            "Size": item["size"],
            "Topping": item["topping"],
            "Mức độ đường": item["sugar"],
            "Mức độ đá": item["ice"],
            "Số lượng": item["quantity"],
            "Đơn giá": item["unit_price"],
            "Thành tiền": item["total"]
        })

    df = pd.DataFrame(csv_rows)

    csv_file = df.to_csv(
        index=False
    ).encode("utf-8-sig")


    # =====================================================
    # 17. NÚT XUẤT HÓA ĐƠN
    # =====================================================

    st.markdown("### 📥 Xuất hóa đơn")

    c1, c2 = st.columns(2)

    with c1:

        st.download_button(
            label="📄 TẢI HÓA ĐƠN",
            data=bill_text.encode("utf-8"),
            file_name=f"{bill_number}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with c2:

        st.download_button(
            label="📊 TẢI CHI TIẾT CSV",
            data=csv_file,
            file_name=f"{bill_number}.csv",
            mime="text/csv",
            use_container_width=True
        )


    # =====================================================
    # 18. TẠO HÓA ĐƠN MỚI
    # =====================================================

    st.divider()

    if st.button(
        "🔄 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.bill_number = ""
        st.session_state.payment_time = None

        st.rerun()


# =========================================================
# 19. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#999;">
        🧋 Milk Tea POS • Quản lý hóa đơn trà sữa
    </div>
    """,
    unsafe_allow_html=True
)
