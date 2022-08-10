import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib as mpl
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import gunicorn
import pandas as pd
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as Dset


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css])

#### Creazione delle Fig da inserire poi nell'applicazione Dash
sharks = ['Bathyraja_brachyurops', 'Chimaera_monstrosa', 'Dalatias_licha',
'Dipturus_oxyrinchus', 'Etmopterus_spinax', 'Galeus_melastomus',
'Mustelus_asterias', 'Mustelus_mustelus', 'Myliobatis_aquila', 'RSH',
'RSS', 'Raja_asterias', 'Raja_clavata', 'Raja_miraletus',
'Raja_polystigma', 'SSH', 'SSS', 'Scyliorhinus_canicula',
'Squalus_blainville', 'Torpedo_marmorata', 'Torpedo_torpedo',
'RSH_C1', 'RSS_C1', 'SSH_C1', 'SSS_C1', 'SSS_C2', 'ESH',
'ESS', 'RAY', 'SHK']
models = [
    'TOT',
    'CUT3',
    'CUT2',
    'CUT1',
    'ORI',
    'ESSESH',
    'SHKRAY']
Pastel = px.colors.qualitative.Pastel
mycolorlist=[
    [0, Pastel[0]],
    [0.13, 'rgb(255,255,255)'],
    [0.75, Pastel[1]],
    [1, Pastel[2]],
]
mycolorgrad = [
    [0, 'rgb(255,255,255)'],
    [1, Pastel[2]],
]
mti_color_grad=[
    [0, Pastel[0]],
    [0.5, 'rgb(255,255,255)'],
    [1, Pastel[2]],
]



## Econet 0
econet_stats_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators0.csv').set_index('indicator')
# econet_std_stats_df = econet_stats_df.sub(econet_stats_df['ORI'], axis=0).T
legend_dic = {
    'Ascendency':'Ascendency<br><sup>[bits t/km2/year]</sup>',
    'Capacity':'Capacity<br><sup>[bits t/km2/year]</sup>',
    'Overhead':'Overhead<br><sup>[bits t/km2/year]</sup>',
}
econet_std_stats_df = econet_stats_df.T.rename(columns=legend_dic)
fig = px.bar(econet_std_stats_df, color_discrete_sequence=Pastel)
fig.update_layout(legend_title='', template='plotly_white', title='EcoNet Analysis')
fig.update_xaxes(title_text='Model')
fig.update_yaxes(title_text='')
fig_econet = fig

## Econet 1
econet_utility_list  = []
econet_utility_fig_dic={}
for model in models:
    econet_utility_list.append(pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators1/'+model+'.csv').set_index(model))

for index, df in enumerate(econet_utility_list):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        zmin=-3,
        zmax=20,
        z=df.values.tolist(),
        x=df.index.tolist(),
        y=df.index.tolist(),
        colorscale=mycolorlist,
    ))
    fig.update_layout(
        title=models[index]
    )
    econet_utility_fig_dic[models[index]] = fig

## Econet 2
econet_control_list  = []
econet_control_fig_dic = {}
for model in models:
    econet_control_list.append(pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators2/'+model+'.csv').set_index(model))
for index, df in enumerate(econet_control_list):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        zmin=-3,
        zmax=20,
        z=df.values.tolist(),
        x=df.index.tolist(),
        y=df.index.tolist(),
        colorscale=mycolorlist,
    ))
    fig.update_layout(
        title=models[index])
    econet_control_fig_dic[models[index]] = fig
## La dalatias licha ha un controllo elevatissimo forse outlier


## Ascendency enar 3
ascend_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators3.csv').set_index('Unnamed: 0')

