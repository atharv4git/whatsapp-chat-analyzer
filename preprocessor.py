import re, pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_dates'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'datetime'}, inplace=True)
    # mask = df['user_message'].str.contains('Media omitted')
    # df = df[~mask]
    df.reset_index(inplace=True, drop=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df.drop(columns=['datetime'], inplace=True)
    df['year'] = df['message_dates'].dt.year
    df['month_num'] = df['message_dates'].dt.month
    df['month'] = df['message_dates'].dt.month_name()
    df['date'] = df['message_dates'].dt.day
    df['hour'] = df['message_dates'].dt.hour
    df['minute'] = df['message_dates'].dt.minute
    # df['date'] = pd.to_datetime(df['message_dates'], errors='coerce')
    df['only_date'] = df['message_dates'].dt.date
    df['day_name'] = df['message_dates'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
