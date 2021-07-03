import streamlit as st
import altair as alt
import pandas as pd
import requests

portals_url ='https://api.aavegotchi.land/open_portal_listing?desired_traits=x,x,x,x,x,x&order_by=min_brs'
gotchi_url ='https://api.aavegotchi.land/gotchi?desired_traits=low_bracket,low_bracket,x,low_bracket,x,x&order_by=brs'

def get_data(url):
    response = requests.get(url=url)
    return response.json()

portals = pd.DataFrame(get_data(portals_url))
portals['brs/ghst'] = portals.max_brs / portals.price

portals_display = portals[['id','price','max_brs','listing_url', 'brs/ghst']]
portals_display.set_index('id', inplace=True)

gotchi = pd.DataFrame(get_data(gotchi_url))
gotchi['brs'] = pd.to_numeric(gotchi['brs'])
gotchi['mbrs'] = pd.to_numeric(gotchi['mbrs'])
gotchi_display = gotchi[['name','brs', 'mbrs','gotchi_url', 'staked']]
gotchi_display.set_index('name', inplace=True)

st.write("## Gotchi with collateral")
st.write("Top 6000, sorted by staked")
st.table(gotchi_display.sort_values(by=['staked'], ascending=False).head(500))

st.write("## Open portals for sale")
st.write("Top 20, sorted by rarity per GHST")
st.table(portals_display.sort_values(by=['max_brs'], ascending=False).head(500))


st.write("Thanks to aavegotchi.land for the API")
