import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

animes = pd.read_csv('C:\\Users\\denis\\Documents\\WSU\\3 Junior\\2 Junior 2nd Semester\\Data Mining (Cpts 315)\\Assignments\\Course Project\\Dataset\\Cleaned\\anime_cleaned.csv')
filtered_animes = animes[animes['scored_by'] >= 100] #Remove entries with less than 100 votes
filtered_animes.rename(columns = {'popularity':'popularity_rank'}, inplace = True) #Rename 'popularity' column with 'popularity_rank'
#print(animes)
# print(filtered_animes)

r = filtered_animes['score'] #Stores the scores for each show
v = filtered_animes['scored_by'] #Stores the number of votes for each show
m = filtered_animes['scored_by'].quantile(0.0001)
c = filtered_animes['score'].mean() #Determines the mean score value for all shows

filtered_animes['weighted_avg'] = (((r * v) + (c * m)) / (v + m)) #Calculates the weighted average for each show and stores it in a new column
sorted_animes = filtered_animes.sort_values('popularity_rank') #Sorts the shows by ascending order of the popularity ranks
# print(filtered_animes[['score', 'weighted_avg']])
# print(sorted_animes[['title', 'score', 'scored_by', 'weighted_avg', 'popularity_rank']])

#Appends the values in popularity_rank to a list and reverses the order to signify popularity score, and adding it to the dataframe as a new column
pop_score = sorted_animes['popularity_rank'].tolist() 
pop_score.reverse()
sorted_animes['popularity_score'] = pop_score
sorted_weight_animes = sorted_animes.sort_values(by = ['weighted_avg'], ascending = False)
# print(sorted_weight_animes[['title', 'score', 'scored_by', 'weighted_avg', 'popularity_rank', 'popularity_score', 'favorites']])

#Normalize the values (weighted averages, popularity scores, number of favourites)
scaling = MinMaxScaler()
scaled_animes = scaling.fit_transform(sorted_weight_animes[['weighted_avg', 'popularity_score', 'favorites']])
normalized_animes = pd.DataFrame(scaled_animes, columns = ['weighted_avg', 'popularity_score', 'favorites'])
sorted_weight_animes[['normalized_weight', 'normalized_popularity', 'normalized_fav']] = normalized_animes
# print(normalized_animes)
# print(sorted_weight_animes)

#Calculate the final scores for each show
sorted_weight_animes['final_score'] = (sorted_weight_animes['normalized_weight'] * 0.33) + (sorted_weight_animes['normalized_popularity'] * 0.33) +(sorted_weight_animes['normalized_fav'] * 0.33)
final_score_animes = sorted_weight_animes.sort_values(['final_score'], ascending = False)
# final_score_animes = final_score_animes[final_score_animes['normalized_weight'].notna()]
# print(sorted_weight_animes)
# print(final_score_animes[['anime_id', 'title', 'weighted_avg', 'normalized_weight', 'normalized_popularity', 'normalized_fav', 'final_score']])

#Split the data into the type of show (TV, Movie, OVA - Original Video Animation, Special, Music or ONA - Original Net Animation)
# print(final_score_animes['type'].unique())
tv_animes = final_score_animes[final_score_animes['type'] == 'TV'].head(100)
movie_animes = final_score_animes[final_score_animes['type'] == 'Movie'].head(100)
ova_animes = final_score_animes[final_score_animes['type'] == 'OVA'].head(100)
special_animes = final_score_animes[final_score_animes['type'] == 'Special'].head(100)
music_animes = final_score_animes[final_score_animes['type'] == 'Music'].head(100)
ona_animes = final_score_animes[final_score_animes['type'] == 'ONA'].head(100)
# print(tv_animes)
# print(movie_animes)
# print(ova_animes)
# print(special_animes)
# print(music_animes)
# print(ona_animes)

#Plotting two classes
ax = tv_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', label = 'TV', c = 'red', title = 'Score vs. Final Score')
movie_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
ova_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
special_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Special')
music_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
ona_animes.plot(x = 'score', y = 'final_score', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', label = 'TV', c = 'red', title = 'Weighted Average vs. Final Score')
# movie_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'weighted_avg', y = 'final_score', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', label = 'TV', c = 'red', title = 'Normalized Weighted vs. Final Score')
# movie_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'normalized_weight', y = 'final_score', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', label = 'TV', c = 'red', title = 'Popularity Score vs. Final Score')
# movie_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'popularity_score', y = 'final_score', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', label = 'TV', c = 'red', title = 'Normalized Popularity vs. Final Score')
# movie_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'normalized_popularity', y = 'final_score', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', label = 'TV', c = 'red', title = 'Final Score vs. Favourites')
# movie_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'final_score', y = 'favorites', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

# ax = tv_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', label = 'TV', c = 'red', title = 'Final Score vs. Normalized Favourites')
# movie_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', ax = ax, label = 'Movie', c = 'grey')
# ova_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', ax = ax, label = 'OVA', c = 'yellow')
# special_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', ax = ax, label = 'Special')
# music_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', ax = ax, label = 'Music', c = 'blue')
# ona_animes.plot(x = 'final_score', y = 'normalized_fav', kind = 'scatter', ax = ax, label = 'ONA', c = 'green')

plt.show()

# #Output the results
final_score_animes.to_csv('Unedited Final Scores.csv', index = False)
tv_animes.to_csv('TV Anime Recommendations.csv', index = False)
movie_animes.to_csv('Anime Movie Recommendations.csv', index = False)
ova_animes.to_csv('Anime OVA Recommendations.csv', index = False)
special_animes.to_csv('Anime Special Recommendations.csv', index = False)
music_animes.to_csv('Music Anime Recommendations.csv', index = False)
ona_animes.to_csv('Anime ONA Recommendations.csv', index = False)
