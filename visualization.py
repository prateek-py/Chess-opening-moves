import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def BarPlot(df,ptitle):
    '''Plots the graph from a dataframe and accepts the plot title as another parameter'''
    fig = plt.figure(figsize=(10, 4))
    plt.style.use("dark_background")
    g=sns.barplot(x=df.index,y='count',data=df,palette='bright')
    g.set(title=ptitle, xlabel='Moves', ylabel='Times Played')
    for i in g.patches:    # puts count number over each bin in the graph
    	g.text(
    		x = i.get_x() + (i.get_width()/2),
    		y = i.get_height() ,
    		s = '{:.0f}'.format(i.get_height()),
            fontsize=12,
            fontweight='medium',
    		ha = 'center'
    		)
    st.pyplot(fig)