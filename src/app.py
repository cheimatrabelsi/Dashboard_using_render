#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html

import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash
from dash import dcc
from dash import html
import plotly.express as px
from scipy.stats import gaussian_kde

# In[7]:


df = pd.read_excel("../data_2022.xlsx")

indices_to_delete = [15352, 15353, 15354]  # indices of the rows to delete
Data = df.drop(indices_to_delete)

attribute = Data['CA (Prix Grossiste TND)']

# Perform kernel density estimation (KDE) for the attribute
pdf = gaussian_kde(attribute)

custom_colors = px.colors.qualitative.Pastel
# Calculate the offset as a fraction of the data range
x_offset_fraction = 0.05  # Adjust this value as needed
x_range = attribute.max() - attribute.min()
x_offset = x_range * x_offset_fraction

# Create x-axis values with an offset before the observed data range
x = np.linspace(attribute.min() - x_offset, attribute.max(), 100)

# Create the PDF trace for Plotly
pdf_trace = go.Scatter(x=x, y=pdf(x), mode='lines', name='PDF Estimation')

laboratories = Data['Laboratoire'].unique()
# Define the desired order of the months
month_order = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

# Aggregate sales data by month 
sales_by_month = Data.groupby('mois - Mois')['CA (Prix Grossiste TND)'].sum().reset_index()

# Aggregate sales data by month and market
sales_by_month_and_market = Data.groupby(['mois - Mois', 'Marché'], as_index=False)['CA (Prix Grossiste TND)'].sum()

# Convert the 'mois - Mois' column to categorical with the desired order
sales_by_month_and_market['mois - Mois'] = pd.Categorical(sales_by_month_and_market['mois - Mois'], categories=month_order, ordered=True)

# Sort the data by the categorical column
sales_by_month_and_market = sales_by_month_and_market.sort_values('mois - Mois')


# Define the desired order of the months
month_order = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

# Convert the 'mois - Mois' column to categorical with the desired order
sales_by_month['mois - Mois'] = pd.Categorical(sales_by_month['mois - Mois'], categories=month_order, ordered=True)

# Sort the data by the categorical column
sales_by_month = sales_by_month.sort_values('mois - Mois')

# Create a custom color scheme for the bars


# Group data by product and calculate total revenue for each product
revenue_by_product = Data.groupby('Produit')['CA (Prix Grossiste TND)'].sum().reset_index()

# Sort the data by revenue in descending order
revenue_by_product = revenue_by_product.sort_values('CA (Prix Grossiste TND)', ascending=False)

# Create a custom color scale for the bars
color_scale = px.colors.qualitative.Plotly
# Group data by product and calculate total revenue for each product over time (months)
sales_by_product = Data.groupby(['Produit', 'mois - Mois'])['CA (Prix Grossiste TND)'].sum().reset_index()

# Convert the 'mois - Mois' column to categorical with the desired order
sales_by_product['mois - Mois'] = pd.Categorical(sales_by_product['mois - Mois'], categories=month_order, ordered=True)

# Sort the data by the categorical column
sales_by_product = sales_by_product.sort_values('mois - Mois')
###
# Filter data for only the "Optifresh" market
optifresh_data = Data[Data['Marché'] == 'Marché OPTIFRESH']

# Group data by product and calculate total revenue for each product in the "Optifresh" market
revenue_by_product = optifresh_data.groupby('Produit')['CA (Prix Grossiste TND)'].sum().reset_index()

# Filter data for the "Optifresh" market and "STERIPHARM" laboratory
optifresh_steripharm_data = Data[(Data['Marché'] == 'Marché OPTIFRESH') & (Data['Laboratoire'] == 'STERIPHARM')]

# Group data by product and calculate total revenue for each product in the "Optifresh" market and "STERIPHARM" laboratory
revenue_by_product_steripharm = optifresh_steripharm_data.groupby('Produit')['CA (Prix Grossiste TND)'].sum().reset_index()

# Aggregate sales data by month 
sales_by_government = Data.groupby('Gouvernorat')['CA (Prix Grossiste TND)'].sum().reset_index()

# Group data by product and gouvernorat and calculate total revenue for each product in each gouvernorat
revenue_by_product_gouvernorat = Data.groupby(['Gouvernorat', 'Produit'])['CA (Prix Grossiste TND)'].sum().reset_index()

# Sort the data by revenue in descending order for each gouvernorat
revenue_by_product_gouvernorat = revenue_by_product_gouvernorat.sort_values(['Gouvernorat', 'CA (Prix Grossiste TND)'], ascending=[True, False])

