import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import reactive, render, req
import palmerpenguins
import seaborn as sns
import pandas as pd

# Define color mapping for species
species_colors = {
    "Adelie": "blue",
    "Gentoo": "green",
    "Chinstrap": "red"
}

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Julia's Penguin Data", fillable=True)

with ui.sidebar(position="right", open="open"):
    ui.h2("Sidebar")
    
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 15)
    
    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 40, 20)

    #Added a checkbox for each species
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Chinstrap"],
        inline=False,
    )
    
    # Added a checkbox for each island
    ui.input_checkbox_group(
        "selected_island_list",
        "Island",
        penguins_df['island'].unique().tolist(),
        selected=penguins_df['island'].unique().tolist(),
        inline=False,
    )
    
    ui.hr()
    
    ui.a("Github", href="https://github.com/julia-fangman/cintel-02-data", target="_blank")

# Accordion Layout with DataTable and DataGrid
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            if not selected_species and not selected_islands:  # If no species or islands are selected, return the original data
                return penguins_df
            else:
                df = penguins_df
                if selected_species:
                    df = df[df['species'].isin(selected_species)]
                if selected_islands:
                    df = df[df['island'].isin(selected_islands)]
                return df

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            if not selected_species and not selected_islands:  # If no species or islands are selected, return the original data
                return penguins_df
            else:
                df = penguins_df
                if selected_species:
                    df = df[df['species'].isin(selected_species)]
                if selected_islands:
                    df = df[df['island'].isin(selected_islands)]
                return df

# Created a card with tabs for graphs
# Created a Plotly Histogram showing all species and islands
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):
        @render_plotly
        def plotly_histogram():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            df = penguins_df
            if selected_species:
                df = df[df['species'].isin(selected_species)]
            if selected_islands:
                df = df[df['island'].isin(selected_islands)]
            return px.histogram(
                df,
                x=input.selected_attribute(),
                color="species",
                color_discrete_map=species_colors,  
                nbins=input.plotly_bin_count(),
                width=800,
                height=400,
                category_orders={input.selected_attribute(): ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']},  # Specify category order for x-axis
                labels={
                    input.selected_attribute(): "Bill Length",  # Updated x-axis label
                    "species": "Species",
                },
                title="Plotly Histogram"
            )

    
# Created a Seaborn Histogram showing all species and islands
    with ui.nav_panel("Seaborn Histogram"):
        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            df = penguins_df
            if selected_species:
                df = df[df['species'].isin(selected_species)]
            if selected_islands:
                df = df[df['island'].isin(selected_islands)]
            histplot = sns.histplot(
                data=df, x="body_mass_g", bins=input.seaborn_bin_count(),
                hue="species", palette=species_colors  
            )
            histplot.set_title("Seaborn Histogram")
            histplot.set_xlabel("Mass")
            histplot.set_ylabel("Count")
            return histplot

    
# Created a Plotly Scatterplot showing all species and islands
    with ui.nav_panel("Plotly Scatterplot"):
        @render_plotly
        def plotly_scatterplot():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            df = penguins_df
            if selected_species:
                df = df[df['species'].isin(selected_species)]
            if selected_islands:
                df = df[df['island'].isin(selected_islands)]
            return px.scatter(
                df,
                x="bill_length_mm",
                y="body_mass_g",
                color="species",
                color_discrete_map=species_colors,  
                title="Penguins Scatterplot",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
                width=1200,
                height=600,
            )

    
# Created a Plotly Boxplot showing all species and islands
    with ui.nav_panel("Plotly Box Plot"):
        @render_plotly
        def plotly_box_plot():
            selected_species = input.selected_species_list()
            selected_islands = input.selected_island_list()
            df = penguins_df
            if selected_species:
                df = df[df['species'].isin(selected_species)]
            if selected_islands:
                df = df[df['island'].isin(selected_islands)]
            return px.box(
                df,
                x="species",
                y=input.selected_attribute(),
                color="species",
                color_discrete_map=species_colors,  
                title="Penguins Box Plot",
                labels={
                    input.selected_attribute(): input.selected_attribute().replace("_", " ").title(),
                    "species": "Species",
                },
            )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    selected_islands = input.selected_island_list()
    if not selected_species and not selected_islands:  
        return penguins_df
    else:
        df = penguins_df
        if selected_species:
            df = df[df['species'].isin(selected_species)]
        if selected_islands:
            df = df[df['island'].isin(selected_islands)]
        return df
