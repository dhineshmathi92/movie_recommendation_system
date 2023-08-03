import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import urllib.request as ur
from footer import footer

##### For page configuration
page_bg_img = '''
<style>
.stApp {
background-image: url("https://images.pexels.com/photos/7794435/pexels-photo-7794435.jpeg?auto=compress&cs=tinysrgb&w=600");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)






def fetch_poster(movie_id):
 try:
     response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b766d8be22c2567721dfa3dfc980d482")
     data = response.json()
     return "http://image.tmdb.org/t/p/w500/"+ data['poster_path']
 except KeyError:
     return "https://th.bing.com/th/id/R.306227404d0b1a42b2a2ab7063e24c8b?rik=3gN4UzVbTeYDMw&riu=http%3a%2f%2fl.rgbimg.com%2fcache1nToqK%2fusers%2fg%2fgr%2fgreekgod%2f600%2fmlns2We.jpg&ehk=JJGAflzTY4kH6m88udYvM7mFNZ3LeNciBquthGa9HF8%3d&risl=&pid=ImgRaw&r=0"
 
def get_recommendation(movie):
 mv_id = req_df[req_df['movie_title']== movie]['movie_id'].values[0]
 get_idx = req_df[req_df['movie_title'] == movie].index[0]

 rec = sorted(list(enumerate(cosine_matrix[get_idx])), key=lambda x: x[1], reverse=True)[1:16]
 idx = []
 for idd in rec:
  idx.append(idd[0])
 recommend_movies = req_df.loc[idx]['movie_title'].values.tolist()
 poster_pth = []
 for mov in recommend_movies:
  mv_id = req_df[req_df['movie_title'] == mov]['movie_id'].values[0]
  poster_path = fetch_poster(mv_id)
  
  poster_pth.append(poster_path)

  ## fetch posters from API
 return recommend_movies, poster_pth






if __name__=="__main__":

    cosine_df = pd.DataFrame()
    ### unpickling the cosine_matrix
    for i in range(8):
        temp_df = pickle.load(open("cosine_matrix_"+str(i)+".pkl","rb"))
        cosine_df = pd.concat([cosine_df,temp_df], axis=0 )
        

    
    cosine_matrix = cosine_df.values
    ## Reading the cleansed file
    req_df = pd.read_csv("final_mv_df_req.csv")

    st.title('I am your :blue[Movie] :red[Recommender]  :sunglasses:')

    footer()
    
    
    usr_input = st.selectbox(
    'Which movie you watched recently?',
     sorted(req_df['movie_title'].values.tolist()) )
     
    import streamlit as st
    from itertools import cycle

    

    if st.button('Recommend'):
        st.write("You can also try following movies...")
        #col1, col2, col3, col4, col5 = st.columns(5)
        #names, posters = get_recommendation(usr_input)
        
        #i=0
        #for col in [col1, col2, col3, col4, col5]:
        # #col.write(names[i])
        # img_name = 'img'+str(i)+'.jpg'
        # ur.urlretrieve(posters[i],img_name)
        # image = Image.open(img_name)
        # new_image = image.resize((150,250))
        # col.image(new_image,  caption=names[i])
        # i+=1
        caption, filteredImages = get_recommendation(usr_input)
        #filteredImages = [] # your images here
        #caption = [] # your caption here
        cols = cycle(st.columns(5)) 
        for idx, filteredImage in enumerate(filteredImages):
            next(cols).image(filteredImage, width=150, caption=caption[idx])


    