# Create a new DataFrame to store the top 5 products for each gouvernorat
top_5_products_by_gouvernorat = pd.DataFrame()

# Loop through each gouvernorat and extract the top 5 products
for gouvernorat in revenue_by_product_gouvernorat['Gouvernorat'].unique():
    top_5_gouv_data = revenue_by_product_gouvernorat[revenue_by_product_gouvernorat['Gouvernorat'] == gouvernorat].head(5)
    top_5_products_by_gouvernorat = pd.concat([top_5_products_by_gouvernorat, top_5_gouv_data])


# Filter data for the "OPTIFRESH" market and "STERIPHARM" laboratory
optifresh_steripharm_data = Data[Data['Laboratoire'] == 'STERIPHARM']

###
# Group data by product and month, calculating total revenue for each product and month combination
sales_by_product_month = optifresh_steripharm_data.groupby(['Produit', 'mois - Mois'])['CA (Prix Grossiste TND)'].sum().reset_index()
# Convert the 'mois - Mois' column to categorical with the desired order
sales_by_product_month['mois - Mois'] = pd.Categorical(sales_by_product_month['mois - Mois'], categories=month_order, ordered=True)

# Sort the data by the categorical column
sales_by_product_month = sales_by_product_month.sort_values('mois - Mois')
###
# Filter data for the "OPTIFRESH" market
optifresh_data = Data[Data['Marché'] == 'Marché OPTIFRESH']

# Group data by product and calculate total revenue for each product in the "OPTIFRESH" market
revenue_by_product_optifresh = optifresh_data.groupby('Produit')['CA (Prix Grossiste TND)'].sum().reset_index()

# Calculate the total revenue for the OPTIFRESH market
total_optifresh_revenue = revenue_by_product_optifresh['CA (Prix Grossiste TND)'].sum()

# Filter data for the "OPTIFRESH" market and "STERIPHARM" laboratory
optifresh_steripharm_data = Data[(Data['Marché'] == 'Marché OPTIFRESH') & (Data['Laboratoire'] == 'STERIPHARM')]

# Group data by product and calculate total revenue for each product in the "OPTIFRESH" market and "STERIPHARM" laboratory
revenue_by_product_steripharm = optifresh_steripharm_data.groupby('Produit')['CA (Prix Grossiste TND)'].sum().reset_index()

# Calculate the contribution of STERIPHARM to the revenue of each product in the OPTIFRESH market
revenue_by_product_optifresh['Contribution_STERIPHARM'] = revenue_by_product_steripharm['CA (Prix Grossiste TND)']


grouped_data = Data.groupby('Marché')['CA (Prix Grossiste TND)'].apply(list)

revenue_data = [grouped_data[category] for category in grouped_data.index]
laboratories = Data['Laboratoire'].unique()
# Create the Dash application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server

