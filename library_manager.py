import streamlit as st
import pandas as pd

# Set page title
st.title("Personal Library Manager")

# Initialize session state to store library data (persisted across sessions)
if 'books_df' not in st.session_state:
    # Check if books data exists, otherwise create an empty DataFrame
    st.session_state.books_df = pd.DataFrame(columns=["Title", "Author", "Genre", "Status", "Rating", "Image"])

# Function to add a new book
def add_book(title, author, genre, status, rating, image):
    new_book = pd.DataFrame([[title, author, genre, status, rating, image]], columns=["Title", "Author", "Genre", "Status", "Rating", "Image"])
    st.session_state.books_df = pd.concat([st.session_state.books_df, new_book], ignore_index=True)

# Function to remove a book
def remove_book(title):
    st.session_state.books_df = st.session_state.books_df[st.session_state.books_df["Title"] != title]

# Function to edit a book
def edit_book(old_title, new_title, new_author, new_genre, new_status, new_rating, new_image):
    st.session_state.books_df.loc[st.session_state.books_df["Title"] == old_title, ["Title", "Author", "Genre", "Status", "Rating", "Image"]] = [new_title, new_author, new_genre, new_status, new_rating, new_image]

# Function to display books with image on the right side
def display_books(books_df):
    if books_df.empty:
        st.write("Your library is empty!")
    else:
        for index, row in books_df.iterrows():
            # Create columns for the layout
            col1, col2 = st.columns([2, 1])  # 2/3 for details, 1/3 for image

            # Display book details on the left (col1)
            with col1:
                st.write(f"**Title:** {row['Title']}")
                st.write(f"**Author:** {row['Author']}")
                st.write(f"**Genre:** {row['Genre']}")
                st.write(f"**Status:** {row['Status']}")
                st.write(f"**Rating:** {get_star_rating(row['Rating'])}")

            # Display image on the right (col2)
            with col2:
                if row['Image']:
                    st.image(row['Image'], width=150)  # Adjust image width

            st.write("-" * 50)

# Function to get star rating based on numeric rating
def get_star_rating(rating):
    full_stars = "⭐" * rating
    empty_stars = "☆" * (5 - rating)
    return full_stars + empty_stars

# Sidebar for actions
st.sidebar.title("Library Actions")
action = st.sidebar.radio("Choose an action:", ["View Library", "Add Book", "Remove Book", "Edit Book", "Search Library"])

if action == "View Library":
    display_books(st.session_state.books_df)

elif action == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Romance", "Thriller"])
    status = st.selectbox("Status", ["Read", "Currently Reading", "Want to Read"])
    rating = st.slider("Rating", 1, 5)
    image = st.text_input("Image URL (Optional)")

    if st.button("Add Book"):
        if title and author:
            add_book(title, author, genre, status, rating, image)
            st.success(f"Book '{title}' added to your library!")
        else:
            st.error("Please fill in all the fields")

elif action == "Remove Book":
    st.subheader("Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove:")

    if st.button("Remove Book"):
        if title_to_remove:
            remove_book(title_to_remove)
            st.success(f"Book '{title_to_remove}' removed from your library!")
        else:
            st.error("Please enter a book title to remove")

elif action == "Edit Book":
    st.subheader("Edit Book Details")
    old_title = st.text_input("Enter the title of the book to edit:")
    if old_title and old_title in st.session_state.books_df['Title'].values:
        book = st.session_state.books_df[st.session_state.books_df['Title'] == old_title].iloc[0]
        new_title = st.text_input("New Book Title", book["Title"])
        new_author = st.text_input("New Author", book["Author"])
        new_genre = st.selectbox("New Genre", ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Romance", "Thriller"], index=["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Romance", "Thriller"].index(book["Genre"]))
        new_status = st.selectbox("New Status", ["Read", "Currently Reading", "Want to Read"], index=["Read", "Currently Reading", "Want to Read"].index(book["Status"]))
        new_rating = st.slider("New Rating", 1, 5, value=book["Rating"])
        new_image = st.text_input("New Image URL", book["Image"])

        if st.button("Update Book"):
            edit_book(old_title, new_title, new_author, new_genre, new_status, new_rating, new_image)
            st.success(f"Book '{old_title}' updated to '{new_title}'!")
    else:
        st.error("No book found with the title!")

elif action == "Search Library":
    st.subheader("Search for a Book")
    search_term = st.text_input("Enter the book title or author to search:")
    if search_term:
        filtered_books = st.session_state.books_df[st.session_state.books_df['Title'].str.contains(search_term, case=False) | st.session_state.books_df['Author'].str.contains(search_term, case=False)]
        display_books(filtered_books)
    else:
        display_books(st.session_state.books_df)
