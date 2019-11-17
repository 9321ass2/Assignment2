============================= Game Recommendation System =============================

							READ ME IF U R NOT JX ZHOU!!!

==================================== Files Needed ====================================

./Data_Visualize/KNN.csv
./DataSet/vgsales-12-4-2019-short.csv
./DataSet/vgsales-12-4-2019.csv
./DataSet/user_favorite.csv' ................... This contains the rank of games the user chose on the website.
./RecommendationSystem/pick_popular_games.py
./RecommendationSystem/gram_matrix.py
./RecommendationSystem/recommend.py
./RecommendationSystem/accuracy.py
(./RecommendationSystem/readme.txt)

====================================== Run Step ======================================

run before server start:
	pick_popular_games.py ............... pick 30 most favourite games
	gram_matrix.py ...................... generate 3000 games' relevance matrix
run after recommend request:
	recommend.py ........................ make recommendation based on matrix
run after accuracy check request:
	accuracy.py ......................... output accuracy based on 'Genre'

===================================== File Paths =====================================

'*.py' are all stored under './RecommendationSystem'
all ***generated*** '*.csv' are stored under './DataSet'

===================================== File Details ===================================

pick_popular_games.py:
	I/O PATH:
		line 18: ***READ*** '../DataSet/vgsales-12-4-2019-short.csv' ..... origin file
		line 53: ***WRITE** '../DataSet/popular_games_output.csv'  ....... temp file
		line 55: ***READ*** '../DataSet/popular_games_output.csv'
		line 56: ***READ*** '../Data_Visualize/KNN.csv' .................. generated from dataloader.py by Marcus
		line 57: ***WRITE** '../DataSet/game_30.csv' ..................... to be used on recommend.py

gram_matrix.py:
	I/O PATH:
		line 21: ***READ*** '../Data_Visualize/KNN.csv' 
		line 69: ***WRITE** '../DataSet/relevance_matrix.csv' ............ to be used on recommend.py

recommend.py:
	I/O PATH:
		line 08: ***READ*** '../DataSet/user_favorite.csv' ............... file shape is 30*1 and all values are int 
		line 13: ***READ*** '../Data_Visualize/KNN.csv'
		line 18: ***READ*** '../DataSet/game_30.csv'  
		line 23: ***READ*** '../DataSet/vgsales-12-4-2019.csv'
		line 41: ***READ*** '../DataSet/relevance_matrix.csv'
		line 98: ***WRITE** '../DataSet/recommend_games.csv' ............. final output file include rank, name, url

accuracy.py:
	I/O PATH:
		line 04: ***READ*** '../Data_Visualize/KNN.csv'
		line 05: ***READ*** '../DataSet/user_favorite.csv'
		line 06: ***READ*** '../DataSet/recommend_rank.csv'
	OUTPUT:
		A float number rounded to 2 dicimals e.g. 0.88

======================================== The End =====================================
									
									  ENJOY TESTING!!!