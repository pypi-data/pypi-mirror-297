import numpy as np
import pandas as pd
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from fuzzy.categories import LandForm, LandCover
from fuzzy.engine import Prototype, engine
from fuzzy.memberships import membership
from fuzzy.rules import SlopeRule
from skfuzzy import control as ctrl
import plotly.graph_objects as go
from numpy.core._multiarray_umath  import  ndarray
from matplotlib import cm

land_form_type = np.arange(LandForm.marshes_and_lowlands, LandForm.highest_mountains + 0.1, 1)
land_cover_type = np.arange(LandCover.permeable_areas, LandCover.marshes + 0.1, 1)
land_form_type, land_cover_type = np.meshgrid(land_form_type, land_cover_type)
pred_val: np.ndarray = np.zeros(shape=(len(land_cover_type), len(land_cover_type[1])))

for i in range(1, len(land_form_type[1])):
    for j in range(1, len(land_cover_type)):
        simulate = Prototype(land_form=i, land_cover=j)
        pred_val[j][i] = simulate.slope_result

fig = go.Figure(data=[go.Surface(x=land_form_type, y=land_cover_type, z=pred_val,
    contours = {
        "z": {"show": True, "start": 0, "end": 100, "size": 5, "color":"grey"}
    },
    )])

fig.update_layout(
    title='Slope evaluation using the fuzzy logic model',
    scene=dict(
        xaxis_title='Land form type',
        yaxis_title='Land cover type',
        zaxis_title='Percent of surface slope',
                zaxis=dict(range=[0, 35])

    ),
    autosize=True,
    width=900,
    height=800,
    font=dict(
            size=14,
        )
    )

fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="black", project_z=True))
fig.show()

