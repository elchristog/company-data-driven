

hashed_passwords = stauth.Hasher(['abc']).generate()
            st.text(hashed_passwords)