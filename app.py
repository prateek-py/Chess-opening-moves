import streamlit as st
from singleplayer import*
from visualization import*
from getrecords import*


st.write("""
	# Opening moves visualization

	""")


uname = st.text_input(label='',placeholder='Chess.com username',help='Enter a chess.com username and press enter')
if uname!='':
    u_rad=st.radio('Game format', ['Blitz','Bullet','Rapid'], index=0)
    games = st.text_input(label='No of games to analyze:',placeholder='Defalut 100') or 100



if st.button('Show my openings'):
    try:
        dfW,dfB=get_player_opening_data(uname,u_rad.lower(),int(games))
        BarPlot(dfW,'White')
        BarPlot(dfB,'Black')
    except:
        st.warning("Enter a valid username")


  


def callback():
    st.session_state.button_clicked = True


if "button_clicked" not in st.session_state:    
    st.session_state.button_clicked = False

if (st.button("Openings by top players",on_click=callback) or st.session_state.button_clicked):    
    rad=st.radio('Game format', ['Blitz','Bullet'], index=0)
    if st.button('Show'):
        if rad=='Bullet':        
            dfW=pd.DataFrame.from_dict(moves_frequency_BulletW(),orient='index', columns=['count'])
            dfB=pd.DataFrame.from_dict(moves_frequency_BulletB(),orient='index', columns=['count'])
            BarPlot(dfW,'White')
            BarPlot(dfB,'Black')
        
        
        else:
            dfW=pd.DataFrame.from_dict(moves_frequency_BlitzW(),orient='index', columns=['count'])
            dfB=pd.DataFrame.from_dict(moves_frequency_BlitzB(),orient='index', columns=['count'])
            BarPlot(dfW,'White')
            BarPlot(dfB,'Black')

