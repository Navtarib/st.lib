
import streamlit as st
import pandas as pd

st.title("Personal Library Manager")

if 'books_df' not in st.session_state:
    st.session_state.books_df = pd.DataFrame(columns=["Title", "Author", "Genre", "Status", "Rating", "Image", "Publication Year"])

def add_book(title, author, genre, status, rating, image, pub_year):
    new_book = pd.DataFrame([[title, author, genre, status, rating, image, pub_year]], columns=["Title", "Author", "Genre", "Status", "Rating", "Image", "Publication Year"])
    st.session_state.books_df = pd.concat([st.session_state.books_df, new_book], ignore_index=True)

def remove_book(title):
    st.session_state.books_df = st.session_state.books_df[st.session_state.books_df["Title"] != title]

def edit_book(old_title, new_title, new_author, new_genre, new_status, new_rating, new_image, new_pub_year):
    st.session_state.books_df.loc[st.session_state.books_df["Title"] == old_title, ["Title", "Author", "Genre", "Status", "Rating", "Image", "Publication Year"]] = [new_title, new_author, new_genre, new_status, new_rating, new_image, new_pub_year]

def display_books(books_df):
    if books_df.empty:
        st.write("Your library is empty!")
    else:
        for index, row in books_df.iterrows():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Title:** {row['Title']}")
                st.write(f"**Author:** {row['Author']}")
                st.write(f"**Genre:** {row['Genre']}")
                st.write(f"**Status:** {row['Status']}")
                st.write(f"**Rating:** {get_star_rating(row['Rating'])}")
                st.write(f"**Publication Year:** {row['Publication Year']}")
            with col2:
                if row['Image']:
                    st.image(row['Image'], width=150)
            st.write("-" * 50)

def get_star_rating(rating):
    full_stars = "⭐" * rating
    empty_stars = "☆" * (5 - rating)
    return full_stars + empty_stars

st.sidebar.title("Library Actions")
action = st.sidebar.radio("Choose an action:", [
    "View Library",
    "Add Book",
    "Remove Book",
    "Edit Book",
    "Search Library",
    "Display Statistics",
    "Exit Application"
])

if action == "View Library":
    display_books(st.session_state.books_df)

elif action == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Romance", "Thriller"])
    status = st.selectbox("Status", ["Read", "Currently Reading", "Want to Read"])
    rating = st.slider("Rating", 1, 5)
    pub_year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    image = st.text_input("Image URL (Optional)")

    if st.button("Add Book"):
        if title and author:
            add_book(title, author, genre, status, rating, image, pub_year)
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
        new_pub_year = st.number_input("New Publication Year", min_value=0, max_value=2100, step=1, value=int(book["Publication Year"]))
        new_image = st.text_input("New Image URL", book["Image"])

        if st.button("Update Book"):
            edit_book(old_title, new_title, new_author, new_genre, new_status, new_rating, new_image, new_pub_year)
            st.success(f"Book '{old_title}' updated to '{new_title}'!")
    else:
        st.error("No book found with the title!")

elif action == "Search Library":
    st.subheader("Search for a Book")
    search_term = st.text_input("Enter the book title or author to search:")
    if search_term:
        filtered_books = st.session_state.books_df[
            st.session_state.books_df['Title'].str.contains(search_term, case=False) |
            st.session_state.books_df['Author'].str.contains(search_term, case=False)
        ]
        display_books(filtered_books)
    else:
        display_books(st.session_state.books_df)

elif action == "Display Statistics":
    st.subheader("Library Statistics")
    total_books = len(st.session_state.books_df)
    if total_books > 0:
        read_books = len(st.session_state.books_df[st.session_state.books_df["Status"] == "Read"])
        read_percentage = (read_books / total_books) * 100
        st.write(f"📚 **Total Books:** {total_books}")
        st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
    else:
        st.write("No books in your library yet!")

elif action == "Exit Application":
    st.subheader("📕 Exiting Library Manager")
    st.write("Thank you for using the Personal Library Manager!")
    st.stop()


# ---- Save/Load to/from local storage ----
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Save/Load Library")

# Download button to export current books as CSV
csv = st.session_state.books_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("⬇️ Save Library to File", csv, "library.csv", "text/csv")

# Upload button to load books from CSV
uploaded_file = st.sidebar.file_uploader("⬆️ Load Library from File", type=["csv"])
if uploaded_file is not None:
    st.session_state.books_df = pd.read_csv(uploaded_file)
    st.sidebar.success("Library loaded successfully!")
