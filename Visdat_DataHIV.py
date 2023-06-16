import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column

# Load the HIV dataset
hiv_data = pd.read_csv('hiv.csv')

# Create the figure
p = figure(plot_width=400, plot_height=400, x_axis_label='Jumlah Kasus', y_axis_label='Kelompok Umur')

# Add HoverTool to display additional information
hover = HoverTool(tooltips=[('Kabupaten/Kota', '@nama_kabupaten_kota'), ('Kelompok Umur', '@kelompok_umur')])  # Specify the tooltips to display kabupaten/kota and kelompok umur information
p.add_tools(hover)

# Create the scatter plot glyphs for each gender
gender_glyphs = {}
for gender in hiv_data['jenis_kelamin'].unique():
    gender_glyphs[gender] = p.circle('jumlah_kasus', 'kelompok_umur', source=None, size=8, color='red', alpha=0.5)

# Create the select widget
gender_list = ['All'] + list(hiv_data['jenis_kelamin'].unique())
select_gender = st.selectbox('Jenis Kelamin', options=gender_list)

# Create the slider based on 'tahun'
slider = st.slider('Tahun', min_value=min(hiv_data['tahun']), max_value=max(hiv_data['tahun']), value=min(hiv_data['tahun']), step=1)

# Update the plot based on the selected gender and year
def update_plot():
    selected_data = hiv_data[(hiv_data['jenis_kelamin'] == select_gender) | (select_gender == 'All') & (hiv_data['tahun'] == slider)]
    source.data = ColumnDataSource(selected_data).data

# Initialize the data source
source = ColumnDataSource(data=dict(jumlah_kasus=[], kelompok_umur=[], nama_kabupaten_kota=[], jenis_kelamin=[], tahun=[]))

# Update the plot initially
update_plot()

# Update the glyph fill alpha based on the selected gender
def update_glyphs():
    for gender, glyph in gender_glyphs.items():
        if select_gender == 'All' or gender == select_gender:
            glyph.glyph.fill_alpha = 0.5
        else:
            glyph.glyph.fill_alpha = 0

# Create the layout
layout = column(p)

# Display the plot and layout
st.bokeh_chart(layout)

# Run the update functions when the select box or slider values change
if select_gender is not None and slider is not None:
    update_plot()
    update_glyphs()
