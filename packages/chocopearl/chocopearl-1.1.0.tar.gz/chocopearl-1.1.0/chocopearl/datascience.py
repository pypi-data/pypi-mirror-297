import numpy as np
import plotly.graph_objects as go

def add_step_histogram(fig, bins, hist,name=None,legendgroup=None, color='blue'):
    x = np.repeat(bins, 2)[1:-1]  
    y = np.repeat(hist, 2)         

    # Calcular los centros de los bins
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Crear el texto personalizado para hover
    hover_text = [f'Freq: {h}<br>Bin: [{bins[i]:.2f}, {bins[i+1]:.2f})' for i, h in enumerate(hist)]

    # Agregar la traza de tipo scatter para el histograma de escalera
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=dict(color=color, width=2),
        hoverinfo='none',
        name=name,
        legendgroup=legendgroup
    ))
    
    if legendgroup==None:
        showlegend_values=True
    else:
        showlegend_values=False
    name="-"
        
        
    # Agregar los puntos en el centro de cada bin, pero hacerlos invisibles con color transparente
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=hist,
        mode='markers',
        marker=dict(color='rgba(0, 0, 0, 0)', size=10),  # Color transparente
        hoverinfo='text',  # Mostrar solo la información de hover
        hovertext=hover_text,
        hoverlabel=dict(bgcolor=color, font=dict(color='white')),
        showlegend=showlegend_values,
        name=name,
        legendgroup=legendgroup
    ))

    return fig


def symmetry_hist(data, center=0, bin_num=None, bin_size=None,density=False):
    if bool(bin_num) == bool(bin_size):
        raise Exception("bins and bin_size parameters can't be both used at the same time")
    else:
        data = np.asarray(data)[~np.isnan(data)]
        l= np.min(data)
        h= np.max(data)
        if bool(bin_size):
            hn= int(np.ceil((h-center-bin_size/2)/bin_size))
            h_edges=[center+bin_size*(0.5 + n) for n in range(hn+1)]
            ln= int(np.ceil((center-l -bin_size/2)/bin_size))
            l_edges=[center-bin_size*(0.5 + n) for n in range(ln+1)]
            edges=np.array(sorted(l_edges + h_edges))

            hist,_=np.histogram(data, bins=edges,density=density)
            
            return edges,hist
        else:
            raise Exception("Not implemented, function works only with bin_size")       
    
