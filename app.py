import streamlit as st
import pandas as pd

# Global variables
cart = []

# Load your data
@st.cache_data
def load_data():
    # Load your data into a DataFrame
    # Replace 'data.csv' with the path to your data file
    data = pd.read_csv('NBT.csv')
    return data

# Checkout logic
def checkout(cart):
    st.write("## Checkout")
    
    total_price = sum(item['Price'] for item in cart)
    
    # Clear the page contents
    st.empty()
    
    # Display cart items in a new page
    with st.expander("Cart Details"):
        st.write("### Cart Items")
        for item in cart:
            st.image(item['Cover_URL'], caption=f"{item['Title']} - ₹{item['Price']}", width=100)
        
        # Display total price
        st.write(f"**Total Price:** ₹{total_price}")


# Create the web store interface
def main():
    if st.sidebar.button('Proceed to Checkout'):
        # Add a link that navigates to the checkout section
        checkout(cart)
    st.title('Book Store')

    # Load the data
    data = load_data()

    # Display filters and cart
    st.sidebar.title('Filters')
    language_filter = st.sidebar.selectbox('Language', ['All'] + data['Language'].unique().tolist())
    price_filter = st.sidebar.slider('Price', data['Price'].min(), data['Price'].max(), (data['Price'].min(), data['Price'].max()))
    age_filter = st.sidebar.selectbox('Age Group', ['All'] + data['AgeGrp'].unique().tolist())

    st.sidebar.title('Cart')
    for item in cart:
        st.sidebar.image(item['Cover_URL'], caption=f"{item['Title']} - ₹{item['Price']}", width=100)

    # Apply filters
    filtered_data = data.copy()
    if language_filter != 'All':
        filtered_data = filtered_data[filtered_data['Language'] == language_filter]
    filtered_data = filtered_data[(filtered_data['Price'] >= price_filter[0]) & (filtered_data['Price'] <= price_filter[1])]
    if age_filter != 'All':
        # Extract numeric part from AgeGrp strings
        age_numeric = age_filter.split('+')[0]
        filtered_data = filtered_data[filtered_data['AgeGrp'].str.extract('(\d+)').astype(float) >= float(age_numeric)]

    # Display book information and add to cart button
    st.subheader('Books')
    for index, row in filtered_data.iterrows():
        st.write(f"**Title:** {row['Title']}")
        st.write(f"**Author:** {row['Author']}")
        st.write(f"**Language:** {row['Language']}")
        st.write(f"**Price:** ₹{row['Price']}")
        st.write(f"**Pages:** {row['Pages']}")
        st.write(f"**Age Group:** {row['AgeGrp']}")
        
        # Add to cart button with a unique key
        button_key = f"add_to_cart_{index}"
        if st.button('Add to Cart', key=button_key):
            cart.append({'Title': row['Title'], 'Price': row['Price'], 'Cover_URL': row['Cover_URL']})

        # Check if the Cover_URL is not NaN
        if not pd.isna(row['Cover_URL']):
            # Convert the Cover_URL to string
            cover_url = str(row['Cover_URL'])
            
            # Display the book cover image
            st.image(cover_url, caption='Book Cover', width=200)
        else:
            st.write("No cover image available")


    

if __name__ == '__main__':
    main()