indicators=[
    'TD',
    'ASC',
    'CAP',
    'OH',
    'ASC.CAP',
    'OH.CAP',
    'A.internal',
    'CAP.internal',
    'OH.internal',
]
legend_dic = {
    'ASC':'Ascendency<br><sup>[bits t/km2/year]</sup>',
    'CAP':'Capacity<br><sup>[bits t/km2/year]</sup>',
    'OH':'Overhead<br><sup>[bits t/km2/year]</sup>',
    'TD':'Trophic Depth',
    'ASC.CAP':'A/C',
    'OH.CAP':'O/C',
    'A.internal':'A (internal)<br><sup>[bits t/km2/year]</sup>',
    'OH.internal':'O (internal)<br><sup>[bits t/km2/year]</sup>',
    'CAP.internal':'C (internal)<br><sup>[bits t/km2/year]</sup>',
}
ascend_std_df = ascend_df.T[indicators].rename(columns=legend_dic)
fig = px.bar(ascend_std_df, color_discrete_sequence=Pastel)
fig.update_layout(legend_title='', template='plotly_white', title='Ascendency Analysis')
fig.update_xaxes(title_text='Model')
fig.update_yaxes(title_text='')
enar_asc_fig = fig


## Betweenness 4
betweennness_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators4.csv').set_index('FG')
## elimino i detriti che sono ovviamente outlier di betweenness e mascherano l'effetto degli altri
betweennness_df = betweennness_df.loc[~betweennness_df.index.isin(['DC','SPOM','BD'])]
box_betw_df = betweennness_df.stack().rename('Betweenness').reset_index().rename(columns={'level_1':'Model'})
fig=go.Figure()
fig.add_trace(go.Box(
    y=box_betw_df['Betweenness'],
    x=box_betw_df['FG'],
    boxpoints=False,
    hoverinfo='none',
    marker=dict(
        color=Pastel[0]
    ),
    line=dict(
        color='rgba(102, 197, 204,0.5)'
    ),
    fillcolor='rgba(102, 197, 204,0.2)',
))
fig.add_traces(
    list(px.strip(box_betw_df, x='FG', y='Betweenness', hover_data=['Model'],stripmode='overlay', color_discrete_sequence=[Pastel[0]]).select_traces())
) 
fig.update_layout(hovermode='x', template='plotly_white', title='Betweenness variation among models', showlegend=False)
betweenness_fig = fig


## enaR Flow 5
flow_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators5.csv').set_index('Unnamed: 0')
flow_df = flow_df.loc[~flow_df.index.str.contains('^mode')]
indicators = [
    'TST',
    'TSTp',
    'APL',
    'FCI',
]
legend_dic = {
    'TST':'TST<br><sup>[t/km2/year]</sup>',
    'TSTp':'TSTp<br><sup>[t/km2/year]</sup>',
}
flow_std_df = flow_df.T[indicators].rename(columns=legend_dic)
fig = px.bar(flow_std_df, color_discrete_sequence=Pastel)
fig.update_xaxes(title='Model')
fig.update_yaxes(title='')
fig.update_layout(legend_title_text='', title='Flow Analysis', template='plotly_white')
enar_flow_fig=fig


## Keystoneness 6
keystoness_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators6.csv').set_index('FG')
key_plot_df = keystoness_df.loc[:, keystoness_df.columns.str.contains(('^RTI.*|^Key1.*'))]
shrk_palette = [
    'rgba(102, 197, 204, 0.4)',
    'rgb(248, 156, 116)',
]
keystone_fig_dic={}
for idx,model in enumerate(models):
    px_df = key_plot_df.loc[:, key_plot_df.columns.str.contains('{}$'.format(model))].copy()
    px_df['shark'] = px_df.index.isin(sharks)
    fig = px.scatter(px_df, x='RTI {}'.format(model), y='Key1 {}'.format(model), hover_data=[px_df.index], color='shark', color_discrete_sequence=shrk_palette)
    fig.update_layout(title=model, showlegend=False, template='plotly_white')
    fig.update_xaxes(title='RTI')
    fig.update_yaxes(title='Key1')
    keystone_fig_dic[model] = fig



## Ecopath MTI 7
mti_list  = []
mti_fig_dic = {}

for model in models:
    mti_list.append(pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators7/'+model+'.csv').set_index('FG'))

for index, df in enumerate(mti_list):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        zmin=-1,
        zmax=1,
        z=df.values.tolist(),
        x=df.index.tolist(),
        y=df.index.tolist(),
        colorscale=mti_color_grad,
    ))
    fig.update_layout(
        title=models[index])
    mti_fig_dic[models[index]] = fig
