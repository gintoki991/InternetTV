# 放映時間と放映日の割り当てを修正してデータを再生成
start_date = 2020-04-06
timedelta = 

# 各エピソードの放映時間と放映日を計算
airing_data_corrected = []
for airing_time_id in range(1, 51):
    channel_id = (airing_time_id - 1) // 10 + 1  # 各チャンネルに10エピソードずつ割り当て
    day_index = (airing_time_id - 1) % 7  # 一週間のうちの日にち
    episode_number = (airing_time_id - 1) % 10 + 1  # エピソード番号
    airing_date = (start_date + timedelta(days=day_index)).strftime('%Y-%m-%d')  # 放映日
    time_index = (airing_time_id - 1) % 14  # 一日に14エピソードまで（2エピソード/チャンネル）
    start_time, end_time = broadcast_times[time_index]  # 放映時間

    airing_data_corrected.append((channel_id, episode_number, start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), airing_time_id, airing_date))

# 正しいSQLコマンドの生成
airing_sql_commands_corrected = []
for ad in airing_data_corrected:
    airing_sql_commands_corrected.append(f"INSERT INTO airing_time (channel_id, episode_number, broadcasting_start_time, broadcasting_end_time, airing_time_id, airing_date) VALUES ({ad[0]}, {ad[1]}, '{ad[2]}', '{ad[3]}', {ad[4]}, '{ad[5]}');")

airing_sql_commands_corrected[:50]  # 最初の50つのコマンドを表示
