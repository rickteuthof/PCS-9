"""
:mod:`geometry` -- Generate geometry parametrically
=======================================================

    module:: geometry
    :synopsis: Generates geometries.
    moduleauthor:: Martijn Besamusca
    moduleauthor:: Ralph Erkamps
    moduleauthor:: Rick Teuthof

bifurcation.py
---------
An example geometry of an idealized flattened abdominal aorta made using
realistic values of the distances and diameters. We made use of multiple sources
and studies. Also some distances not described in the studies we found where
measured using an 3d scan of an actual aorta.
The model is based on:
"Finite Element Modeling of Three-Dimensional Pulsatile Flow in the Abdominal Aorta: Relevance to Atherosclerosis"
(Taylor, C.A., Hughes, T.J.R. & Zarins, C.K.).


:Authors:
    - Martijn Besamusca
    - Ralph Erkamps
    - Rick Teuthof

:Sources:
    - Taylor, C.A., Hughes, T.J.R. & Zarins, C.K.
        Finite Element Modeling of Three-Dimensional Pulsatile Flow in the Abdominal Aorta: Relevance to Atherosclerosis.
        Annals of Biomedical Engineering 26, 975–987 (1998).
    - David Horejs;Perry Gilbert;Scott Burstein;Robert Vogelzang
        Normal Aortoiliac Diameters by CT
        Journal of Computer Assisted Tomography. 12(4):602–603, JULY-AUGUST 1988
    - Boston Scientific Corporation, Dr. Gary Siskin, M.D.
        Peripheral Vasculature - Average Vessel Diameter
        (PI-324504-AA JUNE 2015)
"""

from geometry.vessels import Vessels


def build_abdominal(scale=10):
    """ Build an idealized flattened abdominal aorta.

    This model is made using multiple sourced described in the file header.
    It contains the follwing arteries:
        - aorta from supraceliac to the bifurcation to the iliac arteries
        - celiac artery
        - left and right renal arteries
        - superior and inferior mesentric arteries.
        - left and right iliac arteries.
    The aorta is split at the celiac artery, because at that point the abdominal aorta
    narrows a bit.

    :param scale: The number of pixels per centimeter.
    :return:
        - A `Vessels` object containing all vessels.
        - A dictionary with all vessels.
    """

    width = scale * 15
    height = scale * 6

    w_supraceliac_aorta_start = 2.07
    w_aorta_start = 1.75
    w_aorta_end = 1.6
    pos_celiac = 1
    w_celiac = .78
    pos_lr_renal = 4
    w_lr_renal = .5
    pos_bifur = 11
    pos_superior_mesenteric = 3
    w_superior_mesenteric = .7
    pos_inferior_mesenteric = pos_superior_mesenteric + 5
    w_inferior_mesenteric = .4
    w_lr_iliac = 1.04

    pos_aorta_bot = height/2 + min(w_aorta_start, w_aorta_end)*scale/2-.3*scale
    pos_aorta_top = height/2 - min(w_aorta_start, w_aorta_end)*scale/2+.3*scale

    abdominal = Vessels(width, height)
    supraceliac_aorta = abdominal.add_vessel(
        pos_from=(0, height/2),
        pos_to=(pos_lr_renal*scale, height/2),
        width=w_supraceliac_aorta_start*scale
    )
    supraceliac_aorta_end_l = supraceliac_aorta.add_end(30)
    supraceliac_aorta_end_c = supraceliac_aorta.add_end(0)
    supraceliac_aorta_end_r = supraceliac_aorta.add_end(-30)
    aorta = supraceliac_aorta.append_vessel(
        end_i=supraceliac_aorta_end_c,
        pos=(pos_bifur*scale, height/2),
        width=w_aorta_start*scale
    )
    aorta.taper_to(w_aorta_end*scale)
    a1 = aorta.add_end(30)
    a2 = aorta.add_end(-30)

    left_iliac = aorta.append_vessel((width, 5*scale), end_i=a1, width=w_lr_iliac*scale)
    right_iliac = aorta.append_vessel((width, 1*scale), end_i=a2, width=w_lr_iliac*scale)

    celiac = abdominal.add_vessel(
        pos_from=(pos_celiac*scale, pos_aorta_top - 0.3*scale),
        pos_to=(pos_celiac*scale + 1*scale, 0),
        width=w_celiac*scale,
        angle_from=-50,
        angle_to=-90
    )

    left_renal = supraceliac_aorta.append_vessel(
        end_i=supraceliac_aorta_end_l,
        pos=(pos_lr_renal*scale + 2.5*scale, height),
        width=w_lr_renal*scale,
        angle_to=90)
    right_renal = supraceliac_aorta.append_vessel(
        end_i=supraceliac_aorta_end_r,
        pos=(pos_lr_renal*scale + 2.5*scale, 0),
        width=w_lr_renal*scale,
        angle_to=-90)

    superior_mesenteric = abdominal.add_vessel(
        pos_from=(pos_superior_mesenteric*scale, pos_aorta_top - 0.3*scale),
        pos_to=(pos_superior_mesenteric*scale + .9*scale, 0),
        width=w_superior_mesenteric*scale,
        angle_from=-40,
        angle_to=-90
    )
    inferior_mesenteric = abdominal.add_vessel(
        pos_from=(pos_inferior_mesenteric*scale, pos_aorta_top),
        pos_to=(pos_inferior_mesenteric*scale + 1*scale, 0),
        width=w_inferior_mesenteric*scale,
        angle_from=-60,
        angle_to=-90
    )
    arteries = {
        'supraceliac_aorta': supraceliac_aorta,
        'aorta': aorta,
        'celiac': celiac,
        'superior_mesenteric': superior_mesenteric,
        'left_renal': left_renal,
        'right_renal': right_renal,
        'inferior_mesenteric': inferior_mesenteric,
        'left_iliac': left_iliac,
        'right_iliac': right_iliac
    }
    return abdominal, arteries