### Top MTI plot
reduced_mti_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/reduced_mti_interactions.csv').drop(columns='Unnamed: 0') 
fig=go.Figure()
fig.add_trace(go.Box(
    y=reduced_mti_df['MTI'],
    x=reduced_mti_df['Interaction'],
    boxpoints=False,
    hoverinfo='none',
    marker=dict(
        color=Pastel[0]
    ),
    line=dict(
        color='rgba(102, 197, 204,0.5)'
    ),
    fillcolor='rgba(102, 197, 204,0.2)',
))
fig.add_traces(
    list(px.strip(reduced_mti_df, x='Interaction', y='MTI', hover_data=['Model'],stripmode='overlay', color_discrete_sequence=[Pastel[0]]).select_traces())
) 
fig.update_yaxes(title='MTI')
fig.update_xaxes(title='Interaction FG<sub>1</sub> x FG<sub>2</sub>')
fig.update_layout(hovermode='x', template='plotly_white', title='Top 0.1% Variance MTI Interactions', showlegend=False)
reduced_mti_fig = fig



## Ecopath statistics 8
ewe_stats_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators8.csv').set_index('Parameter')
ewe_ascend_df = pd.read_csv('https://raw.githubusercontent.com/mirk-00/msc-thesis-ecosystem/main/indicators_ewe.csv').rename(columns={'Unnamed: 0':'Model'}).set_index('Model')

ewe_std_stats_df = ewe_stats_df.sub(ewe_stats_df['ORI'], axis=0).T
ewe_std_stats_df = ewe_stats_df.T
fig = px.bar(ewe_std_stats_df, color_discrete_sequence=Pastel)
fig.update_xaxes(title='Model')
fig.update_yaxes(title='')
fig.update_layout(template='plotly_white', legend_title_text='', title='Ecopath System Indicators')
ewe_stats_fig = fig

fig = px.bar(ewe_ascend_df, title='Ecopath Information Statistics', color_discrete_sequence=Pastel)
fig.update_layout(legend_title='', template='plotly_white')
fig.update_yaxes(title='')
fig.update_xaxes(title='Model')
ewe_ascend_fig = fig



######################################################################################################
#####################################################################################################
#### Creazione della Dashboard
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server


