import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer⚡")
upload_file = st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to:",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics📊")
        c1, c2, c3, c4 = st.columns(4)
        total_messages, total_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        with c1:
            st.header("Total Messages")
            st.title(total_messages)

        with c2:
            st.header("Total Words")
            st.title(total_words)

        with c3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with c4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline📆")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline🌤️")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map☀️")
        c1, c2 = st.columns(2)
        with c1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with c2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users (overall)
        if selected_user == 'Overall':
            st.title("Most Busy Users👥")
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()
            c1, c2 = st.columns(2)

            with c1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with c2:
                st.dataframe(new_df)
        # Wordcloud
        st.title("Wordcloud☁️")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words💬")
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(fig)
        with c2:
            st.dataframe(most_common_df)

        # most common emojis🚀
        st.title("Most Common Emojis🚀")
        emoji_df = helper.emoji_helper(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(emoji_df[0], emoji_df[1])
        plt.xticks(rotation='vertical')
        c1, c2 = st.columns(2)
        with c1:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        with c2:
            st.dataframe(emoji_df)

