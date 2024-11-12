import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1 , col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Most Busy Users
        if selected_user == "overall":
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df, width=500)

        #wordcloud
        #df_wc = helper.create_wordcloud(selected_user,df)
        #fig,ax = plt.subplots()
        #ax.imshow(df_wc)
        #st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        #st.dataframe(most_common_df)

        #emoji
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Most Used Emojis")
        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df,width = 500 , height = 450)

        with col2:
            fig, ax = plt.subplots(figsize=(3, 3))  # 3 inches wide by 3 inches high

            # Use .head(5) to get the top 5 emojis and their counts
            ax.pie(emoji_df['count'].head(5), labels=emoji_df['emoji'].head(5),
                   textprops={'fontsize': 8, 'fontname': 'Segoe UI Emoji'}, autopct="%0.2f%%")

            ax.set_title('Top 5 Emojis')

            st.pyplot(fig)