app.layout = html.Div([
    dbc.Tabs([
        dbc.Tab(
            label='Introduction',
            children=[
                html.Div([
                html.Div([html.H1('Trophic Networks'),
                Dset('''
                    Ecosystems are inhabited by a wide range of animals and plants. It is of primary importance understand the entity and the type of interactions that exist in the biocenosis, that is the 
                    whole living compartment of an habitat. In this way it's possible to fine-tune ecological management in order to address the most impactful dangers in the ecosystem. 
                    <br>It is also important to develop a solid framework that allows researchers the objective analysis of the ecosystem. Ecological models are well suited for this purpose.
                    <br>More specifically, the effect of predation in an ecosystem can be described as a network of interactions also called Trophic Network. The intensity of each interaction is proportional to the extent the predator consumes
                    a prey, thus representing a <b>bioenergetic flux</b>. Once this network is obtained it is possible to develop a series of numerical indicators that describe a specific features of the ecosystem, of a species or relating to an interaction.
                '''),
                html.H3('Chord Graph', style={'margin-top':'3px'}),
                Dset(['''
                    The chord graph on the right represents a simplified network of the analyzed ecosystem (see Paragraph <a href='#strait-of-sicily'> Strait of Sicily </a>).
                    The 72 FG have been grouped into few larger groups, and then only the ones showing a consistently large flux have been plotted.
                    You can hover on a group to highlight its interactions.
                    <br> Notice that the fluxes are directed to the predating group (the 'consumer'). The flow to detritus
                    exists because of many activities such as egestion, natural death or fishing discards.
                    <br> Even from this naive representation it is possible to observe that most of the energy in this marine ecosystem flows through groups at the base of the trophic pyramid. This is generally true
                    for all the aquatic ecosystems.<br>
                    Yet it is well known that <b>apex predators</b> play a significant role in shaping the ecosystem, and their extinction can cause a rapid decline of the others population in the community.
                    Their importance can not lie entirely on the magnitude of their direct trophic interaction, in fact their fluxes are negligible compared to those of detritus.
                    '''
                    ])
                ], style={'width':'35%'}),
                
                html.Div(html.Iframe(
                    sandbox='allow-scripts',
                    height='150%' ,
                    width='100%',
                    srcDoc='''
<html>
<head>
<!-- Plotapi - Chord
This package enables the generation of Chord diagrams. They can be saved 
directly to HTML files or displayed in a Jupyter Notebook output cell.

Copyright 2021, Plotapi
http:
https:

Copyright 2021, Dr. Shahin Rostami
http:
-->
<!--LICENSE
Chord (https:
Copyright (C) 2021  Dr. Shahin Rostami
-->
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>Plotapi - Chord Diagram</title>

<link href="https://fonts.googleapis.com/css?family=Lato:400,700,900&display=swap" rel="stylesheet" type="text/css"/>


<style>

#plotapi-chart-98d0eca7, #featured-plotapi-chart-98d0eca7 {
    font-size: 16px;
    font-family: "Lato", sans-serif !important;
    text-align: center;
    fill: #454545;
}

#plotapi-chart-98d0eca7 svg, #featured-plotapi-chart-98d0eca7 svg {
    max-width: 700px;
}

.details_thumbs-plotapi-chart-98d0eca7 {
    margin: 5px;
    max-width: 85px;
    padding: 0;
    display: inline-block; 
}

.details_thumbs-plotapi-chart-98d0eca7 img {
    max-width: 85px;
}

.details_thumbs-plotapi-chart-98d0eca7 figcaption {
    text-align: center;
    font-size: 14px;
}

.hidden_chord {
    display:none;
}

.arc_numbers {
    paint-order: stroke;
    stroke: #454545;
    stroke-width: 2px; 
    font-weight: bold;
    fill: #fff;
    font-size: 10px;
}

@media (min-width: 600px) {
    #plotapi-chart-98d0eca7 svg, #featured-plotapi-chart-98d0eca7 svg {
        font-size: 20px;
    }

    .arc_numbers{
        font-size: 14px;
    }
}


</style>
</head>
<body>
    <div id="plotapi-chart-98d0eca7" class="chord plotapi-container"></div>

    <script>
    (function() {
        var jupyter_classic = !(typeof(IPython)==="undefined");
        var dependencies_paths = {
                        'd3': 'https://plotapi.com/static/js/d3.v7.min',
                        'chord': 'https://plotapi.com/static/js/d3-chord',
                    }

        if(jupyter_classic){
            require.config(
                {
                    paths: dependencies_paths
                }
            );

            require(['d3','tippy','chord', 'pako'], function(d3, tippy, chord, pako) {
                window.d3 = d3;
                window.tippy = tippy;
                window.pako = pako;
                plotapi_plot();
            });
        }
        else{
            var dependencies = Object.values(dependencies_paths);
            
            function dependency_loader(dependencies_loaded){
                var script = document.createElement("script");
                script.type = "text/javascript";
                script.src = dependencies[dependencies_loaded] + ".js";

                script.onload = function () {
                    if(dependencies_loaded < dependencies.length-1){
                    dependency_loader(dependencies_loaded+1)
                    }
                    else{
                        plotapi_plot();
                    }
                };
                document.body.appendChild(script);
            }

            dependency_loader(0);
        }

        function plotapi_plot(){
            margin = {
                left: 100,
                top: 100,
                right: 100,
                bottom: 100
            };

            width = Math.min(window.innerWidth, 700) - margin.left - margin.right;
            height = Math.min(window.innerWidth, 700) - margin.top - margin.bottom;
            Names = ['Bacteria', 'Benthos', 'Cephalopods', 'Decapods', 'Detritus', 'Osteichthyes', 'Plankton', 'Producers'];
            matrix = [[0.0, 0.155, 0.0, 0.022, 0.266, 0.034, 0.218, 0.0], [0.0, 0.209, 0.086, 0.054, 0.925, 0.372, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.032, 0.046, 0.0, 0.0, 0.0], [0.247, 0.852, 0.0, 0.194, 0.111, 0.412, 0.297, 0.0], [0.0, 0.0, 0.0, 0.0, 0.393, 0.0, 0.05, 0.0], [0.0, 0.0, 0.0, 0.058, 0.61, 0.288, 0.469, 0.0], [0.0, 1.0, 0.0, 0.0, 0.806, 0.102, 0.899, 0.0]];
            details = [];
            details_thumbs = [];
            conjunction = "and";
            innerRadius = Math.min(width, height) * 0.4;
            outerRadius = innerRadius * 1.1;

            offset = 0;
            
            
                var colors = d3.scaleSequential(d3.interpolateGnBu)
                    .domain([0,matrix.length]);

            
            var chord_data = chord(true,false)
                .padAngle(0.1)
                .sortChords(d3.descending) 
                (matrix);

            var arc = d3.arc()
                .innerRadius(innerRadius * 1.01)
                .outerRadius(outerRadius)
                .startAngle(startAngle) 
                .endAngle(endAngle);

            var path = d3.ribbonArrow()
                .radius(innerRadius)
                .startAngle(startAngle)
                .endAngle(endAngle);

            
            var svg = d3.select("#plotapi-chart-98d0eca7")
                .append("svg")
                .attr(
                    "viewBox",
                    "0 0 " +
                    (width + margin.left + margin.right) +
                    " " +
                    (height + margin.top + margin.bottom)
                )
                .attr("class","plotapi-plot")
                .attr("preserveAspectRatio", "xMinYMin meet")
                .append("g")
                .attr(
                    "transform",
                    "translate(" +
                    (width / 2 + margin.left) +
                    "," +
                    (height / 2 + margin.top) +
                    ") rotate(0)"
                );




            
            
            function getGradID(d) {
                return ("linkGrad-plotapi-chart-98d0eca7-" + d.source.index + "-" + d.target.index);
            }

            
            var grads = svg.append("defs")
                .selectAll("linearGradient")
                .data(chord_data)
                .enter()
                .append("linearGradient")
                .attr("id", getGradID)
                .attr("gradientUnits", "userSpaceOnUse")
                .attr("x1", function (d, i) {
                    if(d.source.index == d.target.index){
                        return 0;
                    }
                    return (innerRadius * Math.cos((d.source.endAngle - d.source.startAngle) / 2 + d.source.startAngle - Math.PI / 2));
                })
                .attr("y1", function (d, i) {
                    return (innerRadius * Math.sin((d.source.endAngle - d.source.startAngle) / 2 + d.source.startAngle - Math.PI / 2));
                })
                .attr("x2", function (d, i) {
                    return (innerRadius * Math.cos((d.target.endAngle - d.target.startAngle) / 2 + d.target.startAngle - Math.PI / 2));
                })
                .attr("y2", function (d, i) {
                    return (innerRadius * Math.sin((d.target.endAngle - d.target.startAngle) / 2 + d.target.startAngle - Math.PI / 2));
                });

            
            grads.append("stop")
                .attr("offset", "0%")
                .attr("stop-color", function (d) {
                    return colors(d.source.index);
                });

            
            grads.append("stop")
                .attr("offset", "100%")
                .attr("stop-color", function (d) {
                    return colors(d.target.index);
                });

            
            var outerArcs = svg.selectAll("g.group")
                .data(chord_data.groups)
                .enter()
                .append("g")
                .attr("class", "group")
                .on("mouseover", fade(0.1, 1, Names))
                .on("mouseout", fade(0.8, 0.8, Names));

            outerArcs.append("path")
                .style("fill", function (d) {
                    return colors(d.index);
                })
                .attr("d", arc)
                .each(function (d, i) {
                });

                
                    
                    outerArcs.append("text")
                        .each(function (d) {
                            d.angle = (d.startAngle + d.endAngle) / 2 + offset;
                        })
                        .attr("dy", ".35em")
                        .attr("class", function (d) {
                            return "titles";
                        })
                        .attr("text-anchor", function (d) {
                            return d.angle > Math.PI ? "end" : null;
                        })
                        .attr("transform", function (d) {
                            return ("rotate(" + ((d.angle * 180) / Math.PI - 90) + ")" + "translate(" + (outerRadius + 10) + ")" + (d.angle > Math.PI ? "rotate(180)" : ""));
                        })
                        .text(function (d, i) {
                            return Names[i];
                        })
                        .call(wrap, 100);


                
                var chords = svg.selectAll("path.chord")
                    .data(chord_data)
                    .enter()
                    .append("path")

                .attr("class", function (d) {
                    return "chord";
                })                                 
                .style("fill", function (d) {
                    return "url(#" + getGradID(d) + ")";
                })         
                .style("opacity", 0.8)
                .attr("d", path)
                .on("mouseover", mouseoverChord(Names, conjunction, details, details_thumbs))
                .on("mouseout", mouseoutChord(0.8, 0.8));
            
            function startAngle(d) {
                return d.startAngle + offset;
            }
            function endAngle(d) {
                return d.endAngle + offset;
            }

            function wrap(text, width) {
                text.each(function() {
                    var text = d3.select(this);
                    var words = text.text().split(/\s+/).reverse();
                    var word;
                    var line = [];
                    var y = text.attr("y");
                    var dy = parseFloat(text.attr("dy"));
                    var tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
                    var lines = 0;

                    while (word = words.pop()) {
                        line.push(word)
                        tspan.text(line.join(" "))
                        
                        if (tspan.node().getComputedTextLength() > width && line.length > 1) {
                            line.pop()      
                            if(line.length != 0){
                                tspan.text(line.join(" "))
                            }
                            line = [word]
                            tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", "1em").text(word)
                            lines = lines+1;
                        }
                    }
                    text.select("tspan:nth-child(1)").attr("dy", ""+(0.35-(lines * 0.5))+"em");
                })
            }

            
            function fade(opacityIn, opacityOut, names) {
                return function (i, d) {
            
                    d3.select(this.ownerSVGElement)
                        .selectAll("path.chord")
                        .filter(function (k) {
                            return k.source.index !== d.index && k.target.index !== d.index;
                        })
                        .transition()
                        .style("opacity", opacityIn);

                    d3.select(this.ownerSVGElement)
                        .selectAll("path.chord")
                        .filter(function (k) {
                            return k.source.index == d.index || k.target.index == d.index;
                        })
                        .transition()
                        .style("opacity", opacityOut);                            
                };
            }

            
            function mouseoverChord(names, conjunction, details, details_thumbs) {
                return function (i, d) {

                    d3.select(this.ownerSVGElement)
                        .selectAll("path.chord")
                        .transition()
                        .style("opacity", 0.1);

                    
                    d3.select(this).transition().style("opacity", 1);

                };                    
            }

            
            function mouseoutChord(opacityIn, opacityOut) {
                return function (d, i) {
                    d3.select(this.ownerSVGElement)
                        .selectAll("path.chord")
                        .transition()
                        .style("opacity", opacityOut);
                };
            }


            
        

            

            
            d3.select("#plotapi-chart-98d0eca7 svg")
                .append("svg:a")
                .attr("xlink:href", "https://plotapi.com")
                .attr("target", "_blank")
                .append("image")
                .attr("xlink:href", "https://plotapi.com/gallery/icon/plotapi.svg")
                .attr('width', 20)
                .attr('height', 20)
                .attr('x', width+margin.left + margin.right-20)
                .attr('y', 0)
                .style("opacity", 0)
                .attr("id","plotapi-chart-98d0eca7_icon")

            d3.select("#plotapi-chart-98d0eca7_icon")
                .append("title")
                .text("Produced with Plotapi");

            d3.select("#plotapi-chart-98d0eca7_icon").on("mouseover", function(d, i) {
                d3.select("#plotapi-chart-98d0eca7_icon").style("opacity", 1)
            });

            d3.select("#plotapi-chart-98d0eca7_icon").on("mouseout", function(d, i) {
                d3.select("#plotapi-chart-98d0eca7_icon").style("opacity", 0.6)
            });

            d3.select("#plotapi-chart-98d0eca7 svg").on("mouseenter", function() {
                d3.select("#plotapi-chart-98d0eca7_icon").style("opacity", 0.6)
            });

            d3.select("#plotapi-chart-98d0eca7 svg").on("mouseleave", function() {
                                    
                d3.select("#plotapi-chart-98d0eca7_icon").style("opacity", 0);
            });
            

            
            
        }    

    }());
    </script>            
</body>
</html>
                        '''
                    ),
                    style={'width':'65%', 'flex':'right'}
                    )],
                    style={'display':'flex', 'height':'100%',}
                    ),
                html.Div([
                    html.H1('Functional Groups'),
                    Dset('''
                        The species living in the ecosystem can be split into functional groups (FG), that should be made of species with similar <b>ecological role</b>.
                        The intensity of the trophic interaction is calculated between these FG, and this implies that the the network statistics may depend on model construction,
                        and finally on the researcher choice to group some species or others.
                        <br> One of the results of this work is that some indicators can be grouped with no major concern for the interpretation of results, while others are very sensible to such alterations.
                    ''')
                ],
                style={'width':'35%'}
                ),
                html.Div([
                    html.H1('Strait of Sicily - Mediterranean Sea', id='strait-of-sicily'),
                    Dset('''
                        One recent Ecopath model has been published for the Strait of Sicily<sup>1</sup> in 2019, including 72 FG of which 4 groups for Chondrichtyes that encompass
                        38 different species between sharks, rays and skates. <br>
                        I used data with high detail to further break down these 4 groups in order to reveal the effect of single species where possible. In this way i obtained 4 models with 
                        greater ecological resolution and 2 models were obtained aggregating the initial 4 FG.
                        <br> They will be referred to using the notation explained in the table below.
                    ''')
                ],
                style={'width':'35%', 'margin-bottom':'1%'}
                ),
                html.P(html.Small([
                html.Sup('1'),
                '  Ref. Agnetta et al. 2019  ',
                dcc.Link(href='https://doi.org/10.1371/journal.pone.0210659', children=['Online Article'])])),
                html.Table([
                    html.Thead(
                    html.Tr([
                        html.Th(''),
                        html.Th('Aggregated Models'),
                        html.Th('Original Model'),
                        html.Th('Disaggregated Models'),
                    ])),
                    html.Tbody(
                    html.Tr([
                        html.Th('Key Tag'),
                        html.Td('SHKRAY and ESSESH'),
                        html.Td('ORI'),
                        html.Td('TOT, CUT1, CUT2, CUT3'),
                    ])),
                ], className='dbc table table-active', style={'width':'40%', 'margin-bottom':'3%', 'padding-bottom':'3%'})
            ]
        ),
        dbc.Tab(
            label='Home',
            children=[
                html.H1('Base Actions'),
                html.H4('Isolate a Trace'),
                html.P('To isolate a trace in a plot, double click on its legend entry.'),
                html.H4('Hide and Show a trace'),
                html.P('Single click legend entries to toggle the visibility of the corresponding trace'),
                html.H4('Zoom'),
                html.P(['''Click and drag on the graph to zoom in a rectangular area''',
                    html.Br(),
                    '''You can also zoom only over one of the 2 axis, simply click and drag and move only along the axis of interest''']),
                html.H4('Reset Zoom'),
                html.P('''Double click on the graph area to reset the zoom.'''),
            ]
        ),
        dbc.Tab(
            label='Invariant Indicators',
            children=[
                html.H1('Invariant Indicators'),
                html.P('In this page will be presented the results that showed no particular change with model aggregation level', style={'margin-bottom':'1%'}),
                html.H3('Ecopath Statistics'),
                html.P('Ecopath is the software used to create the models. It also allows the user to calculate few statistics.'),
                dcc.Graph(
                    figure=ewe_stats_fig,
                    id='ewe_stats_fig'
                ),
                dcc.Graph(
                    figure=ewe_ascend_fig,
                    id='ewe_ascend_fig'
                ),
                html.H3('EcoNet Information Analysis'),
                html.P('EcoNet is an online tool that can calculate many interesting ecosystem indicators.'),
                dcc.Graph(
                    figure=fig_econet,
                    id='econet_fig'
                ),
                html.H3('enaR Analysis'),
                html.P('The R package enaR has been used to calculate and verify the previous results.'),
                dcc.Graph(
                    figure=enar_asc_fig,
                    id='enar_asc_fig'
                ),
                dcc.Graph(
                    figure=enar_flow_fig,
                    id='enar_flow_fig',
                )

            ]
        ),
        dbc.Tab([
            html.H2('Mixed Trophic Impact between Models'),
            Dset('''
                Mixed Trophic Impact (MTI) measures to which extent a group impacts on another considering both direct and indirect interactions. 
                The boxplot below represents MTI values between different models for the same interactions.
                <br> The total number of interactions exceeds 10000, therefore only the top 0.1% of interactions with the highest variance between models have been shown.
                <br> It is important to notice that different type of aggregations can greatly affect the value of MTI.
            '''),
            dcc.Graph(
                figure=reduced_mti_fig,
                id='reduced_mti_fig',
                style={
                    'height':'80vh',
                    'margin-bottom':'10vh'
                }
            ),
            html.H2('MTI Heatmaps'),
            html.P("Heatmaps below contain the full data used to create the previous boxplot, but they're not easily readable"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            figure=mti_fig_dic['TOT'],
                            id='mti_tot',
                        ),
                        dcc.Graph(
                            figure=mti_fig_dic['CUT2'],
                            id='mti_cut2',
                        ),
                        dcc.Graph(
                            figure=mti_fig_dic['ORI'],
                            id='mti_ori',
                        ),
                        dcc.Graph(
                            figure=mti_fig_dic['SHKRAY'],
                            id='mti_shkray',
                        ),
                    ]),
                ], width=6),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            figure=mti_fig_dic['CUT3'],
                            id='mti_cut3',
                        ),
                        dcc.Graph(
                            figure=mti_fig_dic['CUT1'],
                            id='mti_cut1',
                        ),
                        dcc.Graph(
                            figure=mti_fig_dic['ESSESH'],
                            id='mti_essesh',
                        ),
                    ]),
                ], width=6),
            ],
                style={
                        'margin':'auto',
                        'width':'90vw',
                    }
            )],
            label='Mixed Trophic Impact',
        ),
        dbc.Tab([
            html.H1('Keystoneness'),
            Dset('''
                Keystoneness is a recently designed indicator<sup>1</sup> that identify a FG importance in the community based on its trophic interactions and biomass.
                <br>Few studies are available to determine its dependency on the aggregation level of an ecosystem trophic model. These results show that Keystoneness 
                is highly dependent on the type and the number of groups in the ecosystem.
                <br>For this reason much care must be taken when interpreting keystoneness results to aid management decisions. In this case for example, according to the
                grade of ecological aggregation very different conclusion can be drawn. If the model had been built using distributed taxonomical data, it could have been inferred
                that Chondrichthyes have no particular effects on ecosystem structure.
                On the contrary, using aggregated data sharks and rays show the highest value for keystoneness.
            '''),
            Dset('<b>Chondrychthyes</b> functional groups are colored in <b>orange</b>'),
            html.P([html.Sup([
                html.Sup('1 '),
                'Ref. Libralato et al. 2006  ',
                dcc.Link(href='https://doi.org/10.1016/j.ecolmodel.2005.11.029', children=['  Online Article'])]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            figure=keystone_fig_dic['TOT'],
                            id='keystone_tot',
                        ),
                        dcc.Graph(
                            figure=keystone_fig_dic['CUT2'],
                            id='keystone_cut2',
                        ),
                        dcc.Graph(
                            figure=keystone_fig_dic['ORI'],
                            id='keystone_ori',
                        ),
                        dcc.Graph(
                            figure=keystone_fig_dic['SHKRAY'],
                            id='keystone_shkray',
                        ),
                    ]),
                ], width=6),
                dbc.Col([
                    html.Div([
                        dcc.Graph(
                            figure=keystone_fig_dic['CUT3'],
                            id='keystone_cut3',
                        ),
                        dcc.Graph(
                            figure=keystone_fig_dic['CUT1'],
                            id='keystone_cut1',
                        ),
                        dcc.Graph(
                            figure=keystone_fig_dic['ESSESH'],
                            id='keystone_essesh',
                        ),
                    ]),
                ], width=6),
            ],
            style={
                    'margin':'auto',
                    'width':'90vw',
            }
            )],
            label='Keystone Species',
        ),
        dbc.Tab(
            label='Betweenness',
            children=[
                html.H1('Betweenness Centrality Measure'),
                Dset('Betweenness is a measure of centrality of a node in a graph (network). High values for one group mean that it connects nodes otherwise largely or completely disconnected.'),
                dcc.Graph(
                    figure=betweenness_fig,
                    id='betweenness_plot',
                    style={'width': '80vw', 'height':'90vh', 'margin':'auto'}
                ),
            ]
        ),
    ])
],
style={
                    'margin':'auto',
                    'width':'90vw',
}
)



if __name__ == '__main__':
    app.run_server()