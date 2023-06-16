import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column
from io import BytesIO

# Load the HIV dataset
hiv_data = pd.read_csv('hiv.csv')

# Set up the data source
source = ColumnDataSource(hiv_data)

# Create the figure
p = figure(plot_width=400, plot_height=400, x_axis_label='Jumlah Kasus', y_axis_label='Kelompok Umur')

# Add HoverTool to display additional information
hover = HoverTool(tooltips=[('Kabupaten/Kota', '@nama_kabupaten_kota'), ('Kelompok Umur', '@kelompok_umur')])  # Specify the tooltips to display kabupaten/kota and kelompok umur information
p.add_tools(hover)

# Create the scatter plot glyphs for each gender
gender_glyphs = {}
for gender in hiv_data['jenis_kelamin'].unique():
    gender_glyphs[gender] = p.circle('jumlah_kasus', 'kelompok_umur', source=source, size=8, color='red', alpha=0.5)

# Create the select widget
gender_list = ['All'] + list(hiv_data['jenis_kelamin'].unique())
select_gender = st.selectbox('Jenis Kelamin', options=gender_list)

# Create the slider based on 'tahun'
slider = st.slider('Tahun', min_value=min(hiv_data['tahun']), max_value=max(hiv_data['tahun']), value=min(hiv_data['tahun']), step=1)

# Update the plot based on the selected gender and year
selected_data = hiv_data[(hiv_data['jenis_kelamin'] == select_gender) | (select_gender == 'All') & (hiv_data['tahun'] == slider)]
source.data.update(ColumnDataSource(selected_data).data)

# Update the glyph fill alpha based on the selected gender
for gender, glyph in gender_glyphs.items():
    if select_gender == 'All' or gender == select_gender:
        glyph.glyph.fill_alpha = 0.5
    else:
        glyph.glyph.fill_alpha = 0

# Create the layout
layout = column(p)

# Convert the plot to image
plot_img = BytesIO()
p.save(plot_img, format='png')

# Display the plot as an image
st.image(plot_img)