##
app.layout = html.Div(
    children=[
        html.H1("Analytics Dashboard ", style={"textAlign": "center"}),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-1',
                            figure=px.pie(
                                Data,
                                names='Laboratoire',
                                values='CA (Prix Grossiste TND)',
                                title='Turnover by Laboratory for 2022'
                            )
                        )
                    ],
                    className="seven columns"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-3',
            figure=px.line(sales_by_month, x='mois - Mois', y='CA (Prix Grossiste TND)', title='Sales Trend by Month for 2022')
        
                        )
                    ],
                    className="five columns"
                
                ),
            ],
            className="row"
        ),
         html.Div(
                    [
                        dcc.Graph(
                            
            id='my-graph-7',
            figure=px.pie(Data, names='Marché', values='CA (Prix Grossiste TND)', title='Turnover by Market for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        
               html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-2',
                            figure=px.bar(
                                Data,
                                x='Laboratoire',
                                y='CA (Prix Grossiste TND)',
                                color='Marché',
                                title='Laboratory Turnover Breakdown across markets for 2022',
                                color_discrete_sequence=custom_colors
                            )
                        )
                    ],
                    className="twelve columns"
        ),
        
                html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-4',
            figure=px.line(sales_by_product, x='mois - Mois', y='CA (Prix Grossiste TND)', color='Produit',
                           title='Sales Trend by Product for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        
         html.Div(
                    [
                        dcc.Graph(
                            
                      id='my-graph-5',
            figure=px.line(sales_by_month_and_market, x='mois - Mois', y='CA (Prix Grossiste TND)', color='Marché', 
                          title='Sales Trend by Month for Each Market for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-6',
            figure=px.line(sales_by_product_month, x='mois - Mois', y='CA (Prix Grossiste TND)', color='Produit',
                           title='Sales Trend for STERIPHARM Products for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-8',
            figure=px.pie(revenue_by_product, values='CA (Prix Grossiste TND)', names='Produit',
                          title='Turnover of OPTIFRESH Market by Product for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-9',
            figure=px.pie(revenue_by_product_steripharm, values='CA (Prix Grossiste TND)', names='Produit',
                          title='Turnover of Optifresh Market by Product for STERIPHARM Laboratory for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-13',
            figure=px.pie(revenue_by_product_steripharm, names='Produit', values='CA (Prix Grossiste TND)',
                          title='Turnover by Product for STERIPHARM Laboratory for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-14',
            figure=px.pie(revenue_by_product_optifresh, names='Produit', values='CA (Prix Grossiste TND)',
                          title='Turnover of OPTIFRESH Market by Product with STERIPHARM Contribution',
                          hover_data=['Contribution_STERIPHARM'],
                          labels={'CA (Prix Grossiste TND)': 'Total Revenue', 'Contribution_STERIPHARM': 'STERIPHARM Contribution'},
                          hole=0.3,
                          custom_data=['Contribution_STERIPHARM']
            ))
                    ],
                    className="twelve columns"
                ),
        
        html.Div(
                    [
                        dcc.Graph(
                            id='my-graph-10',
            figure=px.pie(Data, names='Gouvernorat', values='CA (Prix Grossiste TND)', title='Turnover by Government for 2022')
        
                        )
                    ],
                    className="twelve columns"
                ),
       
        html.Div(
                    [
                        dcc.Graph(
                            figure=go.Figure(data=[
                go.Bar(x=top_5_products_by_gouvernorat[top_5_products_by_gouvernorat['Produit'] == produit]['Gouvernorat'],
                       y=top_5_products_by_gouvernorat[top_5_products_by_gouvernorat['Produit'] == produit]['CA (Prix Grossiste TND)'],
                       name=produit
                ) for produit in top_5_products_by_gouvernorat['Produit'].unique()
            ],
            layout=go.Layout(title='Top 5 Products for Each Government', barmode='group')
        ))
                    ],
                    className="twelve columns"
                ),
    ####    # Dropdown to choose between CA and Quantity
        html.Div(
            [
                dcc.Dropdown(
                    id='data-type-dropdown',
                    options=[
                        {'label': 'CA', 'value': 'CA (Prix Grossiste TND)'},
                        {'label': 'Quantity', 'value': 'Quantité'}
                    ],
                    value='CA (Prix Grossiste TND)',
                    clearable=False
                )
            ],

            style={'width': '30%', 'margin': 'auto'}
        ),
        html.Div(id='box-plot'),
        html.P("Choose Laboratory of interest in order to have PDF estimation for the turnover for 2022:"),
        dcc.Dropdown(
            id='lab-dropdown',
            options=[{'label': lab, 'value': lab} for lab in laboratories],
            value='',  
            clearable=False
        ),
        dcc.Graph(id='pdf-plot'),         
    ]
)
laboratories = Data['Laboratoire'].unique()

@app.callback(
    Output('box-plot', 'children'),
    Input('data-type-dropdown', 'value')
)
def update_box_plot(selected_value):
    fig = px.box(Data, x='Marché', y=selected_value, color='Marché', title=f'Box Plot of {selected_value} by Market')
    return dcc.Graph(figure=fig)


# Callback function to update the KDE plot
@app.callback(
    Output('pdf-plot', 'figure'),
    [Input('lab-dropdown', 'value')]  
)
def update_pdf_plot(selected_lab):
    # Filter data for the selected laboratory
    filtered_data = Data[Data['Laboratoire'] == selected_lab]

    # Select the revenue attribute for PDF estimation
    attribute = filtered_data['CA (Prix Grossiste TND)']

    # Perform kernel density estimation (KDE) for the attribute
    pdf = gaussian_kde(attribute)

    # Create x-axis values for plotting
    x = np.linspace(attribute.min(), attribute.max(), 100)

    # Create the PDF trace for Plotly
    pdf_trace = go.Scatter(x=x, y=pdf(x), mode='lines', name='PDF Estimation')

    # Create the plot figure
    figure = {
        'data': [pdf_trace],
        'layout': {
            'title': f'PDF Estimation for Turnover of {selected_lab}',
            'xaxis': {'title': 'Revenue'},
            'yaxis': {'title': 'Probability Density', 'showticksuffix': 'last'},
            'margin': {'l': 60, 'r': 20, 't': 80, 'b': 60},
        }
    }
    return figure
 



 
    


# Run the application in external mode (opens in a new browser tab using http://127.0.0.1:8052/)
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)


# In[ ]:





# In[16]:















