import streamlit as st
from services.api import get_holdings, add_holding, delete_holding, update_holding, get_stock_symbols

def holdings_page():
    st.title("Your Holdings")

    token = st.session_state.token
    holdings_data = get_holdings(token)

    if not holdings_data or "holdings" not in holdings_data:
        st.write("No holdings data available. Add a new holding below.")
    else:
        # Display Portfolio Summary
        st.subheader("📊 Portfolio Summary")
        portfolio_summary = holdings_data["portfolio_summary"]

        # Use st.metric for Total Profit/Loss and Daily Change
        col1, col2, col3 = st.columns(3)  # Create three columns for side-by-side metrics
        with col1:
            st.metric(label="💰 Total Cost", value=f"${portfolio_summary['total_cost']:.2f}")
        with col2:
            st.metric(label="📈 Current Value", value=f"${portfolio_summary['total_value']:.2f}")
        with col3:
            st.metric(
                label="📈 Total Profit/Loss",
                value=f"${portfolio_summary['total_profit_loss']:.2f}",
                delta=f"{portfolio_summary['total_profit_loss_percentage']:.2f}%",
                delta_color="normal"  # Green for positive, red for negative
    )
        # Display Holdings
        st.subheader("Your Holdings")
        for holding in holdings_data["holdings"]:
            with st.expander(f"{holding['stock_symbol']} - {holding['stock_name']}"):
                # Display holding details
                st.markdown(
                f"""
                    ### {holding['stock_symbol']} - {holding['stock_name']}
                    **Total Cost:** `${holding['total_cost']:.2f}`  
                    **Current Value:** `${holding['market_value']:.2f}`  
                    **Total Shares:** `{holding['total_shares']:.2f}`  
                    **Current Share Price:** `${holding['current_price']:.2f}`  
                    """
                )

                # Use st.metric for Total Profit/Loss and Daily Change
                col1, col2 = st.columns(2)  # Create two columns for side-by-side metrics
                with col1:
                    st.metric(
                        label="📈 Total Profit/Loss",
                        value=f"${holding['total_profit_loss']:.2f}",
                        delta=f"{holding['total_profit_loss_percentage']:.2f}%",
                        delta_color="normal"  # Green for positive, red for negative
                    )
                with col2:
                    st.metric(
                        label="📉 Daily Change",
                        value=f"${holding['daily_profit_loss']:.2f}",
                        delta=f"{holding['daily_profit_loss_percentage']:.2f}%",
                        delta_color="normal"  # Green for positive, red for negative
                    )

                # Display Purchases
                st.markdown("### **Purchases:**")
                for purchase in holding["purchases"]:
                    st.markdown(
                        f"""
                        **💰 Cost:** `${purchase['purchase_cost']:.2f}`  
                        **📊 Shares:** `{purchase['shares']:.2f}`  
                        **📅 Date:** `{purchase['purchase_date']}`
                        """
                    )

                    # Initialize session state for modify mode
                    if f"modify_mode_{purchase['holding_id']}" not in st.session_state:
                        st.session_state[f"modify_mode_{purchase['holding_id']}"] = False

                    # Create a container for Delete and Modify buttons
                    with st.container():
                        # Add Delete and Modify buttons inline
                        delete_clicked = st.button(f"🗑️ Delete", key=f"delete_{purchase['holding_id']}")
                        modify_clicked = st.button(f"✏️ Modify", key=f"modify_{purchase['holding_id']}")

                        # Handle Delete Button
                        if delete_clicked:
                            success = delete_holding(token, purchase["holding_id"])
                            if success:
                                st.success(f"Purchase deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to delete purchase.")

                        # Handle Modify Button
                        if modify_clicked:
                            # Toggle modify mode in session state
                            st.session_state[f"modify_mode_{purchase['holding_id']}"] = True

                        # Check if modify mode is active
                        if st.session_state[f"modify_mode_{purchase['holding_id']}"]:
                            # Show input fields for modification
                            st.write("### Modify Purchase")
                            new_shares = st.number_input(f"Update Shares", value=purchase["shares"], min_value=0.00, step=0.01, key=f"shares_{purchase['holding_id']}")
                            new_purchase_cost = st.number_input(f"Update Purchase Cost", value=purchase["purchase_cost"], min_value=0.00, step=0.01, key=f"cost_{purchase['holding_id']}")
                            new_purchase_date = st.date_input(f"Update Purchase Date", value=purchase["purchase_date"], key=f"date_{purchase['holding_id']}")

                            # Add Save and Cancel buttons
                            save_clicked = st.button(f"💾 Save Changes", key=f"save_{purchase['holding_id']}")
                            cancel_clicked = st.button(f"❌ Cancel", key=f"cancel_{purchase['holding_id']}")

                            if save_clicked:
                                success = update_holding(token, purchase["holding_id"], new_shares, new_purchase_cost, new_purchase_date.isoformat())
                                if success:
                                    st.success(f"Purchase updated successfully!")
                                    st.session_state[f"modify_mode_{purchase['holding_id']}"] = False  # Exit modify mode
                                    st.rerun()
                                else:
                                    st.error(f"Failed to update purchase.")

                            if cancel_clicked:
                                st.info("Modification canceled.")
                                st.session_state[f"modify_mode_{purchase['holding_id']}"] = False  # Exit modify mode
                                st.rerun()

    # Fetch stock symbols for dropdown and store them in session state
    if "stock_symbols" not in st.session_state:
        st.session_state.stock_symbols = get_stock_symbols()
        if not st.session_state.stock_symbols:
            st.error("Failed to fetch stock symbols. Please try again later.")
    
    # Add New Holding Section as Expander
    with st.expander("Add New Holding"):
        st.subheader("Add New Holding")

        # Use stock symbols from session state
        stock_symbols = st.session_state.get("stock_symbols", [])
        if stock_symbols:
            stock_symbol = st.selectbox("Stock Symbol", options=stock_symbols, help="Select or type a stock symbol")
        else:
            st.error("No stock symbols available. Please try again later.")

        shares = st.number_input("Shares", min_value=0.00, step=0.01)
        purchase_cost = st.number_input("Purchase Cost", min_value=0.00, step=0.01)
        purchase_date = st.date_input("Purchase Date")

        if st.button("Add Holding"):
            purchase_date_str = purchase_date.isoformat()
            success = add_holding(token, stock_symbol, shares, purchase_cost, purchase_date_str)
            if success:
                st.success("Holding added successfully!")
                st.rerun()
            else:
                st.error("Failed to add holding. Please try again.")